var map;

google.maps.event.addDomListener(window, 'load', initialize);

$(document).ready(function(){
    $('#ajax1').click(function(){
        getRacesFromMapBounds(0,0,1,1);
    });
});

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

    google.maps.event.addListener(map, 'bounds_changed', function() {
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
                    },
                });
        }

        function fillRacesOnResults(results) {
            $("#racelist").html(results);
        }

        function setRacesOnMap(results) {
            // var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
            var myLatlng = new google.maps.LatLng(44.301683, 4.5656561);

            // To add the marker to the map, use the 'map' property
            var marker = new google.maps.Marker({
                position: myLatlng,
                map: map,
                title: "Hello World!"
            });
        }
