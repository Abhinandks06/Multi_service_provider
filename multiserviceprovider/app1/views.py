from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .models import MyUser,Client,Worker,ClientBooking,Service,WorkerReport
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
                    return render(request, 'userpage.html', {'user_id': user_id})
                except Client.DoesNotExist:
                    messages.warning(request, "User profile not found. Please update your profile.")
                    # Pass username and email to google_profile_update view
                    email = user.email
                    return redirect('google_profile_update', username=username, email=email,user=user)  
            else:
                messages.error(request, "You don't have permission to access this page.")
                return redirect('signin')
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('signin')  # Redirect to signin page if user does not exist
    else:
        return render(request, 'userpage.html')  
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
                messages.error(request, "You don't have permission to access this page.")
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
                messages.error(request, "You don't have permission to access this page.")
        except MyUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
        return redirect('signin')  # Redirect should be here if the user is not logged in or doesn't have permission
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
                user_profiles=MyUser.objects.select_related('serviceprovider', 'client','worker').all()
                
                
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
from django.http import HttpResponseForbidden
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
@login_required
def book_service(request):
    return render(request, "book_service.html")


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
                role=role,
                is_active=False
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
                role=role,
                

            )

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
        # Check for empty fields
        if not firstname or not lastname or not username or not phoneno or not state or not dob or not district or not email or not password or not confirmpassword or not role or not providername: 
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        # Check password match
        if password != confirmpassword:
            messages.error(request, 'Password does not match the confirm password.')
            return render(request, 'signup.html')
            # Get provider based on providername
        try:
            provider = ServiceProvider.objects.get(providername=providername)
            User = get_user_model()
            user = User.objects.create_user(
            username=username,
            email=email,
            password=password,  # Store the password (it will be hashed internally)
            role=role,
            is_active=False
            )

            # Create Worker instance associated with the created MyUser instance and provider
            worker = Worker.objects.create(
            user=user,
            first_name=firstname,
            last_name=lastname,
            dob=dob,
            email=email,
            phone=phoneno,
            district=district,
            state=state,
            role="worker",
            status="available",
            provider=provider.user_id   # Assign the provider to the worker
            )
            messages.success(request, 'Registration request sent to provider for approval.')
            return redirect('signin')  # Redirect to signin page after successful registration
        except ServiceProvider.DoesNotExist:
            messages.error(request, 'Invalid provider name.')
            return render(request, 'signup.html')

            # Create MyUser instance
        
    return render(request, 'signup.html')

@login_required
def service_providers_by_category(request, category):
    providers = ServiceProvider.objects.filter(user__is_active=True, service_type=category)
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
def render_booking_form(request, userid=None):
    # Get the current logged-in user
    current_user = request.user

    # Fetch client ID based on user role
    client_id = None
    client_name= None
    client_phone = None
    client_district = None
    if current_user.role == 'client':
        client_id = current_user.userid
        client_phone = current_user.client.phone
        client_district = current_user.client.district
        client_name = current_user.client.username

    # Process the provider ID from the URL parameters
    if userid is not None:
        try:
            provider_id = int(userid)
            # Fetch provider information from the database
            provider = get_object_or_404(ServiceProvider, user_id=provider_id)

            # Include providername and servicetype in the context dictionary
            context = {
                'client_id': client_id,
                'client_phone': client_phone,
                'provider_id': provider_id,
                'client_district': client_district,
                'providername': provider.providername,
                'servicetype': provider.service_type,
                'name':client_name
            }

            return render(request, 'book_service.html', context)

        except ValueError:
            # Handle the case where provider_id is not a valid integer
            # You can raise an error, redirect, or handle it as per your requirement
            pass

    return render(request, 'book_service.html', {'client_id': client_id, 'client_phone': client_phone,'name': client_name, 'provider_id': provider_id, 'client_district': client_district})

