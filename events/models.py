from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Min, Max
from collections import OrderedDict
import copy
import datetime

from random import randint

from core.models import ComparableModelMixin
from core.models import Sport, DistanceCategory, Federation, StageDistance, StageDistanceDefault

from django_countries.fields import CountryField

from django.template.defaultfilters import slugify

from geopy.geocoders import GoogleV3

from haystack.query import SearchQuerySet
from haystack.utils.geo import D, Point


class Location(ComparableModelMixin, models.Model):
    """
        Represent a race location, built upon the Google maps V3 data structure as
        it is supposed to be geocoded by Google maps.
        more here : https://developers.google.com/maps/documentation/javascript/geocoding

        Note that a location may be used by multiple races

    """
    compare_excluded_keys = 'pk', 'id', '_state', 'lat', 'lng'

    street_number = models.CharField(max_length=10, blank=True, null=True, verbose_name='Numéro')
    route = models.CharField(max_length=200, blank=True, null=True, verbose_name='Voie')

    # city/town
    locality = models.CharField(max_length=100, verbose_name='Ville')

    # region / state
    administrative_area_level_1 = models.CharField(max_length=100, verbose_name='Région')
    administrative_area_level_1_short_name = models.CharField(max_length=100)

    # departement
    administrative_area_level_2 = models.CharField(max_length=100, verbose_name='Département')
    administrative_area_level_2_short_name = models.CharField(max_length=100)

    postal_code = models.CharField(max_length=16, verbose_name='Code Postal')
    country = CountryField(verbose_name='Pays')

    lat = models.DecimalField(max_digits=8, decimal_places=5)
    lng = models.DecimalField(max_digits=8, decimal_places=5)

    extra_info = models.TextField(null=True, blank=True, verbose_name='Infos complémentaires')

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

    def natural_key(self):
        return (self.lat, self.lng)

    def geocode(self, raw_address='', postal_code='', country=''):
        raw_address = raw_address or '{0} {1}'.format(self.street_number or '', self.route or '')
        postal_code = postal_code or self.postal_code
        country = country or self.country.code
        return self.geocode_raw_address(raw_address=raw_address,
                                        postal_code=postal_code,
                                        country=country)

    def geocode_raw_address(self, raw_address='', postal_code='', country='FR'):
        """
            Geocode using the Google maps V3 geocoder

        """
        g = GoogleV3(timeout=3)
        loc = g.geocode(query=raw_address, components={'postal_code': postal_code, 'country': country})
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
            return loc.raw
        else:
            return None

    def get_point(self):
        return Point(float(self.lng), float(self.lat))

    def get_address_lines(self):
        result = []
        tmp_addr = ""
        # First line : [Street number,] Route
        tmp_addr = self.getFormattedStreet()
        if tmp_addr:
            result.append(tmp_addr)

        # Second line : Locality [(area2)]
        result.append(self.getFormattedLocality)

        # Third line : [Area 1]
        result.append(self.getFormattedRegion)

        # Fourth line : Country
        result.append(self.getFormattedCountry)

        return result

    def getFormattedStreet(self):
        addr = ""
        # First line : [Street number,] Route
        if self.street_number:
            addr = self.street_number + ", "
        if self.route:
            addr += self.route
        return addr

    def getFormattedLocality(self):
        loc = self.locality
        if self.administrative_area_level_2_short_name:
            loc += " ({0})".format(self.administrative_area_level_2_short_name)
        return loc

    def getFormattedRegion(self):
        if self.administrative_area_level_1:
            return self.administrative_area_level_1

    def getFormattedCountry(self):
        return str(self.country.name)


class Organizer(ComparableModelMixin, models.Model):
    """
        Represent the event organizer
    """
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_organizer_popup', args=(self.pk,))

    def get_absolute_update_url(self):
        url = reverse('add_another_organizer_update', args=(self.pk,))
        url = '%s?_popup=1" target="_blank" onclick="return showAddAnotherPopup(this);' % url
        return url



