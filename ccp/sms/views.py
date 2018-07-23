from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='accounts:login_page')
def upload_recipients_excel_file(request):
    return HttpResponse("ok")


@login_required(login_url='accounts:login_page')
def send_batch_sms(request):
    return HttpResponse("ok")

