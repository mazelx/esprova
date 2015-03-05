"use strict";function RefreshOptions(e){"undefined"==typeof e?(this.refreshMap=!0,this.refreshSidebar=!0):(this.refreshMap="undefined"==typeof e.refreshMap?!0:e.refreshMap,this.refreshSidebar="undefined"==typeof e.refreshSidebar?!0:e.refreshSidebar)}function initialize(){primaryIcons["default"]={url:static_url+"images/primary_marker_default.svg",size:new google.maps.Size(28,42)},primaryIcons.selected={url:static_url+"images/primary_marker_selected.svg",size:new google.maps.Size(28,42)},primaryIcons.hover={url:static_url+"images/primary_marker_hover.svg",size:new google.maps.Size(28,42)},secondaryIcons["default"]={url:static_url+"images/marker_default.png",scaledSize:new google.maps.Size(10,10),anchor:new google.maps.Point(4,4)},secondaryIcons.selected={url:static_url+"images/marker_selected.png",scaledSize:new google.maps.Size(14,14),anchor:new google.maps.Point(7,7)},secondaryIcons.hover={url:static_url+"images/marker_hover.png",scaledSize:new google.maps.Size(10,10),anchor:new google.maps.Point(4,4)},markerIcons.primary=primaryIcons,markerIcons.secondary=secondaryIcons,$("#map-canvas").is(":hidden")?resetSearchForm():(initializeMap(),google.maps.event.addListenerOnce(map,"idle",function(){viewport=default_cache_bounds})),$.ajaxSetup({beforeSend:function(e,t){csrfSafeMethod(t.type)||this.crossDomain||e.setRequestHeader("X-CSRFToken",csrftoken)}}),search_sport=default_sport,addListWindowResize(),addListMapMoves(),addListSearch(),addListResultClick(),addListResetForm(),addListSportSelection(),initializeMapZoomControl(),initializeDOMComponents(),getRaces()}function csrfSafeMethod(e){return/^(GET|HEAD|OPTIONS|TRACE)$/.test(e)}function getCookie(e){var t=null;if(document.cookie&&""!==document.cookie)for(var a=document.cookie.split(";"),s=0;s<a.length;s++){var r=jQuery.trim(a[s]);if(r.substring(0,e.length+1)===e+"="){t=decodeURIComponent(r.substring(e.length+1));break}}return t}function initializeMap(){var e={mapTypeId:google.maps.MapTypeId.TERRAIN,center:{lat:default_lat,lng:default_lng},zoom:6,maxZoom:15,panControl:!1,zoomControl:!1,streetViewControl:!1};map=new google.maps.Map(document.getElementById("map-canvas"),e),map.setOptions({styles:map_styles})}function initializeMapZoomControl(){map&&($("#cd-zoom-in").click(function(){map.setZoom(map.getZoom()+1)}),$("#cd-zoom-out").click(function(){map.setZoom(map.getZoom()-1)}))}function initializeSportDistanceHelper(e){$.ajax({url:"api/distance/"+e,type:"GET",dataType:"text"}).done(function(e){$("#sport-distances-helper").html(e)}).fail(function(){$("#sport-distances-helper").html("")})}function createDatePickerComponent(){$(".datepicker").datepicker({format:"yyyy-mm-dd",language:"fr",autoclose:!0,clearBtn:!0,todayHighlight:!0,todayBtn:"linked"})}function initializeDOMComponents(){search_sport=getParameterByName("sport"),""!==search_sport?saveSportSession(search_sport):search_sport=default_sport;var e=getParameterByName("viewport");viewport=""===e?default_search_bounds:e.split(",");var t=viewport[0],a=viewport[1],s=viewport[2],r=viewport[3];if(map&&""!==t&&""!==s&&""!==a&&""!==r){var n=new google.maps.LatLng(parseFloat(s),parseFloat(a)),o=new google.maps.LatLng(parseFloat(t),parseFloat(r)),i=new google.maps.LatLngBounds(n,o);""===getParameterByName("z")?map.fitBounds(i):(map.setCenter(i.getCenter()),map.setZoom(parseInt(getParameterByName("z"))))}var c=getParameterByName("start_date"),d=getParameterByName("end_date"),l=getParameterByName("search_expr");""!==c&&$("#start_date").val(c),""!==d&&$("#end_date").val(d),""!==l&&$("#search_expr").val(l);var p=getParameterByName("active");if(selected_event_id=""!==p?parseInt(p):"",search_distances=getParameterByName("distances"),""!==search_distances){var u=search_distances.split(",");setCheckDistanceInput("XS",-1!==u.indexOf("XS")),setCheckDistanceInput("S",-1!==u.indexOf("S")),setCheckDistanceInput("M",-1!==u.indexOf("M")),setCheckDistanceInput("L",-1!==u.indexOf("L")),setCheckDistanceInput("XL",-1!==u.indexOf("XL"))}}function setCheckDistanceInput(e,t){$("#distance_input_"+e).prop("checked",!1),$("#distance_selector_"+e).removeClass("active"),t&&($("#distance_input_"+e).prop("checked",!0),$("#distance_selector_"+e).addClass("active"))}function addListWindowResize(){$(window).on("resize",function(){map&&$("#map-canvas").is(":hidden")?map=null:map||(initializeMap(),getRaces(new RefreshOptions({recordState:!1})))})}function setSearchSport(){$.ajax({url:"/api/sport-session/",dataType:"json",type:"GET"}).done(function(e){search_sport=e})}function saveSportSession(e){e&&$.ajax({url:"/api/sport-session/",data:{sport:e},type:"POST"}).done(function(){var t=e.charAt(0).toUpperCase()+e.slice(1);$(".sport-selected").html(t),search_sport!==t&&(search_sport=t,initializeSportDistanceHelper(e))})}function addListSportSelection(){$("#sport-selecter").on("change",function(e){e.preventDefault(),saveSportSession(e.currentTarget.value),getRaces(new RefreshOptions({recordState:!1,refreshMap:!1}))})}function addListMapMoves(){map&&google.maps.event.addListener(map,"idle",function(){$("#follow_map_bounds").is(":checked")&&$(".mapbox").is(":visible")&&(viewport=map.getBounds().toUrlValue().split(","),getRaces(new RefreshOptions({refreshMap:!1})),pushState(getParamQuery()))})}function addListMarkerClick(e){map&&google.maps.event.addListener(e,"click",function(){selectEvent(e.get("id")),pushState(getParamQuery())})}function addListResultClick(){$(".search-result").click(function(e){selectEvent(e.currentTarget.id.replace("event_","")),$(".search-result").removeClass("active"),$(e.currentTarget).addClass("active"),pushState(getParamQuery())})}function addListSearch(){$("#race_search_form").on("change submit",function(e){e.preventDefault(),$("#race_search_form").serialize(),search_distances="",$.each($(".distance_input").serialize().split("&"),function(e,t){search_distances+=t.split("=")[1]+","}),search_distances=search_distances,search_sport=$("#sport-selecter").val(),search_expr=$("#search_expr").val(),search_start_date=$("#start_date").val(),search_end_date=$("#end_date").val(),getRaces(),selected_event_id="",pushState(getParamQuery())})}function addListResetForm(){$("#reset-search-form").click(function(){resetSearchForm()})}function addListHoverSideboxResult(){$(".search-result").hover(function(){highlightResult($(this)[0].id.replace("event_",""))},function(){deHighlightResult($(this)[0].id.replace("event_",""))})}function addListHoverMapResult(e){map&&(google.maps.event.addListener(e,"mouseover",function(){highlightResult(e.get("id"))}),google.maps.event.addListener(e,"mouseout",function(){deHighlightResult(e.get("id"))}))}function getParamQuery(){viewport="undefined"==typeof viewport||""===viewport?default_search_bounds:viewport;var e=map?map.getZoom():"",t="sport="+search_sport;return t+=search_expr?"&q="+search_expr:"",t+=search_start_date?"&start_date="+search_start_date:"",t+=search_end_date?"&end_date="+search_end_date:"",t+=search_distances?"&distances="+search_distances:"",t+="&viewport="+viewport[0],t+=","+viewport[1],t+=","+viewport[2],t+=","+viewport[3],t+="&z="+e,t+=selected_event_id?"&active="+selected_event_id:""}function getRaces(e){"undefined"==typeof e&&(e=new RefreshOptions);var t;t=getParamQuery(),t!==last_query&&ajaxLoad(t,e)}function ajaxLoad(e,t){"undefined"==typeof t&&(t=new RefreshOptions),$("#racelist").html("<div class='spinner'><i class='fa fa-spinner fa-pulse'></i></div>"),$.ajax({url:"api/search/",type:"GET",data:e,dataType:"json",timeout:4e4}).done(function(e){t.refreshSidebar&&refreshRacesOnSidebar(e.html,e.count),t.refreshMap&&refreshRacesOnMap(e.races)}).fail(function(){$("#racelist").html("<div class='alert alert-danger' role='alert'>Une erreur est survenue, veuillez contacter <a href='mailto:contact@esprova.com?subject=[issue]:[ajaxLoad]'>le support</a></div>")})}function refreshRacesOnSidebar(e,t){$("#racelist").html(e),addListResultClick(),addListHoverSideboxResult(),selectEvent(selected_event_id,!1),0===t&&handleNoResult()}function handleNoResult(){var e=$("#try-location-search"),t=e.data("expr"),a=new google.maps.Geocoder;a.geocode({address:t,region:"fr"},function(t,a){if(a==google.maps.GeocoderStatus.OK){if(e.removeClass("hidden"),t.length>0&&t[0].address_components.length>0){var s=t[0].address_components[0].short_name;t[0].address_components.length>1&&(s+=" ("+t[0].address_components[1].short_name+")"),e.children("#location").children("a").text(s)}e.children("#location").click(function(){viewport=t[0].geometry.bounds,$("#search_expr").val(""),map.fitBounds(viewport)})}}),$("#no-result #cde-remove-keywords").click(function(){$("#search_expr").val(""),getRaces()}),$("#no-result #cde-full-year").click(function(){$("#start_date").val(default_start_date),$("#end_date").val(default_end_date),getRaces()}),$("#no-result #cde-all-distances").click(function(){$(".distance_selector").removeClass("active"),$(this).prop("checked",!1),getRaces()}),$("#no-result #cde-all-distances").click(function(){resetSearchForm()}),$("#no-result #cde-full-map").click(function(){var e=new google.maps.LatLng(default_boundsarray[0],default_boundsarray[1]),t=new google.maps.LatLng(default_boundsarray[2],default_boundsarray[3]),a=new google.maps.LatLngBounds(e,t);map.fitBounds(a),getRaces()})}function refreshRacesOnMap(e){for(var t in markers)markers[t].setMap(null);markers={},$.each(e,function(e,t){var a=t.rankClass,s=new google.maps.LatLng(t.lat,t.lng),r=new google.maps.Marker({position:s,map:map,id:t.id,icon:markerIcons[a]["default"],zIndex:1,rankClass:a});markers[t.id]=r,addListMarkerClick(r),addListHoverMapResult(r)}),selectEvent(selected_event_id,!1)}function selectEvent(e,t){if(t="undefined"==typeof t?!0:t,void 0!==markers[selected_event_id]&&($("#event_"+selected_event_id).removeClass("active"),a=markers[selected_event_id],a.setIcon(markerIcons[a.rankClass]["default"])),selected_event_id=e,void 0!==markers[selected_event_id]&&$("#event_"+selected_event_id).length){$("#event_"+selected_event_id).addClass("active"),t?$("#sidebox").animate({scrollTop:$("#sidebox").scrollTop()+$("#event_"+selected_event_id).offset().top-150},500):$("#sidebox").scrollTop($("#event_"+selected_event_id).offset().top-150);var a=markers[selected_event_id];a.setIcon(markerIcons[a.rankClass].selected),a.setZIndex(highest_Z_index+1),highest_Z_index+=1}}function resetSearchForm(){viewport=default_cache_bounds,$("#search_expr").val(default_search_expr),$("#start_date").val(default_start_date),$("#end_date").val(default_end_date),$(".distance_selector").removeClass("active"),$(".distance_selector > input").each(function(){$(this).prop("checked",!1)}),pushState(getParamQuery()),getRaces()}function highlightResult(e){if($("#event_"+e).addClass("mouseover"),e!=selected_event_id){var t=markers[e];t.setIcon(markerIcons[t.rankClass].hover)}}function deHighlightResult(e){$("#event_"+e).removeClass("mouseover");var t;e!=selected_event_id?(t=markers[e],t.setIcon(markerIcons[t.rankClass]["default"])):(t=markers[e],t.setIcon(markerIcons[t.rankClass].selected))}function getParameterByName(e){e=e.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]");var t=new RegExp("[\\?&]"+e+"=([^&#]*)"),a=t.exec(location.search);return null===a?"":decodeURIComponent(a[1].replace(/\+/g," "))}function pushState(e){var t={param_query:e};manualStateChange=!1,History.pushState(t,"index","/search?"+e),last_query=e}var map=null,viewport,last_query,markers={},selected_event_id="",search_sport="",search_distances="",search_start_date="",search_end_date="",search_expr="",highest_Z_index=10,markerIcons={},primaryIcons={},secondaryIcons={},manualStateChange=!1;if("undefined"==typeof map_styles)var map_styles=[];"undefined"!=typeof google&&google.maps.event.addDomListener(window,"load",initialize);var csrftoken=getCookie("csrftoken");History.Adapter.bind(window,"statechange",function(){var e=History.getState();null!==e&&(manualStateChange===!0&&(ajaxLoad(e.data.param_query),google.maps.event.clearListeners(map,"idle"),initializeDOMComponents(),google.maps.event.addListenerOnce(map,"idle",function(){addListMapMoves()})),manualStateChange=!0)});