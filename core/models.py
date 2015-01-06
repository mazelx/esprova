from django.db import models
from django.core.exceptions import ValidationError
from core.utils import geocode
from django_countries.fields import CountryField
from haystack.utils.geo import Point


class Sport(models.Model):
    name = models.CharField(max_length=100)
    combinedSport = models.BooleanField(default=False)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name


class Location(models.Model):
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=16, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField()
    lat = models.DecimalField(max_digits=8, decimal_places=5, blank=True)
    lng = models.DecimalField(max_digits=8, decimal_places=5, blank=True)

    def __str__(self):
        return "{0}, {1}, {2} ({3}, {4})".format(self.address1, self.city, self.country, self.lat, self.lng)

    def save(self, *args, **kwargs):
        # Add + between fields with values:
        location = '+'.join(filter(None,
                                   (self.address1,
                                    self.address2,
                                    self.city,
                                    self.state,
                                    self.zipcode,
                                    self.country.code)))
        # Attempt to get latitude/longitude from Google Geocoder service v.3:
        geo_data = geocode(location)
        if (geo_data):
            self.lat = geo_data["lat"]
            self.lng = geo_data["lng"]
        else:
            raise Exception("Address cannot be found")

        super(Location, self).save(*args, **kwargs)


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

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name


class Federation(models.Model):
    name = models.CharField(max_length=150)
    sport = models.ManyToManyField(Sport)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)

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
    price = models.PositiveIntegerField()
    federation = models.ForeignKey(Federation, blank=True, null=True)
    label = models.ForeignKey(Label, blank=True, null=True)
    contact = models.ForeignKey(Contact)
    description = models.TextField(blank=True, null=True)
    location = models.OneToOneField(Location)

    def save(self, *args, **kwargs):
        super(Race, self).save(*args, **kwargs)
        self.initDistancesFromDefault()
        super(Race, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.event, self.sport, self.distance_cat)

    def __str__(self):
        return "{0} - {1}".format(self.event.name, self.distance_cat.name)

    def initDistancesFromDefault(self):
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


class EntryFee(models.Model):
    race = models.ForeignKey(Race)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    Price = models.DecimalField(max_digits=6, decimal_places=2)
