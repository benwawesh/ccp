import json
import datetime

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from accounts.forms import SetPasswordForm, PasswordResetRequestForm
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models import Q
from app_utility.email_utils import SendEmail
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, get_user_model, login, logout
from accounts.models import WebUser
from django.contrib.auth.decorators import login_required





# Create your views here.

def index(request):
    template = 'accounts/landing.html'
    return render(request, template, {})

def login_page(request):
    template = 'accounts/login_page.html'
    return render(request, template, {})

def register_page(request):
    template = 'accounts/register_page.html'
    return render(request, template, {})

class ResetPasswordRequestView(FormView):
    template_name = "accounts/password_reset_email_template.html"
    success_url = '/login_page'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]
            try:
                user = User.objects.get(Q(username=data) | Q(email=data))
                txt_template = 'email/password_reset_email.txt'
                html_template = 'email/password_reset_email.html'
                recipient = [user]
                email = SendEmail()
                notify_user = email.send_email(recipient, request, txt_template, html_template)
                if notify_user[0]['STATUS'] == '1':
                    result = self.form_valid(form)
                    messages.success(request, 'Email has been sent to ' + data)
                else:
                    result = self.form_invalid(form)
                    messages.success(request, 'Failed to send email!')
                return result
            except Exception as exp:
                print(str(exp))
                result = self.form_invalid(form)
                messages.error(request, 'This user does not exist in the system.')
                return result
        else:
            messages.error(request, 'Invalid Input')

            return self.form_invalid(form)


def login_user(request):
    user_name = request.POST.get("user_name")
    password = request.POST.get("password")
    return_data = {}
    user = User.objects.get(username=user_name)

    if user.is_active is False:
        return_data['STATUS'] = '0'
        return_data['MESSAGE'] = 'Account has been locked. Contact admin to unlock.'
    else:
        user = authenticate(username=user_name, password=password)

        if user is not None:
            login(request, user)
            return_data['STATUS'] = '1'
            return_data['URL'] = 'landing_page'
        else:
            return_data['STATUS'] = '0'
            return_data['MESSAGE'] = 'Invalid credentials.'

    return HttpResponse(
        json.dumps(return_data),
        content_type="application/json"
    )

def user_registration(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    phone_number =request.POST.get('phone_number')
    password = request.POST.get('password')
    return_data = {}
    return_data['MESSAGE'] = []

    try:
        user_exists = User.objects.get(email=username)
        if user_exists:
            return_data['STATUS'] = '0'
            return_data['MESSAGE'].append({
                'STATUS': '0',
                'MESSAGE': 'User was not registered! The email already exist'
            })
            return HttpResponse(json.dumps(return_data))
    except:
        pass

    try:
        phone_number_exists = WebUser.objects.filter(phone_number=phone_number)
        if phone_number_exists:
            return_data['STATUS'] = '0'
            return_data['MESSAGE'].append({
                'STATUS': '0',
                'MESSAGE': 'User was not registered! The phone number already exist'
            })
            return HttpResponse(json.dumps(return_data))
    except:
        pass


    try:

        user_create = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            email= username,
            password= password,
            username= username
        )

        web_user = WebUser()
        web_user.phone_number = phone_number
        web_user.user = User.objects.get(email=username)
        web_user.save()

        return_data['STATUS'] = '1'
        return_data['MESSAGE'].append({
            'STATUS': '1',
            'MESSAGE': 'User has been successfully registered as system user'
        })
    except Exception as e:
        return_data['STATUS'] = '0'
        return_data['MESSAGE'].append({
            'STATUS': '0',
            'MESSAGE': 'User was not registered'
        })
    return HttpResponse(json.dumps(return_data))


@login_required(login_url='accounts:login_page')
def landing_page(request):
    template = 'accounts/landing_page.html'
    context = {}
    return render(request, template, context)

@login_required(login_url='accounts:login_page')
def logout_user(request):
    logout(request)
    return redirect('accounts:login_page')
