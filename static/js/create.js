 var componentForm = {
  street_number : [{id: "id_location-street_number", selector: "short_name"}],
  route : [{id: "id_location-route", selector: "short_name"}],
  locality : [{id: "id_location-locality", selector: "short_name"}],
  administrative_area_level_1 : [
    {id: "id_location-administrative_area_level_1_short_name", selector: "short_name"},
    {id: "id_location-administrative_area_level_1", selector: "long_name"}
    ],
  administrative_area_level_2 : [
    {id: "id_location-administrative_area_level_2_short_name", selector: "short_name"},
    {id: "id_location-administrative_area_level_2", selector: "long_name"}
    ],
  country : [{id: "id_location-country", selector: "short_name"}],
  postal_code : [{id: "id_location-postal_code", selector: "short_name"}],
};

$(document).ready(function() {
  initialize();
});

function initialize() {
  // Create the autocomplete object, restricting the search
  // to geographical location types.
  if (typeof google === 'object' && typeof google.maps === 'object'){
    autocomplete = new google.maps.places.Autocomplete(
        (document.getElementById('autocompleteInput')),{ types: ['geocode'] });
    // When the user selects an address from the dropdown,
    // populate the address fields in the form.
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
      fillInAddress();
    });
  }

  createDatePickerComponent();

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


// [START region_fillform]
function fillInAddress() {
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();


  $("#location-form :input:not(:hidden)").val('');

  // Get each component of the address from the place details
  // and fill the corresponding field on the form.
  for (var i = 0; i < place.address_components.length; i++) {

    var addressType = place.address_components[i].types[0];

    // find form components correpsonding to that address type
    var componentArray = componentForm[addressType]
 
    if (componentArray.length) { 
      for (var j = 0; j < componentArray.length; j++) {
        var val = place.address_components[i][componentArray[j].selector];
        document.getElementById(componentArray[j].id).value = val;
      }
    }

  }

    document.getElementById('id_location-lat').value = place.geometry.location.lat().toFixed(5);
    document.getElementById('id_location-lng').value = place.geometry.location.lng().toFixed(5);
}
// [END region_fillform]

// [START region_geolocation]
// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = new google.maps.LatLng(
          position.coords.latitude, position.coords.longitude);
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}