$(document).on('ready',comenzar);

function comenzar(){

   var bandera=0;


      $('.cuadro').on('click',cambiar);
      $("input[name=modelo]:radio").on('click',elemento);


      $('#formulario').on('submit',agregarItem);
     
     function elemento(e){
        carrito.elemento=$(this);
     }

      function agregarItem(e)
      {
    	     e.preventDefault();
      
          if ($(':radio').length)
          {
               carrito.Modelo=$("input[name='modelo']:checked").val();
       
                id=$("input[name='modelo']:checked").attr('id');
                valor=parseInt($('label[for='+id+']').find('span').html());
                console.log(valor);
                if(valor >= parseInt($('#numero').val()))
                {
                  carrito.agregar($("#comprar"));
                }
                  
                else
                  carrito.getAlerta('<p><label class="icon-sad" ></label> Existencias insuficientes del modelo '+$(carrito.elemento).data('nombre')+'</p>');

                
          }
          else
          {
                valor=parseInt($('#stock').html());


                if (valor >= parseInt($('#numero').val()))
                  carrito.agregar($("#comprar"));
                else
                  carrito.getAlerta('<p><label class="icon-sad" ></label> Existencias insuficientes </p>');
          }
          $('#numero').val(0);
   
      }

}

function cambiar(){

	$('#imagen img' ).attr('src', $(this).find('img').attr('src'));


}




