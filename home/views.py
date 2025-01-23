from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout as logouts
from .models import Doctor,Patient

# Create your views here.
def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def department(request):
    return render(request, "treatment.html")

def doctor(request):
    return render(request, "doctors.html")

# Rename your login view to avoid conflict
def login(request):
    return render(request, 'login_as.html')

from django.contrib.auth import login as auth_login  # Rename the built-in login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is a superuser
            if user.is_superuser:
                # Log in the user
                auth_login(request, user)
                return redirect('newadmin:admindashboard')  # Redirect to the admin dashboard
            else:
                # Not a superuser, show generic error
                messages.error(request, "Incorrect username or password.")
        else:
            # Authentication failed, show generic error
            messages.error(request, "Incorrect username or password.")

    return render(request, "adminlogin.html")



#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'doctorclick.html')


#for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'patientclick.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import DoctorUserForm, DoctorForm

def doctor_signup_view(request):
    form_submitted = False  # Track whether the form is submitted
    if request.method == 'POST':
        form_submitted = True
        user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            # Save the user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            # Save the doctor
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            
            # Add to doctor group
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

            messages.success(request, 'Account created successfully!')
            return redirect('doctor_login')  # Redirect to login page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = DoctorUserForm()
        doctor_form = DoctorForm()

    return render(request, 'doctorsignup.html', {
        'user_form': user_form,
        'doctor_form': doctor_form,
        'form_submitted': form_submitted
    })

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import PatientUserForm, PatientForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import PatientUserForm, PatientForm
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import Group
from . import forms



# def patient_signup_view(request):
#     if request.method == 'POST':
#         userForm = PatientUserForm(request.POST)
#         patientForm = PatientForm(request.POST, request.FILES)
#         if userForm.is_valid() and patientForm.is_valid():
#             # Save the user
#             user = userForm.save(commit=False)
#             user.set_password(user.cleaned_data['password'])
#             user.save()

#             # Save the patient
#             patient = patientForm.save(commit=False)
#             patient.user = user
#             patient.save()

#             # Add the user to the PATIENT group
#             my_patient_group = Group.objects.get_or_create(name='PATIENT')
#             my_patient_group[0].user_set.add(user)

#             messages.success(request, 'Account created successfully!')
#             return redirect('patientlogin')  # Redirect to login page or another page
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         userForm = PatientUserForm()
#         patientForm = PatientForm()

#     return render(request, 'patientsignup.html', {'userForm': userForm, 'patientForm': patientForm})
# def patient_signup_view(request):
#     if request.method == 'POST':
#         userForm = PatientUserForm(request.POST)
#         patientForm = PatientForm(request.POST, request.FILES)

#         if userForm.is_valid() and patientForm.is_valid():
#             # Save the user
#             user = userForm.save(commit=False)
#             user.set_password(user.cleaned_data['password'])
#             user.save()

#             # Save the patient
#             patient = patientForm.save(commit=False)
#             patient.user = user
#             patient.save()

#             # Add the user to the PATIENT group
#             my_patient_group = Group.objects.get_or_create(name='PATIENT')
#             my_patient_group[0].user_set.add(user)

#             messages.success(request, 'Account created successfully!')
#             return redirect('patientlogin')  # Redirect to login page or another page
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         userForm = PatientUserForm()
#         patientForm = PatientForm()

#     return render(request, 'patientsignup.html', {'userForm': userForm, 'patientForm': patientForm})


def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists() and Doctor.objects.filter(user=user).exists()
    
# def afterlogin_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # Authenticate user
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             # Check if the user is a doctor
#             if is_doctor(user):
#                 accountapproval = Doctor.objects.filter(user_id=user.id, status=True)
#                 if accountapproval.exists():
#                     login(request, user)
#                     return redirect('doctor-dashboard')  # Redirect to doctor's dashboard
#                 else:
#                     messages.error(request, "Doctor account not approved yet.")
#                     return render(request, 'doctor_wait_for_approval.html')  # Wait for approval page

#             # Check if the user is a patient
#             elif is_patient(user):
#                 accountapproval = Patient.objects.filter(user_id=user.id, status=True)
#                 if accountapproval.exists():
#                     login(request, user)
#                     return redirect('patient-dashboard')  # Redirect to patient's dashboard
#                 else:
#                     messages.error(request, "Patient account not approved yet.")
#                     return render(request, 'patient_wait_for_approval.html')  # Wait for approval page

#             else:
#                 messages.error(request, "Incorrect username or password.")
#                 return render(request, 'login_as.html')

#         else:
#             messages.error(request, "Incorrect username or password.")
#             return render(request, 'login_as.html')

#     return render(request, 'login')


