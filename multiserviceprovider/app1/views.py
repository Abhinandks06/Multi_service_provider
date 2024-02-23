from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Branch, BranchManager, BranchManagerAssignment, MyUser,Client,Worker,ClientBooking,Service, WorkerLeaveapplication,WorkerReport,ServiceTypes, WorkerStatus
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
                return redirect('userpage')
            elif myuser.role == "provider":
                return redirect('providerpage')
            elif myuser.role == "worker":
                return redirect('workerpage')
            elif myuser.role == "admin":
                return redirect('custom_admin_page')
            elif myuser.role == "branchmanager":
                # Redirect to the branch manager page
                return redirect('managerpage')
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
        pincode = request.POST.get('pincode')  # Add this line to get pincode
        role = "client"  # Get selected role from the dropdown
        
        # Check for empty fields
        if not firstname or not lastname or not username or not phoneno or not state or not dob or not district or not email or not password or not confirmpassword or not pincode or not role:
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
                    pincode=pincode,  # Add this line to save pincode
                    role=role,
                    user=user
                )

                messages.success(request, 'Account successfully registered.')
                return redirect('signin')  # Redirect to signin page after successful registration

        except ValidationError as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'signup.html')
@login_required
def user_logout(request):
    try:
        del request.session['username']
        request.session.flush()
    except KeyError:
        pass
    return redirect('signin')
