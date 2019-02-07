from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import OwnerRequest, SharerRequest, Vehicle
from login.models import User
from .forms import RequestOwnerForm, DriverRegistrationForm, SharerSearchForm, DriverProfileEditForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.mail import EmailMessage


# Create your views here.


@login_required
def home(request):
    request.user.plate_number = None
    return render(request, 'ride/home.html')


"""
Views for Owners
"""


class ViewRequests(LoginRequiredMixin, generic.ListView):
    """
    For all users, view their owner requests and sharer request
    Ride Selection
    """
    template_name = 'ride/view_requests.html'
    context_object_name = 'view_requests_list'

    def get_queryset(self):
        return OwnerRequest.objects.filter(owner=self.request.user).exclude(status='completed')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clicker = 'owner'
        context.update({
            'sharer_requests_list': SharerRequest.objects.filter(sharer=self.request.user)\
                                                                .exclude(owner_request__status='completed'),
            'clicker': clicker,
        })
        return context


@login_required
def request_new(request):
    """
    To make new owner request
    Ride Requesting
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = RequestOwnerForm(request.POST)
        if form.is_valid():
            new_request = OwnerRequest.objects.create(owner=request.user)
            new_request.is_sharable = form.cleaned_data['is_sharable']
            new_request.destination = form.cleaned_data['destination']
            new_request.passenger_num = form.cleaned_data['passenger_num']
            new_request.total_passenger = new_request.passenger_num
            new_request.vehicle_type = form.cleaned_data['vehicle_type']
            new_request.arrival_time = form.cleaned_data['arrival_time']
            new_request.save()
            return redirect('ride:home')
    else:
        form = RequestOwnerForm()
    return render(request, 'ride/request_new.html', {'form': form})


class OwnerRequestDetailView(LoginRequiredMixin, generic.DetailView):
    """
    View Owner Request Detail
    Ride Status Viewing(Owner)
    """
    model = OwnerRequest
    template_name = 'ride/to_confirm.html'
    context_object_name = 'request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner_request = OwnerRequest.objects.get(pk=self.kwargs['pk'])
        if owner_request.driver is not None:
            driver = owner_request.driver
        else:
            driver = None
        try:
            sharer_requests = SharerRequest.objects.filter(owner_request=owner_request)
        except SharerRequest.DoesNotExist:
            sharer_requests = None
        clicker = 'owner'
        context.update({
            'driver': driver,
            'sharer_requests': sharer_requests,
            'clicker': clicker,
        })
        return context


class OwnerRequestEditView(LoginRequiredMixin, generic.UpdateView):
    """
    Edit Owner Request
    Ride Request Editing (Owner)
    """
    model = OwnerRequest
    template_name = 'ride/request_edit.html'
    form_class = RequestOwnerForm
    success_url = reverse_lazy('ride:view_requests')

    def form_invalid(self, form):
        print("form is invalid")
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        request = get_object_or_404(OwnerRequest, pk=pk)
        if request.status == 'open':
            # request.is_sharable = form.cleaned_data['is_sharable']
            # request.passenger_num = form.cleaned_data['passenger_num']
            # passenger_num = form.cleaned_data['passenger_num']
            #
            # request.total_passenger = passenger_num
            #
            # request.destination = form.cleaned_data['destination']
            # request.special_vehicle_info = form.cleaned_data['special_vehicle_info']
            # request.arrival_time = form.cleaned_data['arrival_time']
            # # request.vehicle_type = form.cleaned_data['vehicle_type']
            # request.total_passenger = passenger_num
            #
            # request.save()
            form.instance.total_passenger = form.cleaned_data['passenger_num']
            return super().form_valid(form)
        else:
            return redirect('ride:home')


# class SharerRequestEditView(LoginRequiredMixin, generic.UpdateView):
#     """
#     Edit Sharer Request
#     in view_requests
#     """
#     model = SharerRequest
#     template_name = 'ride/request_edit.html'
#     form_class = SharerForm
#     success_url = reverse_lazy('ride:view_requests')
#
#     def form_invalid(self, form):
#         print("form is invalid")
#         return HttpResponse("form is invalid.. this is just an HttpResponse object")
#
#     def form_valid(self, form):
#         pk = self.kwargs.get('pk')
#         request = get_object_or_404(OwnerRequest, pk=pk)
#         if request.status == 'open':
#             # request.is_sharable = form.cleaned_data['is_sharable']
#             # request.passenger_num = form.cleaned_data['passenger_num']
#             # request.destination = form.cleaned_data['destination']
#             # request.special_vehicle_info = form.cleaned_data['special_vehicle_info']
#             # request.arrival_time = form.cleaned_data['arrival_time']
#             # request.vehicle_type = form.cleaned_data['vehicle_type']
#             form.instance.total_passenger = form.cleaned_data['passenger_num']
#
#             return super().form_valid(form)


