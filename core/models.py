from django.db import models
from django.core.exceptions import ValidationError
from core.utils import geocode
from django_countries.fields import CountryField
from haystack.utils.geo import Point
from django.db.models import Min, Max


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

    def __str__(self):
        return "{0}, {1}, {2} ({3}, {4})".format(self.postal_code, self.locality, self.country, self.lat, self.lng)


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
        return "{0}/{1} : {2}".format(self.sport, self.default_order, self.name)


class Event(models.Model):
    name = models.CharField(max_length=150)
    edition = models.PositiveSmallIntegerField()
    website = models.URLField(blank=True, null=True)

    # def __init__(self):
    #     self. distance_category_set = self._get_event_distance_category()

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name

    def get_start_date(self):
        return self.race_set.all().aggregate(Min('date'))['date__min']

    def get_end_date(self):
        return self.race_set.all().aggregate(Max('date'))['date__max']

    def get_distance_cat_set(self):
        distance_cat_set = []
        for r in self.race_set.all().order_by('distance_cat__order'):
            distance_cat_set.append(r.distance_cat)
        return distance_cat_set

    def get_race_set(self):
        race_set = []
        for r in self.race_set.all().order_by('distance_cat__order'):
            race_set.append(r)
        return race_set


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
        return "{0} - {1} ({2})".format(self.sport.name, self.name, self.long_name)

    def natural_key(self):
        return (self.sport, self.name)

    class Meta:
        verbose_name = "Distance Category"
        verbose_name_plural = "Distance Categories"


class Race(models.Model):
    sport = models.ForeignKey(Sport)
    event = models.ForeignKey(Event)
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField()
    distance_cat = models.ForeignKey(DistanceCategory)
    price = models.PositiveIntegerField(blank=True, null=True)
    federation = models.ForeignKey(Federation, blank=True, null=True)
    label = models.ForeignKey(Label, blank=True, null=True)
    contact = models.ForeignKey(Contact)
    description = models.TextField(blank=True, null=True)
    location = models.OneToOneField(Location)

    def save(self, *args, **kwargs):
        super(Race, self).save(*args, **kwargs)
        self.init_distances_from_default()
        super(Race, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.event, self.sport, self.distance_cat)

    def __str__(self):
        return "{0} - {1}".format(self.event.name, self.distance_cat.name)

    def init_distances_from_default(self):
        """ Initialize the distances from default distances for this category on race creation """
        if not self.stagedistancespecific_set.all():
            for rs in StageDistanceDefault.objects.filter(distance_cat=self.distance_cat):
                rs = StageDistanceSpecific(race=self, order=rs.order, stage=rs.stage, distance=rs.distance)
                rs.save()

    def get_point(self):
        return Point(float(self.location.lng), float(self.location.lat))


class StageDistance(models.Model):
    order = models.PositiveSmallIntegerField()
    stage = models.ForeignKey(SportStage)
    distance = models.PositiveIntegerField()

    class Meta:
        abstract = True


class StageDistanceSpecific(StageDistance):
    race = models.ForeignKey(Race)

    class Meta:
        verbose_name = "Stage distance (for a race)"
        verbose_name_plural = "Stages distance (for a race)"
        ordering = ['pk']

    def natural_key(self):
        return (self.race, self.order)

    def clean(self):
        if (not self.race.sport.combinedSport) & (self.race.stagedistancespecific_set.all().count() > 1):
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

