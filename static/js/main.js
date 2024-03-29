"use strict";
// SPAGHETTI v1.0

/*global $:false */
/*global static_url:false */
/*global jQuery:false */
/*global default_lat */
/*global default_lng */
/*global default_search_bounds */
/*global default_search_expr */
/*global default_start_date */
/*global default_end_date */
/*global default_cache_bounds */
/*global History */
/*global google */
/*global default_sport */
/*global Modernizr */
/*global default_distances */

/*global viewport */
/*global selected_event_id */
/*global search_sport */
/*global search_distances */
/*global search_start_date */
/*global search_end_date */
/*global search_expr */

var map = null;
var last_query;
var markers = {};       

var highest_Z_index = 10;
var markerIcons = {};
var primaryIcons = {};
var secondaryIcons = {};

var last_query_pushed;
var last_query_options_loaded;

// var viewport = ""; // store the current map bounds
// var selected_event_id="";
// var search_sport = "";
// var search_distances = "";
// var search_start_date = "";
// var search_end_date = "";
// var search_expr = "";

var map_hidden = false;
var native_datepicker = Modernizr.touch;

var manualStateChange = false;

var sidebarLoadingLock = false;

var page_title;


function RefreshOptions(options) {
    if (typeof options === "undefined") {
        this.refreshMap = true;
        this.refreshSidebar = true;
        this.fullRefresh = false;
    } else {
        this.refreshMap = (typeof options.refreshMap === "undefined") ? true : options.refreshMap;
        this.refreshSidebar = (typeof options.refreshSidebar === "undefined") ? true : options.refreshSidebar;    
        this.fullRefresh = (typeof options.fullRefresh === "undefined") ? false : options.fullRefresh;    
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

    page_title = document.title;
    // search_sport = default_sport.toLowerCase();
    // viewport = default_search_bounds; 
    // search_distances = default_distances;
    // search_start_date = default_start_date;
    // search_end_date = default_end_date;
    // search_expr = default_search_expr;


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

    // set datepicker on non-touch devices, and native HTML5 for touch devices
    if (!native_datepicker) {
        $("input[type=date]").attr("type", "text");
        createDatePickerComponent();
    }

    // if the map will not be displayed due to the viewport resolution (mobile)
    if( $("#map-canvas").is(":hidden") ) {
        map_hidden = true;
        getRaces();
    } 
    // else initialize map
    else {
        // initialize the map
        initializeMap();
        // no need to call getRaces() as the "idle" event from map will be triggered and call getRaces()
    }

    // Initiliaze CRSF token
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).on({
        ajaxStart: function() { 
            $("#racelist-container").hide();
            $("#filter-cde-results").hide();
            $(".loading-spinner").show();
        },
        ajaxStop: function() { 
            $("#racelist-container").show();
            $("#filter-cde-results").show();
            $(".loading-spinner").hide();
        }    
    });



    // Add custom event listeners
    addListWindowResize();
    addListMapMoves();
    addListSearch();
    addListResultClick();
    addListResetForm();
    addListSportSelection();
    addListSideboxScroll();
    initializeMapZoomControl();

    initializeDOMComponents();

    getRaces({"fullRefresh": true});
}



// ----------------------
// DOM Initialization 
// ----------------------

function initializeMap() {
     var mapOptions = {
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        center: {
            lat: default_lat ,
            lng: default_lng
        },
        // zoom: 6,
        maxZoom: 15,
        minZoom: 2 ,   
        panControl: false,
        zoomControl: false,
        streetViewControl: false
    };

    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

    map.setOptions({styles: map_styles});

    initializeMapSearchBox();

}

function initializeMapSearchBox() {

        var options = {
            types: ['geocode'] 
        };

        // Create the search box and link it to the UI element.
        var input = document.getElementById('cd-place-searchbox');
        input.style.display = 'inherit'
        var searchBox = new google.maps.places.Autocomplete(input, options);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        // Bias the SearchBox results towards current map's viewport.
        map.addListener('bounds_changed', function() {
            searchBox.setBounds(map.getBounds());
        });

        // [START region_getplaces]
        // Listen for the event fired when the user selects a prediction and retrieve
        // more details for that place.
        searchBox.addListener('place_changed', function() {
            var place = searchBox.getPlace();

            // For each place, get the icon, name and location.
            var bounds = new google.maps.LatLngBounds();
        
            // Create a marker for each place.
            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }

            map.fitBounds(bounds);
        });

        // [END region_getplaces]
}

