// SPAGHETTI v1.0
var map;
var mapbounds;
var last_query;
var markers = {};
var selected_event_id="";
var selected_sport = "";

var highestZIndex = 10;

var markerIcons = {};
var primaryIcons = {};
var secondaryIcons = {};

var default_lat = 46.9;
var default_lng = 2.6;
var default_boundsarray = [40,-10,60,12];
var default_search_expr = "" 
var default_start_date = "2015-01-01"
var default_end_date = "2015-12-31"

// var static_url = 'https://esprova-static.s3.amazonaws.com/';
// var static_url = 'http://localhost:8000/static/'


// if the map style has not been provided
if (typeof map_styles === 'undefined'){
    map_styles = [];
}


// ----------------------
// JS Init
// ----------------------
if (typeof google !== "undefined") {
    google.maps.event.addDomListener(window, 'load', initialize);
}


function initialize() {
    primaryIcons['default']= {
        url: static_url + 'images/primary_marker_default.svg',
        size: new google.maps.Size(28,42),
    };

    primaryIcons['selected']={
        url: static_url + 'images/primary_marker_selected.svg',
        size: new google.maps.Size(28,42),
    };

    primaryIcons['hover']= {
        url: static_url + 'images/primary_marker_hover.svg',
        size: new google.maps.Size(28,42),
    };

    secondaryIcons['default']= {
        // url: static_url + 'images/secondary_marker_default.svg',
        url: static_url + 'images/marker_default.png',
        // size: new google.maps.Size(9,9),
        scaledSize: new google.maps.Size(10,10),
        anchor: new google.maps.Point(4,4),
    };

    secondaryIcons['selected']={
        url: static_url + 'images/marker_selected.png',
        // size: new google.maps.Size(26,26),
        scaledSize: new google.maps.Size(14,14),
        anchor: new google.maps.Point(7,7),
    };

    secondaryIcons['hover']= {
        url: static_url + 'images/marker_hover.png',
        // size: new google.maps.Size(26,26),
        scaledSize: new google.maps.Size(10,10),
        anchor: new google.maps.Point(4,4),   
    };

    markerIcons["primary"]=primaryIcons;
    markerIcons["secondary"]=secondaryIcons;

    var mapOptions = {
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        center: {
            lat: default_lat ,
            lng: default_lng
        },
        zoom: 6,
        maxZoom: 15,
        // minZoom:5,   
        panControl: false,
        zoomControl: false,
        streetViewControl: false
    };

    if($('#map-canvas').length ==! 0){

        // initialize the map
        map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);

        map.setOptions({styles: map_styles});

        // If map is not displayed (for mobile access)
        // Initialize results
        if($('#map-canvas').is(':hidden') == true) {    
            resetSearchForm();
        } else {
            // On Firefox (others?), a refresh would not display markers
            google.maps.event.addListenerOnce(map, 'idle', function () {
                 mapbounds = map.getBounds().toUrlValue();
                 // getRaces();
            });
        }
    } else {
        resetSearchForm();
    }

    // Initiliaze CRSF token
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    // Add custom event listeners
    addListMapMoves();
    // addListQuickSearch();
    addListSearch();
    addListAlertMessages();
    addListResultClick();
    addListResetForm();
    addListSportSelection();
    // addListRaceDisplayMap();

    createDatePickerComponent();

    initializeMapZoomControl();
    initializeFromURL();
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



// ----------------------
// DOM Initialization 
// ----------------------


// initialize map zoom controls
function initializeMapZoomControl() {
    if (map !== undefined) {
        // Setup the click event listeners and zoom-in or out according to the clicked element
        $('#cd-zoom-in').click( function(event) {
            map.setZoom(map.getZoom()+1)
        });
        $('#cd-zoom-out').click( function(event) {
            map.setZoom(map.getZoom()-1)
        });
    }
}


function initializeSportDistanceHelper(sport) {
     $.ajax({
        url: 'ajx/distance/' + sport,
        type: 'GET', 
        dataType: 'text'
        })
        .done(function(response, status) {
            $('#sport-distances-helper').html(response);
        })
        .fail(function(response, status){
            $('#sport-distances-helper').html("");
        });
}

// initialize bootstrap-datepicker component
function createDatePickerComponent() {
    $('.datepicker').datepicker({
        format: "yyyy-mm-dd",
        language: "fr",
        autoclose: true,
        clearBtn: true,
        todayHighlight: true,
        todayBtn: "linked"
    });
}


