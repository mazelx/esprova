"use strict";
// SPAGHETTI v1.0

/*global $:false */
/*global static_url:false */
/*global jQuery:false */

var map;
var viewport; // store the current map bounds
var last_query;
var markers = {};
var selected_event_id="";
var selected_sport = "";

var highest_Z_index = 10;

var markerIcons = {};
var primaryIcons = {};
var secondaryIcons = {};

var default_lat = 46.9;
var default_lng = 2.6;
// var default_boundsarray = [40,-10,60,12];
var default_viewport = [36.997739,-14.974121,54.708447,17.853027];
var default_search_expr = "";
var default_start_date = "2015-01-01";
var default_end_date = "2015-12-31";

var initial_viewport = [-90, -90, 90, 90]; // used for fetching map icons at startup

var google;

function RefreshOptions(options) {
    if (typeof options === "undefined") {
        this.recordState = true;
        this.refreshMap = true;
        this.refreshSidebar = true;
    } else {
        this.recordState = (typeof options.recordState === "undefined") ? true : options.recordState;
        this.refreshMap = (typeof options.refreshMap === "undefined") ? true : options.refreshMap;
        this.refreshSidebar = (typeof options.refreshSidebar === "undefined") ? true : options.refreshSidebar;    
    }
    
}
// var static_url = "https://esprova-static.s3.amazonaws.com/";
// var static_url = "http://localhost:8000/static/"


// if the map style has not been provided
if (typeof map_styles === "undefined"){
    var map_styles = [];
}

// var map_styles = map_styles || [];


// ----------------------
// JS Init
// ----------------------
if (typeof google !== "undefined") {
    google.maps.event.addDomListener(window, "load", initialize);
}


