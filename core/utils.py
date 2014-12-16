from urllib import request, parse
import simplejson
from django.utils.encoding import smart_str


def geocode(location):
    location = parse.quote_plus(smart_str(location))
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false'.format(location)
    response = request.urlopen(url).read()
    result = simplejson.loads(response)

    if result['status'] == 'OK':
        lat = str(result['results'][0]['geometry']['location']['lat'])
        lng = str(result['results'][0]['geometry']['location']['lng'])
        return '{0},{1}'.format(lat, lng)
    else:
        return ''
