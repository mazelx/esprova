var map;
var markers = {};
var selected_event_id;
var highestZIndex = 10;

var defaultMarkerIcon = {
        url: 'https://esprova-static.s3.amazonaws.com/images/marker_icon.svg',
        size: new google.maps.Size(28,42),
};

var selectedMarkerIcon = {
        url: 'https://esprova-static.s3.amazonaws.com/images/marker_icon_selected.svg',
        size: new google.maps.Size(28,42),
};

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


// ----------------------
// Document initialization
// ----------------------

google.maps.event.addDomListener(window, 'load', initialize);

function initialize() {
    var mapOptions = {
        center: {
            lat: 46.9,
            lng: 2.6
        },
        zoom: 6,
        maxZoom: 15,
        minZoom:5,
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


    // Add custom event listeners
    addListMapMoves();
    addListQuickSearch();
    addListSearch();
    addListAlertMessages();
    addListResultClick();

    createDatePickerComponent();

}

// ----------------------
// LISTENERS
// ----------------------

// LISTENER : retrieve races when map moves
function addListMapMoves(){
    google.maps.event.addListener(map, 'idle', function() {
        // Do not refresh races if the map is not visible or "follow map bounds" not checked
        if ($("#follow_map_bounds").is(':checked') && $(".mapbox").is(":visible") ) {
            getRacesFromMapBounds(map.getBounds().toUrlValue());
        }
    });
}

function addListMarkerClick(marker){
    google.maps.event.addListener(marker, 'click', function () {
        selectEvent(marker.get("id"));
    });
}

function addListResultClick(){
    $(".event-result").click(function( event ) {
        selectEvent(event.currentTarget.id.replace("event_",""));
    });
}

// LISTENER : retrieve races from quick search
function addListQuickSearch(){ 
    $( "#race_quicksearch_form" ).submit(function( event ) {
        event.preventDefault();
        getRacesFromSearch();
    });
}
    
// LISTENER : retrieve races from basic search
function addListSearch(){
    $( "#race_search_form" ).change(function( event ) {
        event.preventDefault();
        getRacesFromSearch();
    });
}

// En CSS ??
function addListAlertMessages(){
    window.setTimeout(function() {
            $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove(); 
      });
    }, 3000);
}

// initialize bootstrap-datepicker component
function createDatePickerComponent() {
    $('.input-daterange').datepicker({
        format: "yyyy-mm-dd",
        language: "fr",
        autoclose: true,
        clearBtn: true,
        todayHighlight: true,
        todayHighlight: true
    });
}

// ----------------------
// Ajax Handling
// ----------------------

function getRacesFromSearch(data){
     $.ajax({
        url: '/search/?',
        type: 'GET',
        data: $( "#race_search_form" ).serialize() +
              '&q=' + $("#search_expr").val() ,
        dataType: 'json',
        success: function(response, statut) {
            refreshRacesOnSidebar(response.html);
            refreshRacesOnMap(response.races);
            setMapBoundsFromResults();
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


// ----------------------
// Display results
// ----------------------
function refreshRacesOnSidebar(races_html) {
    // replace HTML by ajax provided code
    $("#racelist").html(races_html);

    addListResultClick();
    selectEvent(selected_event_id);
}
        
function refreshRacesOnMap(races) {
    for(var key in markers){
        markers[key].setMap(null);
    }

    // reinitialize markers associative array
    markers = {};

    $.each(races, function(i, race) {
        var latlng = new google.maps.LatLng(race.lat, race.lng);
        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            id: race.id,
            icon : defaultMarkerIcon,
            zIndex : 1
        });
        markers[race.id]=marker;
        
        // Listener : select event on marker click
        addListMarkerClick(marker);
    });

    if (!(selected_event_id in markers)) {
        selected_event_id = null;
    }

    selectEvent(selected_event_id);
}


// ----------------------
// Dynamic display
// ----------------------
function selectEvent(event_id){
    // unselect old event
    if($("#event_" + selected_event_id).length){
        $("#event_" + selected_event_id).removeClass("panel-primary");
        $("#event_" + selected_event_id + "_races").removeClass("in");
        markers[selected_event_id].setIcon(defaultMarkerIcon);
    }

    // select new event
    selected_event_id = event_id;

    if($("#event_" + selected_event_id).length){
        $("#event_" + selected_event_id).addClass("panel-primary");
        $("#event_" + selected_event_id + "_races").addClass("in");
        
        // scroll sidebox to selected race with a 150px reserve (navbar + extra space)
        $(".sidebox").animate({
            scrollTop: $(".sidebox").scrollTop() + $("#event_" + selected_event_id).offset().top - 150
        }, 500);
        markers[selected_event_id].setIcon(selectedMarkerIcon);
        markers[selected_event_id].setZIndex(highestZIndex+1)
        highestZIndex += 1;
    }
   
}


function setMapBoundsFromResults() {

    var bound = new google.maps.LatLngBounds();

    if(!($.isEmptyObject(markers))){
        for(var key in markers) {
            bound.extend(markers[key].getPosition());
        }

        map.fitBounds(bound);
    }

}
