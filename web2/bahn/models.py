from django.db import models

# Create your models here.


class Verbindung(models.Model):
    name = models.TextField()
    favorit = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Segment(models.Model):
    verbindung = models.ForeignKey(Verbindung, on_delete=models.CASCADE)
    start = models.TextField()
    ziel = models.TextField()
    position = models.IntegerField()
    def __str__(self):
        return "{}: {} - {}".format(self.verbindung.name, self.start, self.ziel)

class Fahrt(models.Model):
    segment = models.ForeignKey(Segment, on_delete = models.CASCADE)
    rueckweg = models.BooleanField(default=False)
    abfahrt = models.DateTimeField()
    ankunft = models.DateTimeField()
    verspaetung = models.IntegerField()
    typ = models.TextField()
    gleis = models.TextField()
    zielbahnhof = models.TextField()
    nummer = models.TextField()
    zeit = models.TextField()
    def __str__(self):
        return "{} - {} ({}): {}".format(self.segment.start, self.segment.ziel, self.rueckweg, self.abfahrt)
