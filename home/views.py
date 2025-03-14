from datetime import datetime, timedelta, date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as logouts
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404,redirect,render,reverse
from .forms import PatientForm, PatientUserForm,DoctorUserForm,DoctorForm
from .models import Doctor, Patient
from . import forms,models



@login_required
def admin_dashboard_view(request):
    # Ensure the user is a superuser
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'admin_dashboard.html',context=mydict) # Replace with your actual template


@login_required
def admin_doctor_view(request):
    return render(request, 'admin_doctor.html')  # Replace with your actual template


@login_required
def admin_patient_view(request):
    return render(request, 'admin_patient.html')  # Replace with your actual template

@login_required
def admin_appointment_view(request):
    return render(request, 'admin_appointment.html')  # Replace with your actual template

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
                return redirect('admindashboard')  # Redirect to the admin dashboard
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




def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists() and Doctor.objects.filter(user=user).exists()
  

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Doctor, Patient  # Adjust according to your models

def afterlogin_view(request):
    if request.user.is_authenticated:  # Ensure the user is logged in before checking roles
        if is_doctor(request.user):
            accountapproval = Doctor.objects.filter(user_id=request.user.id, status=True)
            if accountapproval.exists():
                return redirect('doctor-dashboard')
            else:
                return render(request, 'doctor_wait_for_approval.html')

        elif is_patient(request.user):
            accountapproval = Patient.objects.filter(user_id=request.user.id, status=True)
            if accountapproval.exists():
                return redirect('patient-dashboard')
            else:
                return render(request, 'patient_wait_for_approval.html')

    # If the user is not authenticated, show an error message
    messages.error(request, "Incorrect username or password.")
    print("ERROR MESSAGE ADDED:", list(messages.get_messages(request)))  # Debugging
    return redirect('login') # Redirect back to the login page




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




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor_appointment.html',{'doctor':doctor})



# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
def admin_doctor_view(request):
    return render(request,'admin_doctor.html')



@login_required(login_url='adminlogin')
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctor.html',{'doctors':doctors})

@login_required(login_url='adminlogin')
def admin_add_doctor_view(request):
    form_submitted = False  # Track whether the form is submitted

    # Initialize forms outside the POST block to avoid UnboundLocalError
    user_frm = DoctorUserForm()
    doctor_form = DoctorForm()

    if request.method == 'POST':
        form_submitted = True
        user_frm = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        
        if user_frm.is_valid() and doctor_form.is_valid():
            # Save the user
            user = user_frm.save(commit=False)
            user.set_password(user_frm.cleaned_data['password'])
            user.save()
            
            # Save the doctor
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            
            # Add to doctor group
            my_doctor_group, created = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group.user_set.add(user)

            return HttpResponseRedirect('admin-view-doctor')

    return render(request, 'admin_add_doctor.html', {
        'user_form': user_frm,
        'doctor_form': doctor_form,
        'form_submitted': form_submitted
    })






@login_required(login_url='adminlogin')
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'admin_approve_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctor_specialisation.html',{'doctors':doctors})





@login_required(login_url='adminlogin')
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'admin_view_patient.html',{'patients':patients})





@login_required(login_url='adminlogin')
def admin_add_patient_view(request):
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

            context = {'userForm': user_form, 'patientForm': patient_form}
        return HttpResponseRedirect('admin-view-patient')
    return render(request, 'admin_add_patient.html',context)

@login_required(login_url='adminlogin')
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'admin_approve_patient.html',{'patients':patients})


@login_required(login_url='adminlogin')
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'admin_discharge_patient.html',{'patients':patients})





@login_required(login_url='adminlogin')
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'appointment.html',{'appointments':appointments})


@login_required(login_url='adminlogin')
def admin_add_appointment_view(request):
    appointmentForm = forms.AppointmentForm()

    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)

            # Fetch doctor and patient properly
            doctor = models.Doctor.objects.get(id=request.POST.get('doctorId'))
            patient = models.Patient.objects.get(id=request.POST.get('patientId'))

            # Assign the ID values
            appointment.doctorId = doctor.id
            appointment.patientId = patient.id

            # Fetch the doctor and patient names from the User model
            appointment.doctorName = doctor.user.first_name
            appointment.patientName = patient.user.first_name

            appointment.status = True
            appointment.save()
            return HttpResponseRedirect('admin-view-appointment')

    return render(request, 'admin_add_appointment.html', {'appointmentForm': appointmentForm})




@login_required(login_url='adminlogin')
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'admin_approve_appointment.html',{'appointments':appointments})

#--------------------------------------admin end ----------------------------------------------------------------------#
#--------------------------------------doctor stat---------------------------------------------------------------------#

@login_required(login_url='doctor_login')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    doctor = models.Doctor.objects.get(user_id=request.user.id) 
    patientcount=models.Patient.objects.filter(status=True,assignedDoctorId=doctor.id).count()
    appointmentcount = models.Appointment.objects.filter(status=True, doctorId=doctor.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'doctor_dashboard.html',context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'doctor_patient.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients = models.Patient.objects.filter(status=True, assignedDoctorId=request.user.doctor.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    # # Step 1: Fetch the logged-in doctor
    # try:
    #     doctor = models.Doctor.objects.get(user_id=request.user.id)
    # except models.Doctor.DoesNotExist:
    #     return render(request, 'doctor_view_appointment.html', {'error': 'Doctor profile not found.'})

    # # Step 2: Fetch appointments for this doctor
    # appointments = models.Appointment.objects.filter(status=True, doctorId=doctor.id)

    # # Step 3: Fetch patient details linked to these appointments
    # patient_ids = appointments.values_list('patientId', flat=True)  # Get only patient IDs from appointments
    # patients = models.Patient.objects.filter(user_id__in=patient_ids)

    # # Step 4: Ensure correct mapping between appointments and patients
    # patient_dict = {p.user.id: p for p in patients}  # Dictionary mapping patient user_id to patient object
    # appointments_with_patients = [(a, patient_dict.get(a.patientId)) for a in appointments if a.patientId in patient_dict]

    # # Step 5: Render the template

    # return render(request, 'doctor_view_appointment.html', {
    #     'appointments': appointments_with_patients,
    #     'doctor': doctor
    # })
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.filter(status=True, doctorId=doctor.id)
    return render(request, 'doctor_view_appointment.html', {
        'appointments': appointments,
        'doctor': doctor
    })
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.filter(status=True, doctorId=doctor.id)
    return render(request, 'doctor_delete_appointment.html', {
        'appointments': appointments,
        'doctor': doctor
    })



#-----------------------------------------doctor end -------------------------------------------------------------------------#
#----------------------------------------- patient start -------------------------------------------------------------------------#


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'patient_book_appointment.html',context=mydict)



def patient_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'patient_view_doctor.html',{'patient':patient,'doctors':doctors})



def search_doctor_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'patient_view_doctor.html',{'patient':patient,'doctors':doctors})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------









