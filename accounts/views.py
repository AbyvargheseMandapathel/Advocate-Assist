# accounts/views.py
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect ,get_object_or_404 ,HttpResponseRedirect
from django.urls import reverse
from .models import CustomUser, LawyerProfile  
from django.http import HttpResponseForbidden , HttpResponseNotFound , HttpResponse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth.forms import SetPasswordForm
from .forms import CustomPasswordResetForm  
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import LawyerProfile , ContactEntry , Internship , Student , Application , Booking 
from .forms import ContactForm , BookingForm , InternshipForm
import markdown
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'admin':
            return redirect(reverse('admin_dashboard'))
        elif request.user.user_type == 'client':
            return redirect(reverse('client_dashboard'))
        elif request.user.user_type == 'lawyer':
            return redirect(reverse('lawyer_dashboard'))
        elif request.user.user_type == 'student':
            return redirect(reverse('student_dashboard'))
    
    if request.method == 'POST':
        email = request.POST['email']  # Change this to 'email'
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)  # Use email for authentication
        if user is not None:
            login(request, user)
            if user.user_type == 'admin':
                return redirect(reverse('admin_dashboard'))
            elif user.user_type == 'client':
                return redirect(reverse('client_dashboard'))
            elif user.user_type == 'lawyer':
                return redirect(reverse('lawyer_dashboard'))
            elif user.user_type == 'student':
                return redirect(reverse('student_dashboard'))
    
    return render(request, 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'admin':
            return redirect(reverse('admin_dashboard'))
        elif request.user.user_type == 'client':
            return redirect(reverse('client_dashboard'))
        elif request.user.user_type == 'lawyer':
            return redirect(reverse('lawyer_dashboard'))
        elif request.user.user_type == 'student':
            return redirect(reverse('student_dashboard'))
    
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        adharno = request.POST['adharno']
        address = request.POST['address']
        dob = request.POST['dob']
        pin = request.POST['pin']
        state = request.POST['state']
        phone = request.POST['phone']
        user_type = request.POST['user_type']

        
        # Check if the email is already in use
        if CustomUser.objects.filter(email=email).exists():
            # You can customize this error message as needed
            raise ValidationError('This email is already in use.')

        # Check if the user creating the account is a superuser
        # if request.user.is_superuser:
        #     user_type = 'admin'
        # else:
        #     user_type = request.POST['user_type']

        # Create the user with the determined user_type and email as username
        user = CustomUser.objects.create_user(
            email=email,
            username=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            adharno=adharno,
            address=address,
            dob=dob,
            pin=pin,
            state=state,
            phone=phone,
            user_type=user_type,
        )
        return redirect('login')

    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', {'user': request.user})
    else:
        return redirect('login')
    
@login_required
def admin_dashboard(request):
    if request.user.user_type == 'admin':
        # Calculate the number of lawyers
        lawyer_count = LawyerProfile.objects.count()
        booking_count = Booking.objects.count()
        
        
        # Retrieve the recent 5 bookings, ordered by pk in descending order (greatest to smallest)
        recent_bookings = Booking.objects.order_by('-pk')[:5]
        recent_queries = ContactEntry.objects.order_by('-pk')[:5]
        
        context = {
            'user': request.user,
            'lawyer_count': lawyer_count,
            'recent_bookings': recent_bookings,
            'booking_count':booking_count,
            'recent_queries': recent_queries
            }
            
        
        # Pass the count and recent bookings to the template
        return render(request, 'admin/dashboard.html', context)
    else:
        return HttpResponseForbidden("Access Denied")

# def student_dashboard(request):
#     if request.user.user_type == 'student':
#         recent_internships = Internship.objects.order_by('-pk')[:5]
#         print(recent_internships)

        
#         return render(request, 'student/dashboard.html', {'user': request.user, 'recent_internships': recent_internships})
#     else:
#         return HttpResponseForbidden("Access Denied")

# def client_dashboard(request):
#     return render(request, 'client/dashboard.html', {'user': request.user})
@login_required
def client_dashboard(request):
    # Call the home view and return its response
    return home(request)
@login_required
def lawyer_dashboard(request):
    if request.user.user_type == 'lawyer':
        # Get the current lawyer's profile
        lawyer_profile = LawyerProfile.objects.get(user=request.user)
        bookings = Booking.objects.filter(lawyer=lawyer_profile).order_by('-pk')

        
        # Count the number of bookings for this lawyer
        booking_count = Booking.objects.filter(lawyer=lawyer_profile).count()
        
        return render(request, 'lawyer/dashboard.html', {'user': request.user, 'booking_count': booking_count,'bookings': bookings})
    else:
        return HttpResponseForbidden("Access Denied")
@login_required    
def add_lawyer(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Access Denied")

    if request.method == 'POST':
        # username = request.POST['username']
        email = request.POST['email']
        # Save additional fields to LawyerProfile model
        specialization = request.POST['specialization']
        # start_date = request.POST['start_date']
        start_date_str = request.POST['start_date']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        # experience = request.POST['experience']
        profile_picture = request.FILES.get('profile_picture')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        adharno = request.POST['adharno']
        address = request.POST['address']
        dob = request.POST['dob']
        pin = request.POST['pin']
        state = request.POST['state']
        phone = request.POST['phone']

        # Create a new user with user_type 'lawyer'
        user = CustomUser.objects.create_user(
            username=email, 
            email=email, 
            user_type='lawyer',
            first_name = first_name,
            last_name = last_name,
            adharno = adharno,
            address = address,
            dob = dob,
            pin = pin,
            state = state,
            phone   = phone,    
            )

        

        lawyer_profile = LawyerProfile.objects.create(
            user=user,
            specialization=specialization,
            start_date=start_date,  # Use the converted start_date here
            # experience=experience,
            profile_picture=profile_picture
        )

        # Generate a unique token for password reset
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)
        protocol = 'http'  # Change to 'https' if using HTTPS
        password_reset_url = f"{protocol}://{current_site.domain}/accounts/set/{uid}/{token}/"

        # Render the email body template
        message = render_to_string(
            'registration/password_set_email.html',
            {
                'user': user,
                'password_reset_url': password_reset_url,
            }
        )

        # Send the email with custom template
        send_mail(
            'Set Your Password',
            '',
            'noreply@example.com',  # Sender's email address
            [email],
            fail_silently=False,
            html_message=message  # Use the custom HTML template
        )

        return redirect('mail')  
    
    return render(request, 'admin/add_lawyer.html')

# def custom_password_set_confirm(request, uidb64, token):
#     user_id = urlsafe_base64_decode(uidb64)
#     user = CustomUser.objects.get(pk=user_id)
    
#     if request.method == 'POST':
#         form = SetPasswordForm(user, request.POST)
#         if form.is_valid():
#             form.save()
#             # Log the user in after setting the password
#             user = authenticate(username=user.username, password=form.cleaned_data['new_password1'])
#             login(request, user)
#             return redirect('dashboard')  # Redirect to the dashboard or another page
#     else:
#         form = SetPasswordForm(user)
    
#     return render(request, 'registration/password_set_confirm.html', {'form': form, 'user': user})

@login_required
def custom_password_set_confirm(request, uidb64, token):
    user_id = urlsafe_base64_decode(uidb64)
    user = CustomUser.objects.get(pk=user_id)
    
    if request.method == 'POST':
        form = CustomPasswordResetForm(user, request.POST)
        if form.is_valid():
            form.save()
            # Log the user in after setting the password
            user = authenticate(username=user.username, password=form.cleaned_data['new_password1'])
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or another page
    else:
        form = CustomPasswordResetForm(user)
    
    return render(request, 'registration/password_set_confirm.html', {'form': form, 'user': user})

def home(request):
    # Fetch the most recently added 3 lawyers from the database
    lawyers = LawyerProfile.objects.all().order_by('-user__date_joined')[:3]

    # Create a list to store lawyer names and specializations
    lawyer_info = []

    for lawyer in lawyers:
        lawyer_info.append({
            'name': f"{lawyer.user.first_name} {lawyer.user.last_name}",
            'specialization': lawyer.specialization,
            'profile_picture': lawyer.profile_picture.url,
            'id': lawyer.id,  # Add lawyer's ID
        })

    return render(request, 'index.html', {'lawyer_info': lawyer_info})

def about(request):
    return render(request, 'about.html')

# def contact(request):
#     return render(request, 'contact.html')




def lawyer_details(request, lawyer_id):
    # Retrieve the lawyer's details from the database
    lawyer = get_object_or_404(LawyerProfile, pk=lawyer_id)

    # Render a template with the lawyer's details
    return render(request, 'lawyer/lawyer_details.html', {'lawyer': lawyer})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            contact_entry = ContactEntry(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            contact_entry.save()

            # Redirect to a thank you page or the same page with a success message
            return submit(request)
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

@login_required
def error(request):
    return render(request, '404.html')
@login_required
def mail(request):
    return render(request, 'mail.html')
@login_required
def submit(request):
    return render(request, 'submitted.html')
@login_required
def book(request):
    return render(request, 'book.html')

@login_required
def book_lawyer(request, lawyer_id):
    lawyer = get_object_or_404(LawyerProfile, pk=lawyer_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Assign the booking to the logged-in user
            booking.lawyer = lawyer
            booking.save()
            
            # Redirect to a success page or display a success message
            return redirect('home')
    else:
        form = BookingForm()

    return render(request, 'book_lawyer.html', {'form': form, 'lawyer': lawyer})
@login_required
def booking_details(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking_details.html', {'booking': booking})

@login_required
def internship_detail(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    roles_html = markdown.markdown(internship.roles)

    if request.method == 'POST':
        if request.user.user_type == 'student':
            student = Student.objects.get(user=request.user)
            application, created = Application.objects.get_or_create(internship=internship, student=student)
            if created:
                messages.success(request, 'Application submitted successfully.')
            else:
                messages.warning(request, 'You have already applied to this internship.')

            return redirect('internship_detail', internship_id=internship_id)

    return render(request, 'student/internship_detail.html', {'internship': internship, 'roles_html': roles_html})

@login_required
def add_internship(request):
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to the admin dashboard
    else:
        form = InternshipForm()

    return render(request, 'admin/add_internship.html', {'form': form})


# def student_dashboard(request):
#     if request.user.user_type == 'student':
#         try:
#             # Check if the user is a student and if they are approved
#             student = Student.objects.get(user=request.user)
#             if student.is_approved:
#                 recent_internships = Internship.objects.order_by('-pk')[:5]
#                 return render(request, 'student/dashboard.html', {'user': request.user, 'recent_internships': recent_internships})
#             else:
#                 # Display a message or a separate template for unapproved students
#                 return render(request, 'student/not_approved.html')
#         except Student.DoesNotExist:
#             # User is a student but doesn't exist as a student in the database
#             pass

#     return HttpResponseForbidden("Access Denied")

@login_required
def student_dashboard(request):
    # Check if the user is logged in and is a student
    if request.user.is_authenticated and request.user.user_type == 'student':
        try:
            # Try to retrieve the student profile associated with the user
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            # If the student profile doesn't exist, render 'student_details.html'
            return render(request, 'student/student_details.html')  

        if student.is_approved:
            # Check if college and current CGPA fields are filled
            if student.college and student.current_cgpa is not None:
                recent_internships = Internship.objects.order_by('-pk')[:5]
                return render(request, 'student/dashboard.html', {'user': request.user, 'recent_internships': recent_internships})
            else:
                # Redirect to 'student_details.html' if college or CGPA fields are not filled
                return render(request, 'student/student_details.html')

        else:
            # Display a message or a separate template for unapproved students
            return render(request, 'student/not_approved.html')

    # If not a student or not logged in, return forbidden access
    return HttpResponseForbidden("Access Denied")

@login_required
def approve_students(request):
    # Check if the user is an admin
    if not request.user.user_type == 'admin':
        return HttpResponseForbidden("Access Denied")
    
    # Get a list of unapproved students
    unapproved_students = Student.objects.filter(is_approved=False)
    
    if request.method == 'POST':
        # Handle form submissions for approving/rejecting students
        for student in unapproved_students:
            student_id = str(student.id)
            approve_key = 'approve_' + student_id
            reject_key = 'reject_' + student_id
            
            if approve_key in request.POST:
                # Approve the student
                student.is_approved = True
                student.save()
            elif reject_key in request.POST:
                # Reject the student (optional)
                student.delete()
    
        # Redirect to the approve_students page after processing the submissions
        return redirect('approve_students')
    
    return render(request, 'admin/approve_students.html', {'unapproved_students': unapproved_students})

@login_required
def student_save(request):
    if request.method == 'POST':
        # Get the form data from the request
        college = request.POST.get('college')
        current_cgpa = request.POST.get('current_cgpa')

        # Check if college and current_cgpa are not empty
        if college and current_cgpa:
            # Update or create the student profile for the user
            Student.objects.update_or_create(user=request.user, defaults={'college': college, 'current_cgpa': current_cgpa})

            # Redirect to a success page or the dashboard
            return redirect('student_dashboard')  # Replace 'dashboard' with your dashboard URL name
        else:
            return HttpResponse("Please fill in all fields.")
    else:
        return render(request, 'student/student_details.html')

