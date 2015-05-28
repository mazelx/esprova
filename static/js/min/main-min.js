"use strict";function RefreshOptions(e){"undefined"==typeof e?(this.refreshMap=!0,this.refreshSidebar=!0,this.fullRefresh=!1):(this.refreshMap="undefined"==typeof e.refreshMap?!0:e.refreshMap,this.refreshSidebar="undefined"==typeof e.refreshSidebar?!0:e.refreshSidebar,this.fullRefresh="undefined"==typeof e.fullRefresh?!1:e.fullRefresh)}function initialize(){page_title=document.title,search_sport=default_sport,viewport=default_search_bounds,search_distances=default_distances,search_start_date=default_start_date,search_end_date=default_end_date,search_expr=default_search_expr,primaryIcons["default"]={url:static_url+"images/primary_marker_default.svg",size:new google.maps.Size(28,42)},primaryIcons.selected={url:static_url+"images/primary_marker_selected.svg",size:new google.maps.Size(28,42)},primaryIcons.hover={url:static_url+"images/primary_marker_hover.svg",size:new google.maps.Size(28,42)},secondaryIcons["default"]={url:static_url+"images/marker_default.png",scaledSize:new google.maps.Size(10,10),anchor:new google.maps.Point(4,4)},secondaryIcons.selected={url:static_url+"images/marker_selected.png",scaledSize:new google.maps.Size(14,14),anchor:new google.maps.Point(7,7)},secondaryIcons.hover={url:static_url+"images/marker_hover.png",scaledSize:new google.maps.Size(10,10),anchor:new google.maps.Point(4,4)},markerIcons.primary=primaryIcons,markerIcons.secondary=secondaryIcons,native_datepicker||($("input[type=date]").attr("type","text"),createDatePickerComponent()),$("#map-canvas").is(":hidden")?(map_hidden=!0,getRaces()):initializeMap(),$.ajaxSetup({beforeSend:function(e,t){csrfSafeMethod(t.type)||this.crossDomain||e.setRequestHeader("X-CSRFToken",csrftoken)}}),addListWindowResize(),addListMapMoves(),addListSearch(),addListResultClick(),addListResetForm(),addListSportSelection(),addListSideboxScroll(),initializeMapZoomControl(),initializeDOMComponents(),getRaces({fullRefresh:!0})}function csrfSafeMethod(e){return/^(GET|HEAD|OPTIONS|TRACE)$/.test(e)}function getCookie(e){var t=null;if(document.cookie&&""!==document.cookie)for(var a=document.cookie.split(";"),s=0;s<a.length;s++){var r=jQuery.trim(a[s]);if(r.substring(0,e.length+1)===e+"="){t=decodeURIComponent(r.substring(e.length+1));break}}return t}function initializeMap(){var e={mapTypeId:google.maps.MapTypeId.TERRAIN,center:{lat:default_lat,lng:default_lng},maxZoom:15,minZoom:5,panControl:!1,zoomControl:!1,streetViewControl:!1};map=new google.maps.Map(document.getElementById("map-canvas"),e),map.setOptions({styles:map_styles})}function initializeMapZoomControl(){map&&($("#cd-zoom-in").click(function(){map.setZoom(map.getZoom()+1)}),$("#cd-zoom-out").click(function(){map.setZoom(map.getZoom()-1)}))}function getDistanceInfo(e){$.ajax({url:"api/distance/"+e,type:"GET",dataType:"json"}).done(function(e){$("#sport-distances-helper").html(e.helper_html),refreshDistances(e.distances)}).fail(function(){$("#sport-distances-helper").html("")})}function createDatePickerComponent(){$("#datepicker").datepicker({format:"yyyy-mm-dd",language:"fr",autoclose:!0,clearBtn:!0,todayHighlight:!0,todayBtn:"linked"})}function initializeDOMComponents(){search_sport=getParameterByName("sport"),""!==search_sport?saveSportSession(search_sport):search_sport=default_sport,$("#sport-selecter").val(search_sport),getDistanceInfo(search_sport);var t=getParameterByName("viewport");viewport=""===t?default_search_bounds:t.split(",");var a=viewport[0],s=viewport[1],r=viewport[2],n=viewport[3];if(map&&""!==a&&""!==r&&""!==s&&""!==n){var i=new google.maps.LatLng(parseFloat(r),parseFloat(s)),o=new google.maps.LatLng(parseFloat(a),parseFloat(n)),d=new google.maps.LatLngBounds(i,o);""===getParameterByName("z")?map.fitBounds(d):(map.setCenter(d.getCenter()),map.setZoom(parseInt(getParameterByName("z"))))}search_start_date=getParameterByName("start_date")||default_start_date,$("#start_date").val(search_start_date),search_end_date=getParameterByName("end_date")||default_end_date,$("#end_date").val(search_end_date),search_expr=getParameterByName("search_expr")||default_search_expr,$("#search_expr").val(search_expr),native_datepicker||(delListSearch(),$("#start_date").datepicker("update"),$("#end_date").datepicker("update"),addListSearch()),e;var c=getParameterByName("active");if(selected_event_id=""!==c?parseInt(c):"",search_distances=getParameterByName("distances"),""!==search_distances){var l=search_distances.split(",");setCheckDistanceInput("XS",-1!==l.indexOf("XS")),setCheckDistanceInput("S",-1!==l.indexOf("S")),setCheckDistanceInput("M",-1!==l.indexOf("M")),setCheckDistanceInput("L",-1!==l.indexOf("L")),setCheckDistanceInput("XL",-1!==l.indexOf("XL"))}}function setCheckDistanceInput(e,t){$("#distance_input_"+e).prop("checked",!1),$("#distance_selector_"+e).removeClass("active"),t&&($("#distance_input_"+e).prop("checked",!0),$("#distance_selector_"+e).addClass("active"))}function addListSideboxScroll(){function e(){$(window).scrollTop()>=a?t.addClass("sticky-xs"):t.removeClass("sticky sticky-xs")}var t=$("#filter-cde"),a=$("#filter-cde").offset().top;document.onscroll=e,$("#filter-cde-top").on("click",function(e){e.preventDefault(),window.scrollTo(0,0),$("#sidebox").scrollTop(0)}),$("#filter-cde-reset").on("click",function(e){e.preventDefault(),resetSearchForm()})}function addListWindowResize(){$(window).on("resize",function(){var e=$("#map-canvas").is(":hidden");!map_hidden&&e?map_hidden=!0:map_hidden&&!e&&(initializeMap(),getRaces(new RefreshOptions),map_hidden=!1)})}function saveSportSession(e){e&&$.ajax({url:"/api/sport-session/",data:{sport:e},type:"POST"}).done(function(){search_sport=e})}function addListSportSelection(){$("#sport-selecter").on("change",function(e){e.preventDefault(),saveSportSession(e.currentTarget.value),resetSearchForm()})}function addListMapMoves(){map&&google.maps.event.addListenerOnce(map,"idle",function(){google.maps.event.addListener(map,"idle",function(){$("#follow_map_bounds").is(":checked")&&$(".mapbox").is(":visible")&&(viewport=map.getBounds().toUrlValue().split(","),getRaces(new RefreshOptions({refreshMap:!1})),pushState(getParamQuery()))})})}function addListMarkerClick(e){map&&google.maps.event.addListener(e,"click",function(){selectEvent(e.get("id")),pushState(getParamQuery())})}function addListResultClick(){$(".search-result").click(function(e){selectEvent(e.currentTarget.id.replace("event_","")),$(".search-result").removeClass("active"),$(e.currentTarget).addClass("active"),pushState(getParamQuery())})}function addListSearch(){$("#race_search_form").on("change submit",function(e){e.preventDefault(),$("#race_search_form").serialize(),search_distances=default_distances,$.each($(".distance_input").serialize().split("&"),function(e,t){t&&(search_distances+=t.split("=")[1]+",")}),search_expr=$("#search_expr").val(),search_start_date=$("#start_date").val(),search_end_date=$("#end_date").val(),getRaces(new RefreshOptions({fullRefresh:!0})),selected_event_id="",pushState(getParamQuery())})}function delListSearch(){$("#race_search_form").off("change submit")}function addListResetForm(){$("#reset-search-form").click(function(){resetSearchForm()})}function addListHoverSideboxResult(){$(".search-result").hover(function(){highlightResult($(this)[0].id.replace("event_",""))},function(){deHighlightResult($(this)[0].id.replace("event_",""))})}function addListHoverMapResult(e){map&&(google.maps.event.addListener(e,"mouseover",function(){highlightResult(e.get("id"))}),google.maps.event.addListener(e,"mouseout",function(){deHighlightResult(e.get("id"))}))}function getParamQuery(){var e=map?map.getZoom():"",t="sport="+search_sport;return viewport="undefined"==typeof viewport||""===viewport?default_search_bounds:viewport,t+=search_expr?"&q="+search_expr:"",t+=search_start_date?"&start_date="+search_start_date:"",t+=search_end_date?"&end_date="+search_end_date:"",t+=search_distances?"&distances="+search_distances:"",t+="&viewport="+viewport[0],t+=","+viewport[1],t+=","+viewport[2],t+=","+viewport[3],t+="&z="+e,t+=selected_event_id?"&active="+selected_event_id:""}function getRaces(e){var t;t=getParamQuery(),t!==last_query&&ajaxLoad(t,e)}function ajaxLoad(e,t,a){if("undefined"==typeof t&&(t=new RefreshOptions),$("#racelist").html("<div class='spinner'><i class='fa fa-spinner fa-pulse'></i></div>"),$("#filter-cde-results").html("<i class='fa fa-spinner fa-pulse'></i>"),t.fullRefresh){var s=viewport;viewport=default_cache_bounds,ajaxLoad(getParamQuery(),new RefreshOptions({refreshSidebar:!1}),function(){viewport=s,ajaxLoad(getParamQuery(),new RefreshOptions({refreshMap:!1}))}),viewport=s}else last_query_options_loaded!==e+JSON.stringify(t)&&$.ajax({url:"api/races/",type:"GET",data:e,dataType:"json",timeout:4e4}).done(function(s){t.refreshSidebar&&refreshRacesOnSidebar(s.html,s.count),t.refreshMap&&!map_hidden&&refreshRacesOnMap(s.races),last_query_options_loaded=e+JSON.stringify(t),"function"==typeof a&&a()}).fail(function(){$("#racelist").html("<div class='alert alert-danger' role='alert'>Une erreur est survenue, veuillez contacter <a href='mailto:contact@esprova.com?subject=[issue]:[ajaxLoad]'>le support</a></div>")})}function refreshRacesOnSidebar(e,t){$("#racelist").html(e),$("#filter-cde-results").html(t+(t>1?" courses":" course")),addListResultClick(),addListHoverSideboxResult(),selectEvent(selected_event_id,!1),0===t&&handleNoResult()}function handleNoResult(){var e=$("#try-location-search"),t=e.data("expr"),a=new google.maps.Geocoder;"None"!==t&&map_hidden===!1&&a.geocode({address:t,region:"fr"},function(t,a){if(a==google.maps.GeocoderStatus.OK){if(e.removeClass("hidden"),t.length>0&&t[0].address_components.length>0){var s=t[0].address_components[0].short_name;t[0].address_components.length>1&&(s+=" ("+t[0].address_components[1].short_name+")"),e.children("#location").children("a").text(s)}e.children("#location").click(function(){viewport=t[0].geometry.bounds,$("#search_expr").val(""),map.fitBounds(viewport)})}}),search_expr!==default_search_expr&&($("#no-result #cde-remove-keywords").removeClass("hidden"),$("#no-result #cde-remove-keywords").click(function(){$("#search_expr").val(""),search_expr=default_search_expr,getRaces()})),(search_start_date!==default_start_date||search_end_date!==default_end_date)&&($("#no-result #cde-full-year").removeClass("hidden"),$("#no-result #cde-full-year").click(function(){$("#start_date").val(default_start_date),search_start_date=default_start_date,$("#end_date").val(default_end_date),search_end_date=default_end_date,getRaces()})),search_distances!==default_distances&&($("#no-result #cde-all-distances").removeClass("hidden"),$("#no-result #cde-all-distances").click(function(){$(".distance_selector").removeClass("active"),$(this).prop("checked",!1),search_distances=default_distances,getRaces()})),$("#no-result #cde-reset-form").click(function(){resetSearchForm()}),viewport!==default_search_bounds&&($("#no-result #cde-full-map").removeClass("hidden"),$("#no-result #cde-full-map").click(function(){var e=new google.maps.LatLng(default_search_bounds[0],default_search_bounds[1]),t=new google.maps.LatLng(default_search_bounds[2],default_search_bounds[3]),a=new google.maps.LatLngBounds(e,t);map.fitBounds(a),viewport=default_search_bounds,getRaces()}))}function refreshRacesOnMap(e){for(var t in markers)markers[t].setMap(null);markers={},$.each(e,function(e,t){var a=t.rankClass,s=new google.maps.LatLng(t.lat,t.lng),r=new google.maps.Marker({position:s,map:map,id:t.id,icon:markerIcons[a]["default"],zIndex:1,rankClass:a});markers[t.id]=r,addListMarkerClick(r),addListHoverMapResult(r)}),selectEvent(selected_event_id,!1)}function refreshDistances(e){$(".distance_selector").removeClass("hidden"),e.indexOf("XS")<0&&$("#distance_selector_XS").addClass("hidden"),e.indexOf("S")<0&&$("#distance_selector_S").addClass("hidden"),e.indexOf("M")<0&&$("#distance_selector_M").addClass("hidden"),e.indexOf("L")<0&&$("#distance_selector_L").addClass("hidden"),e.indexOf("XL")<0&&$("#distance_selector_XL").addClass("hidden")}function selectEvent(e,t){if(t="undefined"==typeof t?!0:t,void 0!==markers[selected_event_id]&&($("#event_"+selected_event_id).removeClass("active"),a=markers[selected_event_id],a.setIcon(markerIcons[a.rankClass]["default"])),selected_event_id=e,void 0!==markers[selected_event_id]&&$("#event_"+selected_event_id).length){$("#event_"+selected_event_id).addClass("active"),t?$("#sidebox").animate({scrollTop:$("#sidebox").scrollTop()+$("#event_"+selected_event_id).offset().top-150},500):$("#sidebox").scrollTop($("#event_"+selected_event_id).offset().top-150);var a=markers[selected_event_id];a.setIcon(markerIcons[a.rankClass].selected),a.setZIndex(highest_Z_index+1),highest_Z_index+=1}}function resetSearchForm(){window.location.href=window.location.pathname}function highlightResult(e){if($("#event_"+e).addClass("mouseover"),e!=selected_event_id){var t=markers[e];t.setIcon(markerIcons[t.rankClass].hover)}}function deHighlightResult(e){$("#event_"+e).removeClass("mouseover");var t;e!=selected_event_id?(t=markers[e],t.setIcon(markerIcons[t.rankClass]["default"])):(t=markers[e],t.setIcon(markerIcons[t.rankClass].selected))}function getParameterByName(e){e=e.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]");var t=new RegExp("[\\?&]"+e+"=([^&#]*)"),a=t.exec(location.search);return null===a?"":decodeURIComponent(a[1].replace(/\+/g," "))}function pushState(e){var t={param_query:e};manualStateChange=!1,last_query_pushed!==e&&(History.pushState(t,page_title+" - "+search_sport,"/races?"+e),last_query_pushed=e)}var map=null,last_query,markers={},highest_Z_index=10,markerIcons={},primaryIcons={},secondaryIcons={},last_query_pushed,last_query_options_loaded,viewport="",selected_event_id="",search_sport="",search_distances="",search_start_date="",search_end_date="",search_expr="",map_hidden=!1,native_datepicker=Modernizr.touch,manualStateChange=!1,page_title;if("undefined"==typeof map_styles)var map_styles=[];"undefined"!=typeof google&&google.maps.event.addDomListener(window,"load",initialize);var csrftoken=getCookie("csrftoken");History.Adapter.bind(window,"statechange",function(){var e=History.getState();null!==e&&(manualStateChange===!0&&(ajaxLoad(e.data.param_query),google.maps.event.clearListeners(map,"idle"),initializeDOMComponents(),google.maps.event.addListenerOnce(map,"idle",function(){addListMapMoves()})),manualStateChange=!0)});
//# sourceMappingURL=./main-min.js.map