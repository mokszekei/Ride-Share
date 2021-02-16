from django.http import HttpResponse
from .forms import RequestForm,SharedForm
from .models import Ride, RideDetail
from users.models import Driver
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
import logging
import pytz

# Get an instance of a logger
logger = logging.getLogger(__name__)

curr_time = datetime.now()
curr_time = pytz.utc.localize(curr_time)

def create_ride(request):
    # TODO：change to real loggined driver
    user = request.user
    # user = User.objects.filter(pk=1).first()
    # user = User.objects.create(name = "Siqi Mo",email="mosiqi1996@hotmail.com")

    if request.method == 'POST':
        owner_email = user.email
        owner = user.first_name +''+ user.last_name
        form = RequestForm(request.POST)
        if form.is_valid():
            arrival_time = form.cleaned_data['arrival_time']
            party_size = form.cleaned_data['party_size']
            vehicle = form.cleaned_data['vehicle']

            if vehicle == 'Sedan':
                seats = 4
            else:
                seats = 6
            if arrival_time < curr_time or seats < party_size:
                return HttpResponseRedirect('/owner_edit_fail/')
            remaining_seats = seats - party_size
            ride_detail = RideDetail(
                owner = owner,
                owner_email = owner_email,
                destination = form.cleaned_data['destination'],
                arrival_time = arrival_time,
                remaining_seats = remaining_seats,
                vehicle = vehicle,
                sharable = form.cleaned_data['sharable'],
                special_request = form.cleaned_data['special_request'],
            )
            ride_detail.save()
            ride = ride_detail.ride_set.create(user_role='Owner', party_size=party_size)
            user.ride_set.add(ride)
            return HttpResponseRedirect('/create_ride_success/')
        # logger.error(form.errors)
        return HttpResponseRedirect('/owner_edit_fail/')

    else:
        # edit_ride = Ride.objects.filter(id=rideNumber)[0]
        form = RequestForm()
        return render(request, 'ride/create_ride.html', {'form': form})


def edit_ride(request):
    if request.method == 'POST':
        data = request.POST
        ride_detail_id = data['edit_id']

        edit_ride = Ride.objects.filter(ride_detail_id=ride_detail_id, user_role='Owner')[0]
        edit_ride_detail = RideDetail.objects.filter(pk=ride_detail_id)[0]

        arrival_time = data['arrival_time']
        arrival_time = datetime.strptime(arrival_time, '%Y-%m-%dT%H:%M')
        arrival_time = pytz.utc.localize(arrival_time)
        party_size = int(data['party_size'])
        vehicle = data.get('vehicle')

        if vehicle == 'Sedan':
            seats = 4
        else:
            seats = 6
        if arrival_time < curr_time or seats < party_size:
            return HttpResponseRedirect('/owner_edit_fail/')

        remaining_seats = seats - party_size
        # edit_ride_detail = RideDetail.objects.filter(pk=ride_detail_id)[0]
        edit_ride_detail.destination = data.get('destination')
        edit_ride_detail.arrival_time = arrival_time
        edit_ride_detail.remaining_seats = remaining_seats
        # edit_ride_detail.remaining_seats = edit_ride_detail.remaining_seats - party_size
        edit_ride_detail.vehicle = vehicle
        edit_ride_detail.sharable = data.get('sharable')
        edit_ride_detail.special_request = data.get('special_request')
        edit_ride_detail.save()

        # edit_ride = Ride.objects.filter(ride_detail_id=ride_detail_id)[0]
        edit_ride.party_size = party_size
        edit_ride.save()
        messages.success(request, f'You have successfully edited the ride request!')
        return HttpResponseRedirect('/owner_view_open/'+ride_detail_id)


def owner_edit_fail(request):
    return render(request, "ride/owner_edit_fail.html")

def create_ride_success(request):
    return render(request, "ride/create_ride_success.html")

def owner_view_open(request, ride_detail_id):
    ride_detail = RideDetail.objects.filter(id=ride_detail_id)[0]
    ride_list = Ride.objects.filter(ride_detail_id=ride_detail_id,user_role='Sharer')
    sharers_list = []
    for ride in ride_list:
        user = User.objects.filter(pk=ride.user_id).first()
        sharers_list.append(user.first_name)
    context = {'ride': ride_detail, "sharers_list" : sharers_list, "sharers": ride_list}
    return render(request, "ride/owner_view_open.html", context)


