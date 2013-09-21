import requests


from django.conf import settings

def lookup_postcode(postcode):
    """
    Looks up a postcode on MapIt and returns the entire response
    """
    lookup_url = "{}postcode/{}.json".format(settings.MAPIT_URL, postcode.replace(" ", ""))
    return requests.get(lookup_url).json()
    

def geocode_postcode(postcode):
    """
    Geocode a postcode to a WGS84 lat/lon using mySociety MapIt
    """
    content = lookup_postcode(postcode)
    return {
        'lat': content['wgs84_lat'],
        'lon': content['wgs84_lon'],
    }
