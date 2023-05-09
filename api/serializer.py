from rest_framework.serializers import ModelSerializer
from .models import Admin, Student, College, Subject,Enrollment

class AdminSerializer(ModelSerializer):
    class Meta:
        model =  Admin
        fields = '__all__'

class StudentSerializer(ModelSerializer):
    class Meta:
        model =  Student
        fields = '__all__'


class CollegeSerializer(ModelSerializer):
    class Meta:
        model =  College
        fields = '__all__'

class SubjectSerializer(ModelSerializer):
    class Meta:
        model =  Subject
        fields = '__all__'


class EnrollmentSerializer(ModelSerializer):
    class Meta:
        model =  Enrollment
        fields = '__all__'