// initialize map zoom controls
function initializeMapZoomControl() {
    if (map) {
        // Setup the click event listeners and zoom-in or out according to the clicked element
        $("#cd-zoom-in").click( function() {
            map.setZoom(map.getZoom()+1);
        });
        $("#cd-zoom-out").click( function() {
            map.setZoom(map.getZoom()-1);
        });
    }
}


function displayDistanceHelper(sport) {
     $.ajax({
        url: "/api/distance/" + sport,
        type: "GET", 
        dataType: "json"
        })
        .done(function(response) {
            $("#sport-distances-helper").html(response.helper_html);
            $("#distance_selectors").html(response.distance_selectors_html);
            // refreshDistancesButtons(response.distances);
        })
        .fail(function(){
            $("#sport-distances-helper").html("");
        });
}

// called directly from html file for legacy browser datepicker (inpu="date") fallback
function createDatePickerComponent() {
    $("#datepicker").datepicker({
        format: "yyyy-mm-dd",
        language: "fr",
        autoclose: true,
        clearBtn: true,
        todayHighlight: true,
        todayBtn: "linked"
    });
}


function initializeDOMComponents(){

    // need to test whetheir sport exists trhough ajax
    // search_sport = getParameterByName("sport");

    // need to be done in django view 
    // if (search_sport !== "" ) {
    //     saveSportSession(search_sport);
    // } 
    // else {
    //     search_sport = default_sport;
    // }
    
    // if sport has been changed (pushstate)
    if ($("#sport-selecter").val().toLowerCase() !== search_sport.toLowerCase()){
        saveSportSession(search_sport);
        $("#sport-selecter").val(search_sport.charAt(0).toUpperCase() + search_sport.slice(1));
    }

    // $("#sport-selecter").val(search_sport.charAt(0).toUpperCase() + search_sport.slice(1));

    // should be done in django view
    // displayDistanceHelper(search_sport);

    // set map to provided bounds
    var lat_lo = viewport[0];
    var lng_lo = viewport[1];
    var lat_hi = viewport[2];
    var lng_hi = viewport[3];

    if(map && lat_lo !== "" && lat_hi !== "" && lng_lo !== "" && lng_hi !== "") {
        var sw = new google.maps.LatLng(parseFloat(lat_hi), parseFloat(lng_lo));
        var ne = new google.maps.LatLng(parseFloat(lat_lo), parseFloat(lng_hi));
        var bounds = new google.maps.LatLngBounds(sw, ne);
        if (getParameterByName("z") === "") {
            map.fitBounds(bounds);
        } else {
            map.setCenter(bounds.getCenter());
            map.setZoom(parseInt(getParameterByName("z")));
        }
        // wait for the map to be ready to get bounds
        displayLoadingSpinner();
        sidebarLoadingLock = true;
        google.maps.event.addListenerOnce(map, 'bounds_changed', function(){ 
            viewport = map.getBounds().toUrlValue().split(",");
            sidebarLoadingLock = false;
            getRaces(new RefreshOptions({"refreshMap": false}))
        });

    }


    // set dates
    // search_start_date = getParameterByName("start_date") || default_start_date;
    $("#start_date").val(search_start_date);

    // search_end_date = getParameterByName("end_date") || default_end_date;
    $("#end_date").val(search_end_date);

    // search_expr = getParameterByName("q") || default_search_expr;
    $("#search_expr").val(search_expr);
    
    // updates the datepicker in order to save changed value in datepicker window
    if (!native_datepicker) {
        delListSearch();
        $("#start_date").datepicker("update");
        $("#end_date").datepicker("update");
        addListSearch();
    }

    // set active
    // var active = getParameterByName("active");
    // if (active !== "") {
    //     selected_event_id = parseInt(active);    
    // } else {
    //     selected_event_id = "";
    // }

    // search_distances = getParameterByName("distances");
    // if (search_distances !== "") {
        var arr_distances = search_distances.split(",");
        // arr_distances.indexOf("XS") !== -1 => true if distance selected
        setCheckDistanceInput("XS", arr_distances.indexOf("XS") !== -1);
        setCheckDistanceInput("S", arr_distances.indexOf("S") !== -1);
        setCheckDistanceInput("M", arr_distances.indexOf("M") !== -1);
        setCheckDistanceInput("L", arr_distances.indexOf("L") !== -1);
        setCheckDistanceInput("XL", arr_distances.indexOf("XL") !== -1);
    // } 
}


function setCheckDistanceInput(distance, val) {
    $("#distance_input_"+distance).prop("checked", false);
    $("#distance_selector_"+distance).removeClass("active");
    if (val){
        $("#distance_input_"+distance).prop("checked", true);
        $("#distance_selector_"+distance).addClass("active");
    }
}

