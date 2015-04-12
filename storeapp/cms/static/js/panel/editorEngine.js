var colorNavegador=$('nav .list-none').css('background-color'),
    	colorFondoLogo,
    	colorPie,
    	colorHover,
    	colorLetraPie,
    	colorLetraBody,
    	colorLetraMenu=$('nav .list-none li').css('color'),
    	colorBody;

var bandera=false;

        $(document).on('ready',comenzar);

        function comenzar()
        {
            $('.swiper-container').swiper({
            //Your options here:
            mode:'horizontal',
            loop: true,
            autoplay:5000,
            shortSwipes:true,
            useCSS3Transforms:true,
            pagination:'.pagination',
            createPagination:true,
            paginationClickable:true,
            calculateHeight:true
            //etc..
          });

            

            $('.colores').ColorPicker({
  
                onSubmit: function(hsb, hex, rgb, el) {
                  $(el).val('#'+hex);
                  $(el).ColorPickerHide();

                  

                 cambiarElemento($(el).data('element'),
                                  $(el).val(),
                                  $(el).data('tipo')
                                );
                },
                onBeforeShow: function () {
                  $(this).ColorPickerSetColor(this.value);
                }
              })

              .bind('keyup', function(){
                $(this).ColorPickerSetColor(this.value);
              });



            

            $('.file').on('change',uploadImagenes);
            $( ".acordion" ).accordion();
            $('#salir').on('click',confirmacion);
            $('#guardar').on('click',guardar);
            $('input').on('change',cambiarInput);


             $( "#dialog-confirm" ).dialog({
                resizable: false,
                height:200,
                modal: true,
                autoOpen:false,
                buttons: {
                  "Salir": function() {
                     location.href='/pedidosPanel/Pendiente/'
                  },
                  Cancelar: function() {
                    $( this ).dialog( "close" );
                  }
                }
              });
            moverPanel();

         
        }


    function guardar(){
      
     $('#design').submit();

    }




    function confirmacion() 
    {

      if(bandera==true)
        $( "#dialog-confirm" ).dialog("open");
      else
        location.href='/pedidosPanel/Pendiente/'

    }


        function moverPanel()
        {
        	var offset = $("#editor").offset();
            var topPadding = 15;
            $(window).scroll(function() {
                if ($("#editor").height() < $(window).height() && $(window).scrollTop() > offset.top) { /* LINEA MODIFICADA POR ALEX PARA NO ANIMAR SI EL editor ES MAYOR AL TAMAÑO DE PANTALLA */
                    $("#editor").stop().animate({
                        marginTop: $(window).scrollTop() - offset.top + topPadding
                    });
                } else {
                    $("#editor").stop().animate({
                        marginTop: 0
                    });
                };
            });
        }

        function cambiarInput()
        {
          
         color=$(this).val();
         $(this).css('background-color',color);
        }



        

    	function cambiarElemento(elemento,valor,tipo)
       	{
          
          switch(tipo){
            case 'colores':
                $(elemento).css('background-color',valor);

                 asignarValores(elemento,valor,'A');
            break;
            case 'coloresHover':

                $(elemento).on('mouseover',function(e){

                  $(this).css('background-color',valor);
                  
                });

                $(elemento).on('mouseout',function(e){

                    $(this).removeAttr('style');

                      $('nav .list-none').css('background-color',colorNavegador);

                      $('nav .list-none li').css('color',colorLetraMenu);
                });

            break;

            case 'letra':

              $(elemento).css('color',valor);

              asignarValores(elemento,valor,'B');
            break;
          }
       	
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
                      console.log(file.name);
                      $('#imagenSeleccionada').val(file.name);
		              }
		            }
		      	}
		          
		      }
							
			var element=this.elemento;
			var imagesList= new Array();

			function mostrarImagenSubida(source){
				 bandera=true;
		     $('body').css('background-image','url('+source+')');  
         $('body').css('background-size','100% 100%');
         $('body').css('background-attachment','fixed');
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
      bandera=true;

			function getType(sub){
				if(sub=='A')
					return true;
				else
					return false;

			}
		}
		

        