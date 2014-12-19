from datetime import datetime
from core.models import Sport, DistanceCategory, Race, Contact, Event, Location


def quickCreate(name, sport, distance, city, date):
    """ example :
    quickCreate(name="Triathlon de Montélimar", sport="Triathlon", distance="XS", city="Montélimar", date="25/06/2015")
    """
    s = Sport
    try:
        s = Sport.objects.get(name=sport)
    except Sport.DoesNotExist:
        print("Sport {0} does not exist".format(sport))

    dc = DistanceCategory
    try:
        dc = DistanceCategory.objects.get(name=distance)
    except DistanceCategory.DoesNotExist:
        print("Distance {0} does not exist".format(distance))

    e = Event(name=name, edition=1)
    e.save()

    c = Contact(name="Pierre Dupont")
    c.save()

    l = Location(country=Location.objects.all()[0].country, city=city)
    l.save()

    r = Race(
        sport=s,
        event=e,
        date=datetime.strptime(date, "%d/%m/%Y"),
        distance_cat=dc,
        price=40,
        contact=c,
        location=l,
        )
    r.save()

    return r