@login_required
def driver_home(request):
    """
    Driver Home Page
    :param request:
    :return:
    """
    try:
        driver_vehicle = Vehicle.objects.get(plate_number=request.user.plate_number)
    except ObjectDoesNotExist:
        return redirect('ride:driver_registration')

    if request.user.plate_number is None or request.user.plate_number != driver_vehicle.plate_number:
        return redirect('ride:driver_registration')

    return render(request, 'ride/driver_home.html')


@login_required
def driver_registration(request):
    """
    Driver Registration
    :param request:
    :return:
    """
    new_driver = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            new_driver.plate_number = form.cleaned_data['plate_number']
            new_driver.save()
            new_car = Vehicle.objects.create(pk=new_driver.plate_number,
                                             driver=new_driver,
                                             volume=form.cleaned_data['volume'],
                                             vehicle_type=form.cleaned_data['vehicle_type'])
            new_car.special_vehicle_info = form.cleaned_data['special_vehicle_info']
            new_car.save()
            return redirect('ride:driver_home')
    else:
        form = DriverRegistrationForm()
    return render(request, 'ride/driver_registration.html', {'form': form})


@login_required
def driver_profile(request):
    try:
        vehicle = Vehicle.objects.get(plate_number=request.user.plate_number)
    except Vehicle.DoesNotExist:
            return redirect('ride:driver_registration')
    return render(request, 'ride/driver_profile.html', {'vehicle': vehicle})


class DriverProfileEditView(LoginRequiredMixin, generic.UpdateView):
    """
    Edit Owner Request
    Ride Request Editing (Owner)
    """
    model = Vehicle
    template_name = 'ride/driver_profile_edit.html'
    form_class = DriverProfileEditForm
    success_url = reverse_lazy('ride:driver_profile')

    def form_invalid(self, form):
        print("form is invalid")
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

    def form_valid(self, form):

        return super().form_valid(form)


# @login_required
# def ProfileEditor(request):
#     '''
#     Driver Info Editing
#     '''
#     driver_info = get_object_or_404(Driver, user=request.user)
#     if request.method == 'POST':
#         form = DriverUpdateForm(request.POST)
#         if form.is_valid():
#             driver_info.first_name = form.cleaned_data['first_name']
#             driver_info.last_name = form.cleaned_data['last_name']
#             driver_info.type = form.cleaned_data['type']
#             driver_info.plate_number = form.cleaned_data['plate_number']
#             driver_info.max_passenger = form.cleaned_data['max_passenger']
#             driver_info.special_car_info = form.cleaned_data['special_car_info']
#             driver_info.save()
#             return redirect('orders:driver_profile')
#
#     else:
#         first_name = driver_info.first_name
#         last_name = driver_info.last_name
#         type = driver_info.type
#         plate_number = driver_info.plate_number
#         max_passenger = driver_info.max_passenger
#         special_car_info = driver_info.special_car_info
#         form = DriverUpdateForm(initial={'first_name': first_name,
#                                            'last_name': last_name,
#                                            'type': type,
#                                            'plate_number': plate_number,
#                                            'max_passenger': max_passenger,
#                                            'special_car_info': special_car_info,})
#     context = {'form': form,
#                'driver_info': driver_info}
#     return render(request, 'driver/register.html', context)

