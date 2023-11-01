from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .models import MyUser,Client,Worker
from django.core.exceptions import ValidationError
from .views import *
from django.views.decorators.cache import cache_control
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from social_django.models import UserSocialAuth
from django.contrib.auth.hashers import check_password
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
from django.contrib.auth import authenticate, login
from .models import Client, ServiceProvider, Worker

def signin(request):
    request.session.flush() 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        myuser = authenticate(request, username=username, password=password)
        if myuser is not None:
            request.session['username'] = username
            login(request, myuser)
        
            # Redirect to the corresponding user page and pass the user_instance as context
            if myuser.role == "client":
                return render(request, 'userpage.html')
            elif myuser.role == "provider":
                return render(request, 'providerpage.html')
            elif myuser.role == "worker":
                return render(request, 'workerpage.html')
            elif myuser.role == "admin":
                return redirect('custom_admin_page')
        else:
            messages.error(request, "Incorrect Login. Please check your credentials.")
            return redirect('signin')

    return render(request, 'signin.html')


# Register View
def register(request):
    user = None  # Initialize user variable outside the if block
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
        role = "client"  # Get selected role from the dropdown
        
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
            elif Client.objects.filter(phone=phoneno).exists():
                messages.error(request, 'Phone number already taken.')
            else:
                # Create MyUser instance
                hashed_password = make_password(password)
                User = get_user_model()
                user = User.objects.create(
                    username=username,
                    email=email,
                    password=hashed_password,
                    role=role
                )

                # Create Client instance associated with the created MyUser instance
                client = Client.objects.create(
                    first_name=firstname,
                    last_name=lastname,
                    username=username,
                    email=email,
                    dob=dob,
                    password=hashed_password,
                    phone=phoneno,
                    district=district,
                    state=state,
                    role=role,
                    user=user
                )

                messages.success(request, 'Account successfully registered.')
                return redirect('signin')  # Redirect to signin page after successful registration

        except ValidationError as e:
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
def services(request):
    request.session.flush() 
    return render(request, "servicelist.html")
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
        return render(request, 'userpage.html')
        

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

from itertools import chain
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def custom_admin_page(request):
    User = get_user_model()
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = User.objects.get(username=username)
            if user.role == 'admin':
                user_profiles=MyUser.objects.select_related('serviceprovider', 'client', 'worker').all()
                
                
                context = {'user_profiles': user_profiles}
                return render(request, 'admin.html', context)
            else:
                messages.error(request, "You don't have permission to access this page.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
    return redirect('signin')
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import MyUser
from django.template.loader import render_to_string
def deactivate_user(request, userid):
    user = get_object_or_404(MyUser, userid=userid)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'abhinandks2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

    return redirect('custom_admin_page')

def activate_user(request, userid):
    user = get_object_or_404(MyUser, userid=userid)
    if not user.is_active:
        user.is_active = True
        user.save()
        subject = 'Account activated'
        message = 'Your account has been activated.'
        from_email = 'abhinandks2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'user': user})
        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    return redirect('custom_admin_page')
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .forms import ClientProfileForm
def provider_registration(request):
    if request.method == 'POST':
        provider_name = request.POST.get('providername')
        provider_email = request.POST.get('email')
        
        # Validate the input fields here if necessary
        
        # Replace 'YOUR_BASE_URL' with the actual base URL of your website
        base_url = 'http://127.0.0.1:8000/provider_reg'
        
        # Create a registration link
        registration_path = "register"  # Relative path for registration
        registration_link = f"{base_url}/{register}"
        
        # Render HTML content for the email
        html_message = render_to_string('provider_registration_email.html', {
            'provider_name': provider_name,
            'registration_link': registration_link
        })
        
        # Send HTML email to the provider's email
        subject = 'Provider Registration Link'
        plain_message = f"Click the following link to complete your registration: {registration_link}"
        from_email = settings.DEFAULT_FROM_EMAIL
        
        email = EmailMessage(subject, plain_message, from_email, [provider_email])
        email.content_subtype = "html"
        email.send(fail_silently=False)
        
        # Redirect to a success page or display a success message
        return render(request, 'provider_registration_success.html')
    
    return render(request, 'provider_registration_form.html')
def provider_reg(request):
    request.session.flush() 
    return render(request, "provider_registration.html")
from django.urls import reverse
def worker_registration(request):
    if request.method == 'POST':
        # Get data from the form
        worker_name = request.POST.get('workerrname')
        worker_email = request.POST.get('email')
        base_url = 'http://127.0.0.1:8000/worker_reg'
        # Validate the input fields here if necessary
        
        # Generate registration link using reverse() function
        registration_link = f"{base_url}"
        
        # Render HTML content for the email
        html_message = render_to_string('worker_registration_email.html', {
            'worker_name': worker_name,
            'registration_link': registration_link,
          })
        # Send HTML email to the worker's email
        subject = 'Worker Registration Link'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        email = EmailMessage(subject, html_message, from_email, [worker_email])
        email.content_subtype = "html"
        email.send(fail_silently=False)
        # Redirect to a success page or display a success message
        return render(request, 'worker_registration_success.html')
    
    return render(request, 'worker_registration_form.html')
def worker_reg(request):
    request.session.flush() 
    return render(request, "worker_registration.html")

def providerlist(request):
    request.session.flush() 
    return render(request, "providerlist.html")
def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect("signin")


from django.shortcuts import render, redirect
from .models import ServiceProvider
from django.contrib import messages
from django.contrib.auth.hashers import make_password
def providerregister(request):
    if request.method == 'POST':
        # Get form data
        providername = request.POST.get('providername')
        ownername = request.POST.get('ownername')
        username = request.POST.get('username')
        password = request.POST.get('password')
        state = request.POST.get('state')
        district = request.POST.get('district')
        contact_number = request.POST.get('contact_no')
        email = request.POST.get('email')
        service_type = request.POST.get('service_type')
        role = "provider"
        
        # Check for empty fields
        if not providername or not ownername or not username or not password or not state or not district or not contact_number or not email or not service_type:
            messages.error(request, 'All fields are required.')
            return render(request, 'provider_registration.html')
        try:
            if not email:
                raise ValidationError("Email is required.")
            # Create MyUser instance
            User = get_user_model()
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,  # Store the password (it will be hashed internally)
                role=role
            )

            # Create ServiceProvider instance associated with the created MyUser instance
            service_provider = ServiceProvider.objects.create(
                user=user,  # Assign the MyUser instance to the user field of ServiceProvider
                providername=providername,
                ownername=ownername,
                password=make_password(password),  # Store the hashed password
                state=state,
                username=username,
                email=email,
                district=district,
                contact_number=contact_number,
                service_type=service_type,
                role=role

            )

            messages.success(request, 'Account successfully registered.')
            return redirect('signin')  # Redirect to signin page after successful registration

        except ValidationError as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'provider_registration.html')
