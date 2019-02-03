from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import OwnerRequest, SharerRequest, OrderStatus

# Create your views here.

@login_required
def home(request):
    return render(request,'ride/home.html')


class ViewRequests(LoginRequiredMixin, generic.ListView):
    model = OwnerRequest
    template_name = 'ride/view_requests.html'
    context_object_name = 'view_requests_list'


    def get_queryset(self):
        return OwnerRequest.objects.filter(owner__exact=self.request.user, status=OrderStatus.OP)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sharer_requests_list': SharerRequest.objects.filter(sharer__exact=self.request.user).
                exclude(owner_request__status__exact=OrderStatus.COM),
        })
        return context



def request_new(request):
    return render(request, 'ride/home.html')


def driver_home(request):
    return render(request, 'ride/home.html')


def sharer_request_new(request):
    return render(request, 'ride/home.html')