@login_required
def userlogout(request,category,userid):
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
def manager_logout(request):
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
def userpage(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            if user.role == 'client':
                # Check if the user exists in the Client model
                try:
                    client = Client.objects.get(user=user)
                    user_id = user.userid  # Get the user ID

                    # Fetch the list of services
                    services = ServiceTypes.objects.all()

                    return render(request, 'userpage.html', {'user_id': user_id, 'services': services})
                except Client.DoesNotExist:
                    messages.warning(request, "User profile not found. Please update your profile.")
                    # Pass username and email to google_profile_update view
                    email = user.email
                    return redirect('google_profile_update', username=username, email=email, user=user)  
            else:
                messages.error(request, "You dont have permission to access this page.")
                return redirect('signin')
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('signin')  # Redirect to signin page if the user does not exist
    else:
        return render(request, 'userpage.html', {'user_id': user_id, 'services': services})
@login_required
def userpagehome(request,category,userid):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            if user.role == 'client':
                # Check if the user exists in the Client model
                try:
                    client = Client.objects.get(user=user)
                    user_id = user.userid  # Get the user ID

                    # Fetch the list of services
                    services = ServiceTypes.objects.all()

                    return render(request, 'userpage.html', {'user_id': user_id, 'services': services})
                except Client.DoesNotExist:
                    messages.warning(request, "User profile not found. Please update your profile.")
                    # Pass username and email to google_profile_update view
                    email = user.email
                    return redirect('google_profile_update', username=username, email=email, user=user)  
            else:
                messages.error(request, "You dont have permission to access this page.")
                return redirect('signin')
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('signin')  # Redirect to signin page if the user does not exist
    else:
        return render(request, 'userpage.html', {'user_id': user_id, 'services': services})
@login_required
def google_profile_update(request, username, email,user):
    if request.method == 'POST':
        # Get form data from the POST request
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username', '')
        phoneno = request.POST.get('mobile_no')
        state = request.POST.get('state')
        dob = request.POST.get('dob')
        district = request.POST.get('district')
        email = request.POST.get('email')
        role = "client"

        # Retrieve the user object from the database based on the username
        try:
            client = Client.objects.get(user__username=username, user__email=email)
        except MyUser.DoesNotExist:
            client = Client.objects.create(
                    first_name=firstname,
                    last_name=lastname,
                    username=username,
                    email=email,
                    dob=dob,
                    phone=phoneno,
                    district=district,
                    state=state,
                    role= role,
                    user=user
                )
            return redirect('userpage')
        return redirect('userpage')

    # Render the template for the Google profile update form
    return render(request, 'google_profile_update.html', {'username': username, 'email': email})
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def workerpage(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            if user.role == 'worker':
                # Retrieve the Worker object associated with the logged-in user
                worker = Worker.objects.get(user=user)
                return render(request, 'workerpage.html', {'worker': worker})
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
                context = {
                    'user': user,
                    'provider_id': user.userid  # Pass the provider's ID to the template context
                }
                return render(request, 'providerpage.html', context)
            else:
                messages.error(request, "You dont have permission to access this page.")
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
        return redirect('signin')
    
      # Redirect should be here if the user is not logged in or doesn't have permission
@login_required
def providerpagehome(request,provider_id):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            if user.role == 'provider':
                context = {
                    'user': user,
                    'provider_id': user.userid  # Pass the provider's ID to the template context
                }
                return render(request, 'providerpage.html', context)
            else:
                messages.error(request, "You dont have permission to access this page.")
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
        return redirect('signin')
@login_required
def managerpage(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            
            if user.role == 'branchmanager':
                # If the user is a branch manager, you can add specific logic or render a manager-specific template.
                context = {
                    'user': user,
                    'manager_id': user.userid  # Pass the manager's ID to the template context
                }
                return render(request, 'managerpage.html', context)
            else:
                messages.error(request, "You dont have permission to access this page.")
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
        return redirect('signin')
@login_required
def managerpagehome(request,user):
    if 'username' in request.session:
        username = request.session['username']
        try:
            user = MyUser.objects.get(username=username)
            
            if user.role == 'branchmanager':
                # If the user is a branch manager, you can add specific logic or render a manager-specific template.
                context = {
                    'user': user,
                    'manager_id': user.userid  # Pass the manager's ID to the template context
                }
                return render(request, 'managerpage.html', context)
            else:
                messages.error(request, "You dont have permission to access this page.")
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
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
                # Fetch user profiles with their associated service providers, clients, and workers
                user_profiles = MyUser.objects.select_related('serviceprovider', 'client', 'worker').all()
                
                # Fetch all service types
                services = ServiceTypes.objects.all()

                context = {'user_profiles': user_profiles, 'services': services}
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
from django.contrib.auth.decorators import login_required
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
from django.http import HttpResponseForbidden, JsonResponse
@login_required
def provider_registration(request):
    if request.user.role == 'admin':  # Assuming 'role' is the attribute in your User model indicating the user's role
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
        else:
            messages.error(request, "Login failed. Please check your credentials.")
        
        return render(request, 'provider_registration_form.html')
    else:
        return render(request, 'signin.html')
        
def provider_reg(request):
    # Fetch all ServiceType objects from the database
    request.session.flush() 
    service_types = ServiceTypes.objects.all()

    # Convert the queryset to a list of dictionaries
    service_types_list = [{'id': service.service_id, 'name': service.service_type} for service in service_types]

    # Pass the service types data to the template
    return render(request, "provider_registration.html", {'service_types': service_types_list})
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

    # Retrieve the list of providers, branches, and services
    providers_list = ServiceProvider.objects.all()
    branches_list = Branch.objects.all()
    service_types = ServiceTypes.objects.all()

    # Convert the queryset to a list of dictionaries
    service_types_list = [{'id': service.service_id, 'name': service.service_type} for service in service_types]

    # Pass the providers, branches, and services lists to the template context
    context = {'providers_list': providers_list, 'branches_list': branches_list, 'services_list': service_types_list}
    
    return render(request, "worker_registration.html", context)
@login_required
def providerlist(request):
    request.session.flush() 
    return render(request, "providerlist.html")
@login_required
def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect("signin")
@login_required
def book_service(request, userid):
    return render(request, 'book_service.html', {'userid': userid})


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
        service_type_names = request.POST.getlist('service_type')
        role = "provider"
        
        # Check for empty fields
        if not providername or not ownername or not username or not password or not state or not district or not contact_number or not email or not service_type_names:
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
                role=role,
                is_active=True  # Set user to active upon registration
            )
            
            # Create ServiceProvider instance associated with the created MyUser instance
            service_provider = ServiceProvider.objects.create(
                user=user,  # Assign the MyUser instance to the user field of ServiceProvider
                providername=providername,
                ownername=ownername,
                state=state,
                username=username,
                district=district,
                contact_number=contact_number,
            )
            for service_type_name in service_type_names:
                try:
                    service_type = ServiceTypes.objects.get(service_type=service_type_name)
                    service_type.number_of_providers += 1
                    service_type.save()
                    service_provider.service_type.add(service_type)
                except ServiceTypes.DoesNotExist:
                    messages.warning(request, f'Service type "{service_type_name}" does not exist.')

            messages.success(request, 'Registration request sent to admin for approval.')
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
        providername = request.POST.get('providername')  # Get providername from the form
        pincode = request.POST.get('pincode')  # Add this line to get pincode
        service_type_name = request.POST.get('service_type')  # Add this line to get service_type

        # Check for empty fields
        if not firstname or not lastname or not username or not phoneno or not state or not dob or not district or not email or not password or not confirmpassword or not role or not providername or not pincode or not service_type_name:
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        # Check password match
        if password != confirmpassword:
            messages.error(request, 'Password does not match the confirm password.')
            return render(request, 'signup.html')

        # Get provider based on providername
        try:
            provider = ServiceProvider.objects.get(providerid=providername)
            User = get_user_model()
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                is_active=False
            )

            # Create Worker instance associated with the created MyUser instance and provider
            worker = Worker.objects.create(
                user=user,
                provider=provider,
                first_name=firstname,
                last_name=lastname,
                dob=dob,
                email=email,
                phone=phoneno,
                pincode=pincode,
                district=district,
                state=state,
                role="worker",
                status="registered",
            )

            # Save the pincode and service_type in the Worker table
            service_type = ServiceTypes.objects.get(service_id=service_type_name)
            worker.service_types.add(service_type)

            # Assuming branch_ids is a list of branch ids obtained from the form
            branch_ids = request.POST.getlist('branch_id')
            branches = Branch.objects.filter(pk__in=branch_ids)
            worker.branchid.set(branches)

            worker.save()


            messages.success(request, 'Registration request sent to provider for approval.')
            return redirect('signin')  # Redirect to signin page after successful registration
        except ServiceProvider.DoesNotExist:
            messages.error(request, 'Invalid provider name.')
            return render(request, 'workerregister')

    return render(request, 'signin')
@login_required
def service_providers_by_category(request, category, userid):
    # Retrieve the user profile based on the userid
    client = Client.objects.get(user=userid)
    # Retrieve branches associated with the category ID and the client's district
    branches = Branch.objects.filter(service_type=category, district=client.district)

    context = {'providers': branches, 'category': category}
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
@login_required
def profile_view(request):
    client = Client.objects.get(user=request.user)  # Assuming you have a Client model related to the User model
    return render(request, 'profile_view.html', {'client': client})
from django.contrib.auth.hashers import make_password
def google_authenticate(request):
    try:
        user_social = UserSocialAuth.objects.get(provider='google-oauth2', user=request.user)
        user = user_social.user
    except UserSocialAuth.DoesNotExist:
        user = request.user
        user.role = 'client'
        user.save()

    return redirect('userpage')  
from django.shortcuts import get_object_or_404
from .models import ServiceProvider

@login_required
def admin_requests(request):
    provider_requests = ServiceProvider.objects.filter(user__is_active=False)
    return render(request, 'providerrequest.html', {'provider_requests': provider_requests})
@login_required
def activate_provider(request, user_id):
    # Retrieve the ServiceProvider instance associated with the request ID
    provider_request = get_object_or_404(ServiceProvider, user_id=user_id, user__is_active=False)

    # Set is_active to True and save the user
    provider_request.user.is_active = True
    provider_request.user.save()
    subject = 'Account approved'
    message = 'Your account has been approved .'
    from_email = 'abhinandks2024a@mca.ajce.in'  # Replace with your email
    recipient_list = [provider_request.user.email]
    html_message = render_to_string('activation_email.html', {'user': provider_request.user})
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    return redirect('admin_requests') 

    # Return a success response (you can customize the response as needed)

from django.shortcuts import render, get_object_or_404
from .models import ServiceProvider
@login_required
def render_booking_form(request, client_id, branchid):
    current_user = request.user
    client_name = None
    client_phone = None
    client_district = None

    if current_user.role == 'client':
        client_name = current_user.client.username
        client_phone = current_user.client.phone
        client_district = current_user.client.district

    # Process the branch ID from the URL parameters
    try:
        branch_id = int(branchid)
        # Fetch branch information from the database
        branch = get_object_or_404(Branch, branchid=branch_id)

        # Check if there are any incomplete bookings for this client with the same branch
        incomplete_bookings = ClientBooking.objects.filter(clientid=current_user.client, branchid=branch_id, status__in=['pending', 'ongoing'])

        if incomplete_bookings.exists():
            # If there are incomplete bookings, display a message and redirect to the user page
            messages.error(request, 'You already have an incomplete booking with this branch.')
            return redirect('userpage')  # Redirect to the user page or adjust the redirect as needed

        # Include branch information in the context dictionary
        context = {
            'client_id': client_id,
            'client_phone': client_phone,
            'branch_id': branch_id,
            'client_district': client_district,
            'branch_name': branch.providername,  # Adjust this according to your Branch model
            'service_type': branch.service_type,  # Adjust this according to your Branch model
            'name': client_name,
            'branchid':branchid
        }

        return render(request, 'book_service.html', context)

    except ValueError:
        # Handle the case where branch_id is not a valid integer
        # You can raise an error, redirect, or handle it as per your requirement
        messages.error(request, 'Invalid branch ID.')
        return redirect('userpage')
@login_required
def create_booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        service_date = request.POST.get('service_date')
        service_time = request.POST.get('service_time')
        branchid = request.POST.get('branchid')  # Get providerid from the form data
        client_id = request.POST.get('userid')
        client_phone = request.POST.get('clientphone')
        client_district = request.POST.get('clientdistrict')  # Get userid from the form data
        client_instance = Client.objects.get(user=client_id)
        branch=Branch.objects.get(branchid=branchid)
        # Check if the current user has any pending bookings
        existing_bookings = ClientBooking.objects.filter(clientid=client_id, status__in=['pending', 'approved'])
        
        if existing_bookings.exists():
            # If pending bookings exist, display a message and redirect to the user page
            messages.error(request, 'You already have a pending booking. Complete or cancel it to make a new one.')
            return redirect('userpage')  # Redirect to the user page or adjust the redirect as needed
        
        # No pending bookings exist, proceed to create a new booking
        new_booking = ClientBooking(
            name=name,
            phone=client_phone,
            district=client_district,
            date=service_date,
            time=service_time,
            branchid=branch,  # Save providerid in the ClientBooking object
            clientid=client_instance,
            status="pending"  # Save userid in the ClientBooking object
        )
        new_booking.save()
        client_email = new_booking.clientid.email  # Replace with the actual field name for client email
        provider_email = "abhinandks2024a@mca.ajce.in"  # Replace with the actual field name for provider's user email
        
        # Compose email messages for the client and provider
        client_subject = 'Booking Confirmation'
        client_message = f"Dear {name},\nYour appointment has been booked successfully."
        provider_subject = 'New Booking Received'
        provider_message = f"Dear {name},\nA new booking has been made."

        # Send email to the client
        send_mail(client_subject, client_message, 'sender@example.com', [client_email])

        # Send email to the provider
        send_mail(provider_subject, provider_message, 'sender@example.com', [provider_email])
        
        messages.success(request, 'Appointment booked successfully. Confirmation emails sent.')
        return redirect('userpage')
    else:
        # Handle GET request (if needed)
        # ...
        return render(request, 'signup')
from django.db.models import Q

@login_required
def search_providers(request):
    query = request.GET.get('query', '')  # Get the query parameter from the request, default to an empty string if not present
    
    client_id = request.session.get('client_id')  # Assuming client_id is stored in the session
    
    # Use Q objects to perform case-insensitive similar name search
    providers = ServiceProvider.objects.filter(Q(providername__iexact=query) | Q(providername__icontains=query))
    
    context = {
        'query': query,  # Pass the query back to the template to display in the search results
        'providers': providers,
        'client_id': client_id,  # Pass the client ID in the context
    }
    
    return render(request, 'search_results.html', context)


@login_required
def provider_bookings(request,user):
    user_id = user
    manager = BranchManager.objects.get(user=user_id)
    branch_id = BranchManagerAssignment.objects.get(manager=manager)
    bookings = ClientBooking.objects.filter(branchid=branch_id.branch).exclude(status='completed').exclude(status='canceled')

    context = {
        'bookings': bookings
    }

    return render(request, 'manager_bookings.html', context)
@login_required
def bookinghistory(request):
    # Get the logged-in provider's user ID
    userid = request.user.userid
    manager_id=BranchManager.objects.get(user=userid)
    branch=BranchManagerAssignment.objects.get(manager=manager_id)
    bookings = Service.objects.filter(branchid=branch.branch, status='Completed')
    context = {
        'bookings': bookings
    }

    return render(request, 'bookinghistory.html', context)
@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(ClientBooking, bookingid=booking_id)
    booking.status = 'approved'
    booking.save()
    service_id = booking.serviceid_id
    service = Service.objects.get(serviceid=service_id)
    service.status = 'approved'
    service.save()
    messages.success(request, 'Appointment accepted.')
    return redirect('provider_bookings')
@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(ClientBooking, bookingid=booking_id)
    booking.status = 'canceled'
    booking.save()
    service_id = booking.serviceid_id
    service = Service.objects.get(serviceid=service_id)
    service.status = 'canceled'
    service.save()
    messages.success(request, 'Appointment canceled.')

    # Send email notification to the client
    client_email = booking.clientid.email  # Replace 'email' with the actual field name
    subject = 'Work Rejection Notification'
    message = f"Dear {booking.name},\n\nWe regret to inform you that your booking with provider {{provider_name}} has been rejected.\n\nRegards,\nMultiserviceprovider"

    send_mail(subject, message, 'sender@example.com', [client_email], fail_silently=False)

    return redirect('provider_bookings')

@login_required
def worker_requests(request, user_id):
    try:
        # Get the branch manager
        manager = BranchManager.objects.get(user=user_id)

        # Get the branch manager assignment
        manager_assignment = BranchManagerAssignment.objects.get(manager=manager.managerid)

        # Get the branch ID
        branch_id = manager_assignment.branch.branchid

        # Filter workers based on the manager's ID and other criteria (provider, pincode)
        workers = Worker.objects.filter(
            provider=manager.providerid,
            status='registered'
        )

        return render(request, 'workerrequest.html', {'workers': workers, 'manager_id': manager.user.userid, 'branch_id': branch_id})
    except MyUser.DoesNotExist:
        messages.error(request, "Invalid request")
        return redirect('signin')  # Replace 'some_error_page' with an appropriate error page

@login_required
def approve_worker(request, user_id):
    # Retrieve the Worker instance associated with the request ID
    worker_request = get_object_or_404(Worker, user_id=user_id, user__is_active=False)
    
    # Set is_active to True and update the status to 'hired'
    worker_request.user.is_active = True
    worker_request.status = 'hired'
    
    # Save the changes
    worker_request.user.save()
    worker_request.save()

    return redirect('worker_requests')


@login_required
def activate_worker(request, user_id, manager_id, branch_id):
    user = get_object_or_404(MyUser, userid=user_id)
    
    if not user.is_active:
        user.is_active = True
        user.save()

        # Update the status and branch field of the associated Worker instance
        worker = get_object_or_404(Worker, user=user)
        worker.status = 'hired'  # Update to the desired status

        # Add the desired branch to the worker's branches
        worker.branchid.add(branch_id)

        worker.save()
        
        subject = 'Account activated'
        message = 'Your account has been activated by your provider'
        from_email = 'abhinandks2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'user': user})
        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
        
    return redirect('managerpage')
 
@login_required
def available_workers(request, branchid_id, district, booking_id):
    # Retrieve booking details for the specified booking ID
    booking = get_object_or_404(ClientBooking, bookingid=booking_id)

    # Filter workers based on branchid_id, district, status='available' or 'hired', and is_active=1
    workers = Worker.objects.filter(branchid=branchid_id, district=district, status__in=['available', 'hired'], is_active=1)

    context = {
        'booking': booking,
        'workers': workers,
    }

    return render(request, 'available_workers.html', context)
@login_required
def assign_worker(request):
    if request.method == 'POST':
        worker_id = request.POST.get('worker_id')
        booking_id = request.POST.get('booking_id')
        
        # Retrieve worker, booking, and client instances based on IDs
        worker = Worker.objects.get(user_id=worker_id)
        booking = ClientBooking.objects.get(bookingid=booking_id)
        client = booking.clientid
        
        # Create a new Service instance and save it to the database
        service = Service.objects.create(
            bookingid=booking,
            clientid=client,
            district=booking.district,
            branchid=booking.branchid,
            date=booking.date,
            time=booking.time,
            status=Service.ASSIGNED  # You can set the initial status to 'assigned'
        )

        # Add the worker to the ManyToManyField
        service.workerid.add(worker)
        
        # Create a new WorkerStatus instance and save it to the database
        worker_status = WorkerStatus.objects.create(
            branchid=booking.branchid,
            workerid=worker,
            workstatus=WorkerStatus.PENDING  # You can set the initial status to 'pending'
        )
        
        # Update the booking status to 'assigned'
        booking.status = ClientBooking.APPROVED
        booking.save()
        
        # Update the worker status to 'onduty'
        worker.status = 'onduty'
        worker.save()
        
        # Redirect to a success page or back to the previous page
        messages.success(request, 'Service assigned successfully!')
        return redirect('managerpage')  # Replace 'success_page' with the appropriate URL name

    # Handle other cases, e.g., GET requests
    return redirect('managerpage') # Replace 'error_page' with the appropriate URL name
@login_required
def worker_job(request):
    worker_id = request.user.userid  # Assuming the worker's ID is stored in the user object
    assigned_work = Service.objects.filter(workerid=worker_id, status=Service.ASSIGNED)
    return render(request, 'worker_job.html', {'assigned_work': assigned_work, 'worker_id': worker_id})
@login_required
def assignedwork(request):
    worker_id = request.user.userid
    assigned_work = Service.objects.filter(
        workerid=worker_id
    ).exclude(
        status__iexact='COMPLETED'
    ).exclude(
        status__iexact='CANCELED'
    )
    return render(request, 'update_status.html', {'assigned_work': assigned_work})

@login_required
def update_status(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        new_status = request.POST.get('status')

        # Fetch the service
        service = get_object_or_404(Service, serviceid=service_id)

        # Fetch the associated booking and its payment
        client_booking = get_object_or_404(ClientBooking, bookingid=service.bookingid_id)

        # Fetch the worker associated with the service
        worker = service.workerid
        # Check if payment status is completed before updating
        if service.paymentstatus == 'completed':
            # Update the status of the service
            service.status = new_status
            service.save()

            # Get all workers related to this service
            related_workers = Worker.objects.filter(service=service)

            # Update the status of related workers
            related_workers.update(status='available')  # Set status as needed

            # Update the status of the client booking
            client_booking.status = 'completed'
            client_booking.save()

            # Fetch the branch associated with the service
            branch = service.branchid
            # Fetch the manager assigned to the branch
            manager_assignment = BranchManagerAssignment.objects.get(branch=branch)
            manager_email = manager_assignment.manager.user.email

            # Sending emails to client, provider, and manager
            client_email = client_booking.clientid.user.email

            client_message = f"Hi {client_booking.name}, The work for your booking has been marked as completed."
            manager_message = f"Dear Manager, The work for the booking has been marked as completed."

            send_mail('Work Completion Notification - Client', client_message, 'your@email.com', [client_email])
            send_mail('Work Completion Notification - Manager', manager_message, 'your@email.com', [manager_email])

            messages.success(request, 'Service status updated! Emails sent to the client, provider, and manager.')
        else:
            messages.error(request, 'Payment pending. Cannot update service status.')

        return redirect('workerpage')
    return redirect('workerpage')
@login_required
def render_report_form(request, bookingid_id):
    worker_id = request.POST.get('worker_id')  # Get the worker_id from the POST data
    
    service = get_object_or_404(Service, bookingid_id=bookingid_id)
    return render(request, 'generate_report.html', {'service': service, 'worker_id': worker_id})


from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.files.base import ContentFile
from django.http import HttpResponse
from .models import Service, Worker, ServiceProvider, WorkerReport
@login_required
def generate_report(request):
    if request.method == 'POST':
        serviceid = request.POST.get('serviceid')
        branchid = request.POST.get('branchid')
        user_id = request.POST.get('workerid')
        duration_of_work = request.POST.get('duration_of_work')
        requirements = request.POST.get('requirements')
        cost = request.POST.get('cost')
        num_workers_needed = request.POST.get('num_workers_needed')
        
        # Fetch necessary objects from the database
        service = get_object_or_404(Service, serviceid=serviceid)
        worker = get_object_or_404(Worker, user_id=user_id)
        branch = get_object_or_404(Branch, branchid=branchid)
        
        # Create a WorkerReport instance to store the inputs
        report = WorkerReport.objects.create(
            serviceid=service,
            user_id=worker,
            branchid=branch,
            duration_of_work=duration_of_work,
            requirements=requirements,
            cost=cost,
            num_workers_needed=num_workers_needed,
            status="reportgiven"
        )
        
        # Update Service status
        service.status = Service.REPORTGIVEN
        service.save()

        # Fetch additional data from related models
        provider_name = branch.providername  # Replace 'provider_name' with the actual field name
        worker_name = f"{worker.first_name} {worker.last_name}"
        service_type = branch.service_type  # Replace 'service_type' with the actual field name
        
        # Fetch data to render in the PDF template
        context = {
            'duration_of_work': duration_of_work,
            'requirements': requirements,
            'workers': num_workers_needed,
            'cost': cost,
            'provider_name': provider_name,
            'worker_name': worker_name,
            'service_type': service_type,
            # Add other data as needed
        }
        
        # Render the HTML template
        template = get_template('report_template.html')
        html = template.render(context)
        
        # Generate PDF using xhtml2pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="worker_report.pdf"'

        # Generate the PDF file
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('Failed to generate PDF!')
         # Save the PDF content to WorkerReport model
        report.report_pdf.save(f'worker_report_{report.reportid}.pdf', ContentFile(response.content), save=True)
        messages.success(request, 'Work report given!')
        return redirect (workerpage)

    return render(request, 'generate_report.html', {})


def worker_list(request, userid):
    try:
        managerid=BranchManager.objects.get(user=userid)
        manager = BranchManagerAssignment.objects.get(manager=managerid)
        branch_id = manager.branch
        workers = Worker.objects.filter(branchid=branch_id)

        return render(request, 'worker_list.html', {'workers': workers})
    except BranchManagerAssignment.DoesNotExist:
        # Handle the case where there's no manager assignment for the user
        messages.error(request, "You are not assigned as a branch manager.")
        return redirect('home')
@login_required
def worker_report(request, managerid):
    # Get the BranchManager instance based on the provided managerid
    manager = get_object_or_404(BranchManager, user=managerid)

    # Get the BranchManagerAssignment instance for the manager
    assignment = get_object_or_404(BranchManagerAssignment, manager=manager.managerid)

    # Retrieve worker_reports based on the manager's branchid
    worker_reports = WorkerReport.objects.filter(branchid=assignment.branch, status='reportgiven')

    # Create a dictionary to store service status for each report
    service_status = {}

    # Retrieve service status for each report
    for report in worker_reports:
        service_id = report.serviceid_id  # Use _id to get the integer value
        service = Service.objects.get(serviceid=service_id)
        service_status[report.serviceid] = service.status

    context = {
        'worker_reports': worker_reports,
        'service_status': service_status,
        'assignment': assignment.branch.branchid,
        'workerreport':worker_reports
    }
    return render(request, 'worker_report.html', context)


# from django.db.models import Prefetch
# @login_required
# def worker_report(request, provider_id):
#     worker_reports = WorkerReport.objects.filter(providerid_id=provider_id,status="reportgiven")
    
#     # Prefetch the related Service objects and extract only the 'status' field
#     service_status = Service.objects.filter(providerid_id=provider_id).values_list('status', flat=True)
    
#     # Combine the queries into a single call
#     worker_reports = worker_reports.prefetch_related(
#         Prefetch('serviceid', queryset=Service.objects.filter(providerid_id=provider_id))
#     )
    
#     context = {
#         'worker_reports': worker_reports,
#         'service_status': service_status,
#     }
#     return render(request, 'worker_report.html', context)



from django.shortcuts import render
from .models import Service, Client, ServiceProvider
@login_required
def client_bookings(request, client_id):
    client_bookings = Service.objects.filter(clientid_id=client_id)
    client_name = Client.objects.get(user_id=client_id).first_name
    
    provider_info = []
    
    for booking in client_bookings:
        branch_id = booking.branchid_id
        branch = Branch.objects.get(pk=branch_id)
        provider_name = branch.providername
        service_type = branch.service_type.service_type
        
        
    
    context = {
        'client_bookings': client_bookings,
        'client_name': client_name,
        'provider_name': provider_name,
        'service_type': service_type,
        'worker_report': worker_report,
    }
    return render(request, 'client_bookings.html', context)



@login_required
def assign_workers(request, reportid):
    worker_report = WorkerReport.objects.get(reportid=reportid)
    service_id = worker_report.serviceid_id
    service = Service.objects.get(serviceid=service_id)
    
    # Fetch available workers based on the service's district
    workers = Worker.objects.filter(district=service.district, status='available')
    
    context = {
        'worker_report': worker_report,
        'service': service,
        'available_workers': workers,
    }
    return render(request, 'assign_workers.html', context)
@login_required
def assign_workers_service(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        service_id = request.POST.get('service_id')
        selected_worker_ids = request.POST.getlist('selected_workers')
        
        # Retrieve the worker report and service objects
        worker_report = WorkerReport.objects.get(reportid=report_id)
        service = Service.objects.get(serviceid=service_id)

        # Retrieve selected workers based on their IDs
        selected_workers = Worker.objects.filter(user_id__in=selected_worker_ids)

        # Assign selected workers to the service model
        service.workerid.add(*selected_workers)

        # Update status of selected workers to "on duty"
        Worker.objects.filter(user_id__in=selected_worker_ids).update(status='onduty')

        # Update status of worker report to "reportverified"
        worker_report.status = 'reportverified'
        worker_report.save()

        return redirect('providerpage')
  # Redirect to a success page or any other view upon successful assignment

    # Render the page initially or handle GET requests
    return redirect('providerpage')
    

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import WorkerReport
@login_required
def download_worker_report(request, report_id):
    # Fetch the worker report for the specific report ID
    worker_report = get_object_or_404(WorkerReport, reportid=report_id)
    
    # Assuming 'pdf_field' is the field in the WorkerReport model that stores the PDF
    pdf_content = worker_report.report_pdf.read()
    
    # Set up the response to serve the PDF file
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="worker_report_{report_id}.pdf"'
    
    return response
from decimal import Decimal
import razorpay
@login_required
def client_work_reports(request, client_id):
    # Get the client
    client = get_object_or_404(Client, user_id=client_id)

    # Get the services related to the client
    services = Service.objects.filter(clientid_id=client.user_id)

    # Extract the service IDs
    service_ids = [service.serviceid for service in services]

    # Get worker reports associated with those service IDs
    client_reports = WorkerReport.objects.filter(serviceid__in=service_ids)

    # Multiply 'cost' attribute of each report by 100
    for report in client_reports:
        report.cost *= Decimal('100')  # Perform the multiplication

    if request.method == 'POST':
        DATA = {
            "amount": 100,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        }
        client = razorpay.Client(auth=("rzp_test_bWe8tmmP1WXOe7", "qR7WzF8AfC6RxJdGluOKWyUa"))
        payment = client.order.create(data=DATA)

    return render(request, 'client_work_reports.html', {'client_reports': client_reports})
@login_required
def approve_report(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        # Perform logic to approve the report (update database, etc.)
        # Example:
        report = WorkerReport.objects.get(reportid=report_id)
        report.status = 'completed'
        report.save()

        # Update Service status to reportverified
        service_id = request.POST.get('service_id')
        service = Service.objects.get(serviceid=service_id)
        service.status = 'reportverified'
        service.save()

        messages.success(request, 'Report approved successfully!')
    return redirect('userpage')
@login_required
def cancel_service(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        report = WorkerReport.objects.get(reportid=report_id)
        report.status = 'canceled'
        report.save()

        # Update Service status to cancelled
        service_id = request.POST.get('service_id') 
        service = Service.objects.get(serviceid=service_id)
        service.status = 'canceled'
        service.save()
        workers = service.workerid.all()
        for worker in workers:
            worker.status = 'available'
            worker.save()
        worker.save()
        # Update booking status to canceled
        booking_id = service.bookingid_id
        booking = ClientBooking.objects.get(bookingid=booking_id)
        booking.status = 'canceled'
        booking.save()

        # Retrieve provider's email
        provider_email = service.providerid.user.email

        # Send an email to the provider
        client_name = booking.name
        subject = 'Booking Cancellation Notification'
        message = f'Dear Provider, The booking made by {client_name} has been canceled.'
        from_email = 'your@email.com'  # Replace with your email
        recipient_list = [provider_email]
        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Service cancelled successfully! An email has been sent to the provider.')
    return redirect('userpage')


from django.http import HttpResponseRedirect
from django.urls import reverse
@login_required
def update_service_and_booking(request, booking_id):
    try:
        # Retrieve booking details for the specified booking ID
        booking = ClientBooking.objects.get(bookingid=booking_id)

        # Update booking status to 'canceled'
        booking.status = 'canceled'
        booking.save()

        service = Service.objects.get(bookingid_id=booking.bookingid)

        # Update service status to 'canceled'
        service.status = 'canceled'
        service.save()

        # Redirect to 'providerpage' view
        return redirect('managerpage')

    except (ClientBooking.DoesNotExist, Service.DoesNotExist) as e:
        messages.error(request, 'Cancelled booking.')

        return redirect('managerpage')

@login_required
def update_rating(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        rating = request.POST.get('rating')

        # Update the Service model with the received rating
        service = Service.objects.get(serviceid=service_id)
        service.rating = rating
        service.save()

        # Redirect to the client bookings page or any other page
        return redirect('client_bookings', client_id=service.clientid_id)

    # Handle other cases, e.g., GET requests
    return redirect('userpage')
@login_required
def update_review(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        review = request.POST.get('review')

        # Update the Service model with the received review
        service = Service.objects.get(serviceid=service_id)
        service.review = review
        service.save()

        # Redirect to the client bookings page or any other page
        return redirect('client_bookings', client_id=service.clientid_id)

    # Handle other cases, e.g., GET requests
    return redirect('userpage')
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
@csrf_exempt
@login_required
def payment_success(request):
    service_id = request.POST.get('service_id')  # Ensure to pass the service_id via POST
    service = Service.objects.get(pk=service_id)
    service.paymentstatus = 'completed'
    service.save()

    # Get branch_id from the service
    branch_id = service.branchid

    # Get manager_id from BranchManagerAssignment using branch_id
    try:
        branch_manager_assignment = BranchManagerAssignment.objects.get(branch=branch_id)
        manager_id = branch_manager_assignment.manager.managerid

        # Get the manager object
        manager =BranchManager.objects.get(pk=manager_id)

        # Set provider_email as the manager's email
        provider_email = manager.email

        # Get other necessary details for the email
        client_name = service.clientid.user.username
        payment_date = timezone.now().date()

        # Send an email to the provider
        subject = 'Payment Successful Notification'
        message = f'Dear Provider, {client_name} has made the payment on {payment_date}.'
        from_email = 'your@email.com'  # Replace with your email
        recipient_list = [provider_email]
        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, 'Payment successful! Confirmation email has been sent to the provider.')
        return redirect('userpage')

    except BranchManagerAssignment.DoesNotExist:
        # Handle the case where there is no manager assigned to the branch
        messages.error(request, 'Error: No manager assigned to the branch.')
        return redirect('userpage')  # You may want to redirect to an error page or handle this differently

    except BranchManager.DoesNotExist:
        # Handle the case where the manager object is not found
        messages.error(request, 'Error: Manager not found.')
        return redirect('userpage')
def add_service(request):
    if request.method == 'POST':
        # Extract data from the form
        service_type = request.POST.get('serviceType')
        description = request.POST.get('description')

        # Perform any additional processing or validation here

        # Save the data to your ServiceTypes model
        new_service = ServiceTypes.objects.create(
            service_type=service_type,
            description=description,
            # Set other fields as needed
        )

        # Redirect to a success page or any other desired page
        return redirect('custom_admin_page')

    # Render the service form page for GET requests
    return render(request, 'custom_admin_page')

@login_required
def add_branch(request):
    # Check if the user is a provider
    if request.user.role != 'provider':
        return redirect('providerpage')  # Redirect to home or another appropriate page

    provider = ServiceProvider.objects.get(user=request.user)

    if request.method == 'POST':
        service_type_id = request.POST.get('service_type')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')

        if not service_type_id or not district or not pincode:
            messages.error(request, 'All fields for Branch are required.')
            return render(request, 'add_branch.html', {'provider': provider})

        # Convert service_type_id to an instance of ServiceTypes
        service_type = ServiceTypes.objects.get(service_id=service_type_id)

        # Create a new branch
        branch = Branch.objects.create(
            providerid=provider,
            providername=provider.providername,
            service_type=service_type,
            district=district,
            pincode=pincode
        )

        messages.success(request, 'Branch added successfully.')
        return redirect('providerpage')  # Redirect to the branches page

    return render(request, 'add_branch.html', {'provider': provider})
def add_branch_page(request, provider_id):
    # Fetch provider details based on the provider_id
    try:
        service_types = ServiceTypes.objects.all()

    # Convert the queryset to a list of dictionaries
        service_types_list = [{'id': service.service_id, 'name': service.service_type} for service in service_types]
        provider = ServiceProvider.objects.get(providerid=provider_id)
    except ServiceProvider.DoesNotExist:
        # Handle the case where the provider is not found
        return render(request, 'signin')

    return render(request, 'branchregistration.html', {'provider': provider, 'service_types': service_types_list})
def branch_page(request, provider_id):
    # Assuming provider_id is the user ID
    user_id = provider_id  # Rename the variable for clarity

    # Get the ServiceProvider instance based on the user ID
    provider = get_object_or_404(ServiceProvider, user=user_id)

    # Get branches of the provider with status "inactive"
    inactive_branches = Branch.objects.filter(providerid=provider, status='inactive')

    # Pass the provider and inactive branches to the template
    return render(request, 'branch.html', {'provider': provider, 'inactive_branches': inactive_branches})
from datetime import date as dt_date
import secrets
@login_required
def manager_registration(request, provider_id, branch_id):
    provider = get_object_or_404(ServiceProvider, providerid=provider_id)
    branch = get_object_or_404(Branch, branchid=branch_id, providerid=provider)
    
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        state = request.POST.get('state')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        
        # Generate a random password
        password = secrets.token_urlsafe(8)  # Adjust the password length as needed

        # Create MyUser instance with role 'branchmanager'
        user = MyUser.objects.create_user(username=user_name, email=email, password=password)
        user.role = 'branchmanager'
        user.save()

        # Authenticate and login the user
        authenticated_user = authenticate(request, username=user_name, password=password)
        login(request, authenticated_user)

        # Set the date_of_joining to the current date
        current_date = dt_date.today()

        # Create BranchManager instance
        branch_manager = BranchManager.objects.create(
            user=authenticated_user,
            providerid=provider,
            providername=provider.providername,
            date_of_joining=current_date,
            phone_no=phone_no,
            state=state,
            district=district,
            pincode=pincode,
            email=email
        )

        BranchManagerAssignment.objects.create(branch=branch, manager=branch_manager)
        branch.status = 'active'
        branch.save()

        # Send email with username and password
        subject = 'Manager Registration'
        message = f'Your username: {user_name}\nYour password: {password}\n\nPlease keep this information secure.'
        from_email = 'abhinandks2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [email]

        # Send the email
        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Manager registered successfully. Login credentials sent to the registered email.')
        return render(request, 'branch.html', {'provider_id': provider_id, 'branch_id': branch_id, 'provider': provider})

    return render(request, 'branchmanagereg.html', {'provider_id': provider_id, 'branch_id': branch_id, 'provider': provider})

from django.shortcuts import get_object_or_404

@login_required
def apply_leave(request):
    if request.method == 'POST':
        leavetype = request.POST.get('leavetype')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Validate the input if necessary

        # Extract user ID from SimpleLazyObject
        user_id = request.user.userid
        userid = get_object_or_404(MyUser, userid=user_id)

        try:
            # Retrieve the first related branch
            branch = Worker.objects.get(user=userid)

            # Check if there's an existing pending leave request
            existing_leave_request = WorkerLeaveapplication.objects.filter(
                user_id=userid.userid,
                status='pending'
            )

            if existing_leave_request.exists():
                # If there's an existing pending leave request, show a message
                messages.warning(request, 'You already have a pending leave request. Please wait for approval.')
                return redirect('workerpage')

            # Save the leave application
            leave_application = WorkerLeaveapplication(
                user_id=userid.userid,
                leavetype=leavetype,
                start_date=start_date,
                end_date=end_date,
                status='pending'
            )
            leave_application.save()

            return redirect('leave_success')  # Redirect to a success page or your desired page

        except Worker.DoesNotExist:
            # Handle the case where the worker does not exist
            pass

    return render(request, 'apply_leave.html')

# You can add this view if you want to display a success message after applying for leave
def leave_success(request):
    # Add a success message
    messages.success(request, 'Leave has been applied successfully.')

    return redirect('workerpage')
@login_required
def leave_requests(request, provider_id):
    try:
        # Get the branch associated with the provider
        branch_manager = BranchManager.objects.get(user=provider_id)
        
        # Get the branch associated with the manager
        branch_manager_assignment = BranchManagerAssignment.objects.get(manager=branch_manager)
        branch = branch_manager_assignment.branch

        # Get workers in the branch
        workers_in_branch = Worker.objects.filter(branchid=branch)

        # Get leave requests for workers in the branch with status 'requested'
        leave_requests = WorkerLeaveapplication.objects.filter(user__in=workers_in_branch.values('user'), status='pending')

        context = {
            'leave_requests': leave_requests,
            'provider_id': provider_id,
        }

        return render(request, 'leave_requests.html', context)
    except (BranchManager.DoesNotExist, BranchManagerAssignment.DoesNotExist):
        # Handle exceptions as needed
        return render(request, 'managerpage')

    except BranchManagerAssignment.DoesNotExist:
        # Handle the case where the branch manager assignment does not exist
        return redirect('managerpage')

    except Branch.DoesNotExist:
        # Handle the case where the branch does not exist
        return redirect('managerpage')
    
from django.contrib import messages
from django.utils import timezone
@login_required
def approve_leave(request, leave_id):
    leave_request = get_object_or_404(WorkerLeaveapplication, leaveid=leave_id)

    if leave_request.status == 'pending':
        # Approve the leave
        leave_request.status = 'approved'
        leave_request.save()

        # Get the userid and ending date from the leave_request object
        user_id = leave_request.user.userid
        ending_date = leave_request.end_date

        # Update the Worker object's status as 'on leave'
        worker = get_object_or_404(Worker, user=user_id)
        worker.status = 'onleave'
        worker.save()

        messages.success(request, 'Leave has been approved successfully.')

        # Schedule a task to update the worker's status to 'available' after the ending date

    return redirect('managerpage')



def cancel_leave(request, leave_id):
    leave_request = get_object_or_404(WorkerLeaveapplication, leaveid=leave_id)

    if leave_request.status == 'pending':
        # Cancel the leave
        leave_request.status = 'canceled'
        leave_request.save()
    messages.success(request, 'Leave has been rejected')
    return redirect('managerpage')
@login_required
def update_service_status(request, report_id):
    worker_report = get_object_or_404(WorkerReport, reportid=report_id)
    if worker_report.num_workers_needed == 1:
        service = get_object_or_404(Service, serviceid=worker_report.serviceid)
        service.status = 'reportverified'  # Replace 'YOUR_NEW_STATUS' with the desired status
        service.save()
        messages.success(request, 'Service status updated successfully.')
        return redirect('managerpage')  

    else:

        return render(request, 'managerpage')  
@login_required
def branch_list(request, provider_id):
    # Get the logged-in user's ServiceProvider instance
    provider = get_object_or_404(ServiceProvider, user=request.user)

    # Filter branches based on the provider_id
    provider_branches = Branch.objects.filter(providerid=provider)

    # Fetch corresponding branch manager assignments
    branch_manager_assignments = BranchManagerAssignment.objects.filter(branch__in=provider_branches)

    # Create a dictionary to map branchid to branch manager assignment
    branch_manager_assignment_dict = {assignment.branch_id: assignment for assignment in branch_manager_assignments}

    # Attach branch manager assignment to each branch
    for branch in provider_branches:
        branch.branch_manager_assignment = branch_manager_assignment_dict.get(branch.branchid)

    context = {'branches': provider_branches}
    return render(request, 'branch_list.html', context)