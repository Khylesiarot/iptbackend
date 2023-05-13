
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from random import choices
from string import ascii_uppercase, digits
from rest_framework import status





from api.models import Student,Admin,College,Subject,Enrollment
from api.serializer import StudentSerializer,AdminSerializer,CollegeSerializer,SubjectSerializer,EnrollmentSerializer

# Create your views here.
@csrf_exempt
@api_view(['GET','POST',"DELETE",])
def getadminAPI(request, ):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AdminSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == 'GET':
        admin = Admin.objects.all()
        serializer = AdminSerializer(admin, many =True)
        return Response(serializer.data, status=200)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        admin = Admin.objects.get(adminID = data['adminID'])
        serializer = AdminSerializer(admin,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201) 


@csrf_exempt
@api_view(['GET','POST',"DELETE",])
def getStudentsAPI(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        student_id = data.get('studentId')
    # check if student with this ID already exists in the database
        if Student.objects.filter(studentId=student_id).exists():
         return Response({"error": "A student with this ID already exists."}, status=409)
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data, status=200)
    
        
@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def getSubjectsAPI(request, offerCode=""):
    if request.method == 'POST':
        data = request.data
        offer_code = data.get('offerCode')
        if Subject.objects.filter(offerCode=offer_code).exists():
            return Response({'error': 'Offer code already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        if offerCode:
            subject = Subject.objects.get(offerCode=offerCode)
            serializer = SubjectSerializer(subject)
            return Response(serializer.data, status=200)
        else:
            subject = Subject.objects.all()
            serializer = SubjectSerializer(subject, many=True)
            return Response(serializer.data, status=200)

    elif request.method == 'PUT':
        data = request.data
        subject = Subject.objects.get(offerCode=data['offerCode'])
        serializer = SubjectSerializer(subject, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        subject = Subject.objects.get(offerCode=offerCode)
        subject.delete()
        return Response(status=204)
    
    
    
@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def getCollegesAPI(request, id=""):
    if request.method == 'POST':
        data = request.data
        title = data.get('title', None)
        description = data.get('description', None)

        if not title or not description:
            return Response({'error': 'Both title and description are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            existing_college = College.objects.get(title=title, description=description)
            serializer = CollegeSerializer(existing_college)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except College.DoesNotExist:
            pass

        serializer = CollegeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'GET':
        college = College.objects.all()
        serializer = CollegeSerializer(college, many=True)
        return Response(serializer.data, status=200)

    elif request.method == 'PUT':
        data = request.data
        college = College.objects.get(offerCode=data['offerCode'])
        serializer = CollegeSerializer(college, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        college = College.objects.get(collegeId=id)
        college.delete()
        return Response(status=204)
        


@api_view(['POST'])
def loginAPI(request):
    username = request.data.get('username')
    password = request.data.get('password')

    admin = None
    student = None
    
    try:
        # Check if user is an admin
        admin = Admin.objects.get(adminId=username)
        if admin.password == password:
            token = ''.join(choices(ascii_uppercase + digits, k=10))
            return Response({'token': 'A-' + token}, status=status.HTTP_200_OK)
    except Admin.DoesNotExist:
        pass
    
    try:
        # Check if user is a student
        student = Student.objects.get(studentId=username)
        if student.password == password:
            token = ''.join(choices(ascii_uppercase + digits, k=5))
            return Response({'token': 'S-' + token}, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        pass

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def getAdmin(request, id):
     admin = Admin.objects.get(adminId=id)
     serializer = AdminSerializer(admin)
     return JsonResponse(serializer.data, status=200 )

def getUser(request, id):
    student = Student.objects.get(studentId=id)
    serializer = StudentSerializer(student)
    return JsonResponse(serializer.data, status=200)


@api_view(['GET', 'POST'])
def enrollment_list(request, student_id = ""):
    if request.method == 'GET':
        if student_id:
            enrollment = Enrollment.objects.filter(student_id=student_id)
            serializer = EnrollmentSerializer(enrollment, many=True)
            return Response(serializer.data, status=200)
        else:
            enrollment = Enrollment.objects.all()
            serializer = EnrollmentSerializer(enrollment, many=True)
            return Response(serializer.data, status=200)
        
    elif request.method == 'POST':
        data = request.data
        student_id = data.get('student_id')
        offer_code = data.get('offer_code')
        existing_enrollment = Enrollment.objects.filter(student_id=student_id, offer_code=offer_code).first()
        if existing_enrollment:
            return Response({'error': 'Offer code already used by this student.'}, status=400)
        serializer = EnrollmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



@csrf_exempt
@api_view(['GET'])
def getRoutes(request):
    routes = [
            {
            'name': 'home',
            'path': '/',
            'component': 'home',
            },
            {
            'name': 'about',
            'path': '/about',
            'component': 'about',
            },
            {
            'name': 'contact',
            'path': '/contact',
            'component': 'contact',
            },
        ]
    return Response(routes)


class StudentSubjectView(APIView):
    def get(self, request, student_id):
        enrollments = Enrollment.objects.filter(student_id=student_id)
        offer_codes = [enrollment.offer_code.offerCode for enrollment in enrollments]
        subjects = Subject.objects.filter(offerCode__in=offer_codes)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class TotalUnits(APIView):
    def get(self, request, student_id):
        enrollments = Enrollment.objects.filter(student_id=student_id)
        offer_codes = [enrollment.offer_code.offerCode for enrollment in enrollments]
        subjects = Subject.objects.filter(offerCode__in=offer_codes)
        total_units = sum([subject.units for subject in subjects])
        serializer = SubjectSerializer(subjects, many=True)
        data = { "total_units": total_units}
        return Response(data, status=status.HTTP_200_OK)
