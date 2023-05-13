from django.contrib import admin


# Register your models here.
from .models import Student, Admin , College, Enrollment, Subject,Account


class AdminAdmin(admin.ModelAdmin):
    list_display = ('adminId', 'email', 'is_staff', 'is_superuser')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentId', 'email', 'degree_program', 'first_name', 'last_name', 'college', 'year_lvl', 'is_staff', 'is_superuser')


admin.site.register(Student, StudentAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(College)
admin.site.register(Enrollment)
admin.site.register(Subject)