@login_required
def driver_view_requests(request):
    """
    Could only view open, volume-enough, type-matching requests
    Ride Searching (Driver)
    :param request:
    :return:
    """

    driver_vehicle = get_object_or_404(Vehicle, pk=request.user.plate_number)
    driver_is_sharer = SharerRequest.objects.filter(sharer=request.user)

    open_requests_list = OwnerRequest.objects.filter(total_passenger__lte=driver_vehicle.volume) \
        .filter(vehicle_type=driver_vehicle.vehicle_type) \
        .exclude(status="confirmed") \
        .exclude(status="completed") \
        .exclude(owner=request.user) \
        .exclude(id__in=driver_is_sharer)
    clicker = 'driver'
    context = {
        'open_requests_list': open_requests_list,
        'clicker': clicker
    }
    return render(request, 'ride/view_requests.html', context)


# @login_required
# #pk is OwnerRequest's pk
# def driver_to_confirm(request, pk):
#     """
#     :param request:
#     :param request_id:
#     :return:
#     """
#
#     pass


class DriverRequestDetailView(LoginRequiredMixin, generic.DetailView):
    """
    View Owner Request Detail
    Ride Searching
    """
    model = OwnerRequest
    template_name = 'ride/to_confirm.html'
    context_object_name = 'request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner_request = OwnerRequest.objects.get(pk=self.kwargs['pk'])
        if owner_request.driver is not None:
            driver = owner_request.driver
        else:
            driver = None
        try:
            sharer_requests = SharerRequest.objects.filter(owner_request=owner_request)
        except SharerRequest.DoesNotExist:
            sharer_requests = None
        clicker = 'driver'
        context.update({
            'driver': driver,
            'sharer_requests': sharer_requests,
            'clicker': clicker,
        })
        return context


@login_required
def driver_confirm_request(request, pk):
    to_confirm = get_object_or_404(OwnerRequest, pk=pk)
    driver = get_object_or_404(User, pk=request.user.id)
    if to_confirm.status == 'confirmed':
        messages.info(request, "You are slow!")
        return redirect('ride:home')
    if driver != request.user:
        return redirect('ride:home')
    to_confirm.driver = driver
    to_confirm.status = 'confirmed'
    to_confirm.save()
    messages.info(request, "Ride Confirmed!")

    share_requests = SharerRequest.objects.filter(owner_request=to_confirm)

    email = EmailMessage('Request Confirmed',
                         'Hi Driver,\n\nYour request {} has been confirmed.\n\nRide Sharing Service'.format(
                             to_confirm.id),
                         to=[driver.user.email])
    email.send()
    email = EmailMessage('Request Confirmed',
                         'Dear Owner,\n\nYour request {} has been confirmed.\n\nRide Sharing Service'.format(
                             to_confirm.id),
                         to=[to_confirm.owner.email])
    email.send()
    for request in share_requests:
        email = EmailMessage('Request Confirmed',
                             'Dear Sharer,\n\nYour request {} has been confirmed.\n\nRide Sharing Service'.format(
                                 to_confirm.id),
                             to=[request.sharer.email])
        email.send()

    return redirect('ride:home')


# @login_required
# def driver_ongings(request):
#     """
#     Ride Status Viewing (Driver)
#     :param request:
#     :return:
#     """
#     pass


class DriverOngoings(LoginRequiredMixin, generic.ListView):
    """
    For all users, view their owner requests and sharer request
    Ride Selection
    """
    model = OwnerRequest
    template_name = 'ride/driver_ongoings.html'
    context_object_name = 'ongoings'

    def get_queryset(self):
        return OwnerRequest.objects.filter(status='confirmed', driver=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sharer_requests_list': SharerRequest.objects.filter(sharer__exact=self.request.user).
                exclude(owner_request__status__exact='completed'),
        })
        return context