def sharer_view_open(request, ride_detail_id):
    # user = User.objects.filter(pk=1).first()
    user = request.user
    ride = Ride.objects.filter(ride_detail_id=ride_detail_id,user_id=user.id)[0]
    # ride_detail_id = ride.ride_detail_id
    ride_detail = RideDetail.objects.filter(id=ride_detail_id)[0]
    ride_list = Ride.objects.filter(ride_detail_id=ride_detail_id,user_role='Sharer')
    sharers_list = []
    for ride in ride_list:
        # TODO：
        user = User.objects.filter(pk=ride.user_id).first()
        sharers_list.append(user.first_name)
    context = {'ride': ride_detail, "sharers_list" : sharers_list,"ride_id":ride.id}
    return render(request, "ride/sharer_view_open.html", context)


def sharer_edit_ride(request):
    if request.method == 'POST':
        data = request.POST
        ride_detail_id = data['edit_id']
        ride_id = data['ride_id']
        edit_ride = Ride.objects.filter(id=ride_id)[0]
        edit_ride_detail = RideDetail.objects.filter(pk=ride_detail_id)[0]

        party_size = int(data['party_size'])
        old_size = edit_ride.party_size
        old_remain = edit_ride_detail.remaining_seats
        if party_size - old_size - old_remain > 0:
            return HttpResponseRedirect('/owner_edit_fail/')

        remaining_seats = old_size + old_remain - party_size
        edit_ride_detail.remaining_seats = remaining_seats
        edit_ride_detail.save()

        edit_ride.party_size = party_size
        edit_ride.save()

        return HttpResponseRedirect('/sharer_view_open/'+ride_detail_id)


def search_ride(request):
    # TODO：change to real loggined user
    # user = User.objects.filter(pk=1).first()
    user = request.user

    if request.method == 'POST':
        form = SharedForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data['dest']
            earliest_arrival = form.cleaned_data['earliest_arrival']
            latest_arrival = form.cleaned_data['latest_arrival']
            party_size = form.cleaned_data['pnum']

            share_rides = RideDetail.objects.filter(sharable=True, status="Open")
            potential_rides = share_rides.exclude(owner_email=user.email)
            potential_rides = potential_rides.filter(remaining_seats__gt=party_size-1, destination = destination)
            available_rides = potential_rides

            for ride in potential_rides:
                if ride.arrival_time>latest_arrival:
                    available_rides = available_rides.exclude(id=ride.id)

                elif ride.arrival_time<earliest_arrival:
                    available_rides = available_rides.exclude(id=ride.id)

            return render(request, 'ride/search_ride.html', {'form': form, 'available_rides': available_rides, "existRides":True, "size":party_size})
    else:
        form = SharedForm()
        return render(request, 'ride/search_ride.html', {'form': form, "existRides":False})


def join_ride(request):
    # TODO：change to real loggined user
    # user = User.objects.filter(pk=1).first()
    user = request.user

    data = request.POST
    ride_detail_id = data['ride_detail_id']
    party_size = int(data['size'])
    ride_detail = RideDetail.objects.filter(id=ride_detail_id)[0]
    rides_in = Ride.objects.filter(user=user,ride_detail=ride_detail)
    if len(rides_in)==0:
        ride_detail.remaining_seats -= party_size
        ride_detail.save()

        ride = ride_detail.ride_set.create(user_role='Sharer', party_size=party_size)
        user.ride_set.add(ride)
        return render(request, 'ride/join_success.html')
    else:
        return render(request,'ride/join_fail.html')



def driver_search_ride(request):
    # TODO：change to real loggined user
    # user = User.objects.filter(pk=1).first()
    user = request.user
    driver = Driver.objects.filter(user_id=user.id)[0]

    open_rides = RideDetail.objects.filter(vehicle=driver.Vtype, status="Open")
    open_rides = open_rides.exclude(owner_email=user.email)

    # To DO : connect to real logined user
    for ride in open_rides:
        if ride.special_request:
            if ride.special_request != driver.special_info:
                open_rides = open_rides.exclude(id=ride.id)
    return render(request, 'ride/driver_search_ride.html', {'open_rides': open_rides})


