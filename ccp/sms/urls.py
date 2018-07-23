from django.conf.urls import url
from . import views

app_name = 'sms'

urlpatterns = [
    url(r'^upload_recipients_excel_file$', views.upload_recipients_excel_file, name='upload_recipients_excel_file'),
    url(r'^send_batch_sms$', views.send_batch_sms, name='send_batch_sms'),

]