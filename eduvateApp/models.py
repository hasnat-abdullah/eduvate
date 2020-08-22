from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime

#================================#
#============Instructor==========#
#================================#

class Country(models.Model):
    name = models.CharField(max_length=35, null=False)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    details = RichTextUploadingField()
    city = models.TextField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    image = models.ImageField(default='default', upload_to='image/pro_pics', blank=True)
    fb_url = models.URLField()
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name.username


class InstructorWorkHistory(models.Model):
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=60)
    designation = models.CharField(max_length=60)
    start_date = models.DateField(default=datetime.now, blank=False)
    end_date = models.DateField(default=None, blank=True)

    def __str__(self):
        return self.instructor_id.name.username+","+self.designation


class InstructorRating (models.Model):
    instructor_id = models.OneToOneField(Instructor, on_delete=models.CASCADE)
    rating_count = models.PositiveSmallIntegerField (default=0)
    rating_total_value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.instructor_id.name.username + "-"+str(self.rating_count)



#================================#
#==============Scale=============#
#================================#

class MeasuringScale(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


class QuestionDetails(models.Model):
    scale_id= models.ForeignKey(MeasuringScale, on_delete=models.CASCADE)
    serial = models.SmallIntegerField(null=False, default=1)
    question = models.CharField(max_length=800, null=False)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.scale_id.name +": "+ self.question


class AnswerDetails(models.Model):
    scale_id= models.ForeignKey(MeasuringScale, on_delete=models.CASCADE)
    choice = models.CharField(max_length=30,null=False)
    serial = models.SmallIntegerField(null=False, default=1)
    value = models.SmallIntegerField(null=False, default=1)

    def __str__(self):
        return self.scale_id.name +": "+ self.choice


class ScoringDetails(models.Model):
    scale_id= models.ForeignKey(MeasuringScale, on_delete=models.CASCADE)
    from_value = models.SmallIntegerField(null=False, default=0)
    to_value = models.SmallIntegerField(null=False, default=0)
    result = models.CharField(max_length=40, null=False,default="Minimal")

    def __str__(self):
        return self.scale_id.name +": "+ self.result




#================================#
#==============Course============#
#================================#

class Language(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(allow_unicode=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, null=False)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(allow_unicode=True)

    def __str__(self):
        return self.name


class CourseLevel(models.Model):
    name = models.CharField(max_length=50, null=False)
    slug = models.SlugField(allow_unicode=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=250, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    short_description = RichTextUploadingField()
    long_description = RichTextUploadingField()
    featured_image = models.ImageField(default='default', upload_to='image/courseImage', blank=True)
    featured_video = models.CharField(max_length = 400)
    course_lang = models.ForeignKey(Language, on_delete=models.PROTECT)
    requirement = models.CharField(max_length=500)
    pre_requisite = models.CharField(max_length=500)
    level = models.ForeignKey(CourseLevel, on_delete=models.PROTECT)
    what_u_will_learn = RichTextField(null=True)
    course_Lectures = models.IntegerField()

    total_student_enrolled = models.PositiveIntegerField( default=1)
    is_active = models.BooleanField(default=True)

    price = models.IntegerField()

    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(allow_unicode=True)

    def __str__(self):
        return self.name


class CourseInstructor(models.Model):
    course_id= models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    instructor_id= models.ForeignKey(Instructor,on_delete=models.CASCADE, default=1)



class LearningPath(models.Model):
    name = models.CharField(max_length=250, null=False)
    short_description = RichTextUploadingField()
    long_description = RichTextUploadingField()
    level = models.ForeignKey(CourseLevel, on_delete=models.PROTECT)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(allow_unicode=True)

    def __str__(self):
        return self.name


class PathCourse(models.Model):
    learning_path = models.ForeignKey(LearningPath, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    serial = models.IntegerField(null=False)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.learning_path.name


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module_position = models.SmallIntegerField(null=False)
    name = models.CharField(max_length=250, null=False)
    how_many_time_weekly_accessable = models.PositiveSmallIntegerField(null=False,default=1)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.course.name+": "+ self.name

LESSON_CHOICE= (
        ('content', 'Content'),
        ('scale', 'Scale'),
        ('feedback', 'Feedback Form')
    )

class Lesson(models.Model):
    module_id = models.ForeignKey(CourseModule, on_delete=models.CASCADE, default=1)
    lesson_type = models.CharField(max_length=8, choices=LESSON_CHOICE, default='content')
    lesson_position = models.SmallIntegerField(null=False)
    title = models.CharField(max_length=250, null=False)
    video = models.CharField(null=True, blank=True, max_length=350)
    description = RichTextUploadingField(null=True)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.module_id.course.name +": "+ self.module_id.name +": "+ self.title


class LessonScale(models.Model):
    lesson_id = models.OneToOneField(Lesson,on_delete=models.CASCADE)
    scale_name = models.ForeignKey(MeasuringScale, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.lesson_id.module_id.course.name +": "+ self.lesson_id.module_id.name +": "+ self.lesson_id.title+ " - " + self.scale_name.name


class MeasuringScaleForModule(models.Model):
    module_id = models.ForeignKey(CourseModule,on_delete=models.CASCADE, default=1)
    scale_name = models.ForeignKey(MeasuringScale, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.module_id.name +": "+ self.module_id.name + " - " + self.scale_name.name


#================================#
#=============Payment============#
#================================#

PAYMENT_STATUS_CHOICES = (
        ('completed', 'COMPLETED'),
        ('partial', 'PARTIAL'),
        ('cancel', 'CANCEL'),
        ('hold', 'HOLD'),
        ('pending', 'pending'),
        ('incomplete', 'INCOMPLETE'),
        ('refund', 'REFUND')
    )

PAYMENT_METHOD_CHOICE= (
        ('bkash', 'BKASH'),
        ('rocket', 'ROCKET')
    )


class Payment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    paid_for_module= models.ForeignKey(CourseModule, on_delete=models.PROTECT)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHOD_CHOICE, default='bkash')
    paid_amount = models.DecimalField(max_digits=8 ,decimal_places=2)
    txn_id = models.CharField(max_length=20)
    reference = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='incomplete')

    def __str__(self):
        return self.user_id.username+","+self.payment_method +"-"+ str(self.paid_amount) +"tk -"+ self.txn_id



#================================#
#============Student=============#
#================================#

class StudentManager(models.Manager):
    def create_student(self, username,age,gender,address,education,ocupation,religion,marial_status,socio_economic_status,mental_problem,mental_treatment_type,medicine_taken_duration,physical_problem,knowing_source):
        student = self.create(name=username,age=age,gender=gender,address=address,education=education,ocupation=ocupation,religion=religion,marial_status=marial_status,socio_economic_status=socio_economic_status,mental_problem=mental_problem,mental_treatment_type=mental_treatment_type,medicine_taken_duration=medicine_taken_duration,physical_problem=physical_problem,knowing_source=knowing_source,created_on=datetime.now)
        return student


GENDER_STATUS_CHOICES = (
        ('', '-নির্বাচন করুন-'),
        ('male', 'পুরুষ'),
        ('female', 'মহিলা'),
        ('other', 'অন্যান্য')
    )

MARITAL_STATUS_CHOICES = (
        ('', '-নির্বাচন করুন-'),
        ('unmarried', 'অবিবাহিত'),
        ('married', 'বিবাহিত'),
        ('divorced', 'তালাকপ্রাপ্ত'),
        ('widow', 'বিপত্নীক বা বিধবা'),
        ('other', 'অন্যান্য'),
    )

RELIGION_STATUS_CHOICES = (
        ('', '-নির্বাচন করুন-'),
        ('islam', 'ইসলাম'),
        ('hindu', 'হিন্দু'),
        ('christian', 'খ্রিষ্টান'),
        ('bouddho', 'বৌদ্ধ'),
        ('other', 'অন্যান্য'),
    )

SOCIALECONOMIC_STATUS_CHOICES = (
        ('', '-নির্বাচন করুন-'),
        ('lower', 'নিম্নবিত্ত (৫,০০০ টাকার নিচে)'),
        ('lower_middle', 'নিম্ন-মধ্যবিত্ত (৫,০০১ থেকে ৩০,০০০ টাকা)'),
        ('middle', 'মধ্যবিত্ত (৩০,০০১ থেকে ৭০,০০০ টাকা)'),
        ('higher', 'উচ্চবিত্ত (৭০,০০১ টাকা বা তার উপরে)'),
    )

YESNO_STATUS_CHOICES = (
        ('', '-নির্বাচন করুন-'),
        ('yes', 'হ্যাঁ'),
        ('no', 'না')
    )

TREATMENT_STATUS_CHOICES = (
        ('', '-নির্বাচন করুন-'),
        ('medicine', 'ওষুধ'),
        ('counseling', 'কাউন্সেলিং/ সাইকোথেরাপি')
    )

EDUCATIONAL_STATUS_CHOICES = (
        ('', '-নির্বাচন করুন-'),
        ('primary', 'প্রাথমিক'),
        ('secondary', 'মাধ্যমিক'),
        ('higher_secondary', 'উচ্চমাধ্যমিক'),
        ('graduation', 'স্নাতক'),
        ('post_graduation', 'স্নাতকোত্তর')
    )

OCUPATION_STATUS_CHOICES = (
        ('', '-নির্বাচন করুন-'),
        ('student', 'ছাত্র/ছাত্রী'),
        ('job', 'চাকুরী'),
        ('business', 'ব্যবসা'),
        ('other', 'অন্যান্য')
    )

MENTAL_PROBLEM_CHOICES = (
        ('', '-নির্বাচন করুন-'),
        ('depression', 'বিষন্নতা'),
        ('stress', 'উদ্বেগজনিত সমস্যা'),
        ('suicide', 'আত্নহত্যার প্রবণতা'),
        ('schizophrenia', 'সিজোফ্রেনিয়া'),
        ('bipolar', 'বাইপোলার মুড ডিসর্ডার'),
        ('other', 'অন্যান্য')
    )

KNOWING_WEBSITE_CHOICES = (
        ('', '-নির্বাচন করুন-'),
        ('friend', 'বন্ধু'),
        ('family', 'পরিবার'),
        ('fb', 'ফেসবুক'),
        ('counselor', 'মনোবিজ্ঞানী'),
        ('dr', 'ডাক্তার'),
        ('google', 'গুগল'),
        ('other', 'অন্যান্য')
    )


class Student(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_STATUS_CHOICES, default='male')
    address = models.CharField(max_length=200)
    education = models.CharField(max_length=60, choices=EDUCATIONAL_STATUS_CHOICES, default='primary')
    ocupation = models.CharField(max_length=30, choices=OCUPATION_STATUS_CHOICES, default='student')
    religion = models.CharField(max_length=30, choices=RELIGION_STATUS_CHOICES, default='islam')
    marial_status = models.CharField(max_length=30, choices=MARITAL_STATUS_CHOICES, default='unmarried')
    socio_economic_status = models.CharField(max_length=80, choices=SOCIALECONOMIC_STATUS_CHOICES, default='lower')
    mental_problem = models.CharField(max_length=40, null=True, choices=MENTAL_PROBLEM_CHOICES, default='depression')
    mental_treatment_type = models.CharField(max_length=50, null=True, choices=TREATMENT_STATUS_CHOICES, default='medicine')
    medicine_taken_duration = models.CharField(max_length=25,null=True)
    physical_problem = models.CharField(max_length=70, null=True)
    knowing_source = models.CharField(max_length=50, null=True, choices=KNOWING_WEBSITE_CHOICES,default='friend')

    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name.username

    objects = StudentManager()


class StudentWorkHistory(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=60)
    designation = models.CharField(max_length=60)
    start_date = models.DateField(default=datetime.now, blank=False)
    end_date = models.DateField(default=None, blank=True)

    def __str__(self):
        return self.student_id.name.username+","+self.designation


ENROLMENT_STATUS_CHOICES = (
        ('completed', 'COMPLETED'),
        ('partial', 'PARTIAL'),
        ('notStarted', 'NOTSTARTED')
    )


class EnrolledCourse(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolment_status = models.CharField(max_length=11, choices=ENROLMENT_STATUS_CHOICES, default='notStarted')
    percent_complited = models.SmallIntegerField(null=True)
    enrolled_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.course_id.name + " - " + self.student_id.name.username


class EnrolledModule(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    module_id = models.ForeignKey(CourseModule,models.CASCADE, default=1)
    payment_status= models.ForeignKey(Payment, on_delete=models.PROTECT, null=True)
    enrolment_status = models.CharField(max_length=11, choices=ENROLMENT_STATUS_CHOICES, default='notStarted')
    enrolled_module_on = models.DateField(auto_now=False, auto_now_add=True)
    last_visited_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.module_id.name + " - " + self.student_id.name.username


class CompletedLesson(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.PROTECT, null=True)
    complete_lesson_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)
    def __str__(self):
        return  self.student_id.name.username + " : " + self.lesson_id.module_id.name+ " : " + self.lesson_id.title


class CompletedCourse(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.PROTECT)
    complete_course_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return  self.student_id.name.username + " : " + self.course_id.name




class ScoreManager(models.Manager):
    def create_score(self, username, scale_name, totalMarks):
        studentScore = self.create(user_id=username,scale_name=scale_name,totalMarks=totalMarks,created_on=datetime.now)
        return studentScore


class MeasuringScaleForModuleResult(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    scale_name = models.ForeignKey(MeasuringScale, on_delete=models.CASCADE)
    totalMarks = models.PositiveSmallIntegerField()
    result = models.CharField(max_length=25, null=True)
    created_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user_id.username +": "+ str(self.created_on)

    objects=ScoreManager()



#================================#
#===========Appointment==========#
#================================#

DAY_CHOICES = (
        ('saturday', 'SATURDAY'),
        ('sunday', 'SUNDAY'),
        ('monday', 'MONDAY'),
        ('tuesday', 'TUESDAY'),
        ('wednesday', 'WEDNESDAY'),
        ('thursday', 'THURSDAY'),
        ('Friday', 'FRIDAY')
    )


class SlotList(models.Model):
    counselor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    from_time = models.TimeField(default=None)
    to_time = models.TimeField(default=None)
    day = models.CharField(max_length=9, choices=DAY_CHOICES, default='saturday')

    def __str__(self):
        return self.counselor.name.username+"; "+ self.day + ": " + str(self.from_time) +"-"+str(self.to_time)


class Booking (models.Model):
    booked_by=models.ForeignKey(Student, on_delete=models.PROTECT)
    slot_id = models.ForeignKey(SlotList, on_delete=models.PROTECT)
    booking_date = models.DateField(default=datetime.today)
    note = models.CharField(max_length=150)

    def __str__(self):
        return self.booked_by.name.username+"; "+ str(self.booking_date) + ": " + str(self.slot_id.from_time) +"-"+ str(self.slot_id.to_time)


#================================#
#=============Feedback===========#
#================================#

class Feedback(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.PROTECT)
    quality = models.CharField(max_length=4, null=True, blank=True)
    satisfaction = models.CharField(max_length=4, null=True, blank=True)
    good_comment = models.CharField(max_length=400, null=True, blank=True)
    bad_comment = models.CharField(max_length=400, null=True, blank=True)
    opinion = models.CharField(max_length=400, null=True, blank=True)
    complete_course_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return  self.course_id.name + " : " + self.student_id.name.username


