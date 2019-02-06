from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import OwnerRequest, SharerRequest, Vehicle
from login.models import User
from .forms import RequestOwnerForm, DriverRegistrationForm, SharerRequestForm
# Create your views here.


@login_required
def home(request):
    return render(request,'ride/home.html')


"""
Views for Owners
"""
class ViewRequests(LoginRequiredMixin, generic.ListView):
    """
    For all users, view their owner requests and sharer request
    Ride Selection
    """
    model = OwnerRequest
    template_name = 'ride/view_requests.html'
    context_object_name = 'view_requests_list'


    def get_queryset(self):
        return OwnerRequest.objects.filter(owner__exact=self.request.user).exclude(status='completed')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clicker = 'owner'
        context.update({
            'sharer_requests_list': SharerRequest.objects.filter(sharer__exact=self.request.user).
                exclude(owner_request__status__exact='completed'),
            'clicker':clicker
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
    template_name = 'ride/request_detail.html'
    context_object_name = 'request'


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
            request.is_sharable = form.cleaned_data['is_sharable']
            request.passenger_num = form.cleaned_data['passenger_num']
            request.destination = form.cleaned_data['destination']
            request.special_vehicle_info = form.cleaned_data['special_vehicle_info']
            request.arrival_time = form.cleaned_data['arrival_time']
            request.vehicle_type = form.cleaned_data['vehicle_type']
            request.total_passenger = request.passenger_num
            request.save()
            return super().form_valid(form)



class SharerRequestEditView(LoginRequiredMixin, generic.UpdateView):
    """
    Edit Sharer Request
    in view_requests
    """
    model = SharerRequest
    template_name = 'ride/request_edit.html'
    form_class = SharerRequestForm
    success_url = reverse_lazy('ride:view_requests')

    def form_invalid(self, form):
        print("form is invalid")
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        request = get_object_or_404(OwnerRequest, pk=pk)
        if request.status == 'open':
            request.is_sharable = form.cleaned_data['is_sharable']
            request.passenger_num = form.cleaned_data['passenger_num']
            request.destination = form.cleaned_data['destination']
            request.special_vehicle_info = form.cleaned_data['special_vehicle_info']
            request.arrival_time = form.cleaned_data['arrival_time']
            request.vehicle_type = form.cleaned_data['vehicle_type']
            request.total_passenger = request.passenger_num
            request.save()
            return super().form_valid(form)



@login_required
def driver_home(request):
    """
    Driver Home Page
    :param request:
    :return:
    """
    return redirect('ride:home')
    if request.user.plate_number:
        pass
    else:
        return redirect('ride:driver_registration')

    return render(request, 'ride/driver_home.html')


@login_required
def driver_view_requests(request):
    """
    Could only view open, volume-enough, type-matching requests
    Ride Searching (Driver)
    :param request:
    :return:
    """
    driver_vehicle = Vehicle.objects.get(plate_number=request.user.plate_number)
    open_requests_list = OwnerRequest.objects.filter(status='open',total_passenger__lte=driver_vehicle.volume)\
        .filter(vehicle_type=driver_vehicle.type)
    clicker = 'driver'
    context = {
        'open_requests_list': open_requests_list,
        'clicker': clicker
    }
    return render(request, 'ride/view_requests.html', context)


@login_required
def driver_request_detail(request, request_id):
    """

    :param request:
    :param request_id:
    :return:
    """
    pass



@login_required
def confirm_request(request):

    pass

@login_required
def driver_onging(request):
    """
    Ride Status Viewing (Driver)
    :param request:
    :return:
    """
    return

@login_required
def complete_request(request):
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
            new_car = Vehicle.objects.create(pk=new_driver.plate_number)
            new_car.volume = form.cleaned_data['volume']
            new_car.type = form.cleaned_data['type']
            new_car.special_vehicle_info = form.cleaned_data['special_vehicle_info']
            new_driver.save()
            new_car.save()
            return redirect('ride:driver_home')
    else:
        form = DriverRegistrationForm()
    return render(request, 'ride/driver_home.html', {'form': form})


class DriverRegistrationView(LoginRequiredMixin, generic.CreateView):
    pass



@login_required
def sharer_request_search(request):
    """
    Enter some requirements to search
    Ride Searching (Sharer)
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = SharerRequestForm(request.POST)
        destination = form.cleaned_data['destination']
        type = form.cleaned_data['vehicle_type']
        earlist_time = form.cleaned_data['earliest_time']
        latest_time = form.cleaned_data['latest_time']
        sharer_result_list = OwnerRequest.objects.filter(destination=destination, arrival_time__range=[earlist_time, latest_time], type=type)
        clicker = 'sharer',
        context = {
            'sharer_result_list': sharer_result_list,
            'clicker':clicker,
        }
        return render(request,'ride/view_requests.html')


@login_required
def sharer_ownerrequest_detail(request, request_id):
    """
    After search, check detail of owner request
    :param request:
    :return:
    """
    pass


class SharerRequestDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Ride Status Viewing(Sharer)
    ongoing
    """
    model = SharerRequest
    template_name = 'ride/request_detail.html'
    context_object_name = 'request'


@login_required
def sharer_join(request, owner_request_id):
    new_sharer_request = SharerRequest.objects.create(sharer=request.user, owner_request=OwnerRequest.objects.get(pk=owner_request_id))
    return redirect('ride:home')