# Redirect after login
def afterlogin_view(request):
    if is_doctor(request.user):
        accountapproval = Doctor.objects.filter(user_id=request.user.id, status=True)
        if accountapproval.exists():
            return redirect('doctor-dashboard')
        else:
            return render(request, 'doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'patient_wait_for_approval.html')
    return redirect('login')  # Default fallback

# # Doctor dashboard view
# @login_required(login_url='doctor_login')
# @user_passes_test(is_doctor)
# def doctor_dashboard_view(request):
#     patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
#     appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
#     patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

#     #for  table in doctor dashboard
#     appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
#     patientid=[]
#     for a in appointments:
#         patientid.append(a.patientId)
#     patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
#     appointments=zip(appointments,patients)
#     mydict={
#     'patientcount':patientcount,
#     'appointmentcount':appointmentcount,
#     'patientdischarged':patientdischarged,
#     'appointments':appointments,
#     'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
#     }
#     return render(request, 'doctor_dashboard.html')

@login_required(login_url='doctor_login')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # Get the Doctor instance
    patientcount = models.Patient.objects.filter(status=True, assignedDoctorId=doctor.id).count()

    mydict = {
        'patientcount': patientcount,
        'doctor':models.Doctor.objects.get(user_id=request.user.id),  # For profile picture of doctor in the sidebar
    }
    return render(request, 'doctor_dashboard.html', mydict)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from . import forms
from .models import Doctor, Patient

def patient_signup_view(request):
    user_form = forms.PatientUserForm()
    patient_form = forms.PatientForm()
    context = {'userForm': user_form, 'patientForm': patient_form}

    if request.method == 'POST':
        user_form = forms.PatientUserForm(request.POST)
        patient_form = forms.PatientForm(request.POST, request.FILES)
        
        if user_form.is_valid() and patient_form.is_valid():
            # Save user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Save patient
            patient = patient_form.save(commit=False)
            patient.user = user

            # Validate doctor ID
            assigned_doctor_id = request.POST.get('assignedDoctorId')
            if assigned_doctor_id and Doctor.objects.filter(id=assigned_doctor_id).exists():
                patient.assignedDoctorId = assigned_doctor_id
            else:
                messages.error(request, "Invalid Doctor ID.")
                return render(request, 'patientsignup.html', context)

            patient.save()

            # Add user to patient group
            patient_group, _ = Group.objects.get_or_create(name='PATIENT')
            patient_group.user_set.add(user)

            messages.success(request, "Registration successful. Please login to continue.")
            return redirect('patientlogin')
        else:
            # Pass the forms with errors back to the template
            context = {'userForm': user_form, 'patientForm': patient_form}
            # messages.error(request, "Please correct the errors below.")

    return render(request, 'patientsignup.html', context)

from django.shortcuts import get_object_or_404

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient = get_object_or_404(models.Patient, user_id=request.user.id)

    doctor = None
    if patient.assignedDoctorId:
        try:
            doctor = models.Doctor.objects.get(id=patient.assignedDoctorId)  # Use 'id' instead of 'user_id'
        except models.Doctor.DoesNotExist:
            doctor = None

    mydict = {
        'patient': patient,
        'doctorName': doctor.get_name if doctor else "Not Assigned",
        'doctorMobile': doctor.mobile if doctor else "N/A",
        'doctorAddress': doctor.address if doctor else "N/A",
        'symptoms': patient.symptoms,
        'doctorDepartment': doctor.department if doctor else "N/A",
        'admitDate': patient.admitDate,
    }
    return render(request, 'patient_dashboard.html', mydict)

# #-----------for checking user is doctor , patient or admin(by sumit)
# def is_admin(user):
#     return user.groups.filter(name='ADMIN').exists()
# def is_doctor(user):
#     return user.groups.filter(name='DOCTOR').exists()



# #---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
# def afterlogin_view(request):
#     if is_doctor(request.user):
#         # Check if the doctor is approved
#         accountapproval = models.Doctor.objects.filter(user_id=request.user.id, status=True)
#         if accountapproval.exists():
#             return redirect('doctor-dashboard')  # Redirect to doctor dashboard
#         else:
#             return render(request, 'doctor_wait_for_approval.html')  # Pending approval page
#     # Add other roles (admin, patient) if needed
#     return redirect('login')  # Default redirection if no role matches

    # elif is_patient(request.user):
    #     accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
    #     if accountapproval:
    #         return redirect('patient-dashboard')
    #     else:
    #         return render(request,'hospital/patient_wait_for_approval.html')



# @login_required(login_url='doctor_login')  # Redirects to login if not authenticated
# @user_passes_test(is_doctor)  # Ensures only doctors access this view
# def doctor_dashboard_view(request):
    # Fetch counts and details for dashboard cards
    # patientcount = models.Patient.objects.filter(status=True, assignedDoctorId=request.user.id).count()
    # appointmentcount = models.Appointment.objects.filter(status=True, doctorId=request.user.id).count()
    # patientdischarged = models.PatientDischargeDetails.objects.filter(
    #     assignedDoctorName=request.user.first_name
    # ).distinct().count()

    # # Fetch recent appointments
    # appointments = models.Appointment.objects.filter(status=True, doctorId=request.user.id).order_by('-id')
    # patientid = [a.patientId for a in appointments]
    # patients = models.Patient.objects.filter(status=True, user_id__in=patientid).order_by('-id')
    # appointments = zip(appointments, patients)

    # # Context for the template
    # context = {
    #     'patientcount': patientcount,
    #     'appointmentcount': appointmentcount,
    #     'patientdischarged': patientdischarged,
    #     'appointments': appointments,
    #     'doctor': models.Doctor.objects.get(user_id=request.user.id),  # Doctor profile
    # }
    # return render(request, 'doctor_dashboard.html')






@login_required
def admin_doctor_view(request):
    return render(request, "admin_doctor.html")  # Replace with your actual template


@login_required
def admin_patient_view(request):
    return render(request, "admin_patient.html")  # Replace with your actual template

@login_required
def admin_appointment_view(request):
    return render(request, "admin_appointment.html")  # Replace with your actual template

def logout(request):
    logouts(request)
    return redirect('index')
