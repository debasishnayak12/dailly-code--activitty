from django.http import JsonResponse
from .models import Employee
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .serializers import EmployeeSerializer
from rest_framework.response import Response


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        age = request.POST['Age']
        department = request.POST['department']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        employee = Employee.objects.create(user=user, age=age, department=department)
        user.save()
        employee.save()
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('home')

    return render(request, 'signup.html')

@csrf_protect
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'home.html')

def employee_list(request):
    employees = Employee.objects.all().values('user', 'age', 'department')
    return JsonResponse(list(employees), safe=False)



@api_view(['GET'])
def api_employee_list(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def setemployee(request):
    user = request.POST['user']
    age = request.POST['Age']
    department = request.POST['department']
    employee = Employee.objects.create(user=user, age=age, department=department)
    serializer = EmployeeSerializer(employee, many=False)
    return Response({"status":True, "message":"Employee created successfully","data":serializer.data})