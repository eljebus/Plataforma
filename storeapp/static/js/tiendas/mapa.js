	$(document).on("ready",iniciar);

		function iniciar()
		{
			
			codeAddress();
		}

		function codeAddress() 
  		{
  			var geocoder = new google.maps.Geocoder();
         
        //obtengo la direccion del formulario
       
            geocoder.geocode( { 'address': address}, function(results, status) {
         
     
        if (status == google.maps.GeocoderStatus.OK) {
           	
            
            var myOptions = {
	          center: results[0].geometry.location,//centro del mapa
	          zoom: 15,//zoom del mapa
	          mapTypeId: google.maps.MapTypeId.ROADMAP //tipo de mapa, carretera, híbrido,etc
	        };
             map = new google.maps.Map(document.getElementById("mapa"), myOptions);
	         
             marker = new google.maps.Marker({
	            map: map,//el mapa creado en el paso anterior
	            position: results[0].geometry.location,//objeto con latitud y longitud
	            draggable: false
	        });
                
         
            
      } else {
          //si no es OK devuelvo error
          console.log("No podemos encontrar la direcci&oacute;n, error: " + status);
      }
    });
  }