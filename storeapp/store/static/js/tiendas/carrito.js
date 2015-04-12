

function Carrito(){
	var that = this; 
	this.cantidad=1;
	this.Modelo='Default';
	this.elemento=null;
	
	 $( "#aviso" ).dialog({
	 	show:'clip',
	 	hide:'clip',
	 	modal:true,
	 	autoOpen:false
	 });

	  $( "#alerta" ).dialog({
	 	show:'clip',
	 	hide:'clip',
	 	modal:true,
	 	autoOpen:false
	 });



	 this.asignarCantidad=function(numero){
	 	that.cantidad=numero;
	 }
	 this.vaciarCarrito=function(){
	 	vaciar();
	 }

	this.agregar=function(elemento){
		var datos=$('#formulario').serialize();
		if (that.Modelo == 'Default'){
			datos+='&modelo=' + $('#comprar').data('id');
		}
			cantidad=$('#numero').val()
		
		$.ajax({
			  url: '/Armar/',
			  type: 'POST',
			  dataType: "json",
			  data:datos,
			  success:function(data){

			  	if(data.Error==true){
			  		that.getAlerta('<p><label class="icon-sad" ></label> '+data.test+'</p>');
			  	}
			  	else{

					$('#items').html(data.cesta);
					console.log($('#numero').val());

			  		$("#stock").html(parseInt($("#stock").html())-parseInt(cantidad));
			  		valor=$('input:contains("'+that.Modelo+'"")').val();
			  		console.log(valor);
			  		if(that.elemento != null){
			  			id=$(that.elemento).attr('id');
			  			valor=parseInt($('label[for="'+id+'"]').find('span').html());
			  			$('label[for="'+id+'"]').find('span').html(valor-parseInt(cantidad));
			  		}

			  		 that.getDialog($("#comprar").data('nombre'));			  		 
			  	}
			  }
			});
		
	};



	this.quitar=function(elemento){

		var datos={modelo:$(elemento).data('id')}

		$.ajax({
			  url: '/Desarmar/',
			  type: 'POST',
			  dataType: "json",
			  data:datos,
			  success:function(data){

			  	if(data.Error==true){
			  		that.getAlerta('<p><label class="icon-sad" ></label> No se puedo eliminar</p>');
			  	}
			  	else{

					$('#items').html(data.cesta);
					resta=$(elemento).parent().parent().find('.precioItem').html();
			  		carrito.setPrecio(resta);
			  		$(elemento).parent().parent().remove();	  		 
			  	}
			  }
			});

	};

	this.getDialog=function(item){

		 $( "#aviso" ).dialog('open');
		 $("#nameItem").html(item);

	}

	this.getAlerta=function(mensaje){

			$('#alerta').dialog('open');
			$('#mensaje-alerta').html(mensaje);
	}


	this.setPrecio=function(resta){

		texto=$('#precio').html();
		texto=texto.replace(',','');
		texto=texto.replace('$ ','');
		texto=texto.replace(' ','');
		var precio=parseFloat(texto);
		subs=resta.replace(',','');
		subs=subs.replace('$','');

		precio=precio-parseFloat(subs);
		if(precio>0)
			precio=precio;
		else
			precio=0;

		$("#precio").html('$ '+formato_numero(precio, 2,'.',','));
	}


	this.setProducts=function(){

		var numeroItems=parseFloat($("#items").html());
		if(numeroItems==0){
			
			render='<p><label class="icon-cart3"></label> Carrito de Compras vacío, agrega algún producto</p>';

			$('#alerta').dialog('open');
			$('#mensaje-alerta').html(render);
		}
		else
			location.href='/Carrito/'
		


	}



	function formato_numero(numero, decimales, separador_decimal, separador_miles){ // v2007-08-06
	    numero=parseFloat(numero);
	    if(isNaN(numero)){
	        return "";
	    }

	    if(decimales!==undefined){
	        // Redondeamos
	        numero=numero.toFixed(decimales);
	    }

	    // Convertimos el punto en separador_decimal
	    numero=numero.toString().replace(".", separador_decimal!==undefined ? separador_decimal : ",");

	    if(separador_miles){
	        // Añadimos los separadores de miles
	        var miles=new RegExp("(-?[0-9]+)([0-9]{3})");
	        while(miles.test(numero)) {
	            numero=numero.replace(miles, "$1" + separador_miles + "$2");
	        }
	    }

	    return numero;
	}

}


var carrito=new Carrito();

$(document).on('ready',car);

function car(){

	
	$('#carrito').on('click',carrito.setProducts);
	$(document).on('click','.delete',quitarItem);

	function quitarItem(){
		elemento=$(this);
		carrito.quitar($(this));
	
	}


	//mandar ajax sin token----------------------------------------
	$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
	        // url could be relative or scheme relative or absolute
	        var host = document.location.host; // host + port
	        var protocol = document.location.protocol;
	        var sr_origin = '//' + host;
	        var origin = protocol + sr_origin;
	        // Allow absolute or scheme relative URLs to same origin
	        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	            // or any other URL that isn't scheme relative or absolute i.e relative.
	            !(/^(\/\/|http:|https:).*/.test(url));
	    }


	    function safeMethod(method) {
	        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	    }

	    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
	        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	    }
	});
	//-----------------------------------------------------------------------

}