function initializeFromURL(){

    // need to test whetheir sport exists trhough ajax
    _selected_sport = getParameterByName('sport');
    if (_selected_sport !== "" ) {
        saveSportSession(_selected_sport);
    }


    // set map to provided bounds
    lat_lo = getParameterByName('lat_lo');
    lat_hi = getParameterByName('lat_hi');
    lng_lo = getParameterByName('lng_lo');
    lng_hi = getParameterByName('lng_hi');

    if(lat_lo !== "" && lat_hi !== "" && lng_lo !== "" && lng_hi !== "") {
        sw = new google.maps.LatLng(parseFloat(lat_hi), parseFloat(lng_lo));
        ne = new google.maps.LatLng(parseFloat(lat_lo), parseFloat(lng_hi));
        bounds = new google.maps.LatLngBounds(sw, ne);
        if (getParameterByName('z') === "") {
            map.fitBounds(bounds);
        } else {
            map.setCenter(bounds.getCenter());
            map.setZoom(parseInt(getParameterByName('z')))
        }
        mapbounds = bounds.toUrlValue();
    }

    // set dates
    start_date = getParameterByName('start_date');
    end_date = getParameterByName('end_date');
    search_expr = getParameterByName('search_expr');

    if (start_date !== "") {
        $("#start_date").val(start_date);
    }
    if (end_date !== "") {
        $("#end_date").val(end_date);
    }
    if (search_expr !== "") {
        $("#search_expr").val(search_expr);
    }

    // set active
    active = getParameterByName('active')
    if (active !== "") {
        selected_event_id = parseInt(active);    
    } else {
        selected_event_id = ""
    }

    getRaces(false);    
}

// ----------------------
// LISTENERS
// ----------------------

function saveSportSession(sport){
       $.ajax({
        url: '/ajx/sport-session/',
        data: {sport: sport},
        type: 'POST',
        success: function(response, statut) {
            formatted_sport = sport.charAt(0).toUpperCase() + sport.slice(1);
            $('.sport-selected').html(formatted_sport);
            selected_sport = formatted_sport;
            getRaces();
            initializeSportDistanceHelper(sport);
        },
    });
}

function addListSportSelection(){
    // change sport
    $('.sport-selecter').on('change', function (event) { 
        event.preventDefault();
        saveSportSession(event.currentTarget.value);
   });
}

// LISTENER : retrieve races when map moves
function addListMapMoves(){
    if (map !== undefined) {
        google.maps.event.addListener(map, 'idle', function() {
            // Do not refresh races if the map is not visible or "follow map bounds" not checked
            if ($("#follow_map_bounds").is(':checked') && $(".mapbox").is(":visible") ) {
                mapbounds = map.getBounds().toUrlValue()
                getRaces();
            }
        });
    }
}

function addListMarkerClick(marker){
    if (map !== undefined) {
        google.maps.event.addListener(marker, 'click', function () {
            selectEvent(marker.get("id"));
            param_query = getParamQuery();
            pushState(param_query, false);
        });
    }
}

function addListResultClick(){
    $(".search-result").click(function( event ) {
        selectEvent(event.currentTarget.id.replace("event_",""));
        $(".search-result").removeClass("active");
        $(event.currentTarget).addClass("active");
        param_query = getParamQuery();
        pushState(param_query, false);
    });
}

// LISTENER : retrieve races from quick search
function addListQuickSearch(){ 
    $( "#search_expr_go" ).click(function( event ) {
        event.preventDefault();
        getRaces();
    });
}
    
// LISTENER : retrieve races from basic search
function addListSearch(){

    $("#race_search_form").on('change submit', function(event) {
        event.preventDefault();
        getRaces();
        selected_event_id = ""
    });
}


// function addListSearch() {
//     // $('#start_date').datepicker().on('hide', getRaces);
// }

