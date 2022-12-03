from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_system_flags, name='getMailFlags'),
    path('getMailObject', views.create_mail_object, name='getMailObject'),
    path('addAttachment', views.add_attachment, name='addAttachment'),
    path('sendMail', views.send_mail, name='sendMail'),
    path('getMailHeads', views.get_mail_heads, name='getMailHeads'),
    path('getMailBody', views.get_mail_body, name='getMailBody'),
    path('changeFlag', views.change_mail_flag, name='changeFlag'),
    path('clearMailFlag', views.clear_mail_flag, name='clearMailFlag')
]
