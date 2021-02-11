from django.core.exceptions import ValidationError
from django.db import models

from alias.manager import AliasManager, AliasHistoricalManager


class Alias(models.Model):
    alias = models.CharField(max_length=50)
    target = models.CharField(max_length=24)
    start = models.DateTimeField()
    end = models.DateTimeField()

    objects = AliasManager()
    historical_objs = AliasHistoricalManager()


class AliasHistorical(Alias):
    objects = AliasHistoricalManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(AliasHistorical, self).save(*args, **kwargs)

    def clean(self):
        if self.end and self.start >= self.end:
            raise ValidationError("The 'start' value can't be bigger than 'end' field")
        if Alias.objects.filter(
            alias=self.alias, target=self.target,
        ).exists():
            raise ValidationError("We should't have two active aliases at the same period")
