from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager, PermissionsMixin,Group,Permission

# Create your models here.

from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    class Meta:
        abstract = True  # This is the key change

    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = AccountManager()

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='customuser_groups',
        related_query_name='customuser_group',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='customuser_permissions',
        related_query_name='customuser_permission',
    )

    REQUIRED_FIELDS = []  # you might want to include email as a required field


class Admin(Account):
    adminId = models.CharField(max_length=100, primary_key=True)
    
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='admin_groups',  # unique related_name
        related_query_name='admin_group',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='admin_permissions',  # unique related_name
        related_query_name='admin_permission',
    )
    
    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)

    USERNAME_FIELD = 'adminId' 
    
    def __str__(self):
        return self.adminId

class Student(Account):
    studentId = models.CharField(max_length=100, primary_key=True)
    degree_program = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    college = models.CharField(max_length=100)
    year_lvl = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
  
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='student_groups',  # unique related_name
        related_query_name='student_group',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='student_permissions',  # unique related_name
        related_query_name='student_permission',
    )

    USERNAME_FIELD = 'studentId' 
    def __str__(self):
        return self.studentId



# class AccountManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError('The Username field must be set')
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(username, password, **extra_fields)
    
# class Admin(AbstractBaseUser, PermissionsMixin):
#     adminId = models.CharField(max_length=100, primary_key=True)
#     password = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#     last_login = models.DateTimeField(blank=True, null=True)

#     groups = models.ManyToManyField(
#         Group,
#         blank=True,
#         related_name='admin_groups',
#         related_query_name='admin_group',
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         blank=True,
#         related_name='admin_permissions',
#         related_query_name='admin_permission',
#     )

#     USERNAME_FIELD = 'adminId'
#     REQUIRED_FIELDS = []

#     objects = AccountManager()

#     def __str__(self):
#         return self.adminId

#     def save(self, *args, **kwargs):
#         self.is_superuser = True
#         super().save(*args, **kwargs)

        
# class Student(AbstractBaseUser, PermissionsMixin):
#     studentId = models.CharField(max_length= 100, primary_key= True)
#     password = models.CharField(max_length= 100)
#     degree_program = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     college = models.CharField(max_length = 100)
#     year_lvl = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#     last_login = models.DateTimeField(blank=True, null=True)

#     groups = models.ManyToManyField(
#         Group,
#         blank=True,
#         related_name='student_groups',
#         related_query_name='student_group',
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         blank=True,
#         related_name='student_permissions',
#         related_query_name='student_permission',
#     )

#     USERNAME_FIELD = 'studentId'
#     REQUIRED_FIELDS = []

#     objects = AccountManager()
    

#     def __str__(self):
#         return (self.studentId)


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



class Enrollment(models.Model):
    enrollment_id = models.CharField(max_length=100, primary_key=True)
    student_id = models.ForeignKey(Student, on_delete= models.CASCADE, null = True, blank = True)
    offer_code = models.ForeignKey(Subject, on_delete= models.CASCADE, null = True, blank = True)
    date_enrolled = models.DateField(auto_now_add=True)


    def __str__(self):
        return (self.enrollment_id)
