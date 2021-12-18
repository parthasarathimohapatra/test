
var allLatLngArr = [];

// google.maps.event.addDomListener(window, 'load', initMap);

$(function() {
    
    console.log( "ready!" );
    var order_id = $( "input[name=order_id]" ).val();
    // alert("order_id = "+order_id);
    var url = "../../map_route_list_json/"+ order_id ;
    // alert("url = "+url);

    var latLngCoordinates = [];
        serverCall(url, null, 'get', true, null, null, null, function (res) {
            var slat = parseFloat(res[0].data.latLngSingle.latitude);
            var slng = parseFloat(res[0].data.latLngSingle.longitude);
            $( "#central_lat" ).val(slat);
            $( "#central_lng" ).val(slng);

            //Start lat lng
            var slat = parseFloat(res[0].data.latLngStart.latitude);
            var slng = parseFloat(res[0].data.latLngStart.longitude);
            $( "#start_lat" ).val(slat);
            $( "#start_lng" ).val(slng);

            //1st dropoff lat lng
            var slat = parseFloat(res[0].data.latLngFirstDrop.latitude);
            var slng = parseFloat(res[0].data.latLngFirstDrop.longitude);
            $( "#firstDrop_lat" ).val(slat);
            $( "#firstDrop_lng" ).val(slng);

            //2nd dropoff lat lng
            var slat = parseFloat(res[0].data.latLngSecDropoff.latitude);
            var slng = parseFloat(res[0].data.latLngSecDropoff.longitude);
            $( "#secondDrop_lat" ).val(slat);
            $( "#secondDrop_lng" ).val(slng);


            $.each(res[0].data.latLngList, function() {
             var obj = {};var centerpos = {};
              $.each(this, function(key, v) {
                if(key == "latitude"){
                    obj['lat']=parseFloat(v);
                }
                if(key == "longitude"){
                    obj['lng']=parseFloat(v);
                }
              });
              allLatLngArr.push(obj);
              // alert("in ajax allLatLngArr = "+JSON.stringify(allLatLngArr));
            });
            // alert("in ajax allLatLngArr = "+JSON.stringify(allLatLngArr));

              initMap(allLatLngArr);
            // initMap(allLatLngArr);
        });

      

    
        
        // google.maps.event.addDomListener(window, 'load', initMap);
        // $(document).ajaxStop(initMap);  
        function initMap(allLatLngArr) {
            var centerLat = parseFloat($("#central_lat").val());
            var centerLng = parseFloat($("#central_lng").val()); 

            var start_lat = parseFloat($("#start_lat").val());
            var start_lng = parseFloat($("#start_lng").val());

            var firstDrop_lat = parseFloat($("#firstDrop_lat").val());
            var firstDrop_lng = parseFloat($("#firstDrop_lng").val());

            var secondDrop_lat = parseFloat($("#secondDrop_lat").val());
            var secondDrop_lng = parseFloat($("#secondDrop_lng").val());

            var pickup_location = $("#location").val();
            var first_dropoff_loc = $("#drop_location_1").val();
            var second_dropoff_loc = $("#drop_location_2").val();

            var iconBase = 'https://diaxrbad0p1f6.cloudfront.net/static/images/';
            var icons = {
              start: {
                icon: iconBase + 'pickuser.png'
              },

              first_dropoff: {
                icon: iconBase + 'pind1.png'
              },
              second_dropoff: {
                icon: iconBase + 'pind2.png'
              }
            };
            // alert("centerLat = "+centerLat+" centerLng = "+centerLng);
            // alert("allLatLngArr = "+JSON.stringify(allLatLngArr));
                var map = new google.maps.Map(document.getElementById('map'), {
                  zoom: 15,
                  center: {lat: centerLat, lng: centerLng},
                  // alert(" centerpos lat = "+centerpos['lat']);
                  // center: centerpos,

                  mapTypeId: 'roadmap'
                });
                // var flightPlanCoordinates = [
                //   {lat: 37.772, lng: -122.214},
                //   {lat: 21.291, lng: -157.821},
                //   {lat: -18.142, lng: 178.431},
                //   {lat: -27.467, lng: 153.027}
                // ];
                // alert(" in map B4 flightPlanCoordinates = "+JSON.stringify(flightPlanCoordinates));
                var flightPlanCoordinates = allLatLngArr;
                // alert(" in map after flightPlanCoordinates = "+JSON.stringify(flightPlanCoordinates));
                var flightPath = new google.maps.Polyline({
                  path: flightPlanCoordinates,

                  geodesic: true,
                  strokeColor: '#138cff',
                  strokeOpacity: 1.0,
                  strokeWeight: 5
                });

                flightPath.setMap(map);
                // Map marker start

                var locations = [
                  ['<b>Pickup Location:</b>'+pickup_location, start_lat, start_lng,'start'],
                  ['<b>1st Dropoff Location : </b>'+first_dropoff_loc, firstDrop_lat, firstDrop_lng,'first_dropoff'],
                  ['<b>2nd Drop off location :</b>'+second_dropoff_loc, secondDrop_lat, secondDrop_lng,'second_dropoff']
                ];

                var infowindow = new google.maps.InfoWindow();

                var marker, i;

                for (i = 0; i < locations.length; i++) {  
                    // alert(locations[i][1]+", "+locations[i][2]);
                      var icon = {
                            url: icons[locations[i][3]].icon, // url
                            scaledSize: new google.maps.Size(50, 50), // scaled size
                           
                        };

                      marker = new google.maps.Marker({
                        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
                        icon: icon,
                        map: map
                      });

                      google.maps.event.addListener(marker, 'click', (function(marker, i) {
                        return function() {
                          infowindow.setContent(locations[i][0]);
                          infowindow.open(map, marker);
                        }
                      })(marker, i));
                }

                // var marker = new google.maps.Marker({
                //   position: {lat: centerLat, lng: centerLng},
                //   map: map
                // });
                // var infowindow = new google.maps.InfoWindow({
                //   content: '<p>Marker Location:' + marker.getPosition() + '</p>'
                // });

                // google.maps.event.addListener(marker, 'click', function() {
                //   infowindow.open(map, marker);
                // });
                // // End of marker

                //  // 1st Dropoff Map marker start
                // var marker = new google.maps.Marker({
                //   position: {lat: firstDrop_lat, lng: firstDrop_lng},
                //   map: map
                // });
                // var infowindow = new google.maps.InfoWindow({
                //   content: '<p>Marker Location:' + marker.getPosition() + '</p>'
                // });

                // google.maps.event.addListener(marker, 'click', function() {
                //   infowindow.open(map, marker);
                // });
                // // 1st Dropoff End of marker

                // // 2nd Dropoff Map marker start
                // var marker = new google.maps.Marker({
                //   position: {lat: secondDrop_lat, lng: secondDrop_lng},
                //   map: map
                // });
                // var infowindow = new google.maps.InfoWindow({
                //   content: '<p>Marker Location:' + marker.getPosition() + '</p>'
                // });

                // google.maps.event.addListener(marker, 'click', function() {
                //   infowindow.open(map, marker);
                // });
                // // 2nd Dropoff End of marker

           
        } 

        // google.maps.event.addDomListener(window, 'load', initialize);  
    
});