// ----------------------
// LISTENERS
// ----------------------

function addListSideboxScroll() {
    var filter_cde = $("#filter-cde");
    var origOffsetY = $("#filter-cde").offset().top;

    function scroll() {
        if ($(window).scrollTop() >= origOffsetY) {
            filter_cde.addClass("sticky-xs");
            $("#filter-cde-top").show();
        } 
        else {
            filter_cde.removeClass("sticky sticky-xs");
            $("#filter-cde-top").hide();

        }
    }
    document.onscroll = scroll;

    var displayCdeTreshold = $("#sidebox-content").offset().top - 100 ;
    $("#sidebox").scroll(function sideboxScroll(){
        if($("#sidebox-content").offset().top > displayCdeTreshold) {
            $("#filter-cde-top").hide();
        }
        else {
            $("#filter-cde-top").show();

        }
    })

    $("#filter-cde-top").on("click", function (e){
        e.preventDefault();
        window.scrollTo(0, 0);
        $("#sidebox").scrollTop(0);
    });

    $("#filter-cde-reset").on("click", function (e){
         e.preventDefault();
         resetSearchForm();
    });
}

// when the window is resized ()

// TODO : KO, should test if the map CAN be displayed, if true, initialize the map and never delete
function addListWindowResize () {
    $(window).on("resize", function() {
        // if the map is being hid
        var willbe_hidden = $("#map-canvas").is(":hidden");
        if(!map_hidden && willbe_hidden){
            // do erase map
            // map = null;
            map_hidden = true;
        }
        // if the map is being shown
        else if (map_hidden && !willbe_hidden) {
            // initialize map    
            initializeMap();
            getRaces(new RefreshOptions());
            map_hidden = false;
        }
    });
}

function saveSportSession(sport){
    // setter
    if (sport) {
         $.ajax({
        url: "/api/sport-session/",
        data: {sport: sport},
        type: "POST",
        }).done(function() { 
            search_sport = sport;
        });
    } 

      
}


function addListSportSelection(){
    // change sport
    $("#sport-selecter").on("change", function (event) { 
        event.preventDefault();
        event.stopPropagation();
        search_sport = event.currentTarget.value
        saveSportSession(search_sport);
        // as distance are not common between sports, clear the distance addListSportSelection 
        search_distances = ''
        displayDistanceHelper(search_sport);
        getRaces(new RefreshOptions({"fullRefresh": true}));
        pushState(getParamQuery());
   });
}

// LISTENER : retrieve races when map moves
function addListMapMoves(){
    if (map) {
        // attach proper event listener after first idle
        // as the races have already been fetched in initialize()
        google.maps.event.addListenerOnce(map, "idle", function() {
            google.maps.event.addListener(map, "idle", function() {
                // Do not refresh races if the map is not visible or "follow map bounds" not checked
                if ($("#follow_map_bounds").is(":checked") && $(".mapbox").is(":visible") ) {
                    viewport = map.getBounds().toUrlValue().split(",");
                    getRaces(new RefreshOptions({"refreshMap": false}));
                    pushState(getParamQuery());
                }
            });
        });
    }
}

function addListMarkerClick(marker){
    if (map) {
        google.maps.event.addListener(marker, "click", function () {
            selectEvent(marker.get("id"));
            pushState(getParamQuery());
        });
    }
}

function addListResultClick(){
    $(".search-result").click(function( event ) {
        selectEvent(event.currentTarget.id.replace("event_",""));
        $(".search-result").removeClass("active");
        $(event.currentTarget).addClass("active");
        pushState(getParamQuery());
    });
}

    
// LISTENER : retrieve races from basic search
function addListSearch(){
    $("#race_search_form").on("change submit", function(event) {
        event.preventDefault();
        $("#race_search_form").serialize();
        search_distances = default_distances;
        $.each($(".distance_input").serialize().split("&"), function(i, d) {
                              if(d) { search_distances += d.split("=")[1] + ",";}
                        }); 
        // only set when sport changed (api call)
        search_expr = $("#search_expr").val();
        search_start_date = $("#start_date").val();
        search_end_date = $("#end_date").val();

        getRaces(new RefreshOptions({"fullRefresh": true}));
        selected_event_id = "";
        pushState(getParamQuery());
    });
}

// LISTENER : retrieve races from basic search
function delListSearch(){
    $("#race_search_form").off("change submit");
    }

