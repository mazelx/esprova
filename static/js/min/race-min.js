function addListRaceDisplayMap(){$("#link-display-map").click(function(e){$("#address-map").is(":hidden")?$("#address-map").show("fast",function(){map.set({styles:map_styles}),google.maps.event.trigger(map,"resize"),map.setCenter({lat:lat,lng:lng})}):$("#address-map").hide("fast")})}function createMap(){"undefined"==typeof map_styles&&(map_styles=[]),map=new google.maps.Map(document.getElementById("address-map"),mapOptions),map.setOptions({styles:map_styles});var e=new google.maps.Marker({position:{lat:lat,lng:lng},map:map,zIndex:1})}function getCookie(e){var a=null;if(document.cookie&&""!=document.cookie)for(var t=document.cookie.split(";"),o=0;o<t.length;o++){var n=jQuery.trim(t[o]);if(n.substring(0,e.length+1)==e+"="){a=decodeURIComponent(n.substring(e.length+1));break}}return a}function csrfSafeMethod(e){return/^(GET|HEAD|OPTIONS|TRACE)$/.test(e)}function validateRace(e){$.ajax({url:"/ajx/validate/"+e,type:"PUT",success:function(e,a){alert("validé")}})}function deleteRace(e){$.ajax({url:"/ajx/delete/"+e,type:"DELETE",success:function(e,a){alert("supprimé"),window.location.replace("/list")}})}var mapOptions,lat,lng;google.maps.event.addDomListener(window,"load",createMap),$(document).ready(function(){lat=parseFloat($("#race-location").data("lat")),lng=parseFloat($("#race-location").data("lng")),mapOptions={mapTypeId:google.maps.MapTypeId.TERRAIN,center:{lat:lat,lng:lng},zoom:10,maxZoom:15,panControl:!1,zoomControl:!0,streetViewControl:!1},addListRaceDisplayMap()});var csrftoken=getCookie("csrftoken");$.ajaxSetup({beforeSend:function(e,a){csrfSafeMethod(a.type)||this.crossDomain||e.setRequestHeader("X-CSRFToken",csrftoken)}});