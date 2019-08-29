var colors =  ['brown','navy', 'grey', 'fuchsia', 'lime', 'red', 'green', 'silver', 'olive', 'blue', 'yellow', 'teal'];

function initMap() {
     var mapSettings= {
     center:new google.maps.LatLng(53.350140,-6.266155),
     zoom:7,
     };
     map = new google.maps.Map(document.getElementById("map"),mapSettings);

     var input = document.getElementById('search');
     var searchBox = new google.maps.places.SearchBox(input);
     var add_location_b = document.getElementById('add_location_b');

     var cities = "";
     var markers = [];
     var new_markers = [];
     var ltlg = [];

     var base_icon = {
          url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
          scaledSize: new google.maps.Size(50, 40)
     };


     map.addListener('bounds_changed', function() {
          searchBox.setBounds(map.getBounds());
     });

     searchBox.addListener('places_changed', function () {
          var places = searchBox.getPlaces();

          new_markers.forEach(function(m){
               m.setMap(null);
          });
          new_markers = [];

          if (places.length == 0)
               return;



          var bounds = new google.maps.LatLngBounds();
          p = places[0]
          if (!p.geometry)
               return;

          if (p.geometry.viewport)
               bounds.union(p.geometry.viewport);
          else
               bounds.extend(p.geometry.location);

          map.fitBounds(bounds);
          if (ltlg.indexOf(JSON.stringify(p.geometry.location)) == -1){
               if (markers.length == 0){
                    new_markers.push(new google.maps.Marker({
                         position: p.geometry.location,
                         animation: google.maps.Animation.BOUNCE,
                         map: map,
                         icon: base_icon
                    }));
               }
               else{
                    new_markers.push(new google.maps.Marker({
                         position: p.geometry.location,
                         animation: google.maps.Animation.BOUNCE,
                         map: map
                    }));
               }
          }


          add_location_b.onclick = function(){
               new_markers.forEach(function(m){
                    m.setMap(null);
               });


               if (ltlg.indexOf(JSON.stringify(p.geometry.location)) == -1){
                    if (markers.length == 0){
                         markers.push(new google.maps.Marker({
                              position: p.geometry.location,
                              map: map,
                              icon: base_icon
                         }));
                    }
                    else{
                         markers.push(new google.maps.Marker({
                              position: p.geometry.location,
                              map: map
                         }));
                    }
                    ltlg.push(JSON.stringify(p.geometry.location));
                    var city_name = p.formatted_address.replace(/\s/g,'');
                    console.log(city_name);
                    coordinates[city_name] = p.geometry.location;
                    console.log(JSON.stringify(coordinates[city_name]))
                    cities = cities + p.formatted_address + "|";
                    console.log(cities);
                    console.log("added marker");
               }

               if (markers.length > 1) {
                    var bounds = new google.maps.LatLngBounds();
                    for (var i = 0; i < markers.length; i++) {
                         bounds.extend(markers[i].getPosition());
                    }
                    map.fitBounds(bounds);
               }
          };

     });

     driver_select = document.getElementById("driver-select");
     input_drivers = document.getElementById("no-drivers");
     driver_select.addEventListener("change", function() {

          if(driver_select.value === "flexible"){
               input_drivers.readOnly = true;
               input_drivers.style.background = "grey";
               input_drivers.style.border = "grey";
               input_drivers.style.color = "grey";
          }
          else{
               input_drivers.readOnly = false;
               input_drivers.style.background = "white";
               input_drivers.style.border = "white";
               input_drivers.style.color = "black";

          }
     });


     document.getElementById("compute_route_b").onclick = function() {
          document.getElementById("cities").value = cities;
     };

}

