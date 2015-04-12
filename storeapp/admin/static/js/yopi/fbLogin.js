$(document).on('ready',loguear);


var face;
function loguear(){
	
	var permisos='email,publish_stream,user_birthday,user_location,user_friends,user_photos';
 	face=new FacebookLogin(permisos,loginSuccess,'.fb');
 	face.iniciar();

}


function loginSuccess(data){




	var genero=0;

	if(data.perfil.gender=='male')
		genero=1;

	var ubicacion='Desconocida';
	var mail='Desconocido';
	if(data.perfil.location)
		ubicacion=data.perfil.location.name
	if(data.perfil.email)
		mail=data.perfil.email

	var datos={
		nombre:data.perfil.name,
		ubicacion:ubicacion,
		genero:1,
		tipo:tipo,//esta variable se toma del archivo yopi.js en la apertura de los dialogos
		avatar:data.photo,
		mail:mail,
		csrfmiddlewaretoken:$('#ghost input[name=csrfmiddlewaretoken]').val()
	}
	console.log(datos);

	$.ajax({
	  type: "POST",
	  url: '/yopiRegister/',
	  data: datos,
	  dataType: 'json',
	  success: registerSuccess,
	});


}

function registerSuccess(data){
		$(".dialogos").html('<h3>Gracias por Registrarte</h3><p>Serás de las primara personas en utilizar YOPi</p>');
	
}



function FacebookLogin(permisos,callback,objectEvent){


	var datos={};

	this.iniciar=function(){

		window.fbAsyncInit = function() {
        FB.init({
          appId      : '522902607815845',
          status     : true,
          cookie     : true,
          xfbml         : true,
          oauth      : true // habilita oauth 2.0
        });


        $(objectEvent).on('click', function(){

			FB.login(function(data){

				getData(data);

			}, { scope: permisos });
			});
		} 



	};

	function getData(){
	
       		FB.api('/me', function(me){
       			datos.perfil=me;

       			FB.api('/me/picture', function(photo){
       				datos.photo=photo.data.url;
       				callback(datos);
       			});
       		});
	       	
   		
	}


	this.fillFields=function(data,form){
				
		$(form).find(':input').each(function() {

			var fieldName=$(this).attr('name');
			var elemento=$(this);

			$.each(data, function(index,value) {
				if (fieldName==index){

					$(elemento).attr('value',value);
				}

			});
		});


	}

}




