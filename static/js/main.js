var map;
var markers =[];

google.maps.event.addDomListener(window, 'load', initialize);

function initialize() {
    var mapOptions = {
        center: {
            lat: 44.301683,
            lng: 4.5656561
        },
        zoom: 8,
        panControl: false,
        streetViewControl: false
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);

    google.maps.event.addListener(map, 'idle', function() {
        getRacesFromMapBounds(map.getBounds().toUrlValue())
    });

}

function addRaceMarker(_name, _ltlng) {
    var myLatlng = new google.maps.LatLng(_latlng);
    var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        title: _name
    });
}

function getRacesFromMapBounds(mapbounds) {
    // returns a HTML of races results
    boundsarray = mapbounds.split(',')
    $.ajax({
        url: '/search/?',
        type: 'GET', // Le type de la requête HTTP, ici devenu POST
        data: 'lat_lo=' + boundsarray[0] + '&lng_lo=' + boundsarray[1] + '&lat_hi=' + boundsarray[2] + '&lng_hi=' + boundsarray[3],
        dataType: 'json',
        success: function(response, statut) {
            fillRacesOnResults(response.html);
            setRacesOnMap(response.races)
        },
    });
}

function fillRacesOnResults(html_races) {
    $("#racelist").html(html_races);
}

function setRacesOnMap(races) {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(null);
    }
    markers = [];
    $.each(races, function(i,race) {
      var latlng = new google.maps.LatLng(race.lat, race.lng);
      var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        id: race.pk
      });
      markers.push(marker);
    });

}
