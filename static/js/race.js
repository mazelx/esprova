
var mapOptions;

google.maps.event.addDomListener(window, 'load', createMap);

$( document ).ready(function() {
    mapOptions = {
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        center: {
            lat: $("#race-location").data("lat"),
            lng: $("#race-location").data("lng")
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

function validateRace(pk) {
    // TODO : Propose a cancel link and delay for few seconds
    $.ajax({
        url: '/ajx/validate/'+pk,
        type: 'PUT',
        success: function(response, statut) {
            alert('validé')
        },
    });
}
function deleteRace(pk) {
    // TODO : Propose a cancel link and delay for few seconds
     $.ajax({
        url: '/ajx/delete/'+pk,
        type: 'DELETE',
        success: function(response, statut) {
            alert('supprimé')
            window.location.replace("/list")
        },
    });
}