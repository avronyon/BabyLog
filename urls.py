from django.conf.urls import url

from . import views

urlpatterns = [
               url(r'^$', views.index, name='index'),
               url(r'^(?P<baby_name>[a-zA-Z]+)/feed$', views.feed, name='feed'),
               # ex: /BabyLog/Yuval/feed/
               url(r'^(?P<baby_name>[a-zA-Z]+)/poop$', views.poop, name='poop'),
               # ex: /BabyLog/Yuval/poop/
               url(r'^(?P<baby_name>[a-zA-Z]+)/action/$', views.action, name='action'),
               # ex: /BabyLog/Yuval/action/
               url(r'^(?P<baby_name>[a-zA-Z]+)/history/$', views.history, name='history'),
               # ex: /BabyLog/Yuval/history/
               url(r'^(?P<baby_name>[a-zA-Z]+)/medicine/$', views.medicine, name='medicine'),
               # ex: /BabyLog/Yuval/medice/
               url(r'^(?P<id>[0-9]+)/edit/$', views.edit, name='edit'),
               # ex: /BabyLog/45/edit/
               url(r'^(?P<id>[0-9]+)/delete/$', views.delete, name='delete'),
               # ex: /BabyLog/45/edit/
               ]