function addListResetForm(){
     $( "#reset-search-form" ).click(function() {
        resetSearchForm();
    });
}

function addListHoverSideboxResult(){
    $(".search-result").hover(function() {
        highlightResult($(this)[0].id.replace("event_",""));
    }, function() {
        deHighlightResult($(this)[0].id.replace("event_",""));
    }
    );
}

function addListHoverMapResult(marker){
    if (map) {
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
    var zoom = map ? map.getZoom() : "";
    var param_query = (search_expr) ? ("&q=") + search_expr : "" ;
    param_query += (search_start_date) ? ("&start_date=" + search_start_date) : "";
    param_query += (search_end_date) ? ("&end_date=" + search_end_date) : "";
    param_query += (search_distances) ? ("&distances=" + search_distances) : "";
    param_query += "&viewport=" + viewport[0];
    param_query += "," + viewport[1];
    param_query += "," + viewport[2];
    param_query += "," + viewport[3];
    param_query += "&z=" + zoom;
    param_query += (selected_event_id) ? ("&active="  + selected_event_id) : "";


    return param_query;
}

function getRaces(options) {
    // returns a HTML of races results
    var param_query;
    param_query = getParamQuery();
    if (param_query !== last_query) {
        ajaxLoad(param_query, options);
    }
}

function ajaxLoad(data, options, fallback) {
    if (typeof options === "undefined") { options = new RefreshOptions();}

    if (options.refreshSidebar) {
        displayLoadingSpinner();
    }

    if (options.fullRefresh) {
        var tmp_viewport = viewport;
        viewport = default_cache_bounds;
        ajaxLoad(getParamQuery(), 
                 new RefreshOptions({"refreshSidebar": false}),
                 function () {
                    viewport = tmp_viewport;
                    ajaxLoad(getParamQuery(), new RefreshOptions({"refreshMap": false}));
                 }         
            );
        viewport = tmp_viewport;
    } 
    else {
        if(last_query_options_loaded !==  "&search_sport=" + search_sport + data + JSON.stringify( options ) ) {

            // console.log("load:" + data + JSON.stringify( options ));

            $.ajax({
            url: "/api/races/",
            type: "GET", 
            data: 'sport=' + search_sport + data,
            dataType: "json",
            timeout: 40000,
            })
            .done(function(response) {
                if (options.refreshSidebar) { refreshRacesOnSidebar(response.html, response.count); }
                if (options.refreshMap && !map_hidden) { refreshRacesOnMap(response.races); }
                last_query_options_loaded =  "&search_sport=" + search_sport + data + JSON.stringify( options );

                if(typeof fallback === "function") {fallback();}
            })
            .fail(function(){
                $("#racelist").html(
                    "<div class='alert alert-danger' role='alert'>Une erreur est survenue, " +
                    "veuillez contacter <a href='https://esprova.zendesk.com/hc/fr/requests/new'>" +
                    "le support</a></div>");
            });
        }
    }
}


// ----------------------
// Display results
// ----------------------

function displayLoadingSpinner(){
    // $("#racelist").html("<div class='spinner'><i class='fa fa-spinner fa-pulse'></i></div>");
    // $("#filter-cde-results").html("<i class='fa fa-spinner fa-pulse'></i>");
}


function refreshRacesOnSidebar(raceshtml, count) {
    if (sidebarLoadingLock === false) {
        // replace HTML by ajax provided code
        $("#racelist").html(raceshtml);
        $("#filter-cde-results").html(count + (count>1 ? " courses" : " course"));

        addListResultClick();
        addListHoverSideboxResult();
        selectEvent(selected_event_id, false);

        // if no result, try to find if the search expression is a location, and propose a link to search
        if (count === 0) {
            handleNoResult();
        }   
    }
}
       
function handleNoResult(){
    var selector = $("#try-location-search");
    var address = selector.data("expr");

    // try to geocode expression
    var geocoder = new google.maps.Geocoder();
    if (address !== "None" && map_hidden === false) {
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

                // handle click event on location proposal
                selector.children("#location").click(function (e) {
                    e.preventDefault();
                    var viewport_bounds = results[0].geometry.bounds;
                    viewport = viewport_bounds.toUrlValue().split(",")
                    $("#search_expr").val("");
                    search_expr = "";
                    getRaces();
                    map.fitBounds(viewport_bounds);
                });
            }
        });
    }
    
    if(search_expr !== default_search_expr) {
        $("#no-result #cde-remove-keywords").removeClass("hidden");
        $("#no-result #cde-remove-keywords").click(function () {
            $("#search_expr").val("");
            search_expr = default_search_expr;
            getRaces();
        });
    }
   
    if(search_start_date !== default_start_date || search_end_date !== default_end_date) {
        $("#no-result #cde-full-year").removeClass("hidden");
        $("#no-result #cde-full-year").click(function () {
            $("#start_date").val(default_start_date);
            search_start_date = default_start_date;
            $("#end_date").val(default_end_date);
            search_end_date = default_end_date;
            getRaces();
        });
    }

    if(search_distances !== default_distances) {
        $("#no-result #cde-all-distances").removeClass("hidden");
        $("#no-result #cde-all-distances").click(function () {
            $(".distance_selector").removeClass("active");
            $(this).prop("checked", false);
            search_distances = default_distances;
            getRaces();
        });
    }

    $("#no-result #cde-reset-form").click(function () {
        resetSearchForm();
    });


    if(viewport !== default_search_bounds) {
        $("#no-result #cde-full-map").removeClass("hidden");
        $("#no-result #cde-full-map").click(function () {  
            var sw = new google.maps.LatLng(default_search_bounds[0],default_search_bounds[1]);
            var ne = new google.maps.LatLng(default_search_bounds[2], default_search_bounds[3]);
            var bounds = new google.maps.LatLngBounds(sw, ne);
            map.fitBounds(bounds);
            viewport = default_search_bounds;

            getRaces();
        });
    }
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

    selectEvent(selected_event_id, false);
}