def workerregister(request):
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
        role = "worker"  # Get selected role from the dropdown
        
        # Check for empty fields
        if not firstname or not lastname or not username or not phoneno or not state or not dob or not district or not email or not password or not confirmpassword or not role: 
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        # Check password match
        if password != confirmpassword:
            messages.error(request, 'Password does not match the confirm password.')
            return render(request, 'signup.html')

        try:
            if not email:
                raise ValidationError("Email is required.")
            # Create MyUser instance
            User = get_user_model()
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,  # Store the password (it will be hashed internally)
                role=role
            )

            # Create Worker instance associated with the created MyUser instance
            worker = Worker.objects.create(
                user=user,  # Assign the MyUser instance to the user field of Worker
                first_name=firstname,
                last_name=lastname,
                dob=dob,
                email=email,
                password=make_password(password),  # Store the hashed password
                phone=phoneno,
                username=username,
                district=district,
                state=state,
                role=role,
            )

            messages.success(request, 'Account successfully registered.')
            return redirect('signin')  # Redirect to signin page after successful registration

        except ValidationError as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'signup.html')

def service_providers_by_category(request, category):
    providers = ServiceProvider.objects.filter(service_type=category)
    context = {'providers': providers, 'category': category}
    return render(request, 'providerlist.html', context)

#update profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
@login_required
def update_profile(request):
    client = Client.objects.get(user=request.user)
    if request.method == 'POST':
        # Get data from the POST request
        username = request.POST.get('username')  # Assuming username is unique
        email = request.POST.get('email')  # Note: Email field is read-only in the form, no need to process it here
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')

        try:
            # Retrieve the Client object based on the username
            client = Client.objects.get(username=username)

            # Update Client model fields
            client.first_name = first_name
            client.last_name = last_name
            client.phone = phone
            client = client  # Get the related User object
            client.username = username
            client.email = email
            client.save()

            # Update User model fields (assuming User is your custom User model)
            user = client.user  # Get the related User object
            user.username = username
            user.email = email  # Update email field if needed
            user.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('update_profile')  # Replace 'login' with your desired redirect URL

        except Client.DoesNotExist:
            messages.error(request, 'Client not found')
            # Handle the error, redirect to an error page or show an error message as needed

    return render(request, 'update_profile.html',{'client': client})
def profile_view(request):
    client = Client.objects.get(user=request.user)  # Assuming you have a Client model related to the User model
    return render(request, 'profile_view.html', {'client': client})
from django.contrib.auth.hashers import make_password
def google_authenticate(request):
    # Handle the Google OAuth2 authentication process
    # ...

    # After successful authentication, create or get the user
    try:
        user_social = UserSocialAuth.objects.get(provider='google-oauth2', user=request.user)
        user = user_social.user
    except UserSocialAuth.DoesNotExist:
        user = request.user
        user.role = 'client'
        user.save()
    # Set the user's is_patient field to True

    # Redirect to the desired page (phome.html for Patient role)
    return redirect('userpage')  # Make sure you have a URL named 'phome