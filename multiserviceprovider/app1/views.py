from django.shortcuts import render, redirect
from .models import MyUser
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        myuser = authenticate(request, username=username, password=password)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login successful")
            return redirect('userpage')  # Redirect to userpage.html after successful login
        else:
            messages.error(request, "Login failed. Please check your credentials.")
            return redirect('signin')  # Redirect back to the signin page if login fails
    return render(request, 'signin.html')
def index(request):
    return render(request, "index.html")
def userpage(request):
    return render(request, "userpage.html")
def register(request):
    if request.method == 'POST': 
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST.get('username','')
        phoneno  = request.POST['mobile_no']
        state = request.POST['state']
        dob=request.POST['dob']
        district = request.POST['district']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirm_password']
        if password!=confirmpassword:
            messages.warning(request,'Password is not matching')
            return render(request,'signup.html')
        try:
            if MyUser.objects.get(username=username):
                messages.warning(request,'Username already taken')
                return render(request,'signup.html')
        except Exception as identifiers:
            pass
        user=MyUser.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,state=state,district=district,password=password,dob=dob,phone=phoneno)
        user.save()
        return redirect('signin')
    return render(request,'signup.html')