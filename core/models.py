from django.db import models
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from haystack.utils.geo import Point
from django.db.models import Min, Max
from django.template.defaultfilters import slugify
from geopy.geocoders import GoogleV3

from haystack.query import SearchQuerySet
from haystack.utils.geo import D

import datetime
import logging


class Sport(models.Model):
    name = models.CharField(max_length=100)
    combinedSport = models.BooleanField(default=False)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name


# That class is inspired by the google address types
# see https://developers.google.com/maps/documentation/javascript/geocoding
class Location(models.Model):

    street_number = models.CharField(max_length=10, blank=True, null=True)
    route = models.CharField(max_length=200, blank=True, null=True)

    # city/town
    locality = models.CharField(max_length=100)

    # region / state
    administrative_area_level_1 = models.CharField(max_length=100)
    administrative_area_level_1_short_name = models.CharField(max_length=100)
    # departement
    administrative_area_level_2 = models.CharField(max_length=100)
    administrative_area_level_2_short_name = models.CharField(max_length=100)

    postal_code = models.CharField(max_length=16)
    country = CountryField()

    lat = models.DecimalField(max_digits=8, decimal_places=5)
    lng = models.DecimalField(max_digits=8, decimal_places=5)

    geocode_mapping = [{'field': 'street_number',
                        'geo_field': {'name': 'street_number', 'type': 'short_name'}
                        },
                       {'field': 'route',
                        'geo_field': {'name': 'route', 'type': 'short_name'}
                        },
                       {'field': 'locality',
                        'geo_field': {'name': 'locality', 'type': 'short_name'}
                        },
                       {'field': 'administrative_area_level_1',
                        'geo_field': {'name': 'administrative_area_level_1', 'type': 'long_name'}
                        },
                       {'field': 'administrative_area_level_1_short_name',
                        'geo_field': {'name': 'administrative_area_level_1', 'type': 'short_name'}
                        },
                       {'field': 'administrative_area_level_2',
                        'geo_field': {'name': 'administrative_area_level_2', 'type': 'long_name'}
                        },
                       {'field': 'administrative_area_level_2_short_name',
                        'geo_field': {'name': 'administrative_area_level_2', 'type': 'short_name'}
                        },
                       {'field': 'postal_code',
                        'geo_field': {'name': 'postal_code', 'type': 'short_name'}
                        },
                       {'field': 'country',
                        'geo_field': {'name': 'country', 'type': 'short_name'}
                        }]

    def __str__(self):
        return "{0}, {1}, {2} ({3}, {4})".format(self.postal_code, self.locality, self.country, self.lat, self.lng)

    def geocode_raw_address(self, raw_address):
        g = GoogleV3()
        loc = g.geocode(raw_address)
        if loc:
            # list comprehension to retrieve data
            for f in self._meta.fields:
                for line in loc.raw['address_components']:
                    fmap = [i.get('geo_field', None) for i in self.geocode_mapping if i.get('field', None) == f.attname]
                    if fmap:
                        if fmap[0].get('name', None) in line['types']:
                            setattr(self, f.name, line[fmap[0]['type']])

            self.lat = loc.latitude
            self.lng = loc.longitude

    def get_point(self):
        return Point(float(self.lng), float(self.lat))


class SportStage(models.Model):
    sport = models.ForeignKey(Sport)
    name = models.CharField(max_length=20)
    default_order = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Sport Stage"
        verbose_name_plural = "Sport Stages"
        ordering = ['sport', 'default_order']

    def natural_key(self):
        return (self.sport, self.name)

    def __str__(self):
        return "{0}".format(self.name)


class Event(models.Model):
    name = models.CharField(max_length=150)
    edition = models.PositiveSmallIntegerField()
    website = models.URLField(blank=True, null=True)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name

    def get_start_date(self):
        return self.races.all().aggregate(Min('date'))['date__min']

    def get_end_date(self):
        return self.races.all().aggregate(Max('date'))['date__max']

    def get_distance_cat_set(self):
        distance_cat_set = []
        for r in self.races.order_by('distance_cat__order'):
            distance_cat_set.append(r.distance_cat)
        return distance_cat_set

    def get_races(self):
        races = []
        for r in self.races.order_by('distance_cat__order'):
            races.append(r)
        return races


class Federation(models.Model):
    name = models.CharField(max_length=150)
    sport = models.ManyToManyField(Sport)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name