function initialize() {
    primaryIcons.default = {
        url: static_url + "images/primary_marker_default.svg",
        size: new google.maps.Size(28,42),
    };

    primaryIcons.selected ={
        url: static_url + "images/primary_marker_selected.svg",
        size: new google.maps.Size(28,42),
    };

    primaryIcons.hover= {
        url: static_url + "images/primary_marker_hover.svg",
        size: new google.maps.Size(28,42),
    };

    secondaryIcons.default = {
        // url: static_url + "images/secondary_marker_default.svg",
        url: static_url + "images/marker_default.png",
        // size: new google.maps.Size(9,9),
        scaledSize: new google.maps.Size(10,10),
        anchor: new google.maps.Point(4,4),
    };

    secondaryIcons.selected={
        url: static_url + "images/marker_selected.png",
        // size: new google.maps.Size(26,26),
        scaledSize: new google.maps.Size(14,14),
        anchor: new google.maps.Point(7,7),
    };

    secondaryIcons.hover= {
        url: static_url + "images/marker_hover.png",
        // size: new google.maps.Size(26,26),
        scaledSize: new google.maps.Size(10,10),
        anchor: new google.maps.Point(4,4),   
    };

    markerIcons.primary = primaryIcons;
    markerIcons.secondary = secondaryIcons;

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

    if( $("#map-canvas").length !== 0 ){

        // initialize the map
        map = new google.maps.Map(document.getElementById("map-canvas"),
            mapOptions);

        map.setOptions({styles: map_styles});

        // If map is not displayed (for mobile access)
        // Initialize results
        if($("#map-canvas").is(":hidden") === true) {    
            resetSearchForm();
        } else {
            // On Firefox (others?), a refresh would not display markers
                google.maps.event.addListenerOnce(map, "idle", function () {
                viewport = initial_viewport;
                getRaces();
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
    addListSearch();
    // addListAlertMessages();
    addListResultClick();
    addListResetForm();
    addListSportSelection();

    createDatePickerComponent();

    initializeMapZoomControl();
    initializeFromURL();
}


var csrftoken = getCookie("csrftoken");

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




// ----------------------
// DOM Initialization 
// ----------------------


// initialize map zoom controls
function initializeMapZoomControl() {
    if (map !== undefined) {
        // Setup the click event listeners and zoom-in or out according to the clicked element
        $("#cd-zoom-in").click( function() {
            map.setZoom(map.getZoom()+1);
        });
        $("#cd-zoom-out").click( function() {
            map.setZoom(map.getZoom()-1);
        });
    }
}


function initializeSportDistanceHelper(sport) {
     $.ajax({
        url: "api/distance/" + sport,
        type: "GET", 
        dataType: "text"
        })
        .done(function(response) {
            $("#sport-distances-helper").html(response);
        })
        .fail(function(){
            $("#sport-distances-helper").html("");
        });
}

// initialize bootstrap-datepicker component
function createDatePickerComponent() {
    $(".datepicker").datepicker({
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
    var _selected_sport = getParameterByName("sport");
    if (_selected_sport !== "" ) {
        saveSportSession(_selected_sport);
    }


    // set map to provided bounds
    var str_viewport = getParameterByName("viewport");
    viewport = (str_viewport === "") ? default_viewport : str_viewport.split(","); 

    var lat_lo = viewport[0];
    var lng_lo = viewport[1];
    var lat_hi = viewport[2];
    var lng_hi = viewport[3];

    if(lat_lo !== "" && lat_hi !== "" && lng_lo !== "" && lng_hi !== "") {
        var sw = new google.maps.LatLng(parseFloat(lat_hi), parseFloat(lng_lo));
        var ne = new google.maps.LatLng(parseFloat(lat_lo), parseFloat(lng_hi));
        var bounds = new google.maps.LatLngBounds(sw, ne);
        if (getParameterByName("z") === "") {
            map.fitBounds(bounds);
        } else {
            map.setCenter(bounds.getCenter());
            map.setZoom(parseInt(getParameterByName("z")));
        }
    }

    // set dates
    var start_date = getParameterByName("start_date");
    var end_date = getParameterByName("end_date");
    var search_expr = getParameterByName("search_expr");

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
    var active = getParameterByName("active");
    if (active !== "") {
        selected_event_id = parseInt(active);    
    } else {
        selected_event_id = "";
    }

    // var options = new RefreshOptions({"recordState": true});
    // getRaces(options);    
}

// ----------------------
// LISTENERS
// ----------------------

function saveSportSession(sport){
       $.ajax({
        url: "/api/sport-session/",
        data: {sport: sport},
        type: "POST",
        }).done(function() {
            var formatted_sport = sport.charAt(0).toUpperCase() + sport.slice(1);
            $(".sport-selected").html(formatted_sport);
            if (selected_sport !== formatted_sport) {
                selected_sport = formatted_sport;
                getRaces( new RefreshOptions({"recordState": false, "refreshMap": false}) );
                initializeSportDistanceHelper(sport);
            }
        });
}

function addListSportSelection(){
    // change sport
    $(".sport-selecter").on("change", function (event) { 
        event.preventDefault();
        saveSportSession(event.currentTarget.value);
   });
}

// LISTENER : retrieve races when map moves
function addListMapMoves(){
    if (map !== undefined) {
        google.maps.event.addListener(map, "idle", function() {
            // Do not refresh races if the map is not visible or "follow map bounds" not checked
            if ($("#follow_map_bounds").is(":checked") && $(".mapbox").is(":visible") ) {
                viewport = map.getBounds().toUrlValue().split(",");
                getRaces(new RefreshOptions({"refreshMap": false}));
            }
        });
    }
}

function addListMarkerClick(marker){
    if (map !== undefined) {
        google.maps.event.addListener(marker, "click", function () {
            selectEvent(marker.get("id"));
            pushState(getParamQuery(), false);
        });
    }
}

function addListResultClick(){
    $(".search-result").click(function( event ) {
        selectEvent(event.currentTarget.id.replace("event_",""));
        $(".search-result").removeClass("active");
        $(event.currentTarget).addClass("active");
        pushState(getParamQuery(), false);
    });
}

    
// LISTENER : retrieve races from basic search
function addListSearch(){

    $("#race_search_form").on("change submit", function(event) {
        event.preventDefault();
        getRaces();
        selected_event_id = "";
    });
}


// function addListSearch() {
//     // $("#start_date").datepicker().on("hide", getRaces);
// }

function addListResetForm(){
     $( "#reset-search-form" ).click(function() {
        resetSearchForm();
    });
}


// // En CSS ??
// function addListAlertMessages(){
//     window.setTimeout(function() {
//             $(".alert").fadeTo(500, 0).slideUp(500, function(){
//             $(this).remove(); 
//       });
//     }, 3000);
// }

function addListHoverSideboxResult(){
    $(".search-result").hover(function() {
        highlightResult($(this)[0].id.replace("event_",""));
    }, function() {
        deHighlightResult($(this)[0].id.replace("event_",""));
    }
    );
}

function addListHoverMapResult(marker){
    if (map !== undefined) {
        google.maps.event.addListener(marker, "mouseover", function() {
            highlightResult(marker.get("id"));
        });
        google.maps.event.addListener(marker, "mouseout", function() {
            deHighlightResult(marker.get("id"));
        });
    }
}

// ----------------------
// Ajax Handling
// ----------------------

function getParamQuery(){

    viewport = (typeof viewport === "undefined" || viewport === "") ? default_viewport : viewport;
    var param_query = $( "#race_search_form" ).serialize() +
                      "&viewport=" + viewport[0] +
                      "," + viewport[1] +
                      "," + viewport[2] +
                      "," + viewport[3] +
                      "&active=" + selected_event_id +
                      "&z=" + map.getZoom();

    return param_query;
}

function getRaces(options) {
    if (typeof options === "undefined") { options = new RefreshOptions();}

    // returns a HTML of races results
    var param_query;
    param_query = getParamQuery();
    if (param_query !== last_query) {
        ajaxLoad(param_query, options);
        if ( options.recordState === true) {
            pushState(param_query);
            last_query = param_query;
        }
    }
}

function ajaxLoad(data, options) {
    if (typeof options === "undefined") { options = new RefreshOptions();}


    $("#racelist").html("<div class='spinner'><i class='fa fa-spinner fa-pulse'></i></div>");

    $.ajax({
        url: "api/search/",
        type: "GET", 
        data: data,
        dataType: "json",
        timeout: 40000,
        })
        .done(function(response) {
            if (options.refreshSidebar) { refreshRacesOnSidebar(response.html, response.count); }
            if (options.refreshMap) { refreshRacesOnMap(response.races); }
        })
        .fail(function(){
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
    var selector = $("#try-location-search");
    var address = selector.data("expr");

    // try to geocode expression
    var geocoder = new google.maps.Geocoder();

    geocoder.geocode( { "address": address, region: "fr" }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            selector.removeClass("hidden");
            if (results.length > 0){
                if (results[0].address_components.length > 0){
                    var text = results[0].address_components[0].short_name;
                    if (results[0].address_components.length > 1){
                        text += " (" + results[0].address_components[1].short_name + ")";
                    }
                    selector.children("#location").children("a").text(text);
                }
            }

            selector.children("#location").click(function () {
                viewport = results[0].geometry.bounds;
                $("#search_expr").val("");
                map.fitBounds(viewport);
            });
        }
    });

    $("#no-result #cde-remove-keywords").click(function () {
        $("#search_expr").val("");
        getRaces();
    });

    $("#no-result #cde-full-year").click(function () {
        $("#start_date").val(default_start_date);
        $("#end_date").val(default_end_date);
        $("#start_date").datepicker("update");
        $("#end_date").datepicker("update");
        getRaces();
    });

    $("#no-result #cde-all-distances").click(function () {
        $(".distance_selector").removeClass("active");
        $(this).prop("checked", false);
        getRaces();
    });

    $("#no-result #cde-all-distances").click(function () {
        resetSearchForm();
    });


    $("#no-result #cde-full-map").click(function () {  
        var sw = new google.maps.LatLng(default_boundsarray[0],default_boundsarray[1]);
        var ne = new google.maps.LatLng(default_boundsarray[2], default_boundsarray[3]);
        var bounds = new google.maps.LatLngBounds(sw, ne);
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
        $("#event_" + selected_event_id).removeClass("active");
        marker = markers[selected_event_id];
        marker.setIcon(markerIcons[marker.rankClass]["default"]);
    }
    
    // select new event
    selected_event_id = event_id;

    if ( markers[selected_event_id] !== undefined ) {
        if($("#event_" + selected_event_id).length) {
            $("#event_" + selected_event_id).addClass("active");
            
            // scroll sidebox to selected race with a 150px reserve (navbar + extra space)
            $("#sidebox").animate({
                scrollTop: $("#sidebox").scrollTop() + $("#event_" + selected_event_id).offset().top - 150
            }, 500);
            var marker = markers[selected_event_id];
            marker.setIcon(markerIcons[marker.rankClass].selected);
            marker.setZIndex(highest_Z_index+1);
            highest_Z_index += 1;
        }
    }
}



function resetSearchForm(){
    viewport = initial_viewport;
    $("#search_expr").val(default_search_expr);
    $("#start_date").val(default_start_date);
    $("#end_date").val(default_end_date);
    $("#start_date").datepicker("update");
    $("#end_date").datepicker("update");
    $(".distance_selector").removeClass("active");
    $(".distance_selector > input").each( function() {
        $(this).prop("checked", false);
    });
    getRaces();
}

function highlightResult(event_id){
    $("#event_" + event_id).addClass("mouseover");
    if(event_id != selected_event_id){
        var marker = markers[event_id];
        marker.setIcon(markerIcons[marker.rankClass].hover);
    } 
}

function deHighlightResult(event_id){
    $("#event_" + event_id).removeClass("mouseover");
    var marker;
    if(event_id != selected_event_id){
        marker = markers[event_id];
        marker.setIcon(markerIcons[marker.rankClass].default);
    } else {
        marker = markers[event_id];
        marker.setIcon(markerIcons[marker.rankClass].selected);
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

function pushState(param_query){
    var stateObj = { param_query: param_query
                };

    if (param_query !== last_query && typeof last_query !== "undefined"){
        history.pushState(stateObj, "index", "/search?" + param_query);
        last_query = param_query;
    } else if (location.search === ""){
        history.replaceState(stateObj, "index", "/search?" + param_query);
        last_query = param_query;
    }
}

window.onpopstate = function(event){
    if(event.state !== null) {
        ajaxLoad(event.state.param_query); 

        // disable map move listener to avoid refresh upon initialization
        google.maps.event.clearListeners(map, "idle");
        // initialize document from URL parameters
        initializeFromURL();
        // enable map move listener
        google.maps.event.addListenerOnce(map, "idle", function() {
            addListMapMoves();
        });
    }

};


