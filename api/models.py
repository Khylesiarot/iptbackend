from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Admin(models.Model):
    adminId = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.adminId

    def save(self, *args, **kwargs):
        self.is_superuser = True
        super(Admin, self).save(*args, **kwargs)


class College(models.Model):
    college_adminID = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    collegeId = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_college_title'),
        ]

    def __str__(self):
        return self.title


class Subject(models.Model):
    subject_adminID = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    offerCode = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100, null=False)
    course_number = models.CharField(max_length=1000)
    desc_title = models.CharField(max_length=1000)
    units = models.IntegerField()
    college_title = models.ForeignKey(College, on_delete=models.CASCADE, to_field='title', null=True, blank=True)

    def __str__(self):
        return self.title


  

    

    

class Student(models.Model):
    studentId = models.CharField(max_length= 100, primary_key= True)
    password = models.CharField(max_length= 100)
    degree_program = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    college = models.CharField(max_length = 100)
    year_lvl = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return (self.studentId)

    



class Enrollment(models.Model):
    enrollment_id = models.CharField(max_length=100, primary_key=True)
    student_id = models.ForeignKey(Student, on_delete= models.CASCADE, null = True, blank = True)
    offer_code = models.ForeignKey(Subject, on_delete= models.CASCADE, null = True, blank = True)
    date_enrolled = models.DateField(auto_now_add=True)


    def __str__(self):
        return (self.enrollment_id)
