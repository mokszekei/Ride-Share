from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .forms import UserRegistrationForm, DriverRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Driver,Rider

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to login!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
        return render(request, 'users/user_register.html',{'form':form})

@login_required
def profile(request):
    return render(request,'users/profile.html')

@login_required
def driver_register(request):
    curr_user = request.user
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            dob=form.cleaned_data['DOB']
            licenseNum = form.cleaned_data['licenseNum']
            Vtype = form.cleaned_data['Vtype']
            brand = form.cleaned_data['brand']
            model= form.cleaned_data['model']
            plateNum= form.cleaned_data['plateNum']
            max_pnum= form.cleaned_data['max_pnum']
            special_info= form.cleaned_data['special_info']
            driver = Driver(user=curr_user,DOB=dob,licenseNum=licenseNum,Vtype=Vtype,
                    brand=brand,model=model,plateNum=plateNum,max_pnum=max_pnum,special_info=special_info)
            driver.save()
            messages.success(request, f'You have successfully registered to be a driver!')
            return redirect('driver',curr_user.id)
    elif len(Driver.objects.filter(user_id=curr_user.id))==0:
            form = DriverRegistrationForm()
            return render(request, 'users/driver_register.html', {'form': form})
    else:
        return redirect('driver')

@login_required
def driver(request):
    curr_user = request.user
    driver = Driver.objects.filter(user_id=curr_user.id)
    if len(driver)==0:
        return redirect('driver_register')
    else:
        return render(request, 'users/driver.html')
