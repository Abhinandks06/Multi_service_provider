from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .models import MyUser
from .views import *
from django.views.decorators.cache import cache_control
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'  # Your template for the password reset form
    email_template_name = 'password_reset_email.html'  # Your email template for the password reset email
    success_url = reverse_lazy('resetpassworddone')  # URL to redirect after successful form submission
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'  # Your template for password reset confirmation form
    success_url = reverse_lazy('passwordresetcomplete')  # URL to redirect after successful password reset
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'  # Your template for password reset done page
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'  # Your template for password reset complete page
# Signin View
def signin(request):
    request.session.flush() 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        myuser = authenticate(request, username=username, password=password)
        if myuser is not None:
            request.session['username'] = username
            login(request, myuser)
            if myuser.role == "client":
                return redirect('userpage')
            elif myuser.role == "worker":
                return redirect('workerpage')
            elif myuser.role == "provider":
                return redirect('providerpage')
            elif myuser.role == "admin":
                return redirect('custom_admin_page')
        else:
            messages.error(request, "Incorrect Login. Please check your credentials.")
            return redirect('signin')
    return render(request, 'signin.html')

# Register View
def register(request):
    if request.method == 'POST':
        # Get form data
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username', '')
        phoneno = request.POST.get('mobile_no')
        state = request.POST.get('state')
        dob = request.POST.get('dob')
        district = request.POST.get('district')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')
        role = request.POST.get('role')  # Get selected role from the dropdown
        
        # Check for empty fields
        if not firstname or not lastname or not username or not phoneno or not state or not dob or not district or not email or not password or not confirmpassword or not role:
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        # Check password match
        if password != confirmpassword:
            messages.error(request, 'Password does not match the confirm password.')
            return render(request, 'signup.html')

        try:
            if MyUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            elif MyUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already taken.')
            # elif MyUser.objects.filter(phone=phoneno).exists():
            #     messages.error(request, 'Phone number already taken.')
            else:
                # Create user with the selected role
                user = MyUser.objects.create_user(
                    first_name=firstname,
                    last_name=lastname,
                    username=username,
                    email=email,
                    state=state,
                    district=district,
                    password=password,
                    dob=dob,
                    phone=phoneno,
                    role=role  # Set user role from the dropdown
                )
                messages.success(request, 'Account successfully registered.')
                return redirect('signin')  # Redirect to signin page after successful registration
        except Exception as e:
            if MyUser.objects.filter(phoneno=phoneno).exists():
                messages.error(request, 'Phone Number already taken.')
            messages.error(request, f'Error: {e}')

    return render(request, 'signup.html')
def user_logout(request):
    try:
        del request.session['username']
        request.session.flush()
    except KeyError:
        pass
    return redirect('signin')


def worker_logout(request):
    try:
        del request.session['username']
        request.session.flush() 
    except KeyError:
        pass
    return redirect('signin')

def provider_logout(request):
    try:
        del request.session['username']
        request.session.flush() 
    except KeyError:
        pass
    return redirect('signin')

def admin_logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('index')
def index(request):
    request.session.flush() 
    return render(request, "index.html")
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def userpage(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            if user.role == 'client':
                return render(request, 'userpage.html')
            else:
                messages.error(request, "You dont have permission to access this page.")
                return redirect('signin')
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
        return redirect('signin')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def workerpage(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            if user.role == 'worker':
                return render(request, 'workerpage.html')
            else:
                messages.error(request, "You dont have permission to access this page.")
                return redirect('signin')
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
        return redirect('signin')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def providerpage(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            if user.role == 'provider':
                return render(request, 'providerpage.html')
            else:
                messages.error(request, "You dont have permission to access this page.")
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
    messages.error(request, "You dont have permission to access this page.")
    return redirect('signin')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def custom_admin_page(request):
    User = get_user_model()
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = User.objects.get(username=username)
            if user.role == 'admin':
                user_profiles = User.objects.all()
                context = {'user_profiles': user_profiles}
                return render(request, 'admin.html', context)
            else:
                messages.error(request, "You dont have permission to access this page.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
    return redirect('signin')

    
    
