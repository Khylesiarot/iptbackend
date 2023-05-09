from django.contrib import admin


# Register your models here.
from .models import Student, Admin , College, Enrollment, Subject
admin.site.register(Student)
admin.site.register(Admin)
admin.site.register(College)
admin.site.register(Enrollment)
admin.site.register(Subject)