@login_required
def create_booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        service_date = request.POST.get('service_date')
        service_time = request.POST.get('service_time')
        provider_id = request.POST.get('providerid')  # Get providerid from the form data
        client_id = request.POST.get('userid')
        client_phone = request.POST.get('clientphone')
        client_district = request.POST.get('clientdistrict')  # Get userid from the form data
        new_booking = ClientBooking(
            name=name,
            phone=client_phone,
            district=client_district,
            date=service_date,
            time=service_time,
            providerid_id=provider_id,  # Save providerid in the ClientBooking object
            clientid_id=client_id,
            status="pending" # Save userid in the ClientBooking object
        )
        new_booking.save()
        messages.success(request, 'Appointment booked successfully.')
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
def provider_bookings(request):
    provider_id = request.user.userid
    bookings = ClientBooking.objects.filter(providerid=provider_id).exclude(status='completed')

    context = {
        'bookings': bookings
    }

    return render(request, 'provider_bookings.html', context)
@login_required
def bookinghistory(request):
    # Get the logged-in provider's user ID
    provider_id = request.user.userid

    # Filter bookings based on the provider's providerid and status is 'pending'
    bookings = Service.objects.filter(providerid_id=provider_id, status='Completed')
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
    return redirect('provider_bookings')
@login_required
def worker_requests(request, user_id):
    # Filter workers based on the user_id
    workers = Worker.objects.filter(user__is_active=False, provider=user_id,)
    return render(request, 'workerrequest.html', {'workers': workers})
@login_required
def approve_worker(request, user_id):
    # Retrieve the ServiceProvider instance associated with the request ID
    worker_request = get_object_or_404(Worker, user_id=user_id, user__is_active=False)
    # Set is_active to True and save the user
    worker_request.user.is_active = True
    worker_request.user.save()

    return redirect('worker_requests') 

@login_required
def activate_worker(request, userid):
    user = get_object_or_404(MyUser, userid=userid)
    if not user.is_active:
        user.is_active = True
        user.save()
        subject = 'Account activated'
        message = 'Your account has been activated by ur provider'
        from_email = 'abhinandks2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'user': user})
        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
        return redirect('providerpage')
 
@login_required       
def available_workers(request, providerid_id, district, booking_id):
    # Retrieve booking details for the specified booking ID
    booking = get_object_or_404(ClientBooking, bookingid=booking_id)

    # Filter workers based on providerid_id, district, status='available', and is_active=1
    workers = Worker.objects.filter(provider=providerid_id, district=district, status='available', user__is_active=1)

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
            providerid=booking.providerid,
            date=booking.date,
            time=booking.time,
            status=Service.ASSIGNED  # You can set the initial status to 'assigned'
        )
        service.workerid.set([worker])
        # Update the booking status to 'assigned'
        booking.status = ClientBooking.APPROVED
        booking.save()
        
        # Update the worker status to 'onduty'
        worker.status = 'onduty'
        worker.save()
        
        # Redirect to a success page or back to the previous page
        messages.success(request, 'Service assigned successfully!')
        return redirect('providerpage')  # Replace 'success_page' with the appropriate URL name

    # Handle other cases, e.g., GET requests
    return redirect('providerpage') # Replace 'error_page' with the appropriate URL name
@login_required
def worker_job(request):
    worker_id = request.user.userid  # Assuming the worker's ID is stored in the user object
    assigned_work = Service.objects.filter(workerid=worker_id, status=Service.ASSIGNED)
    return render(request, 'worker_job.html', {'assigned_work': assigned_work, 'worker_id': worker_id})
@login_required
def assignedwork(request):
    worker_id = request.user.userid
    assigned_work = Service.objects.filter(workerid=worker_id).exclude(status__iexact='COMPLETED')
    return render(request, 'update_status.html', {'assigned_work': assigned_work})
