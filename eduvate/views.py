from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from eduvateApp.models import *
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def getIndex(request):
    course = Course.objects.all().order_by('-updated_on')
    context = {
        'course':course,
    }
    return render(request, 'index.html',context)


def getDashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'lms/student-dashboard.html', {'dashboard_active':'active'})

def getSingleCourse(request,id):
    course = get_object_or_404(Course,id=id)
    instructor = CourseInstructor.objects.filter(course_id=course.id).select_related('instructor_id')
    module = CourseModule.objects.filter(course=course.id)
    totalModule = len(module)
    relatedCourse = Course.objects.filter(category=course.category).exclude(id=course.id)[:3].select_related('category')
    context = {
        'course': course,
        'instructor':instructor,
        'module':module,
        'totalModule':totalModule,
        'relatedCourse':relatedCourse,
        'all_course_active':'active'
    }
    if request.user.is_authenticated:
        return render(request, 'lms/student-course.html',context)
    return render(request, 'course-single.html',context)


def gettakeCourse(request,cid,sid,lid):
    if not request.user.is_authenticated:
        return redirect('login')

    course = get_object_or_404(Course, id=cid)
    current_student = get_object_or_404(Student,name=request.user.id)

    if not EnrolledCourse.objects.filter(student_id=current_student.name.id, course_id=course.id).exists():
        return redirect('singleCourse', cid)

    module = get_object_or_404(CourseModule,id=sid)
    lesson = get_object_or_404(Lesson,id=lid)
    lesson_list = Lesson.objects.filter(module_id=module.id).order_by('lesson_position')
    total_lesson = Lesson.objects.filter(module_id__course__id=course.id).count()
    total_completed_lesson = completedLesson.objects.filter(student_id=request.user.id, lesson_id__module_id__course__id=course.id).count()
    percentage_complete = int((total_completed_lesson*100)/total_lesson)

    ######-----Mark as complete this lesson------####
    obj, created = completedLesson.objects.update_or_create(student_id=current_student, lesson_id=lesson)


    ######-----Next button url----########
    next_Lesson_id=''
    next_module_id=module.id
    for l in lesson_list:
        if l.lesson_position>lesson.lesson_position:
            next_Lesson_id=l.id
            break
    if not next_Lesson_id:
        next_module= CourseModule.objects.filter(course=course.id, module_position__gt=module.module_position)[:1]
        for m in next_module:
            next_module_id=m.id
            break
        if next_module_id !=module.id:
            next_lesson_list = Lesson.objects.filter(module_id=module.id).order_by('lesson_position')[:1]
            for l in next_lesson_list:
                next_Lesson_id = l.id

    relatedCourse = Course.objects.filter(category=course.category).exclude(id=course.id)[:3].select_related('category')

    context = {
        'course': course,
        'module':module,
        'lesson':lesson,
        'lesson_list':lesson_list,
        'relatedCourse':relatedCourse,
        'next_Lesson_id':next_Lesson_id,
        'next_module_id':next_module_id,
        'percentage_complete':percentage_complete,
        'running_course_active':'active'
    }
    return render(request, 'lms/student-take-course.html',context)


def getSaveScore(request,scaleId):
    if request.user.is_authenticated:
        user= request.user.username
        scale = get_object_or_404(MeasuringScale, id=scaleId)
        scaleScore = request.POST["score"]
        scaleToSave = MeasuringScaleForModuleResult.objects.create_score(
            request.user,
            scale,
            request.POST["score"],
        )
        scaleToSave.save()
        return redirect('dashboard')
    return render(request, 'lms/student-dashboard.html')


def getScale(request, scaleId):
    scale = get_object_or_404(MeasuringScale,id=scaleId)
    question = QuestionDetails.objects.filter(scale_id=scale.id).order_by('serial')
    answer = AnswerDetails.objects.filter(scale_id=scale.id).order_by('serial')
    score = ScoringDetails.objects.filter(scale_id=scale.id).order_by('-to_value')
    context = {
        'scale': scale,
        'question': question,
        'answer': answer,
        'score':score,
        'test_active':'active'
    }
    if request.user.is_authenticated:
        return render(request, 'scale.html',context)
    else:
        return render(request, 'scale_guest.html',context)


def getScaleList(request):
    scale = MeasuringScale.objects.all().order_by('name')
    context = {
        'scale': scale,
        'test_active':'active'
    }
    if request.user.is_authenticated:
        return render(request, 'lms/scale-list.html',context)
    else:
        return render(request, 'scale-list-guest.html',context)


def getSignup(request):
    # if this is a POST request we need to process the form data
    template = 'sign-up.html'
    if request.user.is_authenticated:
        return redirect('index')

    elif request.method== 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            inputedUserName = form.cleaned_data['username']
            if User.objects.filter(username=inputedUserName).exists():
                messages.add_message(request, messages.ERROR, "Mobile number already exists.")
                return render(request, template, {
                    'form': form,
                })
            elif not inputedUserName.isdigit():
                messages.add_message(request, messages.ERROR, "Enter correct mobile number")
                return render(request, template, {
                    'form': form,
                })
            else:
                fullName = form.cleaned_data['full_name']
                lName = ""
                if ' ' in fullName:
                    fName,lName = fullName.split(" ", 1)
                else:
                    fName=fullName
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],"",
                    form.cleaned_data['password']
                )
                user.first_name = fName
                user.last_name = lName
                user.save()

                # Login the user
                login(request, user)

                #Create Student user
                student = Student.objects.create_student(
                    request.user,
                    form.cleaned_data['age'],
                    form.cleaned_data['gender'],
                    form.cleaned_data['address'],
                    form.cleaned_data['education'],
                    form.cleaned_data['ocupation'],
                    form.cleaned_data['religion'],
                    form.cleaned_data['marial_status'],
                    form.cleaned_data['socio_economic_status'],
                    form.cleaned_data['mental_problem'],
                    form.cleaned_data['mental_treatment_type'],
                    form.cleaned_data['medicine_taken_duration'],
                    form.cleaned_data['physical_problem'],
                    form.cleaned_data['knowing_source'],
                )
                student.save()
                # redirect to accounts page:
                return redirect('dashboard')
    # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})


def getLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('password')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('dashboard')
            else:
                messages.add_message(request, messages.ERROR, "Username or Password Mismatch")
    #if request.method == 'POST' and request.user.is_authenticated == False:
    return render(request, 'login.html')


def getLogout(request):
    logout(request)
    return redirect('index')


def getCourse(request):
    course = Course.objects.all().order_by('-updated_on')
    category = Category.objects.all().order_by('name')
    context = {
        'course': course,
        'all_course_active':'active',
        'category':category
    }
    if request.user.is_authenticated:
        return render(request, 'lms/student-courses.html', context)
    return render(request, 'courses.html', context)


def getRunningCourse(request):
    if request.user.is_authenticated:
        course = EnrolledCourse.objects.filter(student_id=request.user.id).order_by('-enrolled_on').select_related('course_id')
        context = {
            'course': course,
            'running_course_active':'active'
        }
        return render(request, 'lms/student-running-courses.html', context)
    return render(request, 'courses.html')


def getPayment(request):
    return render(request, 'payment.html')