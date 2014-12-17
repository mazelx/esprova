function initialize() {
  var mapOptions = {
    center: { lat: 44.301683, lng: 4.5656561},
    zoom: 8,
    panControl: false,
    streetViewControl: false
  };
  var map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
}


function addRaceMarker(_name, _ltlng) {
  var myLatlng = new google.maps.LatLng(_latlng);
  var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    title: _name
  });
}