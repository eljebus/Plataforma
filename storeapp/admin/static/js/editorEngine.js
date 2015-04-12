var colorNavegador=$('nav .list-none').css('background-color'),
    	colorFondoLogo,
    	colorPie,
    	colorHover,
    	colorLetraPie,
    	colorLetraBody,
    	colorLetraMenu=$('nav .list-none li').css('color'),
    	colorBody;

        $(document).on('ready',comenzar);

        function comenzar()
        {
            $('#slider').bjqs({
                                    height      : 320,
                                    width       : '100%',
                                    responsive  : true
                                  });

            $('.colores').on('change',cambiarElemento);
            $('.coloresHover').on('change',cambiarColoresHover);
            $('.letra').on('change',cambiarLetra);
            $('.file').on('change',uploadImagenes);
            $( ".acordion" ).accordion();
            moverPanel();

         
        }

        function moverPanel()
        {
        	var offset = $("#sidebar").offset();
            var topPadding = 15;
            $(window).scroll(function() {
                if ($("#sidebar").height() < $(window).height() && $(window).scrollTop() > offset.top) { /* LINEA MODIFICADA POR ALEX PARA NO ANIMAR SI EL SIDEBAR ES MAYOR AL TAMAÑO DE PANTALLA */
                    $("#sidebar").stop().animate({
                        marginTop: $(window).scrollTop() - offset.top + topPadding
                    });
                } else {
                    $("#sidebar").stop().animate({
                        marginTop: 0
                    });
                };
            });
        }


       	function cambiarElemento(elemento,sub)
       	{
       		var elemento=$(this).data('element');

       		console.log(elemento);
       		$(elemento).css('background',$(this).val());

       		$(this).parent().children().css('background-color',$(this).val());
       		$(this).parent().children().val($(this).val());
       		asignarValores(elemento,$(this).val(),'A');


       	}

       	function cambiarLetra(elemento,sub)
       	{
       		var elemento=$(this).data('element');


       		console.log(elemento);
       		
       		$(elemento).css('color',$(this).val());
       		$(this).parent().children().css('background',$(this).val());
       		$(this).parent().children().val($(this).val());
       		asignarValores(elemento,$(this).val(),'B');
       	}

       	function uploadImagenes()
		{		
			
		      var i = 0, len = this.files.length, img, reader, file;
		     
		      for( ; i < len; i++){
		      	if(i<=3){
		      		file = this.files[i];

		            if(!!file.type.match(/image.*/)){
		              if(window.FileReader){
		                  reader = new FileReader();
		                  reader.onloadend = function(e){

		                      mostrarImagenSubida(e.target.result);

		                  };
		                  reader.readAsDataURL(file);

		              }
		            }
		      	}
		          
		      }
							
			var element=this.elemento;
			var imagesList= new Array();

			function mostrarImagenSubida(source){
				console.log(source);
		     $('body').css('background-image','url('+source+')');  
		    }

	}






		function asignarValores(opcion,color,subelement)
		{
			switch(opcion){
				case 'nav .list-none':

				colorNavegador=color;
				break;
				 case 'nav .list-none li':
				 
				 	colorLetraMenu=color;
				 break;

			    case 'footer':

			    if(getType(subelement))
			    	colorPie=color;
			    else
			    	colorLetraPie=color;
			    break;

			    case '#logo':
			       colorFondoLogo=color;
			    break;

			    case '#inferior':
			       colorLetraPie=color;
			    break;

			    case 'body':
			    if(getType(subelement))
			    	colorBody=color;
			    else
			    	colorLetraBody=color;
 				
			    break;



  
			}

			function getType(sub){
				if(sub=='A')
					return true;
				else
					return false;

			}
		}
		

         function cambiarColoresHover()
        {

        	$(this).parent().children().css('background-color',$(this).val());
       		$(this).parent().children().val($(this).val());
          	var elemento=$(this).data('element');
              color=$(this).val();
              $(elemento).on('mouseover',function(e){

              	$(this).css('background-color',color);
              	
              });

              $(elemento).on('mouseout',function(e){

              		$(this).removeAttr('style');

                    $('nav .list-none').css('background-color',colorNavegador);

                    $('nav .list-none li').css('color',colorLetraMenu);

              	
              });


              
        }
        