

function Localizar(intoFunction){



	this.coordenadas=function(){

		navigator.geolocation.getCurrentPosition(coordenadas,error);
	}

	function error(){

		intoFunction();
	}

	function coordenadas(position){
		var latitud = position.coords.latitude;
		var longitud = position.coords.longitude;


		var latLng = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
		var geocoder = new google.maps.Geocoder();
			geocoder.geocode({ 'latLng': latLng },processGeocoder);
    }


	function processGeocoder(results, status)
	{
		
		if (status == google.maps.GeocoderStatus.OK) 
		{

			console.log(results);
			if (results[3]) 
			{
				direccion=results[3].formatted_address;
				sessionStorage.setItem("direccion",direccion);
				intoFunction();			
			} 
		}

		return direccion;
	}



}