$(document).on('ready',procesar);
var numeroPedido=0;
var banderaCierre=false;



function procesar(){

	$('#estado').on('change',metodos);

	$(document).on('change',"input[name='metodo-envio']",function(e){

				metodo=$(this).val();
				metodo=metodo.split(':');
				metodo=parseFloat(metodo[1]);
				$('#precio').html(formato_numero(precio+metodo, 2,'.',','));
			}
		);
	$('#pagar').dialog({
        width:350,
        modal:true,
        autoOpen:false,
        show: "clip",
        hide: "clip"
      });
	//pagosOxxo();


	$('#card-form').on('submit',enviarPago);

	$('#send-form').on('submit',function(e){
			e.preventDefault();
			$('#card-errors').html('');
			switch($('input[name=formaPago]:checked').val())
				{
					case 'Conekta':
					case 'Conekta Meses Sin Intereses':
						if($('input[name=formaPago]:checked').val()=='Conekta Meses Sin Intereses')
								$('.ui-dialog-title').html('12 Meses Sin Intereses');
						$('#pagar').dialog('open');
					break;
					case 'Conekta Pagos OXXO':
					case 'Conekta Deposito Bancario':
						if($('input[name=formaPago]:checked').val()=='Conekta Pagos OXXO')
							$('.ui-dialog-title').html('Pago en Oxxo');
						else
							$('.ui-dialog-title').html('Deposito BANORTE');

						$('#pagar').dialog('open');
						$('#card-form').html('<center>Generando Pago<br><img src="/static/imagenes/ajax.gif"></center>');
						enviarPago(e);
					break;
					default:
						console.log($('input[name=formaPago]:checked').val());
					break;
				}
			
	});

	Conekta.setPublishableKey(llave);

	//fin metodo de pagos
}



function enviarPago(e){
	e.preventDefault();
	$('#card-errors').html('');
	
	var bandera=true;
	var opcion=$('input[name=formaPago]:checked').val();
	var letrero='';
	if(opcion == 'Conekta' || opcion == 'Conekta Meses Sin Intereses'){
		

		numero=parseInt($('input[name=card-number]').val());
		mes=parseInt($('input[name=card-expiry-month]').val());
		year=parseInt($('input[name=card-expiry-year]').val())
		cvc=parseInt($('input[name=card-cvc]').val());

		if(Conekta.card.validateNumber(numero) === false){
			bandera=false;
			letrero='Número de tarjeta incorrecto';
		}
			
		if(Conekta.card.validateExpirationDate(mes, year) === false){
			bandera=false;
			letrero='Fecha de expiración icorrecta';
		}
		if (Conekta.card.validateCVC(cvc) === false){
			bandera=false;
			letrero='CVC incorrecto';
		}
	
	}




		if(bandera == true){

			$('#card-errors').html('<center>Calculando precio<br><img src="/static/imagenes/ajax.gif"></center>');

			 $.post( "/Total/",$('#send-form').serialize(), function( data ) 
              {
              	switch($('input[name=formaPago]:checked').val())
				{
					case 'Conekta':
						cargoTarjeta(data);
					break;
					case 'Conekta Meses Sin Intereses':
						mesesSinIntereses(data);
					break;
					case 'Conekta Pagos OXXO':
						numeroPedido=data.pedido;
						ordenOxxo(data);

					break;
					case 'Conekta Deposito Bancario':
						ordenBancos(data);
					break;
				}
              	
              	 
              });
		}
		else
			$('#card-errors').html('<center style="margin-top:10px;display:block"><label class="icon-sad iconosp color-rojo" ></label> '+letrero+'</center>');
	 
}


function mesesSinIntereses(data){

	mes=parseInt($('input[name=card-expiry-month]').val());
	year=parseInt($('input[name=card-expiry-year]').val())
	numero=parseInt($('input[name=card-number]').val());
	cvc=parseInt($('input[name=card-cvc]').val());

	

  		 Conekta.charge.create({
		  amount: data.total*100,
		  currency: 'MXN',
		  description: 'Latest E-Zine',
		  monthly_installments:12,
		  card: {
		    name: userName,
		    cvc:cvc,
		    exp_month:mes ,
		    exp_year:year,
		    number: numero,
		    address: {
		      street1: $('input[name=direccion]').val(),
		      state: $('select[name=estado]').val(),
		      country: 'MX',
		      zip:  $('input[name=cp]').val()
		    }
		  }
		 
		}, conektaSuccessResponseHandler, conektaErrorResponseHandler);  

}


