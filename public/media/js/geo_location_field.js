function initialize_geo_location_field(id, address, latitude, longitude, zoom, startinglat, startinglong){
	
	var geoEncodingCount = 0; 
		
	// Clear the js not found message:
	$('.js-missing-msg').remove();
	
	id = '#' + id;
	
	address = !address ? '' : address;
	latitude = !latitude && !parseFloat(latitude) ? startinglat : latitude;
	longitude = !longitude && !parseFloat(longitude) ? startinglong : longitude;
	zoom = !zoom && !parseFloat(zoom) ? 3 : zoom;
	
  if(GBrowserIsCompatible()){
    var map = new GMap2($(id + "_geo_location_map_canvas").get(0));
		var marker;
		
		// Add the zoom control.
		map.addControl(new GLargeMapControl());
		
		// Allow satelite view, etc.
		map.addControl(new GMapTypeControl());
		
		var center = new GLatLng(latitude, longitude);
		map.setCenter(center, 13);
		
		marker = new GMarker(center, {draggable: true});
		map.addOverlay(marker);
		
		map.setZoom(zoom);
		map.enableScrollWheelZoom();
		
		update_geo_location_fields(id, address, latitude, longitude);
		
    GEvent.addListener(marker, "dragstart", function(){
      map.closeInfoWindow();
    });

    GEvent.addListener(marker, "dragend", function(){
			var gLatLngPoint = marker.getLatLng();
      update_geo_location_fields(id, address, gLatLngPoint.lat(), gLatLngPoint.lng());
    });
		
		// When the address is changed, get the new lat and lng values.
		$(id + '_geo_location_field_address').change(function(){
			var newAddress = $(id + '_geo_location_field_address').attr('value');
			var geocoder = new GClientGeocoder();

		//favour Australian addresses when geocoding
				geocoder.setBaseCountryCode('AU');

			if(newAddress != '') {
				geoEncodingCount++;
				// Show geocoding in progress indicators
				$(id +'_geo_location_field_encoding_msg').show();
				$('div.submit-row').prepend('<p class="geo_location_field_encoding_msg" style="font-weight:bold; color: red;">Geo encoding your address, please wait....</p>');

				geocoder.getLatLng(newAddress, function(gLatLngPoint){
					geoEncodingCount--;
					// Hide geocoding in progress indicators
					$(id +'_geo_location_field_encoding_msg').hide();
					$('.geo_location_field_encoding_msg').remove();
					
					if (gLatLngPoint == null) {
						alert('Unable to geocode the provided address.');
					}else{
						map.setCenter(gLatLngPoint);
						marker.setLatLng(gLatLngPoint);
						
						if(zoom < 10){
							zoom = 10;
							map.setZoom(zoom);
						}
						
						update_geo_location_fields(id, address, gLatLngPoint.lat(), gLatLngPoint.lng());
					}
				});
			}
		});
		
		// Cause the change event for the address to fire when an update is forced.
		$(id + '_geo_location_field_force_update').click(function(){
			$(id + '_geo_location_field_address').change();
		});
		
		// Cause change to fire once  if we have an address.
		if(address && address.length > 0){
			$(id + '_geo_location_field_address').attr('value', address);
			$(id + '_geo_location_field_address').change();
		}
						
		// Get the form tag so we can prevent saving while encoding is going on.
		// Note this is fired once for each geo location field on the page.
		$('form').submit(function(){
			if(geoEncodingCount > 0){
				return false;
			}else{
				// Create the json to save.
				var geoData = {};
				geoData.address = $(id + '_geo_location_field_address').attr('value');
				geoData.latitude = $(id + '_geo_location_field_latitude').text();
				geoData.longitude = $(id + '_geo_location_field_longitude').text();
				geoData.adminzoom = zoom;
				
				// Set the value of the hidden field to the json.
				$(id + '_geo_location_field_hidden_json').attr('value', $.toJSON(geoData));
			}
		});
		
	}else{
		alert("Your browser does not support the Google Maps API, therefore you will not be able to add geo encoded addresses.");
	}
}

function update_geo_location_fields(id, address, latitude, longitude){
	$(id + '_geo_location_field_latitude').html(latitude);
	$(id + '_geo_location_field_longitude').html(longitude);
}
