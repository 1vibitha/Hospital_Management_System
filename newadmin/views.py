from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout as logouts

# Create your views here.

@login_required
def admin_dashboard_view(request):
    # Ensure the user is a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'newadmin/admin_dashboard.html')  # Replace with your actual template


@login_required
def admin_doctor_view(request):
    return render(request, 'newadmin/admin_doctor.html')  # Replace with your actual template


@login_required
def admin_patient_view(request):
    return render(request, 'newadmin/admin_patient.html')  # Replace with your actual template

@login_required
def admin_appointment_view(request):
    return render(request, 'newadmin/admin_appointment.html')  # Replace with your actual template
