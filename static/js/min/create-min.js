function initialize(){"object"==typeof google&&"object"==typeof google.maps&&(autocomplete=new google.maps.places.Autocomplete(document.getElementById("autocompleteInput"),{types:["geocode"]}),google.maps.event.addListener(autocomplete,"place_changed",function(){fillInAddress()})),createDatePickerComponent()}function createDatePickerComponent(){$(".datepicker").datepicker({format:"yyyy-mm-dd",language:"fr",autoclose:!0,clearBtn:!0,todayHighlight:!0,todayBtn:"linked"})}function fillInAddress(){var e=autocomplete.getPlace();$("#location-form :input:not(:hidden)").val("");for(var o=0;o<e.address_components.length;o++){var t=e.address_components[o].types[0],a=componentForm[t];if(a.length)for(var n=0;n<a.length;n++){var i=e.address_components[o][a[n].selector];document.getElementById(a[n].id).value=i}}document.getElementById("id_location-lat").value=e.geometry.location.lat().toFixed(5),document.getElementById("id_location-lng").value=e.geometry.location.lng().toFixed(5)}function geolocate(){navigator.geolocation&&navigator.geolocation.getCurrentPosition(function(e){var o=new google.maps.LatLng(e.coords.latitude,e.coords.longitude),t=new google.maps.Circle({center:o,radius:e.coords.accuracy});autocomplete.setBounds(t.getBounds())})}var componentForm={street_number:[{id:"id_location-street_number",selector:"short_name"}],route:[{id:"id_location-route",selector:"short_name"}],locality:[{id:"id_location-locality",selector:"short_name"}],administrative_area_level_1:[{id:"id_location-administrative_area_level_1_short_name",selector:"short_name"},{id:"id_location-administrative_area_level_1",selector:"long_name"}],administrative_area_level_2:[{id:"id_location-administrative_area_level_2_short_name",selector:"short_name"},{id:"id_location-administrative_area_level_2",selector:"long_name"}],country:[{id:"id_location-country",selector:"short_name"}],postal_code:[{id:"id_location-postal_code",selector:"short_name"}]};$(document).ready(function(){initialize()});