function addListResetForm(){
     $( "#reset-search-form" ).click(function( event ) {
        resetSearchForm();
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

function addListHoverSideboxResult(){
    $(".search-result").hover(function() {
        highlightResult($(this)[0].id.replace("event_",""))
    }, function() {
        deHighlightResult($(this)[0].id.replace("event_",""))
    }
    );
}

function addListHoverMapResult(marker){
    if (map !== undefined) {
        google.maps.event.addListener(marker, 'mouseover', function() {
            highlightResult(marker.get("id"));
        });
        google.maps.event.addListener(marker, 'mouseout', function() {
            deHighlightResult(marker.get("id"));
        });
    }
}

// ----------------------
// Ajax Handling
// ----------------------

function getRaces(recordState) {
    recordState = (typeof recordState === "undefined") ? true : recordState;
    // returns a HTML of races results
    if (mapbounds !== undefined) {
        boundsarray = mapbounds.split(',')
        
        param_query = getParamQuery();

        if (param_query !== last_query) {
            ajaxLoad(param_query);
            if (recordState === true) {
                pushState(param_query);
                last_query = param_query
            }
        }
    } else if ($("#map-canvas").is(":hidden")) {
        param_query = getParamQuery();
         if (param_query !== last_query) {
            ajaxLoad(param_query);
            if (recordState === true) {
                pushState(param_query);
                last_query = param_query
            }
        }
    }
}

function ajaxLoad(params) {
    console.log("ajaxload: " + params)
    $("#racelist").html('<div class="spinner"><i class="fa fa-spinner fa-pulse"></i></div>');

    $.ajax({
        url: 'ajx/search/',
        type: 'GET', 
        data: params,
        dataType: 'json',
        timeout: 10000,
        })
        .done(function(response, status) {
            refreshRacesOnSidebar(response.html, response.count);
            refreshRacesOnMap(response.races);
        })
        .fail(function(response, status){
            $("#racelist").html(
                "<div class='alert alert-danger' role='alert'>Une erreur est survenue, " +
                "veuillez contacter <a href='mailto:contact@esprova.com?subject=[issue]:[ajaxLoad]'>" +
                "le support</a></div>");
        });
}


// ----------------------
// Display results
// ----------------------
function refreshRacesOnSidebar(raceshtml, count) {
    // replace HTML by ajax provided code
    $("#racelist").html(raceshtml);

    addListResultClick();
    addListHoverSideboxResult();
    selectEvent(selected_event_id);

    // if no result, try to find if the search expression is a location, and propose a link to search
    if (count === 0) {
        handleNoResult();
    }   

}
       
function handleNoResult(){
    selector = $('.try-location-search');
    address = selector.data('expr')

    // try to geocode expression
    geocoder = new google.maps.Geocoder();

    geocoder.geocode( { 'address': address, region: 'fr' }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            selector.removeClass('hidden');
            text = results[0].address_components[0].short_name + 
                ' (' + results[0].address_components[1].short_name + ')';

            selector.children('.location').children('a').text(text);

            selector.children('.location').click(function (event) {
                mapbounds = results[0].geometry.bounds;
                $('#search_expr').val('');
                map.fitBounds(mapbounds);
            });
        }
    });

    $('.no-result .cde-remove-keywords').click(function (event) {
        $("#search_expr").val('');
        getRaces();
    });

    $('.no-result .cde-full-year').click(function (event) {
        $("#start_date").val(default_start_date);
        $("#end_date").val(default_end_date);
        $('#start_date').datepicker('update');
        $('#end_date').datepicker('update');
        getRaces();
    });

    $('.no-result .cde-all-distances').click(function (event) {
        $(".distance_selector").removeClass("active");
        $(this).prop('checked', false);
        getRaces();
    });

    $('.no-result .cde-all-distances').click(function (event) {
        resetSearchForm();
    });


    $('.no-result .cde-full-map').click(function (event) {  
        sw = new google.maps.LatLng(default_boundsarray[0],default_boundsarray[1]);
        ne = new google.maps.LatLng(default_boundsarray[2], default_boundsarray[3]);
        bounds = new google.maps.LatLngBounds(sw, ne);
        map.fitBounds(bounds);

        getRaces();
    });

}

function refreshRacesOnMap(races) {
    for(var key in markers){
        markers[key].setMap(null);
    }

    // reinitialize markers associative array
    markers = {};

    $.each(races, function(i, race) {
        var rankClass = race.rankClass;
        var latlng = new google.maps.LatLng(race.lat, race.lng);
        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            id: race.id,
            icon : markerIcons[rankClass]["default"],
            zIndex : 1,
            // own property
            rankClass : rankClass,
        });
        markers[race.id]=marker;
        
        // Listener : select event on marker click
        addListMarkerClick(marker);
        addListHoverMapResult(marker);
    });

    // if (!(selected_event_id in markers)) {
    //     selected_event_id = null;
    // }

    selectEvent(selected_event_id);
}


