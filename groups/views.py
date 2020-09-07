from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.views import generic

from groups.models import Group,GroupMember
from . import models

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description',)
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except:
            messages.warning(self.request,('warning already a member'))

        else:
            messages.success(self.request,('you are now a member'))
            
        return super(JoinGroup, self).get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        try:
            membership = models.GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,'you are not in this group, bitch')
        else:
            messages.success(self.request, ('you left'))

        return super(JoinGroup, self).get(request, *args, **kwargs)