class Event(ComparableModelMixin, models.Model):
    """
        Represent an edition of an event
        Races instances are direcly tied to an event distance.
    """
    # for _compare() method of ComparableModelMixin
    compare_excluded_keys = 'pk', 'id', '_state', 'event_mod_source', 'validated', 'event_mod_source'

    name = models.CharField(max_length=150, verbose_name="Nom de l'événement")
    website = models.URLField(blank=True, null=True, verbose_name='Site internet')
    organizer = models.ForeignKey(Organizer, blank=True, null=True, verbose_name='Organisateur')
    # event_ref = models.ForeignKey(EventReference)
    edition = models.PositiveSmallIntegerField(verbose_name="Numéro d'édition")
    event_prev_edition = models.OneToOneField("Event", related_name='event_next_edition', blank=True, null=True)
    validated = models.BooleanField(default=False)
    event_mod_source = models.ForeignKey("Event", related_name='event_modified_set', blank=True, null=True)
    to_be_deleted = models.BooleanField(default=False)

    def natural_key(self):
        return self.name + self.edition

    def __str__(self):
        return "{0} - {1}".format(self.pk, self.name)

    def get_start_date(self):
        return self.races.all().aggregate(Min('date'))['date__min']

    def get_end_date(self):
        return self.races.all().aggregate(Max('date'))['date__max']

    def get_distance_cat_set(self, unique=False):
        distance_cat_set = []
        already_added = {}
        for r in self.races.all().order_by('distance_cat__order'):
            if r.distance_cat in already_added and unique is True:
                continue
            already_added[r.distance_cat] = 1
            distance_cat_set.append(r.distance_cat)
        return distance_cat_set

    def get_races(self):
        races = []
        for r in self.races.all().order_by('distance_cat__order'):
            races.append(r)
        return races

    def get_races_by_sports(self):
        races_list = {}
        for r in self.races.all().order_by('distance_cat__order'):
            races_for_sport = races_list.get(r.sport.name) or []
            races_for_sport.append(r)
            races_list.update({r.sport.name: races_for_sport})
        return OrderedDict(sorted(races_list.items(), key=lambda x: len(x[1]), reverse=True))

    def clone(self):
        try:
            race_list = []
            for r in self.get_races():

                # copy location
                l = r.location
                l.pk = None
                l.save()
                r.location = l

                # copy contact
                c = r.contact
                c.pk = None
                c.save()
                r.contact = c

                r.race_mod_source = r

                # copy race
                r.pk = None
                r.save()

                # save race in list
                race_list.append(r)

            e = copy.copy(self)

            # clone event into new event (no pk yet)
            e.pk = None
            e.validated = False
            e.save()

            for r in race_list:
                r.event = e
                r.save()

            e.event_mod_source = self
            e.save()

            return e

        except Exception as exception:
            print(exception)
            for r in race_list:
                r.location.delete()
                r.delete()
            if e.pk:
                e.delete()

    def get_nb_changes(self):
        if self.pk:
            return Event.objects.filter(event_mod_source=self.pk).count()

    def get_changed_event(self):
        if self.pk:
            return Event.objects.filter(event_mod_source=self.pk)

    def get_changes(self):
        if self.pk and self.event_mod_source:
            # Compare only event fields (not race fields)
            event_changes = self._compare(self.event_mod_source)
            races_changes = {}
            ref_races = [r.pk for r in self.event_mod_source.get_races()]

            for r in self.get_races():
                # race updated
                if r.race_mod_source:
                    changes = r._compare(r.race_mod_source)
                    if any(changes):
                        races_changes.update({'race_updated_{0}'.format(r.pk): changes})
                    ref_races.remove(r.race_mod_source.pk)
                # race added
                else:
                    races_changes.update({'race_added_{0}'.format(r.pk): ({}, None)})

            # race deleted
            for race_deleted_pk in ref_races:
                    races_changes.update({'race_deleted_{0}'.format(race_deleted_pk): (None, {})})

            return {'attributes': event_changes, 'races': races_changes}

    def validate(self):
        if self.pk and not self.validated:

            # create
            if not self.event_mod_source:
                self.validated = True
                return self.save()
            else:
                # update
                if not self.to_be_deleted:
                    data = self.__dict__.copy()

                    del data['id']
                    event_mod_source_id = data.pop('event_mod_source_id')
                    # remove _ keys
                    data = {k: v for k, v in data.items() if not k[:1] == '_'}
                    data['validated'] = True
                    try:
                        for r in self.get_races():
                            r.validate()
                        self.delete()
                        # update event
                        Event.objects.filter(id=event_mod_source_id).update(**data)
                        # remove all other modifications
                        Event.objects.filter(event_mod_source_id=event_mod_source_id).delete()

                    except Exception as e:
                        # if update fails, recreate the deleted object
                        data['validated'] = False
                        data['event_mod_source_id'] = event_mod_source_id
                        Event(**data).save()
                        print('update failed, object has been recreated:' + str(e))

                # delete
                else:
                    self.event_mod_source.delete()