function cargoTarjeta(data){

	mes=parseInt($('input[name=card-expiry-month]').val());
	year=parseInt($('input[name=card-expiry-year]').val())
	numero=parseInt($('input[name=card-number]').val());
	cvc=parseInt($('input[name=card-cvc]').val())
	
		
	 Conekta.charge.create({
	  amount: data.total*100,
	  currency: 'MXN',
	  description: 'Latest E-Zine',
	  card: {
	    name: userName,
	    cvc:cvc,
	    exp_month:mes ,
	    exp_year:year,
	    number: numero,
	    address: {
	      street1: $('input[name=direccion]').val(),
	      state: $('select[name=estado]').val(),
	      country: 'MX',
	      zip:  $('input[name=cp]').val()
	    }
	  }
	}, conektaSuccessResponseHandler, conektaErrorResponseHandler);

}


function ordenBancos(response){
	Conekta.charge.create({
	  amount: response.total*100,
	  currency: 'MXN',
	  description: 'Latest E-Zine',
	  bank: {
	    type: 'banorte'
	  }
	}, conektaSuccessResponseHandler, conektaErrorResponseHandler);
}

function ordenOxxo(response){
	console.log(response);
	Conekta.charge.create({
	  amount: response.total*100,
	  currency: 'MXN',
	  description: 'Latest E-Zine',
	  cash: {
	    type: 'oxxo'
	  }
	}, conektaSuccessResponseHandler, conektaErrorResponseHandler);
}

function redireccionar()
{
	location.href='/panelUsuario/'
} 
function conektaSuccessResponseHandler(response) {

				switch($('input[name=formaPago]:checked').val())
				{
					case 'Conekta':
					case 'Conekta Meses Sin Intereses':


						 $.ajax({
				            url: "/reportar/",
				            type: 'post',
				            dataType: 'json',
				            success: function (data) {
				            	
				            	$('#card-form').html('<center><label class="icon-checkmark iconos color-azul"></label><br> El Cargo ha sido Pagado</center>')
				                

							setTimeout ("redireccionar()", 1000);
				            },
				            data: response
				        });
					break;

					case 'Conekta Pagos OXXO':

						console.log(response);
					

						$('#oxxoForm').append("&nbsp;&nbsp;<input type='hidden'  value='"+response.id+"'name='idcargo'> <input type='hidden' value='"+response.payment_method.barcode_url+"' name='url'>  <input type='hidden' value='"+response.payment_method.barcode+"' name='numero'>");
						$('#oxxoForm').submit();
						//location.href='/pagoOxxo/';
					
					break;
					case 'Conekta Deposito Bancario':
						console.log(response);
						$('#bancoForm').append("&nbsp;&nbsp;<input type='hidden'  value='"+response.id+"'name='idcargo'>  <input type='hidden' value='"+response.payment_method.type+"' name='banco'>  <input type='hidden' value='"+response.payment_method.reference+"' name='referencia'>");
						$('#bancoForm').submit();

					break;

					
				}
	
}

function conektaErrorResponseHandler(response) {
  // show the errors on the form
   $.ajax({
            url: "/reportarError/",
            type: 'post',
            dataType: 'json',
            success: function (data) {
            	
            	 $('#card-errors').html('<center><label class="icon-sad iconos color-rojo"></label><br>Error:'+response.message+'</center>')
                

			setTimeout ("location.href='/'", 2000);
            },
            data: response
        });
 
}

function metodos(e){
	$('#envios').css({
			padding:'1em',
			marginBottom:'2em'
		});
	$('#envios').html('<center><img src="/static/imagenes/ajax.gif"></center>');

	estado={estado:$(this).val()}
	$('#precio').html(formato_numero(precio, 2,'.',','));
	$.ajax({
	  url: '/costoPaquete/',
	  type: 'POST',
	  dataType: "json",
	  data:estado,
	  success:function(data){
	  	var render='';
	  	if(data.Error==true)
	  		render=data.letrero;
	  	else{
	  			
	  			metodos=JSON.parse(data.metodos);
	  			precios=JSON.parse(data.datos);
	  			for(m in metodos)
	  				render+="<figure class='class-envio inline medio'> <img src='/static/"+metodos[m]+"' alt='' class='inline medio'><figcaption class='inline medio'><div class='radio-envio inline medio'>&nbsp;&nbsp;<input type='radio' id='"+m+"' name='metodo-envio' value='"+m+":"+precios[m]+"' required><label class='inline medio' for='"+m+"'>$ "+formato_numero(precios[m], 2,'.',',')+"</label></div></figcaption></figure>";
	  			if (data.letrero)
					render+=data.letrero;
	  		}

	  	$('#envios').html(render);

	  }
	});
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