class DistanceCategory(models.Model):
    sport = models.ForeignKey(Sport)
    name = models.CharField(max_length=2)
    long_name = models.CharField(max_length=20, blank=True, null=True)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return "{0}".format(self.name)

    def natural_key(self):
        return (self.sport, self.name)

    class Meta:
        verbose_name = "Distance Category"
        verbose_name_plural = "Distance Categories"


class Race(models.Model):
    slug = models.SlugField(max_length=100, blank=True, null=True)
    sport = models.ForeignKey(Sport)
    event = models.ForeignKey(Event, related_name='races')
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField()
    distance_cat = models.ForeignKey(DistanceCategory)
    price = models.PositiveIntegerField(blank=True, null=True)
    federation = models.ForeignKey(Federation, blank=True, null=True, related_name='races')
    label = models.ForeignKey(Label, blank=True, null=True, related_name='races')
    contact = models.ForeignKey(Contact)
    description = models.TextField(blank=True, null=True)
    location = models.OneToOneField(Location)
    validated = models.BooleanField(default=False)

    def __str__(self):
        return "{0} - {1}".format(self.event.name, self.distance_cat.name)

    def pre_delete(self, *args, **kwargs):
        if len(self.contact.races) < 2:
            self.contact.delete()
        if len(self.location.races) < 2:
            self.location.delete()

        # delete event that will not have any race remaining
        if len(self.event.races) < 2:
            self.event.delete()

        # # delete label that will not have any race remaining
        # if len(self.label.races) < 2:
        #     self.label.delete()

    def save(self, *args, **kwargs):
        if self.pk is None:
            # Newly created object, so set slug
            seq = (self.event.name, self.distance_cat.name)
            self.slug = slugify("-".join(seq))
            logging.debug(args, kwargs)
            super(Race, self).save(*args, **kwargs)
            self.init_distances_from_default()

        # do not insert the same instance if a force_insert has been set to true
            if kwargs.get('force_insert', None):
                kwargs.pop('force_insert')
        super(Race, self).save(force_update=True, *args, **kwargs)

    def natural_key(self):
        return (self.event, self.sport, self.distance_cat)

    def init_distances_from_default(self):
        """ Initialize the distances from default distances for this category on race creation """
        if not self.distances.all():
            for rs in StageDistanceDefault.objects.filter(distance_cat=self.distance_cat):
                rs = StageDistanceSpecific(race=self, order=rs.order, stage=rs.stage, distance=rs.distance)
                rs.save()

    def get_potential_doubles(self):
        sqs = SearchQuerySet()

        pk = self.pk
        if pk:
            sqs = sqs.exclude(django_id=pk)

        sqs = sqs.dwithin('location', self.location.get_point(), D(km=10))
        sqs = sqs.filter(date__gte=self.date + datetime.timedelta(days=-1),
                         date__lte=self.date + datetime.timedelta(days=1),
                         distance_cat=self.distance_cat
                         )

        # return race objects instead of haystack searchresul
        return [sr.object for sr in sqs]


class StageDistance(models.Model):
    order = models.PositiveSmallIntegerField()
    stage = models.ForeignKey(SportStage)
    distance = models.PositiveIntegerField()

    class Meta:
        abstract = True


class StageDistanceSpecific(StageDistance):
    race = models.ForeignKey(Race, related_name='distances')

    class Meta:
        verbose_name = "Stage distance (for a race)"
        verbose_name_plural = "Stages distance (for a race)"
        ordering = ['pk']

    def natural_key(self):
        return (self.race, self.order)

    def clean(self):
        if (not self.race.sport.combinedSport) & (self.race.distances.all().count() > 1):
            raise ValidationError('Only combined sport should be able to have multiple stages')

    def __str__(self):
        return "{0}/{1} - {2} : {3}m".format(self.race, self.order, self.stage.name, self.distance)


class StageDistanceDefault(StageDistance):
    distance_cat = models.ForeignKey(DistanceCategory)

    class Meta:
        verbose_name = "Stage distance (default)"
        verbose_name_plural = "Stages distance (default)"
        ordering = ['pk']

    def clean(self):
        if (not self.distance_cat.sport.combinedSport) & (self.distance_cat.stagedistancedefault_set.all().count() > 1):
            raise ValidationError('Only combined sport should be able to have multiple stages')

    def natural_key(self):
        return (self.race, self.order)

    def __str__(self):
        return "{0}/{1} - {2} : {3}m".format(self.distance_cat, self.order, self.stage.name, self.distance)

