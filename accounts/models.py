from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime
from datetime import datetime, timedelta ,time
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model  # Import the get_user_model function
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .constants import PaymentStatus


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('lawyer', 'Lawyer'),
        ('student', 'Student'),
        ('client', 'Client'),
    )
    
    STATES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Delhi', 'Delhi'),
    ('Puducherry', 'Puducherry'),
)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='client')
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, default='')  # Change: Use email as the username
    first_name = models.CharField(max_length=30, default='')  # Added: First name field
    last_name = models.CharField(max_length=30, default='')  # Added: Last name field
    # adharno = models.CharField(max_length=12,  blank=True,unique=True)  # Added: Adhar number field
    address = models.TextField(default='',blank=True,)  # Added: Address field
    dob = models.DateField(default='2000-01-01',blank=True,)  # Added: Date of birth field
    pin = models.CharField(max_length=6, default='',blank=True,)  # Added: PIN code field
    state = models.CharField(max_length=50, choices=STATES, blank=True, null=False)
    # state = models.CharField(max_length=10, choices=STATES, default='kerala')  # Added: State field
    phone = models.CharField(max_length=15,blank=True)  # Added: Phone number field


class TimeSlot(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    id = models.AutoField(primary_key=True)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lawyers = models.ManyToManyField('LawyerProfile', blank=True, related_name='working_slots')

    def __str__(self):
        return f"{self.get_day_display()} - {self.start_time.strftime('%I:%M %p')} to {self.end_time.strftime('%I:%M %p')}"

    class Meta:
        unique_together = ('day', 'start_time', 'end_time')

class LawyerProfile(models.Model):
    SPECIALIZATIONS = (
        ('family', 'Family Lawyer'),
        ('criminal', 'Criminal Lawyer'),
        ('consumer', 'Consumer Lawyer'),
        ('coperatelawyer', 'Coperate Lawyer'),
        ('civilrightlawyer', 'Civil Right Lawyer'),
        ('divorcelawyer', 'Divorce Lawyer'),
        # Add more as needed
    )
    COURT = (
        ('jfcmcchangancherry', 'Judicial First Class Magistrate Court  Changancherry'),
        ('munsiff', 'Munsiff Court Changancherry'),
        ('jfcmcKanjirapally', 'Judicial First Class Magistrate Court  Kanjirapally'),
        ('munsifcourtkanjirapally', 'Munsiff Court Kanjirapally'),
        ('districtcourtkottayam', 'District Court Kottayam'),
        ('highcourtkochi', 'High Court Kochi'),
        # Add more as needed
    )
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='lawyer_profile')
    # lawyer_id = models.AutoField(primary_key=True)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATIONS,blank=True)
    start_date = models.DateField(null=True)  # Date profession started
    experience = models.IntegerField(blank=True)  # Experience in years
    
    # Define a default profile picture path
    DEFAULT_PROFILE_PICTURE_PATH = 'uploads/default_profile_picture.png'
    
    profile_picture = models.ImageField(
        upload_to='uploads/',
        default=DEFAULT_PROFILE_PICTURE_PATH,  # Set the default profile picture path
        blank=True,
        null=True
    )
    # bar_enrollment_number = models.CharField(max_length=50,blank=True)  # Bar enrollment number
    certificates = models.ManyToManyField('Certificate', blank=True)
    license_no = models.CharField(max_length=30,blank=False)
    # working_days = models.ManyToManyField('Day', blank=True)
    # working_time_start = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name='lawyer_start_time')
    # working_time_end = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name='lawyer_end_time')
    locations = TaggableManager()
    # budget = models.CharField(max_length=30,blank=False)
    cases_won = models.IntegerField(null=True, blank=True)
    cases_lost = models.IntegerField(null=True, blank=True)
    total_cases_handeled = models.IntegerField(null=True, blank=True)
    currendly_handling = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    court = models.CharField(max_length=200, choices=COURT,blank=True)
    working_hours = models.ManyToManyField(TimeSlot, blank=True)
    time_update = models.DateTimeField(null=True, blank=True)
    
    def get_available_time_slots(self, day_of_week):
        # Retrieve the time slots associated with this lawyer for the given day_of_week
        time_slots = self.working_slots.filter(day=day_of_week).order_by('main_slot')

        # Initialize a list to store available time slots
        available_time_slots = []

        # Iterate through the time slots and generate available slots
        for time_slot in time_slots:
            main_slot_parts = time_slot.main_slot.split(' - ')

            # Ensure that there are two parts (start time and end time)
            if len(main_slot_parts) == 2:
                start_time_str, end_time_str = main_slot_parts

                # Remove leading/trailing spaces
                start_time_str = start_time_str.strip()
                end_time_str = end_time_str.strip()

                # Parse the start and end times
                start_time = datetime.strptime(start_time_str, '%I:%M %p')
                end_time = datetime.strptime(end_time_str, '%I:%M %p')

                while start_time < end_time:
                    available_time_slots.append(start_time.strftime('%I:%M %p'))
                    start_time += timedelta(minutes=15)  # Adjust the slot duration as needed

        return available_time_slots
    
    def is_within_7_days(self, date_to_check):
        if self.time_update:
            # Calculate the difference between the last update and the given date
            time_difference = date_to_check - self.time_update.date()

            # Check if the difference is within 7 days
            if 0 <= time_difference.days <= 14:
                return True

        return False

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.specialization}"
    
    def is_available(self, selected_date, selected_slot):
        try:
            selected_time = datetime.strptime(selected_slot, '%I:%M %p').time()
        except ValueError:
            return False

        # Filter based on the 'status' field in the Payment class
        conflicting_appointments = self.appointments.filter(
            appointment_date=selected_date,
            time_slot=selected_time,
            payment__status='confirmed',  # Use 'payment__status' to access the 'status' field in Payment
        )

        # Now 'conflicting_appointments' will contain only those with 'confirmed' status
        # Add additional checks or logic as needed

        return not conflicting_appointments.exists()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.specialization}"
    
    @property
    def appointments(self):
        return Appointment.objects.filter(lawyer=self)

    def save(self, *args, **kwargs):
        # self.experience = self.calculate_experience()
        super().save(*args, **kwargs)
    
