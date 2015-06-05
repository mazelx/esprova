
var mapOptions;
var lat, lng;

google.maps.event.addDomListener(window, 'load', createMap);

$( document ).ready(function() {

    lat = parseFloat( $("#race-location").data("lat"));
    lng = parseFloat( $("#race-location").data("lng"));

    mapOptions = {
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        center: {
            lat: lat,
            lng: lng
        },
        zoom: 10,
        maxZoom: 15,
        // minZoom:5,   
        panControl: false,
        zoomControl: true,
        streetViewControl: false
    };

    addListRaceDisplayMap(); 

});


function addListRaceDisplayMap() {
    $("#link-display-map").click(function (event) {
        if( $( "#address-map" ).is(":hidden")) {
            $( "#address-map" ).show("fast", function () {
               map.set({styles: map_styles});
               google.maps.event.trigger(map, 'resize');
               map.setCenter({lat:lat, lng:lng});
            });            
        } else {
            $( "#address-map" ).hide("fast");
        }

    });
}

function createMap(){
    if (typeof map_styles === 'undefined'){
        map_styles = [];
    }
        map = new google.maps.Map(document.getElementById('address-map'),
            mapOptions);
        map.setOptions({styles: map_styles});

        var marker = new google.maps.Marker({
            position: {lat:lat, lng:lng} ,
            map: map,
            zIndex : 1,
        });
}   

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function addToPlanning(pk) {
      $.ajax({
        url: '/api/planning/add',
        type: 'POST',
        data: { race: pk },
        success: function(response, statut) {
            window.location.replace("/planning/")

        },
    });
}