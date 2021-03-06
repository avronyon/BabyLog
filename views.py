#!/usr/bin/python
# coding=utf-8

from __future__ import division
from builtins import str
from builtins import range
from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
import datetime
from django.utils import formats
from .models import Event

def get_latest_event(Baby_Name,Event_Type):
    latest_event = Event.objects.filter(baby_name=Baby_Name).filter(event_type=Event_Type).order_by('-dt')[0]
    return latest_event

def vitamin_today(baby_name):
    try:
        today = datetime.datetime.today()
        midnight_today = datetime.datetime(today.year,today.month,today.day)
        vitamin = Event.objects.filter(baby_name=baby_name).filter(event_subtype='vitamin').filter(dt__gte = midnight_today).order_by('-dt')[0]
        return 'got vitamin'
    except:
        return 'no vitamin'

def latest_medicine(baby_name):
    try:
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        med = Event.objects.filter(baby_name=baby_name).filter(event_type='medicine').filter(dt__gte = date_from).exclude(event_subtype='vitamin').order_by('-dt')[0]
        return med
    except:
        return ' '

def get_bottle_text(Baby_Name):
    e = get_latest_event(Baby_Name,'feed')
    dt = e.dt
    date_from = dt - datetime.timedelta(hours=1)
    last_feeds = Event.objects.filter(baby_name=Baby_Name).filter(event_type='feed').filter(dt__gte = date_from).order_by('-dt')
    subtype =''
    value =''
    for e in last_feeds:
        subtype += e.event_subtype + ' + '
        if e.event_subtype == 'breastfeed':
            if e.value == 1:
                value+= u"קצרה"+' + '
            if e.value == 2:
                value+= u"רגילה" + ' + '
        else:
            value += str(e.value) + ' +  '

    subtype = subtype[:-3]
    value = value[:-3]
    subtype = subtype.replace('bottle',u"סימילאק").replace('breastfeed',u"הנקה").replace('moms_milk',u"חלב אם").replace('veg',u"ירקות").replace('fruit',u"פירות")
    return (dt,subtype,value)

def collect_stats(baby_name,start_date,end_date):
    stats = {'total_feeds':0, 'measurable_feeds':0, 'food_amount':0, 'total_poop':0,'average_meal':0,'average_feeds_per_day':0}
    last_feed_time = datetime.datetime.now()+datetime.timedelta(hours=5)
    for event in Event.objects.filter(baby_name=baby_name).filter(dt__gte = start_date).filter(dt__lte = end_date).order_by('-dt'):
        if event.event_type == 'feed':
            if not event.event_subtype == 'breastfeed':
                stats['food_amount'] += event.value
            if event.dt.replace(tzinfo=None) < last_feed_time-datetime.timedelta(hours=1): #combine feeds within one hour
                last_feed_time = event.dt.replace(tzinfo=None)
                stats['total_feeds'] += 1
                if not event.event_subtype == 'breastfeed':
                    stats['measurable_feeds'] += 1
        elif event.event_subtype == 'poop':
            stats['total_poop'] += 1
    try:
        stats['average_meal']=stats['food_amount']/stats['measurable_feeds']
        stats['average_feeds_per_day']="{0:.1f}".format(float(stats['total_feeds'])/(end_date-start_date).days)
    except:
        pass
    return stats

def index(request):
    y = get_latest_event('Yuval','poop')
    s = get_latest_event('Shay','poop')
    b1_dt,b1_subtype,b1_value = get_bottle_text('Yuval')
    b2_dt,b2_subtype,b2_value = get_bottle_text('Shay')
    b1_v = vitamin_today('Yuval')
    b2_v = vitamin_today('Shay')
    b1_m = latest_medicine('Yuval')
    b2_m = latest_medicine('Shay')
    return render(request, 'BabyLog/front_page.html', {'p1': y, 'p2':s , 'b1_name':'Yuval','b1_dt': b1_dt,'b1_subtype':b1_subtype, 'b1_value':b1_value , 'b2_name':'Shay','b2_dt': b2_dt,'b2_subtype':b2_subtype, 'b2_value':b2_value,'b1_v':b1_v , 'b2_v':b2_v , 'b1_m':b1_m, 'b2_m':b2_m})

def feed(request, baby_name):
    amount =[]
    for i in range(2,50):
        amount.append(i*5)
    background = 'lightblue'
    if baby_name == 'Shay':
        background = 'pink'
    return render(request, 'BabyLog/feed.html', {'baby_name': baby_name,'amount': amount, 'background':background})

def history(request,baby_name):
    today = datetime.datetime.today()
    midnight_today = datetime.datetime(today.year,today.month,today.day)
    stats_d =  collect_stats(baby_name,midnight_today-datetime.timedelta(days=1),midnight_today)
    stats_w =  collect_stats(baby_name,midnight_today-datetime.timedelta(days=7),midnight_today)
    stats_m =  collect_stats(baby_name,midnight_today-datetime.timedelta(days=30),midnight_today)
    event_list = Event.objects.filter(baby_name=baby_name).order_by('-dt')
    return render(request, 'BabyLog/history.html', {'event_list':event_list, 'stats_d':stats_d,'stats_w':stats_w,'stats_m':stats_m})


def poop(request, baby_name):
    background = 'lightblue'
    if baby_name == 'Shay':
        background = 'pink'
    return render(request, 'BabyLog/poop.html', {'baby_name': baby_name, 'background':background})

def medicine(request, baby_name):
    background = 'lightblue'
    if baby_name == 'Shay':
        background = 'pink'
    return render(request, 'BabyLog/medicine.html', {'baby_name': baby_name, 'background':background},)

def edit(request, id):
    return render(request, 'BabyLog/edit.html', {'id': id,},)

def action(request, baby_name):
    new_entry = Event(baby_name=baby_name, event_type=request.POST['type'],event_subtype=request.POST['subtype'], value=request.POST['value'],dt=request.POST['date'])
    new_entry.save()
    return HttpResponseRedirect("/BabyLog/")

def delete(request, id):
    instance = Event.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect("/BabyLog/")
