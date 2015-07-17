from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey


class ComparableModelMixin(object):
    compare_excluded_keys = 'pk', 'id', '_state'

    def _compare(self, obj1, no_follow=False):
        d1, d2 = self.__dict__, obj1.__dict__
        old, new = {}, {}

        # remove _cache fields
        fields = {field: value for (field, value) in d1.items() if not field[-6:] == '_cache'}

        for k, v in fields.items():
            # pass if excluded
            if k in self.compare_excluded_keys:
                continue

            # if field is a relationship, try to call the _compare() method
            # the field name is followed by 'id' thus need concat (ex. contact_id -> contact)
            instance_field = ''
            rel_field_name = k[:-3]
            if not no_follow:
                try:
                    instance_field = self._meta.get_field_by_name(rel_field_name)[0]
                except:
                    pass

            if isinstance(instance_field, ForeignKey):
                try:
                    instance_rel = getattr(self, rel_field_name)
                    old_rel = getattr(obj1, rel_field_name)
                    field_old, field_new = instance_rel._compare(old_rel)
                    if field_old or field_new:
                        old.update({rel_field_name: field_old})
                        new.update({rel_field_name: field_new})
                    pass
                except:
                    pass
            else:
                try:
                    if v != d2[k]:
                        old.update({k: v})
                        new.update({k: d2[k]})
                except KeyError:
                    old.update({k: v})

        return old, new


class Sport(ComparableModelMixin, models.Model):
    """
        Represent a sport : "Triathlon" / "Duathlon" / "Trail" ...
        Sports that contains multiple stages are defined with combinedSport = true

    """
    name = models.CharField(max_length=100)
    combinedSport = models.BooleanField(default=False)
    hidden = models.BooleanField(default=True)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name

    @property
    def distances(self):
        distances = []
        for dc in self.distancecategory_set.all().order_by('order'):
            distance = {}
            distance['order'] = dc.order
            distance['name'] = dc.name
            distance['long_name'] = dc.long_name
            distance['stages'] = []
            for sd in dc.stagedistancedefault_set.all().order_by('order'):
                stage = {}
                stage['order'] = sd.order
                stage['name'] = sd.stage.name
                stage['distance'] = sd.get_formatted_distance
                distance['stages'].append(stage)

            distances.append(distance)

        return distances


class SportStage(models.Model):
    """
        Represent a sport stage (ie. Run / Swim) for a sport.
        Only combined sport may have multiple stages

    """
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


class Season(models.Model):
    """
        Represent a season (year). As sport are not played the whole year in most place in the world,
        it often not refers to a calendar year
    """

    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name)


class Federation(models.Model):
    """
        Represent a sport Federation

    """
    name = models.CharField(max_length=150,)
    sport = models.ManyToManyField(Sport)

    def natural_key(self):
        return (self.name, self.sport)

    def __str__(self):
        return self.name


class DistanceCategory(ComparableModelMixin, models.Model):
    """
        Represent a distance category (ie: XS, S, M, L, XL)

    """
    sport = models.ForeignKey(Sport)
    name = models.CharField(max_length=2)
    long_name = models.CharField(max_length=20, blank=True, null=True)
    order = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Distance Category"
        verbose_name_plural = "Distance Categories"

    def __str__(self):
        return "{0} ({1})".format(self.name, self.sport)

    def natural_key(self):
        return (self.sport, self.name)

    def get_formatted_name(self):
        var = "{0} {1}".format(self.sport.name, self.name)
        if self.long_name:
            var += " ({0}) ".format(self.long_name)
        return var


def get_limit_for_distancecat():
    return {'sport': Sport.objects.get(name='Triathlon').id}


class StageDistance(models.Model):
    """
        Abstract model that contains stage distance structure and to be inherited by either
        the stage distance specific (race) or stage distance default (category)

    """
    order = models.PositiveSmallIntegerField()
    stage = models.ForeignKey(SportStage)
    # TODO : use geopy.D for units conversion
    distance = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def natural_key(self):
        return (self.stage,)

    def get_formatted_distance(self):
        """
            Return a distance string formatted in meters if distance < 1km, and in km if above
        """
        n = self.distance + 0.0
        if n > 1000:
            return '{0} km'.format(str(n/1000).rstrip('0').rstrip('.'))
        return '{:.0f} m'.format(n)


class StageDistanceDefault(StageDistance):
    """
        Distance for a stage (in meters) to be defined in category distance
    """
    distance_cat = models.ForeignKey(DistanceCategory)

    class Meta:
        verbose_name = "Stage distance (default)"
        verbose_name_plural = "Stages distance (default)"
        ordering = ['pk']

    def clean(self):
        if (not self.distance_cat.sport.combinedSport) & (self.distance_cat.stagedistancedefault_set.all().count() > 1):
            raise ValidationError('Only combined sport should be able to have multiple stages')

    def natural_key(self):
        return (self.order,) + self.race.natural_key()

    def __str__(self):
        return "{0}/{1} - {2} : {3}m".format(self.distance_cat, self.order, self.stage.name, self.distance)
