from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 200)
    playerId = models.IntegerField()
    registrationDate = models.DateTimeField('registration date')

    def __str__(self):
        return self.name

    def isRecent():
        self.registrationDate >= timezone.now() - datetime.timedelta(days=1)
