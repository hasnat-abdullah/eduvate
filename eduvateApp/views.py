from django.db import transaction
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from eduvateApp.models import *
from django.http import HttpResponseRedirect
from .forms import RegisterForm, FeedbackForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json


class IndexView(ListView):
    model = Course
    template_name = 'index.html'
    context_object_name = 'course'


class DashboardView(View):
    template_name = 'lms/student-dashboard.html'

    def get(self, request):
        course = EnrolledCourse.objects.filter(student_id=request.user.id).order_by('-enrolled_on').select_related(
            'course_id')
        context = {
            'course': course,
            'dashboard_active': 'active',
        }
        return render(request, self.template_name, context)


class EnrollCourseView(View):

    @transaction.atomic
    def get(self, request, id):
        current_student = get_object_or_404(Student, name=request.user.id)
        course = get_object_or_404(Course, id=id)

        first_module = CourseModule.objects.filter(course=course.id).order_by('module_position').first()

        first_lesson = Lesson.objects.filter(module_id=first_module.id).order_by('lesson_position').first()

        if not (EnrolledCourse.objects.filter(student_id=current_student.id, course_id=course.id).exists()):
            ec = EnrolledCourse(student_id=current_student, course_id=course, percent_complited=0)
            ec.save()
            em = EnrolledModule(student_id=current_student, module_id=first_module)
            em.save()
            # last_completed_lesson=CompletedLesson.objects.filter(student_id=current_student.id,lesson_id__module_id__course__id=course.id).order_by('lesson_id__lesson_position')[:1]

        return redirect('takeCourse', cid=course.id, sid=first_module.id, lid=first_lesson.id)


class CourseDetailsView(View):
    authenticated_template = 'lms/student-course.html'
    unauthenticated_template = 'course-single.html'

    def get(self, request, id):
        course = get_object_or_404(Course, id=id)

        instructor = CourseInstructor.objects.filter(course_id=course.id).select_related('instructor_id')
        module = CourseModule.objects.filter(course=course.id)
        first_module = module.first()
        totalModule = len(module)

        relatedCourse = Course.objects.filter(category=course.category).exclude(id=course.id)[:3].select_related('category')
        context = {
            'course': course,
            'instructor': instructor,
            'module': module,
            'first_module': first_module,
            'totalModule': totalModule,
            'relatedCourse': relatedCourse,
            'all_course_active': 'active'
        }

        if request.user.is_authenticated:
            current_student = Student.objects.get(name=request.user.id)
            is_enrolled = EnrolledCourse.objects.filter(student_id=current_student.id, course_id=course.id).exists()
            context['is_enrolled'] = is_enrolled
            return render(request, self.authenticated_template, context)

        return render(request, self.unauthenticated_template, context)


class CourseSessionView(View):

    def get(self, request, cid, sid):
        course = get_object_or_404(Course, id=cid)
        current_student = get_object_or_404(Student, name=request.user.id)
        module = get_object_or_404(CourseModule, id=sid)
        instructor = CourseInstructor.objects.filter(course_id=course.id).select_related('instructor_id')
        module_list = CourseModule.objects.filter(course=course.id)
        lesson = Lesson.objects.filter(module_id=module.id).first()

        return redirect('takeCourse', cid=course.id, sid=module.id, lid=lesson.id)