@login_required
def update_status(request):
    worker_id = request.user.userid
    
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        new_status = request.POST.get('status')

        # Update the status of the service
        service = get_object_or_404(Service, serviceid=service_id)
        service.status = new_status
        service.save()

        # Get all workers related to this service
        related_workers = Worker.objects.filter(service=service)
        clientbooking=ClientBooking.objects.filter(bookingid=service.bookingid_id)
        clientbooking.update(status='completed')
        # Update the status of related workers
        related_workers.update(status='available')  # Set status as needed

        messages.success(request, 'Service status updated!')
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
        providerid = request.POST.get('providerid')
        user_id = request.POST.get('workerid')
        duration_of_work = request.POST.get('duration_of_work')
        requirements = request.POST.get('requirements')
        cost = request.POST.get('cost')
        num_workers_needed = request.POST.get('num_workers_needed')
        
        # Fetch necessary objects from the database
        service = get_object_or_404(Service, serviceid=serviceid)
        worker = get_object_or_404(Worker, user_id=user_id)
        provider = get_object_or_404(ServiceProvider, user_id=providerid)
        
        # Create a WorkerReport instance to store the inputs
        report = WorkerReport.objects.create(
            serviceid=service,
            user_id=worker,
            providerid=provider,
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
        provider_name = provider.providername  # Replace 'provider_name' with the actual field name
        worker_name = f"{worker.first_name} {worker.last_name}"
        service_type = provider.service_type  # Replace 'service_type' with the actual field name
        
        # Fetch data to render in the PDF template
        context = {
            'serviceid': serviceid,
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
        return redirect (workerpage)

    return render(request, 'generate_report.html', {})


@login_required
def worker_list(request, provider_id):
    # Fetch workers belonging to the specific provider using the provider_id
    workers = Worker.objects.filter(provider=provider_id)

    return render(request, 'worker_list.html', {'workers': workers})
@login_required
def worker_report(request, provider_id):
    worker_reports = WorkerReport.objects.filter(providerid_id=provider_id)
    service_status = {}
    
    for report in worker_reports:
        service_id = report.serviceid_id
        service = Service.objects.get(serviceid=service_id)
        service_status[report.serviceid] = service.status
    context = {
        'worker_reports': worker_reports,
        'service_status': service_status,
    }
    return render(request, 'worker_report.html', context)

from django.db.models import Prefetch
@login_required
def worker_report(request, provider_id):
    worker_reports = WorkerReport.objects.filter(providerid_id=provider_id)
    
    # Prefetch the related Service objects and extract only the 'status' field
    service_status = Service.objects.filter(providerid_id=provider_id).values_list('status', flat=True)
    
    # Combine the queries into a single call
    worker_reports = worker_reports.prefetch_related(
        Prefetch('serviceid', queryset=Service.objects.filter(providerid_id=provider_id))
    )
    
    context = {
        'worker_reports': worker_reports,
        'service_status': service_status,
    }
    return render(request, 'worker_report.html', context)


@login_required
def client_bookings(request, client_id):
    client_bookings = Service.objects.filter(clientid_id=client_id)
    client_name = Client.objects.get(user_id=client_id).first_name
    
    # Fetching provider names for each booking
    provider_name = [ServiceProvider.objects.get(user_id=booking.providerid_id).providername for booking in client_bookings]
    service_type = [ServiceProvider.objects.get(user_id=booking.providerid_id).service_type for booking in client_bookings]
    
    context = {
        'client_bookings': client_bookings,
        'client_name': client_name,
        'provider_name': provider_name,
        'service_type': service_type,  # Pass provider objects to the template
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

        return redirect('providerpage')  # Redirect to a success page or any other view upon successful assignment

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

    return render(request, 'client_work_reports.html', {'client_reports': client_reports})
def approve_report(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        # Perform logic to approve the report (update database, etc.)
        # Example:
        report = WorkerReport.objects.get(reportid=report_id)
        report.status = 'completed'
        report.save()

        # Update Service status to reportverified
        service_id = report.serviceid_id
        service = Service.objects.get(serviceid=service_id)
        service.status = 'reportverified'
        service.save()

        messages.success(request, 'Report approved successfully!')
    return redirect('userpage')
def cancel_service(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        # Perform logic to cancel the service (update database, etc.)
        # Example:
        report = WorkerReport.objects.get(reportid=report_id)
        report.status = 'canceled'
        report.save()

        # Update Service status to cancelled
        service_id = report.serviceid_id
        service = Service.objects.get(serviceid=service_id)
        service.status = 'cancelled'
        service.save()

        messages.success(request, 'Service cancelled successfully!')
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
        return redirect('providerpage')

    except (ClientBooking.DoesNotExist, Service.DoesNotExist) as e:
        messages.error(request, 'Cancelled booking.')

        # Redirect to an appropriate page or handle the error scenario
        return redirect('providerpage')

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
