from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from actions.models import Action
from actions.utils import create_action
from taggit.models import Tag
from django.http import JsonResponse, HttpResponse
from operator import attrgetter
from .models import Pin, Comment
from .forms import PinCreateForm
from django import forms
import requests, json

def get_notifications(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.profile.following.values_list('id', flat=True)
    # new_followers and new_pins
    if following_ids:
        notifications = actions.filter(target_id=request.user.id) | actions.filter(user_id__in=following_ids, verb='created a new pin')
    else:
        notifications = actions.filter(target_id=request.user.id)
    notifications = notifications.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return notifications

"""
    1. user created and saved pins
    2. pins posted by people who user follows
    3. pins related to tags used by user or people who they follows
    4. pins related to user search (not yet implemented)
    To include all of above three criteria, it is possible to only query with tags
    i.e.user created and saved pins' tags,
        tags of pins created by people who user follows
        and then other pins related to above tags 
"""
@login_required
def pins_feed(request):
    user = request.user
    # tags of pins user created
    all_tags = [tag for pin in Pin.objects.filter(user_id=user.id) for tag in pin.tags.values_list('id', flat=True)]
    # tags of pins user saved
    all_tags += [tag for pin in user.saved_pins.all() for tag in pin.tags.values_list('id', flat=True)]

    # tags of pins created by people who user follows
    following_ids = user.profile.following.values_list('id', flat=True)
    if following_ids:
        all_tags += [tag for pin in Pin.objects.filter(user_id__in=following_ids) for tag in pin.tags.values_list('id', flat=True)]

    all_tags = list(set(all_tags))

    pins = Pin.objects.filter(tags__in=all_tags)
    pins = pins.annotate(same_tags=Count('tags')).order_by('-same_tags')
    pins = sorted(pins, key=attrgetter('created'), reverse=True)

    # to a new user who has no followers, following, created or saved pins
    # we have to show all pins
    if not pins:
        pins = Pin.objects.all()

    paginator = Paginator(pins, 20)
    page = request.GET.get('page')
    # this means only new pins of new pages will be rendered
    pins_only = request.GET.get('pins_only')
    try:
        pins = paginator.page(page)
    except PageNotAnInteger:
        pins = paginator.page(1)
    except EmptyPage:
        if pins_only:
            return HttpResponse('')
        # the last page
        pins = paginator.page(paginator.num_pages)
    if pins_only:
        # new pins of new pages will be rendered in separate template and
        # will be included in main feed (pins_feed.html)
        return render(request, 'pins/pins_list_extension.html', {
            'pins': pins,
        })

    # to render the first time
    return render(request, 'pins/pins_feed.html', {
        'pins': pins,
        'notifications': get_notifications(request),
    })

# not finished yet
@login_required
def pins_create(request):
    error_message = None
    if request.method == 'POST':
        form = PinCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_pin = form.save(commit=False)
            new_pin.user = request.user
            new_pin.save()
            # Without this next line the tags won't be saved
            # this line is required for all many to many fields
            form.save_m2m()
            create_action(request.user, 'created a new pin', new_pin)
            return redirect(new_pin.get_absolute_url())
        else:
            # this is not the right way to validate form error
            # if you come back to upgrade the project,
            # make sure to catch potential form errors properly
            error_message = 'Make sure your file length is at most 100 characters!'
    return render(request, 'pins/pins_create.html', {
        'notifications': get_notifications(request),
        'error_message': error_message,
    })

@login_required
def pins_detail(request, id, slug):
    pin = Pin.objects.get(pk=id, slug=slug)
    comments = pin.comments.all()
    pin_tags_id = pin.tags.values_list('id', flat=True)
    similar_pins = Pin.objects.filter(tags__in=pin_tags_id)\
                            .exclude(id=id)
    similar_pins = similar_pins.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags')

    paginator = Paginator(similar_pins, 20)
    page = request.GET.get('page')
    # this means only new pins of new pages will be rendered
    pins_only = request.GET.get('pins_only')
    try:
        similar_pins = paginator.page(page)
    except PageNotAnInteger:
        similar_pins = paginator.page(1)
    except EmptyPage:
        if pins_only:
            return HttpResponse('')
        # the last page
        similar_pins = paginator.page(paginator.num_pages)
    if pins_only:
        # new pins of new pages will be rendered in separate template and
        # will be included in main feed (pins_feed.html)
        return render(request, 'pins/pins_list_extension.html', {
            'pins': similar_pins,
        })

    return render(request, 'pins/pins_detail.html', {
        'pin': pin,
        'comments': comments,
        'pins': similar_pins,
        'notifications': get_notifications(request),
    })

@login_required
@require_POST
def pins_save(request):
    # id and action are data-id and data-action (save, unsave) of <a> tag
    # when click, they are sent as form data
    pin_id = request.POST.get('id')
    user_action = request.POST.get('action')
    print(pin_id, user_action)
    if pin_id and user_action:
        try:
            pin = Pin.objects.get(id=pin_id)
            if user_action == 'save':
                pin.users_saved.add(request.user)
            else:
                pin.users_saved.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Pin.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

@require_POST
def pins_comment(request):
    pin_id = request.POST.get('pin_id')
    pin_comment = request.POST.get('pin_comment')
    try:
        pin = get_object_or_404(Pin, id=pin_id)
        Comment.objects.create(user=request.user, pin=pin, body=pin_comment)
        # parameters for pins_detail
        comments = pin.comments.all()
        pin_tags_id = pin.tags.values_list('id', flat=True)
        similar_pins = Pin.objects.filter(tags__in=pin_tags_id)\
                                .exclude(id=pin_id)
        similar_pins = similar_pins.annotate(same_tags=Count('tags'))\
                                    .order_by('-same_tags')
    except Pin.DoesNotExist:
        raise forms.ValidationError('Error')

    return render(request, 'pins/pins_detail.html', {
        'pin': pin,
        'comments': comments,
        'pins': similar_pins,
        'notifications': get_notifications(request),
    })

"""
    How to search
    1. search by request tag slug
    2. search by tags of pins which include request tag slug
    3. search by tags similar to reqeust tag slug (eg. 'aesthetic-girl' similar to 'aesthetic-girls')
"""
@login_required
def search(request, slug):
    all_tags = [slug]

    exact_pins_tags = [pin.tags.slugs() for pin in Pin.objects.filter(tags__slug__icontains=slug)]
    exact_pins_tags = [tag for tag_set in exact_pins_tags for tag in tag_set] # list comprehension does not work for some reasons

    similar_tags = [tag.slug for tag in Tag.objects.filter(slug__icontains=slug)]

    all_tags += exact_pins_tags + similar_tags

    pins = Pin.objects.filter(tags__slug__in=all_tags)
    pins = pins.annotate(same_tags=Count('tags')).order_by('-same_tags')

    paginator = Paginator(pins, 20)
    page = request.GET.get('page')
    pins_only = request.GET.get('pins_only')
    try:
        pins = paginator.page(page)
    except PageNotAnInteger:
        pins = paginator.page(1)
    except EmptyPage:
        if pins_only:
            return HttpResponse('')
        pins = paginator.page(paginator.num_pages)
    if pins_only:
        return render(request, 'pins/pins_list_extension.html', {
            'pins': pins,
        })
    # first time render
    return render(request, 'search/search_pins.html', {
        'pins': pins,
        'notifications': get_notifications(request),
    })

@login_required
def fetch_suggestions(request):
    if request.method == 'OPTIONS':
        tags_set = [{'value': tag.name, 'data': tag.slug} for tag in Tag.objects.all()]
        users_set = [{'value': user.username, 'data': user.username} for user in User.objects.all()]
        suggestions_set = tags_set + users_set
        return JsonResponse(json.dumps(suggestions_set), safe=False)