@method_decorator(login_required, name='dispatch')
class RunningCourseView(View):
    template_name = 'lms/student-running-courses.html'

    def get(self, request):
        course = EnrolledCourse.objects.filter(student_id=request.user.id) \
            .order_by('-enrolled_on').select_related('course_id')

        context = {
            'course': course,
            'running_course_active': 'active'
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class TakeCourseView(View):
    def get_data_from_db(self, request, cid, sid, lid):
        data = {
            'course' : get_object_or_404(Course, id=cid),
            'current_student' : get_object_or_404(Student, name=request.user.id),
            'module' : get_object_or_404(CourseModule, id=sid),
            'lesson' : get_object_or_404(Lesson, id=lid)
        }
        return data

    def get_value_to_get_next_lesson_url(self, module, lesson, lesson_list,enrolled_module,course,current_student):
        ######-----Next button url----########
        next_Lesson_id = ''
        next_module_id = module.id
        for l in lesson_list:
            if l.lesson_position > lesson.lesson_position:
                next_Lesson_id = l.id
                # if next lesson found, update module status 'completed'
                enrolled_module.enrolment_status = 'partial'
                enrolled_module.save()
                break

        if not next_Lesson_id:
            # if no next lesson found, update module status 'completed'
            enrolled_module.enrolment_status = 'completed'
            enrolled_module.save()
            next_module = CourseModule.objects.filter(course=course.id,
                                                      module_position__gt=module.module_position).order_by(
                'module_position')[:1]
            if next_module is not None:
                next_lesson = Lesson.objects.filter(module_id=next_module.id).order_by('lesson_position').first()
                em = EnrolledModule(student_id=current_student, module_id=next_module)
                em.save()
                if next_lesson is not None:
                    next_Lesson_id = next_lesson.id
        return next_Lesson_id, next_module_id

    def get(self, request, cid, sid, lid):
        data = self.get_data_from_db(request, cid, sid, lid)
        course = data.get('course')
        current_student = data.get('current_student')
        module = data.get('module')
        lesson = data.get('lesson')

        enrolled_module = EnrolledModule.objects.filter(student_id=current_student.id, module_id=module.id)\
            .order_by('-enrolled_module_on').first()
        enrolled_course = EnrolledCourse.objects.filter(student_id=current_student.id, course_id=course.id)\
            .order_by('-enrolled_on').first()

        # ---if the student does not enrolled in requested course---
        if enrolled_course is None:
            return redirect('singleCourse', cid)

        # ---if the student does not enrolled in requested module---
        if enrolled_module is None:
            return redirect('denied')

        # ---if the student does not enrolled in this course---
        if not (lesson.lesson_position == 1 or CompletedLesson.objects.filter(student_id=current_student.id,
                                                                              lesson_id__module_id=module.id,
                                                                              lesson_id__lesson_position=lesson.lesson_position - 1).exists()):
            return redirect('denied')

        module_list = CourseModule.objects.filter(course=course.id)
        lesson_list = Lesson.objects.filter(module_id=module.id).order_by('lesson_position')
        total_lesson = Lesson.objects.filter(module_id__course__id=course.id).count()
        total_completed_lesson = CompletedLesson.objects.filter(student_id=request.user.id,
                                                                lesson_id__module_id__course__id=course.id).count()
        percentage_complete = int((total_completed_lesson * 100) / total_lesson)

        enrolled_course.percent_complited = percentage_complete
        enrolled_course.save()
        ######-----Mark as complete this lesson------####
        obj, created = CompletedLesson.objects.update_or_create(student_id=current_student, lesson_id=lesson)
        scale = ''
        question = ''
        answer = ''
        score = ''
        if lesson.lesson_type == 'scale':
            scale = LessonScale.objects.get(lesson_id=lesson.id)
            question = QuestionDetails.objects.filter(scale_id=scale.scale_name.id).order_by('serial')
            answer = AnswerDetails.objects.filter(scale_id=scale.scale_name.id).order_by('serial')
            score = ScoringDetails.objects.filter(scale_id=scale.scale_name.id).order_by('-to_value')

        next_Lesson_id, next_module_id = self.get_value_to_get_next_lesson_url(
                                                            module=module,
                                                            lesson=lesson,
                                                            lesson_list=lesson_list,
                                                            enrolled_module=enrolled_module,
                                                            course=course,
                                                            current_student=current_student
                                                        )

        ######-----Mark as complete this course if there is no lesson left------####
        if not next_Lesson_id:
            enrolled_course.enrolment_status = 'completed'
            enrolled_course.save()

        relatedCourse = Course.objects.filter(category=course.category).exclude(id=course.id)[:3].select_related('category')

        context = {
            'course': course,
            'module': module,
            'lesson': lesson,
            'scale': scale,
            'question': question,
            'answer': answer,
            'score': score,
            'lesson_list': lesson_list,
            'relatedCourse': relatedCourse,
            'next_Lesson_id': next_Lesson_id,
            'next_module_id': next_module_id,
            'module_list': module_list,
            'percentage_complete': percentage_complete,
            'form': FeedbackForm() if lesson.lesson_type == 'feedback' else '',
            'running_course_active': 'active'
        }
        return render(request, 'lms/student-take-course.html', context)

    def post(self, request, cid, sid, lid):
        data = self.get_data_from_db(request, cid, sid, lid)
        course = data.get('course')
        current_student = data.get('current_student')
        module = data.get('module')
        lesson = data.get('lesson')

        enrolled_module = EnrolledModule.objects.filter(student_id=current_student.id, module_id=module.id) \
            .order_by('-enrolled_module_on').first()
        lesson_list = Lesson.objects.filter(module_id=module.id).order_by('lesson_position')

        next_Lesson_id, next_module_id = self.get_value_to_get_next_lesson_url(
            module=module,
            lesson=lesson,
            lesson_list=lesson_list,
            enrolled_module=enrolled_module,
            course=course,
            current_student=current_student
        )

        form = FeedbackForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            ff = Feedback(student_id=current_student, course_id=course,
                          quality=form.cleaned_data['quality'],
                          satisfaction=form.cleaned_data['satisfaction'],
                          good_comment=form.cleaned_data['good_comment'],
                          bad_comment=form.cleaned_data['bad_comment'],
                          opinion=form.cleaned_data['opinion'])
            ff.save()
            if next_Lesson_id:
                return redirect('takeCourse', cid=course.id, sid=next_module_id, lid=next_Lesson_id)
            else:
                return redirect('dashboard')



@method_decorator(login_required, name='dispatch')
class SaveLessonFeedbackView(View):

    @csrf_exempt
    def post(self, request, lessonId):
        user = request.user.id
        lesson = get_object_or_404(Lesson, id=lessonId)
        student = get_object_or_404(Student, name=user)
        inputtedData = request.POST
        inputToSave = LessonFeedbackCollection.objects.create(
            student_id=student,
            lesson=lesson,
            data=inputtedData
        )
        inputToSave.save()
        payload = {'success': True}
        return HttpResponse(json.dumps(payload), content_type='application/json')


class CourseListView(View):
    authenticated_template = 'lms/student-courses.html'
    unauthenticated_template = 'courses.html'

    def get(self, request):
        course = Course.objects.all().order_by('-updated_on')
        category = Category.objects.all().order_by('name')
        context = {
            'course': course,
            'all_course_active': 'active',
            'category': category
        }
        if request.user.is_authenticated:
            return render(request, self.authenticated_template, context)
        return render(request, self.unauthenticated_template, context)


# ############################ #
# ##         SCALE          ## #
# ############################ #

class ScaleListView(View):
    authenticated_template = 'lms/scale-list.html'
    unauthenticated_template = 'scale-list-guest.html'

    def get(self, request):
        scale = MeasuringScale.objects.all().order_by('name')
        context = {
            'scale': scale,
            'test_active': 'active'
        }
        if request.user.is_authenticated:
            return render(request, self.authenticated_template, context)
        else:
            return render(request, self.unauthenticated_template, context)


class ScaleDetailsView(View):
    authenticated_template = 'scale.html'
    unauthenticated_template = 'scale_guest.html'

    def get(self, request, scaleId):
        scale = get_object_or_404(MeasuringScale, id=scaleId)
        question = QuestionDetails.objects.filter(scale_id=scale.id).order_by('serial')
        answer = AnswerDetails.objects.filter(scale_id=scale.id).order_by('serial')
        score = ScoringDetails.objects.filter(scale_id=scale.id).order_by('-to_value')
        context = {
            'scale': scale,
            'question': question,
            'answer': answer,
            'score': score,
            'test_active': 'active'
        }
        if request.user.is_authenticated:
            return render(request, self.authenticated_template, context)
        else:
            return render(request, self.unauthenticated_template, context)


@method_decorator(login_required, name='dispatch')
class SaveScoreView(View):

    def post(self, request, scaleId):
        user = request.user.username
        scale = MeasuringScale.objects.filter(id=scaleId).first()
        if scale is not None:
            scaleToSave = MeasuringScaleForModuleResult.objects.create_score(
                request.user,
                scale,
                request.POST.get("score", 0),
                request.POST.get("result", "Not found")
            )
            scaleToSave.save()
            print("inside save score executed")
        print("outside save score executed")
        return HttpResponse('Successfully saved')


@method_decorator(login_required, name='dispatch')
class TestResultView(View):
    template_name = 'lms/student-test-result.html'

    def get(self, request):
        test_result = MeasuringScaleForModuleResult.objects.filter(user_id=request.user.id).order_by('-created_on')
        context = {
            'test_result': test_result,
            'self_test_result_active': 'active'
        }
        print(f"test result view template executed. data: {test_result}")
        return render(request, self.template_name, context)


# ############################ #
# ##    AUTHENTICATION      ## #
# ############################ #

class SignUpView(View):
    template_name = 'sign-up.html'
    form = RegisterForm()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template_name, {'form': self.form})

    @transaction.atomic
    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            inputedUserName = form.cleaned_data['username']
            if User.objects.filter(username=inputedUserName).exists():
                messages.add_message(request, messages.ERROR, "Mobile number already exists.")
                return render(request, self.template_name, {
                    'form': form,
                })
            elif not inputedUserName.isdigit():
                messages.add_message(request, messages.ERROR, "Enter correct mobile number")
                return render(request, self.template_name, {
                    'form': form,
                })
            else:
                fullName = form.cleaned_data['full_name']
                lName = ""
                if ' ' in fullName:
                    fName, lName = fullName.split(" ", 1)
                else:
                    fName = fullName
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'], "",
                    form.cleaned_data['password']
                )
                user.first_name = fName
                user.last_name = lName
                user.save()

                # Login the user
                login(request, user)

                # Create Student user
                student = Student.objects.create_student(
                    username=request.user,
                    age=form.cleaned_data['age'],
                    gender=form.cleaned_data['gender'],
                    address=form.cleaned_data['address'],
                    education=form.cleaned_data['education'],
                    ocupation=form.cleaned_data['ocupation'],
                    religion=form.cleaned_data['religion'],
                    marial_status=form.cleaned_data['marial_status'],
                    socio_economic_status=form.cleaned_data['socio_economic_status'],
                    mental_problem=form.cleaned_data['mental_problem'],
                    mental_treatment_type=form.cleaned_data['mental_treatment_type'],
                    medicine_taken_duration=form.cleaned_data['medicine_taken_duration'],
                    physical_problem=form.cleaned_data['physical_problem'],
                    knowing_source=form.cleaned_data['knowing_source'],
                )
                student.save()
                # redirect to accounts page:
                return redirect('dashboard')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, self.template_name)

    def post(self, request):
        user = request.POST.get('user')
        password = request.POST.get('password')
        auth = authenticate(request, username=user, password=password)
        if auth is not None:
            login(request, auth)
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.ERROR, "Username or Password Mismatch")
            return render(request, self.template_name)


def getPayment(request):
    return render(request, 'payment.html')


def getDenied(request, ):
    return render(request, 'lms/access-denied.html')
