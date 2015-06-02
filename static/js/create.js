 
var native_datepicker = Modernizr.touch;

var mapOptions;
var marker;



var componentForm = {
  street_number : [{id: "id_location-street_number", selector: "short_name"}],
  route : [{id: "id_location-route", selector: "short_name"}],
  locality : [{id: "id_location-locality", selector: "short_name"}],
  // administrative_area_level_1 : [
  //   {id: "id_location-administrative_area_level_1_short_name", selector: "short_name"},
  //   {id: "id_location-administrative_area_level_1", selector: "long_name"}
  //   ],
  // administrative_area_level_2 : [
  //   {id: "id_location-administrative_area_level_2_short_name", selector: "short_name"},
  //   {id: "id_location-administrative_area_level_2", selector: "long_name"}
  //   ],
  country : [{id: "id_location-country", selector: "short_name"}],
  postal_code : [{id: "id_location-postal_code", selector: "short_name"}],
};

$(document).ready(function() {
  initialize();
});

function initialize() {
  if (typeof google === 'object' && typeof google.maps === 'object'){

  if(wizard_step === 'location') {
    if(typeof($("#id_location-lat")) !== "undefined"){
      lat = parseFloat( $("#id_location-lat").val());
      lng = parseFloat( $("#id_location-lng").val());
    }
      
      mapOptions = {
          mapTypeId: google.maps.MapTypeId.TERRAIN,
          center: {
              lat: lat,
              lng: lng
          },
          zoom: 8,
          maxZoom: 15,
          // minZoom:5,   
          panControl: false,
          zoomControl: true,
          streetViewControl: false
      };

      if(!lat || !lng) {
          mapOptions.center = {
                  lat: 46.9,
                  lng: 2.6
          }
          mapOptions.zoom = 5
      } 
      createMap();



      // Create the autocomplete object, restricting the search
      // to geographical location types.
      autocomplete = new google.maps.places.Autocomplete(
          (document.getElementById('autocompleteInput')),{ types: ['geocode'] });
      // When the user selects an address from the dropdown,
      // populate the address fields in the form.
      google.maps.event.addListener(autocomplete, 'place_changed', function() {
        clearForm();
        changeAddress();
      });
    }

  }

  if (!native_datepicker) {
        $("input[type=date]").attr("type", "text");
        createDatePickerComponent();
    }
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

function createMap(){
    if (typeof map_styles === 'undefined'){
        map_styles = [];
    }
        map = new google.maps.Map(document.getElementById('address-map'),
            mapOptions);
        map.setOptions({styles: map_styles});

        marker = new google.maps.Marker({
            position: {lat:lat, lng:lng} ,
            map: map,
            zIndex : 1,
        });
}   

function clearForm() {
  var frm_elements = document.getElementById("edit-form").elements
  for(i=0; i<frm_elements.length; i++) {
    field_type = frm_elements[i].type.toLowerCase();
    
    // do not clear the crsf token
    if(frm_elements[i].name === 'csrfmiddlewaretoken'){
      break;
    }

    switch (field_type)
    {
    case "text":
    case "password":
    case "textarea":
    case "hidden":
        frm_elements[i].value = "";
        break;
    case "radio":
    case "checkbox":
        if (frm_elements[i].checked)
        {
            frm_elements[i].checked = false;
        }
        break;
    case "select-one":
    case "select-multi":
        frm_elements[i].selectedIndex = -1;
        break;
    default:
        break;
    }
  }
}

// [START region_fillform]
function changeAddress() {
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();


  $("#location-form :input:not(:hidden)").val('');

  // Get each component of the address from the place details
  // and fill the corresponding field on the form.
  for (var i = 0; i < place.address_components.length; i++) {

    var addressType = place.address_components[i].types[0];

    // find form components corresponding to that address type
    var componentArray = componentForm[addressType]
 
    if (typeof(componentArray) !== 'undefined') { 
      for (var j = 0; j < componentArray.length; j++) {
        var val = place.address_components[i][componentArray[j].selector];
        document.getElementById(componentArray[j].id).value = val;
      }
    }

  }

  if(wizard_step === 'location') {
    // remove the marker from the map
    marker.setMap(null);

    lat = place.geometry.location.lat();
    lng = place.geometry.location.lng();

    marker = new google.maps.Marker({
            position: {lat:lat, lng:lng} ,
            map: map,
            zIndex : 1,
        });

    // center map on new marker
    map.setCenter(marker.getPosition());
    google.maps.event.addListenerOnce(map, 'bounds_changed', function(event) {
          if (this.getZoom()){
              this.setZoom(12);
          }
    });

    // save the lat /lng in the form
    document.getElementById('id_location-lat').value = lat.toFixed(5);
    document.getElementById('id_location-lng').value = lng.toFixed(5);
  }
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