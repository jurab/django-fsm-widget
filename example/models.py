from django.db import models


class Meatball(models.Model):
    diameter = models.CharField(max_length=255)

    def __unicode__(self):
        return "{pk}: Diameter is {diameter}".format(pk=self.pk,
                                                     diameter=self.diameter)


class Noodle(models.Model):
    length = models.CharField(max_length=255)

    def __unicode__(self):
        return "{pk}: Length is {length}".format(pk=self.pk, length=self.length)


class Spaghetti(models.Model):
    class Meta:
        verbose_name_plural = "Spaghetti"

    meatballs = models.ManyToManyField('Meatball')
    noodles = models.ManyToManyField('Noodle')

    def __unicode__(self):
        return "Spaghetti Number {pk}".format(pk=str(self.pk))