from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
class LasUser(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=4, null=True)
    wins = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)
    totalChampionKills = models.IntegerField(null=True)
    totalTurretsKilled = models.IntegerField(null=True)
    totalMinionKills = models.IntegerField(null=True)
    totalNeutralMinionsKilled = models.IntegerField(null=True)
    totalAssists = models.IntegerField(null=True)
    registrationDate = models.DateTimeField('registration date', null=True, blank=True)

    def __str__(self):
        return self.name

    def isRecent(self):
        self.registrationDate >= timezone.now() - datetime.timedelta(days=1)
