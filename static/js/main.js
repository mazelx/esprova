var map;
var mapbounds;
var last_query;
var markers = {};
var selected_event_id="";

var highestZIndex = 10;

var markerIcons = {};
var primaryIcons = {};
var secondaryIcons = {};

var default_lat = 46.9;
var default_lng = 2.6;

var static_url = 'https://esprova-static.s3.amazonaws.com/';
// var static_url = 'http://localhost:8000/static/'

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
    url: static_url + 'images/secondary_marker_default.svg',
    size: new google.maps.Size(26,26),
    anchor: new google.maps.Point(13,13),
};

secondaryIcons['selected']={
    url: static_url + 'images/secondary_marker_selected.svg',
    size: new google.maps.Size(26,26),
    anchor: new google.maps.Point(13,13),
};

secondaryIcons['hover']= {
    url: static_url + 'images/secondary_marker_hover.svg',
    size: new google.maps.Size(26,26),
    anchor: new google.maps.Point(13,13),
};
markerIcons["primary"]=primaryIcons;
markerIcons["secondary"]=secondaryIcons;


// if the map style has not been provided
if (typeof map_styles === 'undefined'){
    map_styles = [];
}


// ----------------------
// JS Init
// ----------------------

google.maps.event.addDomListener(window, 'load', initialize);

function initialize() {

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
    
    // Add custom event listeners
    addListMapMoves();
    addListQuickSearch();
    addListSearch();
    addListAlertMessages();
    addListResultClick();
    addListResetForm();

    // createDatePickerComponent();

    initializeMapZoomControl();
    initializeFromURL();
}

// ----------------------
// DOM Initialization 
// ----------------------


// initialize map zoom controls
function initializeMapZoomControl() {
    // Setup the click event listeners and zoom-in or out according to the clicked element
    $('#cd-zoom-in').click( function(event) {
        map.setZoom(map.getZoom()+1)
    });
    $('#cd-zoom-out').click( function(event) {
        map.setZoom(map.getZoom()-1)
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
    
    // set map to provided bounds
    lat_lo = getParameterByName('lat_lo')
    lat_hi = getParameterByName('lat_hi')
    lng_lo = getParameterByName('lng_lo')
    lng_hi = getParameterByName('lng_hi')

    if(lat_lo !== "" && lat_hi !== "" && lng_lo !== "" && lng_hi !== "") {
        sw = new google.maps.LatLng(parseFloat(lat_hi), parseFloat(lng_lo));
        ne = new google.maps.LatLng(parseFloat(lat_lo), parseFloat(lng_hi));
        bounds = new google.maps.LatLngBounds(sw, ne);
        map.setCenter(bounds.getCenter());
        map.setZoom(parseInt(getParameterByName('z')))
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

    // getRaces(false);
}

// ----------------------
// LISTENERS
// ----------------------

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
    $(".event-result").click(function( event ) {
        selectEvent(event.currentTarget.id.replace("event_",""));
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
    $( "#race_search_form" ).change(function( event ) {
        event.preventDefault();
        getRaces();
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
    $(".event-result").hover(function() {
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
    }
}

function ajaxLoad(params) {
    console.log("ajaxload: "+params)
    $.ajax({
        url: 'ajx/search/',
        type: 'GET', 
        data: params,
        dataType: 'json',
        success: function(response, statut) {
            refreshRacesOnSidebar(response.html);
            refreshRacesOnMap(response.races);
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
    addListHoverSideboxResult();
    selectEvent(selected_event_id);
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
            $("#event_" + selected_event_id).removeClass("panel-primary");
            $("#event_" + selected_event_id + "_races").removeClass("in");
            marker = markers[selected_event_id];
            marker.setIcon(markerIcons[marker.rankClass]["default"]);
        }
    }
    
    // select new event
    selected_event_id = event_id;

    if ( markers[selected_event_id] !== undefined ) {
        if($("#event_" + selected_event_id).length) {
            $("#event_" + selected_event_id).addClass("panel-primary");
            $("#event_" + selected_event_id + "_races").addClass("in");
            
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
    $("#race_search_form")[0].reset();
    $('#start_date').datepicker('update')
    $('#end_date').datepicker('update')
    $(".distance_selector").removeClass("active");
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
    param_query = 'z=' + map.getZoom() +
                      '&active=' + selected_event_id +
                      '&lat_lo=' + boundsarray[0] + 
                      '&lng_lo=' + boundsarray[1] + 
                      '&lat_hi=' + boundsarray[2] + 
                      '&lng_hi=' + boundsarray[3] +
                      '&' + $( "#race_search_form" ).serialize()

    return param_query;
}

function pushState(param_query){
    stateObj = { param_query: param_query
                }

    if (param_query !== last_query && typeof last_query !== "undefined"){
        history.pushState(stateObj, 'index', '/list?' + param_query);
        last_query = param_query
        console.log('push') 
        console.log(stateObj)   
    } else if (location.search === ""){
        history.replaceState(stateObj, 'index', '/list?' + param_query);
        last_query = param_query
        console.log('push initial')    
        console.log(stateObj)
    }
}

window.onpopstate = function(event){
    // window.location.href = event.state
    console.log("history pop")
    console.log(event.state)

    if(true) {
        ajaxLoad(event.state["param_query"])    
    }

    // disable map move listener to avoid refresh upon initialization
    google.maps.event.clearListeners(map, 'idle');
    // initialize document from URL parameters
    initializeFromURL();
    // enable map move listener
    google.maps.event.addListenerOnce(map, 'idle', function() {
            addListMapMoves();
        });

}

