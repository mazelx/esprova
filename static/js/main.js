var map;
var markers = [];

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

    // On Firefox (others?), a refresh would not display markers
    google.maps.event.addListenerOnce(map, 'idle', function() {
        getRacesFromMapBounds(map.getBounds().toUrlValue());
    });


    google.maps.event.addListener(map, 'idle', function() {
        if ($('#follow_map_bounds').prop('checked')) {
            getRacesFromMapBounds(map.getBounds().toUrlValue())
        }
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
            refreshRacesOnSidebar(response.html);
            refreshRacesOnMap(response.races)
        },
    });
}

function refreshRacesOnSidebar(races_html) {
    $("#racelist").html(races_html);
}

function refreshRacesOnMap(races) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
    $.each(races, function(i, race) {
        var latlng = new google.maps.LatLng(race.lat, race.lng);
        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            id: race.pk
        });
        markers.push(marker);
    });

}
