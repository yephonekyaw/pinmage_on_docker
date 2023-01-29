from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from actions.utils import create_action
from pins.models import Pin
from pins.views import get_notifications
from django.http import JsonResponse, HttpResponse
from operator import attrgetter
from .models import Profile
from .forms import EditUserForm, EditProfileForm
    
@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    visit = False
    # check if a user is just visiting another user profile
    if request.user != user:
        visit = True
    
    created_pins = Pin.objects.filter(user_id=user.id)
    saved_pins = user.saved_pins.all()

    # sorted by created date (querysets are already sorted due to ordering :3)
    # created_pins = sorted(created_pins, key=lambda instance: instance.created, reverse=True) --> same but with lambda
    # saved_pins = sorted(saved_pins, key=lambda instance: instance.created, reverse=True) --> same but with lambda
    # created_pins = sorted(created_pins, key=attrgetter('created'), reverse=True)
    # saved_pins = sorted(saved_pins, key=attrgetter('created'), reverse=True)

    created_paginator = Paginator(created_pins, 10)
    saved_paginator = Paginator(saved_pins, 10)

    page = request.GET.get('page')
    pins_only = request.GET.get('pins_only')
    mode = request.GET.get('mode')
    
    # the very first time
    if mode == None:
        created_pins = created_paginator.page(1)
        saved_pins = saved_paginator.page(1)
        return render(request, 'account/user_profile.html', {
            'user': user,
            'created_pins': created_pins,
            'saved_pins': saved_pins,
            'visit': visit,
            'notifications': get_notifications(request),
        })
    
    if mode == 'created':
        try:
            created_pins = created_paginator.page(page)
        except EmptyPage:
            if pins_only:
                return HttpResponse('')
            created_pins = created_paginator.page(created_paginator.num_pages)
        if pins_only:
            return render(request, 'pins/pins_list_extension.html', {
                'pins': created_pins,
            })
    elif mode == 'saved':
        try:
            saved_pins = saved_paginator.page(page)
        except EmptyPage:
            if pins_only:
                return HttpResponse('')
            saved_pins = saved_paginator.page(saved_paginator.num_pages)
        if pins_only:
            return render(request, 'pins/pins_list_extension.html', {
                'pins': saved_pins,
            })

@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    user_action = request.POST.get('action')
    if user_id and user_action:
        try:
            user = User.objects.get(id=user_id)
            if user_action == 'follow':
                request.user.profile.following.add(user)
                user.profile.followers.add(request.user)
                create_action(request.user, 'is now following', user)
            else:
                request.user.profile.following.remove(user)
                user.profile.followers.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

@require_POST
@login_required
def user_profile_edit(request):
    user_form = EditUserForm(instance=request.user, data=request.POST)
    profile_form = EditProfileForm(instance=request.user.profile, files=request.FILES)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'error_message': 'Username already in use!'})

