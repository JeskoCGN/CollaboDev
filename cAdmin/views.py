import random
import os
import requests
import json

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import Settings

# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    """
    Front page of administrative app
    """

    context = {}

    return render(request, 'admin/index.html', context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    """
    User management page of administrative app
    """
    try:
        temporary_password = request.session['temp_password']
        del request.session['temp_password']
    except KeyError:
        temporary_password = ''

    user_list = User.objects.all()
    context = {
        'users': user_list,
        'temporary_password': temporary_password,
    }
    return render(request, 'admin/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request):
    """
    View to handle the deletion of users
    """
    user = User.objects.get(pk=int(request.POST['user']))
    if not user.is_superuser or request.user.profile.server_owner and user != request.user:
        user.delete()

    return HttpResponseRedirect(reverse('cAdmin:users'))


@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    """
    View to handle the creation of user
    """
    temporary_password = ''.join(random.choice('0123456789ABCDEF') for i in range(8))
    user = User.objects.create_user(
        username=request.POST['username'],
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=temporary_password,
    )

    user.clean()
    user.save()

    request.session['temp_password'] = temporary_password

    return HttpResponseRedirect(reverse('cAdmin:users'))


@user_passes_test(lambda u: u.is_superuser)
def reset_collabodev(request):
    settings = Settings.objects.get(pk=1)
    settings.settings_initialised = False

    os.system('python manage.py flush --noinput')

    return HttpResponseRedirect(reverse('cAdmin:reset_page'))


def reset_page(request):
    try:
        Settings.objects.get(pk=1)
        context = {
            'derail': True
        }
    except ObjectDoesNotExist:
        context = {}

    return render(request, 'admin/reset_page.html', context)


@user_passes_test(lambda u: u.is_superuser)
def github(request):
    """
    GitHub Integration settings page. Provides administrators with the ability to
    associate a GitHub Organisation with CollaboDev and import all of its repositories
    """
    session_data = dict(request.session)

    request.session.pop('invalid_org_name', None)
    request.session.pop('valid_org_name', None)

    settings = Settings.objects.get(pk=1)
    session_data['current_org'] = settings.github_org_name

    if request.method == 'POST':
        org_name = request.POST['org_name']
        org_data = requests.get('https://api.github.com/orgs/' + org_name).json()

        try:
            if org_data['login'] == org_name:
                settings.github_org_name = org_name
                settings.save()
                request.session['valid_org_name'] = True
            else:
                raise KeyError
        except KeyError:
            request.session['invalid_org_name'] = True

        return HttpResponseRedirect(reverse('cAdmin:github'))
    return render(request, 'admin/github.html', session_data)

@user_passes_test(lambda u: u.is_superuser)
def update(request):
    """
    Uses Git to update CollaboDev to its latest version.
    """
    update_response = os.popen('git pull https://github.com/dob9601/CollaboDev.git').read()

    if update_response.startswith('Updating'):
        response = 1
    elif update_response == 'Already up to date.\n':
        response = 2
    elif update_response == '':
        response = -1


    payload = {
        'success': True,
        'response': response
    }

    return HttpResponse(json.dumps(payload), content_type='application/json')

def first_time_setup(request):
    """
    First time setup for when the software is first installed on a server
    """

    settings = Settings.objects.get(pk=1)

    if request.method == 'POST':
        if 'setup-key' in request.POST:
            if request.POST['setup-key'] == settings.settings_setup_code:
                context['stage'] = 1
        else:
            context = {}
            admin_pwd = request.POST['admin-password']
            admin_pwd_conf = request.POST['admin-password-conf']
            if admin_pwd == admin_pwd_conf:
                admin_user = User.objects.create_user(
                    username=request.POST['admin-username'],
                    first_name=request.POST['admin-first-name'],
                    last_name=request.POST['admin-last-name'],
                    email=request.POST['admin-email'],
                    password=admin_pwd,
                    is_superuser=True,
                )
                admin_user.profile.server_owner = True
                admin_user.save()
            else:
                context['stage'] = 1
                # Raise password error

            if context == {}:
                context['stage'] = 2
                settings.settings_initialised = True
                settings.save()

    else:
        context['stage'] = 0
        try:
            open("setup-key.txt", "r")
            if settings.settings_setup_code == "":
                raise FileNotFoundError
        except FileNotFoundError:
            key_parts = ''.join(random.choice('0123456789ABCDEF') for i in range(16))

            key_string = "CollaboDev Setup Code: " + key

            with open("setup-key.txt", "w") as key_file:
                key_file.write(key_string)

            settings.settings_setup_code = key
            settings.save()

    return render(request, 'admin/first-time-setup.html', context)