class DriverOngoingDetailView(LoginRequiredMixin, generic.DetailView):
    """
    View Owner Request Detail
    Ride Searching
    """
    model = OwnerRequest
    template_name = 'ride/driver_ongoing_detail.html'
    context_object_name = 'request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner_request = OwnerRequest.objects.get(pk=self.kwargs['pk'])
        if owner_request.driver is not None:
            driver = owner_request.driver
        else:
            driver = None
        try:
            sharer_requests = SharerRequest.objects.filter(owner_request=owner_request)
        except SharerRequest.DoesNotExist:
            sharer_requests = None
        clicker = 'driver'
        context.update({
            'driver': driver,
            'sharer_requests': sharer_requests,
            'clicker': clicker,
        })
        return context


@login_required
def driver_complete_request(request, pk):
    to_complete = get_object_or_404(OwnerRequest, pk=pk)
    if to_complete.driver != request.user:
        messages.info(request, "You are fake!")
        return redirect('ride:home')
    to_complete.status = 'completed'
    to_complete.save()
    messages.info(request, "Ride Completed!")
    return redirect('ride:home')


@login_required
def sharer_search_ride(request):
    """
    Enter some requirements to search
    Ride Searching (Sharer)
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = SharerSearchForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            vehicle_type = form.cleaned_data['vehicle_type']
            passenger_num = form.cleaned_data['passenger_num']
            earlist_time = form.cleaned_data['earliest_time']
            latest_time = form.cleaned_data['latest_time']
            sharer_result_list = OwnerRequest.objects \
                .filter(destination=destination, arrival_time__range=[earlist_time, latest_time],
                        is_sharable=True,
                        vehicle_type=vehicle_type) \
                .exclude(owner=request.user) \
                .exclude(status='confirmed') \
                .exclude(status='completed')
            clicker = 'sharer'
            context = {
                'sharer_result_list': sharer_result_list,
                'clicker': clicker,
                'passenger_num': passenger_num
            }
            return render(request, 'ride/view_requests.html', context)
    else:
        form = SharerSearchForm()
    return render(request, 'ride/sharer_search_ride.html', {'form': form})


class SharerOwnerRequestDetailView(LoginRequiredMixin, generic.DetailView):
    """
    View Owner Request Detail
    Ride Status Viewing(Owner)
    """
    model = OwnerRequest
    template_name = 'ride/sharer_ownerto_confirm.html'
    context_object_name = 'request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'passenger_num': self.kwargs['passenger_num']
        })
        return context


class MySharerRequestDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Ride Status Viewing(Sharer)
    ongoing
    """
    model = OwnerRequest
    template_name = 'ride/to_confirm.html'
    context_object_name = 'request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner_request = SharerRequest.objects.get(pk=self.kwargs['pk']).owner_request
        if owner_request.driver is not None:
            driver = owner_request.driver
        else:
            driver = None
        try:
            sharer_requests = SharerRequest.objects.filter(owner_request=owner_request)
        except SharerRequest.DoesNotExist:
            sharer_requests = None
        clicker = 'sharer'

        context.update({
            'driver': driver,
            'sharer_requests': sharer_requests,
            'clicker': clicker
        })

        return context


@login_required
def sharer_join(request, owner_request_id, passenger_num):
    owner_request = OwnerRequest.objects.get(pk=owner_request_id)
    new_sharer_request = SharerRequest.objects.create(sharer=request.user,
                                                      owner_request=owner_request,
                                                      destination=owner_request.destination,
                                                      passenger_num=passenger_num,
                                                      vehicle_type=OwnerRequest.objects.get(
                                                          pk=owner_request_id).vehicle_type)
    new_total = new_sharer_request.passenger_num + owner_request.total_passenger
    owner_request.total_passenger = new_total
    owner_request.status = 'shared'
    owner_request.save()
    messages.info(request, "Join Success!")
    return redirect('ride:home', )
