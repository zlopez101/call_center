const user_input = document.getElementById('addressInput');
const user_submit = document.getElementById('userSubmit');
const bigWelcome = document.getElementById('bigWelcomeContainer')
const resultMap = document.getElementById('resultMap');
const resultContainer = document.getElementById("resultContainer");

//user_submit.addEventListener('click', function() {
//  console.log('successfully found the input key!');
//  console.log(user_input.value);
//  resultMap.src="https://maps.googleapis.com/maps/api/staticmap?center="+user_input.value+"&//markers="+user_input.value+"&zoom=13&size=500x700&key="+key
//  resultContainer.removeAttribute("hidden");
//});


var map, infoWindow;
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 29.7604, lng: 95.3698},
          zoom: 11
        });
        infoWindow = new google.maps.InfoWindow;
        
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('You are here.');
            infoWindow.open(map);
            map.setCenter(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
        map.data.loadGeoJson("https://utphysicians2--workingtitle.repl.co/api/locations_json")
      map.data.setStyle(feature => {
  return {
    icon: {
      url: `img/icon_${feature.getProperty('category')}.png`,
      scaledSize: new google.maps.Size(64, 64)
    }
  };
});
      }
      
      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }
