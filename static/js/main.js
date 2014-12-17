var map;

function initialize() {
  var mapOptions = {
    center: { lat: 44.301683, lng: 4.5656561},
    zoom: 8,
    panControl: false,
    streetViewControl: false
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  google.maps.event.addListener(map, 'bounds_changed', function() {
    getRacesFromMapBounds(map.getBounds().toUrlValue())
  });

}


function addRaceMarker(_name, _ltlng) {
  var myLatlng = new google.maps.LatLng(_latlng);
  var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    title: _name
  });
}

function getRacesFromMapBounds(mapbounds) {
  boundsarray = mapbounds.split(',')
  $.ajax({
    url : '/racejson/?',
    type : 'GET', // Le type de la requête HTTP, ici devenu POST
    data : 'lat_lo=' + boundsarray[0] + '&lng_lo=' + boundsarray[1] + '&lat_hi=' + boundsarray[2] + '&lng_hi=' + boundsarray[3],
    dataType : 'html',
    success : function(response, statut){
      fillRacesOnResults(response);
      setRacesOnMap(response);
      ;
    },
  });
}

function fillRacesOnResults(json) {
  $("#racelist").html(json);
}

function setRacesOnMap(json) {
  // var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
  var myLatlng = new google.maps.LatLng(44.301683, 4.5656561);

  // To add the marker to the map, use the 'map' property
    var marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      title:"Hello World!"
    });
}


