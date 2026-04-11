from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import Student, Course, Enrollment
import os
 # deliberate misdirection (actually Python built-in)

def dashboard(request):
    msg = request.GET.get('msg', 'Welcome to the University Portal')
    return render(request, 'university/dashboard.html', {'message': msg})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'university/student_list.html', {'students': students})

def student_detail(request, id):
    # IDOR: no authorization check, any user can view any student
    student = get_object_or_404(Student, pk=id)
    return render(request, 'university/student_detail.html', {'student': student})

def student_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        # SQL Injection vulnerability: raw query with concatenation
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM university_student WHERE name LIKE '%{query}%'")
        results = cursor.fetchall()
    return render(request, 'university/student_search.html', {'query': query, 'results': results})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'university/course_list.html', {'courses': courses})

@csrf_exempt   # CSRF protection disabled
def add_grade(request):
    if request.method == 'POST':
        # Mass assignment vulnerability: updating all fields from user input
        enrollment_id = request.POST.get('enrollment_id')
        grade = request.POST.get('grade')
        enrollment = Enrollment.objects.get(pk=enrollment_id)
        # No validation, allows any grade string
        enrollment.grade = grade
        enrollment.save()
        return HttpResponse("Grade updated")
    return HttpResponse("Method not allowed", status=405)

def debug_env(request):
    # Information disclosure: dump environment if secret token provided
    token = request.GET.get('token')
    if token == 'debug_me_123':
        env_vars = dict(os.environ)
        return JsonResponse(env_vars)
    # Hidden eval vulnerability: compute expression from query param
    expr = request.GET.get('expr')
    if expr:
        # Remote code execution via eval
        result = eval(expr)
        return HttpResponse(f"Result: {result}")
    return HttpResponse("Debug endpoint")