def confirm_ride(request,ride_detail_id):
    # TODO：change to real loggined driver
    # user = User.objects.filter(pk=76).first()
    # user = User.objects.create(name="Jimmy", email="jjssid333@gmail.com")
    user = request.user

    ride_detail = RideDetail.objects.filter(id=ride_detail_id)[0]
    ride_detail.status = 'Confirmed'
    ride_detail.driver = user.first_name
    ride_detail.save()

    ride = ride_detail.ride_set.create(user_role='Driver', party_size=1)
    user.ride_set.add(ride)

    email_list = []
    rides = Ride.objects.filter(ride_detail_id=ride_detail_id)
    for ride in rides:
        if ride.user_role == "Driver":
            continue
        passenger = User.objects.filter(id=ride.user_id)[0]
        email_list.append(passenger.email)

    # Email content:
    subject = 'Your ride has been confirmed!'
    message = 'Here is the info of the ride\n'
    message += 'Destination: ' + ride_detail.destination + '\n'
    message += 'Arrival time: ' + str(ride_detail.arrival_time) + '\n'
    message += 'Driver: ' + user.first_name + '\n'
    message += 'Vehicle: ' + ride_detail.vehicle + '\n'

    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, email_list, fail_silently=False)

    return render(request, 'ride/claim_success.html')

def complete_ride(request,ride_detail_id):
    ride_detail = RideDetail.objects.filter(id=ride_detail_id)[0]
    ride_detail.status = 'Completed'
    ride_detail.save()
    return HttpResponseRedirect('/driver_view_confirmed/')

def driver_view_confirmed(request):

    # TODO：change to real loggined driver
    # driver =User.objects.filter(pk=76).first()
    driver = request.user
    rides = Ride.objects.filter(user_id = driver.id ,user_role = 'Driver')
    confirmed_rides = []
    completed_rides = []

    for ride in rides:
        ride_detail = RideDetail.objects.filter(id=ride.ride_detail_id)[0]
        if ride_detail.status == 'Confirmed':
            confirmed_rides.append(ride_detail)
        elif ride_detail.status == 'Completed':
            completed_rides.append(ride_detail)

    return render(request, 'ride/driver_view_confirmed.html', {'confirmed_rides': confirmed_rides, 'completed_rides': completed_rides})


def view_confirmed(request):

    user = request.user
    rides = Ride.objects.filter(user_id=user.id)
    rides = rides.exclude(user_role='Driver')
    confirmed_rides = []

    for ride in rides:
        ride_detail = RideDetail.objects.filter(id=ride.ride_detail_id)[0]
        if ride_detail.status == 'Confirmed':
            confirmed_rides.append(ride_detail)

    return render(request, 'ride/view_confirmed.html',{'confirmed_rides': confirmed_rides})


def view_confirmed_detail(request, ride_detail_id):
    ride_detail = RideDetail.objects.filter(id=ride_detail_id)[0]
    ride_list = Ride.objects.filter(ride_detail_id=ride_detail_id, user_role='Sharer')
    sharers_list = []
    for ride in ride_list:
        user = User.objects.filter(pk=ride.user_id).first()
        sharers_list.append(user.first_name)

    ride = Ride.objects.filter(ride_detail_id=ride_detail_id, user_role='Driver')[0]
    user = User.objects.filter(pk=ride.user_id).first()
    driver_name = user.first_name+' '+user.last_name
    driver = Driver.objects.filter(user_id=ride.user_id)[0]
    context = {'ride': ride_detail, "sharers_list": sharers_list, "sharers": ride_list,"driver":driver, "driver_name":driver_name}
    return render(request, "ride/view_confirmed_detail.html", context)


def view_open(request):
    # TODO：change to real loggined driver
    # user =User.objects.filter(pk=1).first()
    user = request.user

    owner_rides = Ride.objects.filter(user_id=user.id, user_role='Owner')
    owner_open_rides = []

    for ride in owner_rides:
        ride_detail = RideDetail.objects.filter(id=ride.ride_detail_id)[0]
        if ride_detail.status == 'Open':
            owner_open_rides.append(ride_detail)


    sharer_rides = Ride.objects.filter(user_id=user.id, user_role='Sharer')
    sharer_open_rides = []

    for ride in sharer_rides:
        ride_detail = RideDetail.objects.filter(id=ride.ride_detail_id)[0]
        if ride_detail.status == 'Open':
            sharer_open_rides.append(ride_detail)

    return render(request, 'ride/open_list.html',{'owner_open_rides': owner_open_rides, 'sharer_open_rides':sharer_open_rides})