// ----------------------
// Dynamic display
// ----------------------
function selectEvent(event_id){
    if ( markers[selected_event_id] !== undefined ) {
        // unselect old event
        if($("#event_" + selected_event_id).length) {
            $("#event_" + selected_event_id).removeClass("active");
            marker = markers[selected_event_id];
            marker.setIcon(markerIcons[marker.rankClass]["default"]);
        }
    }
    
    // select new event
    selected_event_id = event_id;

    if ( markers[selected_event_id] !== undefined ) {
        if($("#event_" + selected_event_id).length) {
            $("#event_" + selected_event_id).addClass("active");
            
            // scroll sidebox to selected race with a 150px reserve (navbar + extra space)
            $(".sidebox").animate({
                scrollTop: $(".sidebox").scrollTop() + $("#event_" + selected_event_id).offset().top - 150
            }, 500);
            marker = markers[selected_event_id];
            marker.setIcon(markerIcons[marker.rankClass]["selected"]);
            marker.setZIndex(highestZIndex+1);
            highestZIndex += 1;
        }
    }
}


function setMapBoundsFromResults() {
    if (map !== undefined) {
        var bound = new google.maps.LatLngBounds();
        if(!($.isEmptyObject(markers))){
            for(var key in markers) {
                bound.extend(markers[key].getPosition());
            }
            map.fitBounds(bound);
        }
    }
}

function resetSearchForm(){
    $("#search_expr").val(default_search_expr);
    $("#start_date").val(default_start_date);
    $("#end_date").val(default_end_date);
    $('#start_date').datepicker('update');
    $('#end_date').datepicker('update');
    $(".distance_selector").removeClass("active");
    $('.distance_selector > input').each( function(i) {
        $(this).prop('checked', false);
    });
    getRaces();
}

function highlightResult(event_id){
    $("#event_" + event_id).addClass("mouseover");
    if(event_id != selected_event_id){
        marker = markers[event_id]
        marker.setIcon(markerIcons[marker.rankClass]["hover"]);
    } 
}

function deHighlightResult(event_id){
    $("#event_" + event_id).removeClass("mouseover");
    if(event_id != selected_event_id){
        marker = markers[event_id]
        marker.setIcon(markerIcons[marker.rankClass]["default"]);
    } else {
        marker = markers[event_id]
        marker.setIcon(markerIcons[marker.rankClass]["selected"]);
    }
}


// ----------------------
// Utils
// ----------------------
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function getParamQuery(){
    // selected_sport = $('.sport-selected').text().toLowerCase();
    
    _boundsarray = (typeof boundsarray === "undefined" || boundsarray === "") ? default_boundsarray : boundsarray;
    param_query = $( "#race_search_form" ).serialize() +
                      '&active=' + selected_event_id +
                      '&z=' + map.getZoom() +
                      '&lat_lo=' + _boundsarray[0] + 
                      '&lng_lo=' + _boundsarray[1] + 
                      '&lat_hi=' + _boundsarray[2] + 
                      '&lng_hi=' + _boundsarray[3]
                      

    return param_query;
}

function pushState(param_query){
    stateObj = { param_query: param_query
                }

    if (param_query !== last_query && typeof last_query !== "undefined"){
        history.pushState(stateObj, 'index', '/search?' + param_query);
        last_query = param_query
        console.log('push') 
        console.log(stateObj)   
    } else if (location.search === ""){
        history.replaceState(stateObj, 'index', '/search?' + param_query);
        last_query = param_query
        console.log('push initial')    
        console.log(stateObj)
    }
}

window.onpopstate = function(event){
    // window.location.href = event.state
    // console.log("history pop")
    // console.log(event.state)

    if(event.state !== null) {
        ajaxLoad(event.state["param_query"])    

        // disable map move listener to avoid refresh upon initialization
        google.maps.event.clearListeners(map, 'idle');
        // initialize document from URL parameters
        initializeFromURL();
        // enable map move listener
        google.maps.event.addListenerOnce(map, 'idle', function() {
            addListMapMoves();
        });
    }

}