class Certificate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return self.name

class Day(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name    
    
        
        
class ContactEntry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

    
    
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(LawyerProfile, on_delete=models.CASCADE)
    details = models.TextField()
    booking_date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="pending")
    original_booking_date = models.DateField(null=True, blank=True)

    def is_confirmed(self):
        return self.status == "confirmed"

    def __str__(self):
        return self.user.email
    

class Student(models.Model):

    SPECIALIZATIONS = (
        ('family', 'Family Lawyer'),
        ('criminal', 'Criminal Lawyer'),
        ('consumer', 'Consumer Lawyer'),
        ('corporate', 'Corporate Lawyer'),
        ('civilrights', 'Civil Rights Lawyer'),
        ('divorce', 'Divorce Lawyer'),
        # Add more specializations as needed
    )
    
    SPECIALIZATIONS = (
        ('2019', '2019'),
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        # Add more specializations as needed
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=100, blank=True)
    course_place = models.CharField(max_length=100, blank=True)
    duration_of_course = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS, blank=True,null= True)
    year_of_pass = models.CharField(max_length=50, choices=SPECIALIZATIONS, blank=True,null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    experience = models.TextField(blank=True,null=True)  # You can use a TextField for experience details
    adhaar_no = models.CharField(max_length=12, blank=True, unique=True)
    adhaar_pic = models.ImageField(upload_to='student_uploads/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    lawyer = models.ForeignKey(LawyerProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
     
    
    
class Internship(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    lawyer_profile = models.ForeignKey(LawyerProfile, on_delete=models.CASCADE, related_name='internships')
    min_cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    start_date = models.DateField()
    duration = models.CharField(max_length=50)
    description = models.TextField()
    roles = models.TextField(help_text="Enter roles as bullet points (one per line)")
    image = models.ImageField(upload_to='internship_images/', blank=False, null=True)


    def __str__(self):
        return self.name
    

class Application(models.Model):
    id = models.AutoField(primary_key=True)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.user.username} - {self.internship.name}'
    
# class StudentUser(CustomUser):
#     is_approved = models.BooleanField(default=False)

class LawyerDayOff(models.Model):
    id = models.AutoField(primary_key=True)
    lawyer = models.ForeignKey(LawyerProfile, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.lawyer} - {self.date}"
    
    
class HolidayRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    id = models.AutoField(primary_key=True)
    lawyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.lawyer.username} - {self.date} ({self.status})'
    
    
class Case(models.Model):
    CASE_STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    id = models.AutoField(primary_key=True)
    # Auto-generate a unique case number like 1001, 1002, ...
    case_number = models.CharField(max_length=10, unique=True)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cases', blank=True, null=True)

    # Client information (taken from the CustomUser model)
    client_name = models.CharField(max_length=100, blank=True)
    client_email = models.EmailField(blank=True)
    client_phone = models.CharField(max_length=15, blank=True)
    client_adhar = models.CharField(max_length=12)
    client_adhar_photo = models.ImageField(upload_to='aadhar_photos/', blank=True, null=True)

    # Lawyer details associated with the case
    lawyer = models.ForeignKey(LawyerProfile, on_delete=models.CASCADE, related_name='cases', blank=True, null=True)

    # Incident details
    incident_place = models.CharField(max_length=100)
    incident_date = models.DateField()
    incident_time = models.TimeField()
    witness_name = models.CharField(max_length=100, blank=True)
    witness_details = models.TextField(blank=True)
    incident_description = models.TextField()

    # Case status
    status = models.CharField(max_length=10, choices=CASE_STATUS_CHOICES, default='open')

    def __str__(self):
        return f"Case {self.case_number} ({self.client_name})"
    
    
class CaseTracking(models.Model):
    id = models.AutoField(primary_key=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_tracking')  # Reference to the original case
    posted_date = models.DateTimeField(auto_now_add=True)  # Automatically set the current date and time when an entry is created
    activity = models.CharField(max_length=100)  # Activity related to the case
    description = models.TextField()  # Description of the activity
    date = models.DateField()  # Date of the activity

    def __str__(self):
        return f"Case Tracking - Case {self.case.case_number} ({self.posted_date})"
    
    
class WorkAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    deadline_date = models.DateField()
    case = models.ForeignKey('Case', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    def __str__(self):
        return f"Work Assignment for Case {self.case.case_number}"
    


class CurrentCase(models.Model):
    id = models.AutoField(primary_key=True)
    lawyer = models.ForeignKey(LawyerProfile, on_delete=models.CASCADE, related_name='current_cases')
    case_number = models.CharField(max_length=10)
    client_name = models.CharField(max_length=100)
    email = models.EmailField()
    phnno = models.CharField(max_length=15)
    incident_description = models.TextField()
    # # Incident details
    incident_place = models.CharField(max_length=100)
    incident_date = models.DateField()
    incident_time = models.TimeField()
    witness_name = models.CharField(max_length=100, blank=True)
    witness_details = models.TextField(blank=True)
    
    

    def __str__(self):
        return f"Case {self.case_number} - {self.client_name}"

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    lawyer = models.ForeignKey('LawyerProfile', on_delete=models.CASCADE)
    client = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=20)  # Use TimeSlot model here

    def __str__(self):
        return f'Appointment with {self.lawyer} on {self.appointment_date} at {self.time_slot}'
    
    def clean(self):
        # Calculate the 7-day window start date based on the lawyer's most recent working hours assignment date.
        most_recent_working_hours_date = self.lawyer.working_slots.aggregate(models.Max('created_date'))['created_date__max']
        
        if most_recent_working_hours_date:
            seven_days_ago = most_recent_working_hours_date + timedelta(days=7)  # Changed from 14 to 7
            
            if self.appointment_date < seven_days_ago.date():
                raise ValidationError("You can only schedule appointments within 7 days of your most recent working hours assignment.")

class Payment(models.Model):
    STATUS_CHOICES = (
        (PaymentStatus.SUCCESS, 'Confirmed'),
        (PaymentStatus.FAILURE, 'Cancelled'),
        (PaymentStatus.PENDING, 'Not Paid'),
    )
    id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PaymentStatus.PENDING)
    order_id = models.CharField(max_length=100, blank=True, null=True)  # Add this field for Razorpay order ID
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.order_id}'

    def save_payment_data(self, payment_id, signature_id):
        """
        Save the Razorpay payment ID and signature ID for this appointment.
        """
        self.razorpay_payment_id = payment_id
        self.razorpay_signature = signature_id
        self.status = PaymentStatus.SUCCESS  # Use PaymentStatus to update the status
        self.save()


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    work_assignment = models.ForeignKey(WorkAssignment, on_delete=models.CASCADE)
    files = models.FileField(upload_to='task_files/', blank=True, null=True)
    note = models.TextField(blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task for Case {self.case.case_number} - Student: {self.student.user.first_name} {self.student.user.last_name}"

            
            