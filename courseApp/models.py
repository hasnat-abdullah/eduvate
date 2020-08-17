from django.db import models
from instructorApp.models import Instructor
from scaleApp.models import MeasuringScale
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

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
    what_u_will_learn = RichTextField
    course_hours = models.CharField(max_length=20)
    course_Lectures = models.IntegerField()

    total_student_enrolled = models.PositiveIntegerField()
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
        return self.name


class Lesson(models.Model):
    module_id = models.ManyToManyField(CourseModule)
    lesson_position = models.SmallIntegerField(null=False)
    title = models.CharField(max_length=250, null=False)
    video = models.URLField(max_length=300)
    description = RichTextUploadingField()
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.module_id.name) +": "+ self.title


class MeasuringScaleForModule(models.Model):
    module_id = models.ForeignKey(CourseModule,on_delete=models.CASCADE)
    scale_name = models.ManyToManyField(MeasuringScale)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.module_id.name +": "+ self.module_id.name + " - " + self.scale_name.name