function initTestMap(){
     var mapSettings= {
     center:new google.maps.LatLng(53.350140,-6.266155),
     zoom:7,
     };
     map = new google.maps.Map(document.getElementById("map"),mapSettings);

     var input = document.getElementById('search');
     var searchBox = new google.maps.places.SearchBox(input);
     var add_location_b = document.getElementById('add_location_b');
     addMarker({"lat":53.3498053,"lng":-6.260309699999993}, "", true);
     var bounds = new google.maps.LatLngBounds();

     for(var key in coordinates){
       addMarker(coordinates[key], "", false);
       bounds.extend(coordinates[key])
     }
     map.fitBounds(bounds);

     var markers = [];
     var new_markers = [];
     var ltlg = [];
     var base_icon = {
          url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
          scaledSize: new google.maps.Size(50, 40)
     };





     driver_select = document.getElementById("driver-select");
     input_drivers = document.getElementById("no-drivers");
     driver_select.addEventListener("change", function() {

          if(driver_select.value === "flexible"){
               input_drivers.readOnly = true;
               input_drivers.style.background = "grey";
               input_drivers.style.border = "grey";
               input_drivers.style.color = "grey";
          }
          else{
               input_drivers.readOnly = false;
               input_drivers.style.background = "white";
               input_drivers.style.border = "white";
               input_drivers.style.color = "black";

          }
     });




     document.getElementById("compute_route_b").onclick = function() {
          var cities = "Dublin,Ireland|Sligo,Ireland|Athlone,Co.Westmeath,Ireland|Belfast,UK|NewtownardsBT23,UK|Dundonald,BelfastBT16,UK|GalwayBusinessPark,Barnacranny,Co.Galway,Ireland|LeitrimNorth,Cloonacool,Co.Sligo,Ireland|Tobercurry,Co.Sligo,Ireland|Athenry,Co.Galway,Ireland|Tuam,Co.Galway,Ireland|DooradoyleRd,Dooradoyle,Limerick,Ireland|LatoonNorth,Latoon,Co.Clare,Ireland|Nenagh,Co.Tipperary,Ireland|Kilkenny,Co.Kilkenny,Ireland|Carlow,Ireland|Rinn,Collooney,Co.Sligo,Ireland|"
          document.getElementById("cities").value = cities;
          console.log("test");
     };

}


function initResultsMap(){
     var mapSettings= {
     center:new google.maps.LatLng(53.350140,-6.266155),
     zoom:7,
     };
     map = new google.maps.Map(document.getElementById("map"),mapSettings);
}


function calculateAndDisplayRoute(data) {
    data  = JSON.parse(data);
    console.log(data);


    var i = 0;
     data.forEach(function(route){
          var directionsService = new google.maps.DirectionsService;
          var directionsDisplay = new google.maps.DirectionsRenderer({
                    polylineOptions: {
                         strokeColor: colors[i]
                    },
                    suppressMarkers: true
               }
          );

          i++;

          var wypts = [];
          route.waypoints.forEach(function(location){
            wypts.push({
                 location: location,
                 stopover: true
            });
          });

          directionsService.route({
               origin: route.depot,
               destination: route.depot,
               waypoints: wypts,
               travelMode: 'DRIVING'
               }, function(response, status) {
               if (status === 'OK') {

                    directionsDisplay.setDirections(response);
                    var depot = response.routes[ 0 ].legs[ 0 ].start_location;
                    addMarker(depot, "", true);
                    position = 0

               } else {
                    window.alert('Directions request failed due to ' + status);
               }
          });


          var geocoder = new google.maps.Geocoder();
          var j = 1;
          route.waypoints.forEach(function(wp){
               geocoder.geocode( { 'address' : wp }, function( results, status ) {
                 console.log(wp + ":" + status);
                    if( status == google.maps.GeocoderStatus.OK ) {
                        addMarker(results[0].geometry.location, j + "", false);
                      }
                      j++;
               });
          });

          directionsDisplay.setMap(map);
     });


}

function testCalculateAndDisplayRoute(data) {
    data  = JSON.parse(data);
    console.log(data);

    var i = 0;
     data.forEach(function(route){
          var directionsService = new google.maps.DirectionsService;
          var directionsDisplay = new google.maps.DirectionsRenderer({
                    polylineOptions: {
                         strokeColor: colors[i]
                    },
                    suppressMarkers: true

               }
          );

          i++;

          var wypts = [];
          route.waypoints.forEach(function(location){
            wypts.push({
                 location: location,
                 stopover: true
            });
          });

          directionsService.route({
               origin: route.depot,
               destination: route.depot,
               waypoints: wypts,
               travelMode: 'DRIVING'
               }, function(response, status) {
               if (status === 'OK') {

                    directionsDisplay.setDirections(response);
                    addMarker({"lat":53.3498053,"lng":-6.260309699999993}, "", true);
                    position = 0

               } else {
                    window.alert('Directions request failed due to ' + status);
               }
          });


          var j = 1;
          route.waypoints.forEach(function(wp){
                 console.log('I am in test compute');
                        addMarker(coordinates[wp], j + "", false);
                      j++;
          });

          directionsDisplay.setMap(map);
     });


}

function addMarker(position, label, depot) {
     var base_icon = {
          url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
          scaledSize: new google.maps.Size(50, 40)
     };

     if(depot === true){
          new google.maps.Marker({
               position: position,
               map: map,
               icon: base_icon
          });
     }
     else{
          new google.maps.Marker({
               position: position,
               map: map,
               label: label
          });
     }
}
