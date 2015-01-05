var map;
var markers = [];
var refresh_on_move = true;
    var styles =[
    {
        "featureType": "administrative",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#b1b1b1"
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "simplified"
            },
            {
                "color": "#d3d3d3"
            }
        ]
    },
    {
        "featureType": "administrative.country",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#a9b4c1"
            },
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative.country",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "color": "#94a1b8"
            }
        ]
    },
    {
        "featureType": "administrative.country",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#708991"
            },
            {
                "visibility": "on"
            },
            {
                "weight": "1.00"
            }
        ]
    },
    {
        "featureType": "administrative.country",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative.country",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative.locality",
        "elementType": "all",
        "stylers": [
            {
                "weight": "4.68"
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "all",
        "stylers": [
            {
                "color": "#f2f2f2"
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "featureType": "landscape.natural.terrain",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "color": "#b8c5bb"
            }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "all",
        "stylers": [
            {
                "saturation": -100
            },
            {
                "lightness": 45
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#b1b1b1"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#ff0000"
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "transit",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "all",
        "stylers": [
            {
                "color": "#30f557"
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#7ae8f9"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#65868d"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    }
];

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

    // initialize the map
    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);

    map.setOptions({styles: styles});

    // On Firefox (others?), a refresh would not display markers
    google.maps.event.addListenerOnce(map, 'idle', function() {
        getRacesFromMapBounds(map.getBounds().toUrlValue());
    });

    // LISTENER : retrieve races when map moves
    google.maps.event.addListener(map, 'idle', function() {
        if (refresh_on_move) {
            getRacesFromMapBounds(map.getBounds().toUrlValue());
            refresh_on_move = true
        }
    });

    // LISTENER : enable / disable refresh on map moves
    $('#follow_map_bounds').change(function( ) {
        refresh_on_move = $(this).is(':checked');
    });

    // LISTENER : retrieve races from quick search 
    $( "#race_quicksearch_form" ).submit(function( event ) {
        event.preventDefault();
        getRacesFromSearch();
    });

    // LISTENER : retrieve races from basic search
    $( "#race_search_form" ).submit(function( event ) {
        event.preventDefault();
        getRacesFromSearch();
    });

}

function getRacesFromSearch(data){
     $.ajax({
        url: '/search/?',
        type: 'GET',
        data: '&' + $( "#race_search_form" ).serialize() +
              '&q=' + $("#search_expr").val() ,
        dataType: 'json',
        success: function(response, statut) {
            refreshRacesOnSidebar(response.html);
            refreshRacesOnMap(response.races);
            ajdust_bounds_from_markers();
        },
    });
}

function getRacesFromMapBounds(mapbounds) {
    // returns a HTML of races results
    boundsarray = mapbounds.split(',')
    $.ajax({
        url: '/search/?',
        type: 'GET', 
        data: 'lat_lo=' + boundsarray[0] + 
              '&lng_lo=' + boundsarray[1] + 
              '&lat_hi=' + boundsarray[2] + 
              '&lng_hi=' + boundsarray[3] +
              '&' + $( "#race_search_form" ).serialize() +
              '&q=' + $("#search_expr").val() ,
        dataType: 'json',
        success: function(response, statut) {
            refreshRacesOnSidebar(response.html);
            refreshRacesOnMap(response.races)
        },
    });
}

function refreshRacesOnSidebar(races_html) {
    if(races_html == "") {
        // rendering should be handled by django 
        races_html = 
        "<div class='alert alert-danger' role='alert'>Nous n'avons pas trouvé de courses correspondant à vos critères</div>";   
    }
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

function ajdust_bounds_from_markers() {

    if(markers.length > 0) {
        var bound = new google.maps.LatLngBounds();
        
        for(var i in markers) {
            bound.extend(markers[i].getPosition());
        }

        map.fitBounds(bound);
    }
}