class Contact(ComparableModelMixin, models.Model):
    """
        Represent a race contact

    """
    name = models.CharField(max_length=100, verbose_name='Contact')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True, verbose_name='Téléphone')

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name


class Label(models.Model):
    """
        Represent a race label

    """
    name = models.CharField(max_length=100, verbose_name='Nom')
    website = models.URLField(blank=True, null=True)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_label_popup', args=(self.pk,))


class Challenge(models.Model):
    """
        Represent a race challenge

    """
    name = models.CharField(max_length=100, verbose_name='Nom')
    website = models.URLField(blank=True, null=True)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_challenge_popup', args=(self.pk,))


class RaceManager(models.Manager):
    def random(self):
        sqs = SearchQuerySet()
        sqs = sqs.filter(validated=True,
                         date__gte=datetime.datetime.now(),
                         date__lte=datetime.datetime.now() + datetime.timedelta(days=90),
                         )
        last = sqs.count() - 1
        if last > 0:
            index = randint(0, last)
            return sqs[index].object


class Race(ComparableModelMixin, models.Model):
    """
        Represent a race, main model of the application

    """
    # manager
    objects = RaceManager()

    compare_excluded_keys = 'pk', 'id', '_state', 'event_id', 'slug', 'created_date', 'created_by', 'modified_date'

    slug = models.SlugField(max_length=100, blank=True, null=True)
    sport = models.ForeignKey(Sport, limit_choices_to={'hidden': False})
    event = models.ForeignKey(Event, related_name='races')
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(verbose_name='Date')
    time = models.TimeField(blank=True, null=True, verbose_name='Heure')
    distance_cat = models.ForeignKey(DistanceCategory,
                                     verbose_name="Distance")
    price = models.PositiveIntegerField(blank=True, null=True)
    federation = models.ForeignKey(Federation, blank=True, null=True, related_name='races')
    label = models.ForeignKey(Label, blank=True, null=True, related_name='races')
    challenge = models.ForeignKey(Challenge, blank=True, null=True, related_name='races')
    contact = models.OneToOneField(Contact)
    description = models.TextField(blank=True, null=True, verbose_name='Description de la course')
    location = models.OneToOneField(Location)
    relay = models.BooleanField(default=False, verbose_name='Relais')
    timetrial = models.BooleanField(default=False, verbose_name='Contre-la-montre')
    race_mod_source = models.ForeignKey("Race", related_name='race_modified_set', blank=True, null=True)
    to_be_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    import_source = models.CharField(max_length=100, blank=True, null=True)
    import_source_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{0} - {1} {2} {3} {4}".format(self.event.name,
                                              self.sport.name,
                                              self.distance_cat.name,
                                              (self.relay and 'Relais') or '',
                                              (self.timetrial and 'CLM') or '')

    def natural_key(self):
        return (self.date, self.time, self.distance_cat) + self.event
    natural_key.dependencies = ['events.Event']

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('view_race', args=[self.slug, str(self.id)])

    def get_event_races_same_sport(self):
        # races = []
        # for r in self.event.races.filter(sport=self.sport).order_by('distance_cat__order'):
        #     races.append(r)
        # return races
        return self.event.races.filter(sport=self.sport).order_by('distance_cat__order')

    def save(self, *args, **kwargs):
        """
            Define the slug and initial stage distances when the instance is about to be created in the db

        """
        if self.pk is None:
            seq = (self.event.name, self.distance_cat.name)
            self.slug = slugify("-".join(seq))
            super(Race, self).save(*args, **kwargs)

            self.init_distances_from_default()

            # The instance has just been inserted thus do not insert again even if forced on save() call
            if kwargs.get('force_insert', None):
                kwargs.pop('force_insert')
        super(Race, self).save(force_update=True, *args, **kwargs)

    def init_distances_from_default(self):
        """
            Initialize the distances from default distances for this category on race creation

        """
        if not self.distances.all():
            for rs in StageDistanceDefault.objects.filter(distance_cat=self.distance_cat):
                rs = StageDistanceSpecific(race=self, order=rs.order, stage=rs.stage, distance=rs.distance)
                rs.save()

    def get_potential_doubles(self):
        """
            Returns an instance list of potential double for this race, based on :
            - distance (<10km)
            - date (+- 1 day)
            - samed distance category
        """
        sqs = SearchQuerySet()

        pk = self.pk
        if pk:
            sqs = sqs.exclude(django_id=pk)

        sqs = sqs.dwithin('location', self.location.get_point(), D(km=10))
        sqs = sqs.filter(date__gte=self.date + datetime.timedelta(days=-1),
                         date__lte=self.date + datetime.timedelta(days=1),
                         distance_cat=self.distance_cat.name,
                         sport__exact=self.sport.name,
                         # event_title=self.event.name
                         )

        # return race objects instead of haystack searchresul
        return [sr.object for sr in sqs]

    def validate(self):
        if self.pk:
            # create
            if not self.race_mod_source:
                self.event = self.event.event_mod_source
                self.save()

            else:
                if not self.to_be_deleted:
                    # update
                    data = self.__dict__.copy()
                    # remove _ keys
                    data = {k: v for k, v in data.items() if not k[:1] == '_'}
                    del data['id']
                    race_mod_source_id = data.pop('race_mod_source_id')
                    data['event_id'] = self.event.event_mod_source.pk
                    self.delete()
                    try:
                        Race.objects.filter(id=race_mod_source_id).update(**data)
                    except Exception as e:
                        # if update fails, recreate the deleted object
                        Race(**data)
                        raise e
                else:
                    if self.race_mod_source:
                        self.race_mod_source.delete()
                    self.delete()

    def get_distance_cat_str(self):
        return "{0} {1}".format(self.distance_cat.name,
                                'Relais' if self.relay else '' + 'CLM' if self.timetrial else '')

    def get_distance_cat_long_str(self):
        return "{0} {1}".format(self.distance_cat.long_name,
                                'Relais' if self.relay else '' + 'CLM' if self.timetrial else '')

# @receiver(post_delete, sender=Race)
# def post_delete_race(sender, instance, *args, **kwargs):
#     try:
#         instance.contact.delete()
#     except ObjectDoesNotExist:
#         pass

#     try:
#         instance.location.delete()
#     except ObjectDoesNotExist:
#         pass


class StageDistanceSpecific(StageDistance):
    """
        Distance for a stage (in meters) to be defined in races
    """
    race = models.ForeignKey(Race, related_name='distances')

    class Meta:
        verbose_name = "Stage distance (for a race)"
        verbose_name_plural = "Stages distance (for a race)"
        ordering = ['pk']

    def natural_key(self):
        return (self.order,) + self.race.natural_key()
    natural_key.dependencies = ['events.Race']

    def clean(self):
        if (not self.race.sport.combinedSport) & (self.race.distances.all().count() > 1):
            raise ValidationError('Only combined sport should be able to have multiple stages')

    def __str__(self):
        return "{0}/{1} - {2} : {3}m".format(self.race, self.order, self.stage.name, self.distance)

