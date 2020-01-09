import datetime
import time

import schiene
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from . import models

# Create your views here.

s = schiene.Schiene()

def set_today(dt):
    today = datetime.date.today()
    return dt.replace(year=today.year, month=today.month, day=today.day, tzinfo=None)


def get_fahrten(segment, start, ziel, rueckweg = False):
    res = s.connections(start, ziel)
    for v in res:
        delay = 0
        if 'delay' in v:
            delay = v['delay']['delay_departure']
        # Prüfen ob Fahrt schon bekannt
        v_abfahrt = set_today(datetime.datetime.strptime(v['departure'], '%H:%M'))
        fahrten = models.Fahrt.objects.filter(abfahrt=v_abfahrt, segment=segment, rueckweg=rueckweg)
        if len(fahrten) == 1:
            fahrt = fahrten[0]
        elif len(fahrten) == 0:
            fahrt = models.Fahrt()
        else:
            print("MEHR ALS EINE FAHRT MIT GLEICHER ZEIT!!")
            raise("MEHR ALS EINE FAHRT MIT GLEICHER ZEIT!!")
        fahrt.segment = segment
        fahrt.verspaetung = delay
        fahrt.zielbahnhof = "NOT YET IMPLEMENTED"
        fahrt.gleis = "NOT YET IMPLEMENTED"
        fahrt.nummer = "NOT YET IMPLEMENTED"
        fahrt.abfahrt = v_abfahrt
        fahrt.ankunft = set_today(datetime.datetime.strptime(v['arrival'], '%H:%M'))
        fahrt.typ = v['products'][0]
        fahrt.zeit = v['time']
        fahrt.rueckweg = rueckweg
        fahrt.save()
        print('    Abfahrt: {} | +{}'.format(v['departure'], delay))
        print(v)
    

def get_bahn_data():
    verbindungen = models.Verbindung.objects.all()
    for verbindung in verbindungen:
        for segment in verbindung.segment_set.all().order_by('position'):
            print("Hole Daten für: " + str(segment))
            get_fahrten(segment, segment.start, segment.ziel, rueckweg = False)
            get_fahrten(segment, segment.ziel, segment.start, rueckweg = True)



def fetch(request):
    get_bahn_data()
    return HttpResponse("DONE")

def start(request):
    verbindungen = models.Verbindung.objects.all()
    context = {
        'verbindungen': verbindungen
    }
    return render(request, 'bahn/start.html', context)

def fahrten(request, verbindung_id, richtung):
    rueckweg = richtung == 'zurueck'
    verbindung = get_object_or_404(models.Verbindung, pk=verbindung_id)
    if rueckweg:
        segmente = verbindung.segment_set.all().order_by('-position')
    else:
        segmente = verbindung.segment_set.all().order_by('position')
    for segment in segmente:
        segment.fahrten = segment.fahrt_set.filter(abfahrt__gt = timezone.now(), rueckweg = rueckweg).order_by('abfahrt')
        if rueckweg:
            tmp = segment.start
            segment.start = segment.ziel
            segment.ziel = tmp
    context = {
        'verbindung': verbindung,
        'segmente': segmente
    }
    return render(request, 'bahn/fahrten.html', context)

def setup(request):
    if request.POST:
        if 'name' in request.POST and request.POST['name'].strip() != '':
            verbindung = models.Verbindung()   
            verbindung.name = request.POST['name'].strip()
            verbindung.save()
            verbindung.refresh_from_db()
            i = 1
            while True:
                if 'start{}'.format(i) in request.POST: # wir haben ein segment gefunden
                    segment = models.Segment()
                    segment.start = request.POST['start{}'.format(i)]
                    segment.ziel = request.POST['ziel{}'.format(i)]
                    segment.verbindung = verbindung
                    segment.position = i
                    segment.save()
                    i += 1
                else:
                    break
        return redirect('setup')

    verbindungen = models.Verbindung.objects.all()
    context = {
        'verbindungen': verbindungen
    }



    return render(request, 'bahn/setup.html', context)
