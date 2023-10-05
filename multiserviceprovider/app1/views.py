from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MyUser
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import authenticate, login,get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
@login_required
def signin(request):
    if 'username' in request.session:
        return redirect('userpage')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        myuser = authenticate(request, username=username, password=password)
        if myuser is not None:
            if myuser.role=="client":
                request.session['username'] = username
                login(request, myuser)
                return redirect('userpage')
            elif myuser.role=="worker":
                request.session['username'] = username
                login(request, myuser)
                return redirect('workerpage')
            elif myuser.role=="provider":
                request.session['username'] = username
                login(request, myuser)
                return redirect('providerpage')  
            elif myuser.role=="admin":
                request.session['username'] = username
                login(request, myuser)
                return redirect('custom_admin_page')  # Redirect to userpage.html after successful login
        else:
            messages.error(request, "Login failed. Please check your credentials.")
            return redirect('signin')  # Redirect back to the signin page if login fails
    return render(request, 'signin.html')
def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == 'POST': 
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username','')
        phoneno  = request.POST.get('mobile_no')
        state = request.POST.get('state')
        dob=request.POST.get('dob')
        district = request.POST.get('district')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')
        if password!=confirmpassword:
            messages.warning(request,'Password is not matching')
            return render(request,'signup.html')
        try:
            if MyUser.objects.get(username=username):
                messages.warning(request,'Username already taken')
                return render(request,'register')
        except Exception as identifiers:
            pass
        user=MyUser.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,state=state,district=district,password=password,dob=dob,phone=phoneno,role="client")
        user.save()
        messages.error(request, "Account successfully registred.")
        return render(request,'signin.html')
    return render(request,'signup.html')

def user_logout(request):
    try:
        del request.session['username']
    except:
        return redirect('signin')
    return redirect('signin')
def worker_logout(request):
    try:
        del request.session['username']
    except:
        return redirect('signin')
    return redirect('signin')
def provider_logout(request):
    try:
        del request.session['username']
    except:
        return redirect('signin')
    return redirect('signin')
def admin_logout(request):
    try:
        del request.session['username']
    except:
        return redirect('signin')
    return redirect('signin')
@login_required
def userpage(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            if user.role == 'client':  # Assuming role is a string
                return render(request, 'userpage.html')
            else:
                messages.error(request, "You dont have permission to access this page.")
                request.session.clear()  # Clear the session, effectively logging out the user
                return redirect('signin')  # Redirect to the signin page
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
        return redirect('signin')  # Redirect to the signin page

    return HttpResponse("An error occurred. Please try again.")
@login_required
def workerpage(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            if user.role == 'worker':  # Assuming role is a string
                response = render(request, 'workerpage.html')
                response['Cache-Control'] = 'no-store, must-revalidate'
                return response
            else:
                messages.error(request, "You dont have permission to access this page.")
                request.session.clear()  # Clear the session, effectively logging out the user
                return redirect('signin')
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
    return redirect('signin') 
@login_required
def providerpage(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            if user.role == 'provider':  # Assuming role is a string
                response = render(request, 'providerpage.html')
                response['Cache-Control'] = 'no-store, must-revalidate'
                return response
            else:
                messages.error(request, "You don't have permission to access this page.")
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
    return redirect('signin') 
from django.contrib.auth.decorators import login_required
def custom_admin_page(request):
    User = get_user_model()
    user_profiles = User.objects.all()
    
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    
    # Render the HTML template
    return render(request, 'admin.html', context)

    
    
