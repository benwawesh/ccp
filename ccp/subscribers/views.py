import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings



# Create your views here.

@login_required(login_url='accounts:login_page')
def get_subscribers_list_for_sms(request):
    subscribers_list = User.objects.filter(is_staff=False)\
        .values_list('id', 'first_name', 'last_name', 'phone_number')
    return_data = []
    for obj in subscribers_list:
        obj = list(obj)
        return_data.append({
            'id': obj[0],
            'fullName': obj[1] + ' ' + obj[2],
            'mobileNumber': obj[3]
        })
    return HttpResponse(
        json.dumps(return_data)
    )



@login_required(login_url='accounts:login_page')
def subscribers_list(request, offset=0):
    title = "Subscribers"
    template = 'subscribers/subscribers_list.html'
    offset = int(offset)
    obj_list = []
    limit = offset + settings.PAGINATION_OFFSET

    prev_offset = offset - settings.PAGINATION_OFFSET
    if prev_offset < 0:
        prev_offset = 0

    next_offset = 0

    try:
        obj_list = User.objects.filter(is_staff=False)

        next_offset = (offset + settings.PAGINATION_OFFSET)
        if next_offset > len(obj_list):
            next_offset = offset
    except:
        pass

    context = {
        "title": title,
        "prevOffset": prev_offset,
        "nextOffset": next_offset,
        "currentOffset": offset,
        "subscribers": obj_list[offset:limit]
    }

    return render(request, template, context)