function refreshDistancesButtons(distances) {
    $(".distance_selector").removeClass("hidden");
    if (distances.indexOf("XS") < 0 ) { $("#distance_selector_1").addClass("hidden"); }
    if (distances.indexOf("S") < 0 ) { $("#distance_selector_2").addClass("hidden"); }
    if (distances.indexOf("M") < 0 ) { $("#distance_selector_3").addClass("hidden"); }
    if (distances.indexOf("L") < 0 ) { $("#distance_selector_4").addClass("hidden"); }
    if (distances.indexOf("XL") < 0 )  { $("#distance_selector_5").addClass("hidden"); }
}

// ----------------------
// Dynamic display
// ----------------------
function selectEvent(event_id, animate){
    animate = (typeof animate === "undefined") ? true : animate;

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
            if(animate) {
                $("#sidebox").animate({
                    scrollTop: $("#sidebox").scrollTop() + $("#event_" + selected_event_id).offset().top - 150
                }, 500);
            }
            else {
                $("#sidebox").scrollTop($("#event_" + selected_event_id).offset().top - 150);
            }

            var marker = markers[selected_event_id];
            marker.setIcon(markerIcons[marker.rankClass].selected);
            marker.setZIndex(highest_Z_index+1);
            highest_Z_index += 1;
        }
    }
}



function resetSearchForm(){
    window.location.href = window.location.pathname;
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


function eraseMap(){
    map = null
    map_hidden = true
}


function pushState(param_query){
    var stateObj = { param_query: param_query,
                     viewport: viewport,
                     selected_event_id: selected_event_id,
                     search_sport: search_sport,
                     search_distances: search_distances,
                     search_start_date: search_start_date,
                     search_end_date: search_end_date,
                     search_expr: search_expr,
                };
    manualStateChange = false;

    if (last_query_pushed !== param_query) {
        // console.log("push:" + param_query);
        History.pushState(stateObj, page_title + " - " + search_sport, "/search/" + search_sport + "?" + param_query);        
        last_query_pushed = param_query + "&search_sport=" + search_sport;
    }

}

// Bind to StateChange Event
History.Adapter.bind(window, "statechange", function() {
    var state = History.getState();
    if(state !== null) {
        if(manualStateChange === true) {
            if (typeof(state.data.param_query) != "undefined") {
                // reinit variables from history
                var param_query = state.data.param_query;
                viewport = state.data.viewport;
                selected_event_id = state.data.selected_event_id;
                search_sport = state.data.search_sport;
                search_distances = state.data.search_distances;
                search_start_date = state.data.search_start_date;
                search_end_date = state.data.search_end_date;
                search_expr = state.data.search_exp;

                ajaxLoad(param_query);
                // disable map move listener to avoid refresh upon initialization
                google.maps.event.clearListeners(map, "idle");
                // initialize document from URL parameters

                initializeDOMComponents();
                // enable map move listener
                google.maps.event.addListenerOnce(map, "idle", function() {
                    addListMapMoves();
                });
            }
            else {
                window.location.replace(state.url)
            }
        }

        manualStateChange = true;

    
        }
    });


