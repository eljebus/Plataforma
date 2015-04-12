$(document).ready(function() {

        $('#register-form').on('submit', function(e) {

              e.preventDefault();
              $('#crear').attr("value", 'Creando Mi Tienda');
              $('#crear').attr("disabled", true);
              $.post( "/crearTienda/",$(this).serialize(), function( data ) {
                  console.log(data);
                  if(data.Error==true){
                    mensaje="<center><label class='icon-sad'></label> "+data.letras+"</center>";
                    $('#Error').html(mensaje);
                    $('#crear').attr("value", 'Crear Mi Tienda');
                    $('#crear').attr("disabled", false);
                  }
                    
                  else{
                    $('#Error').html('');
                      mensaje="<center><br> <h1>Listo!! <br><label class='icon-happy'></label></h1><br> <p>Hemos Recibido Tus datos, enviamos a tu correo la información para la activación de tu cuenta, si no lo encuentras revisa el SPAM</p><bR><a href='/ingresar/True/'>Ingresar</a> </center>";

                    $('#register-form').animate(
                      {opacity: .0},
                      400,
                      function() {
                          $('#register-form').html(mensaje).animate({opacity: 1},400);
                      });
                  

                  }
              });
                    
        });

         $('#contact-form').on('submit',enviarCorreo);
         $('#contact-inferior').on('submit',enviarCorreo);

          function enviarCorreo(e) {

              e.preventDefault();
              elemento=$(this);
              console.log(elemento);
              $.post( "/correoContacto/",$(this).serialize(), function( data ) {
                  if(data.Error==true)
                    mensaje="<center><br><h1> Intentalo mas tarde!!<br><label class='icon-sad'></label> </h1></center>";
                  else
                    mensaje="<center><br> <h1>Listo!! <br><label class='icon-happy'></label></h1> </center>";

                 $(elemento).animate(
                      {opacity: .0},
                      400,
                      function() {
                          $(elemento).html(mensaje).animate({opacity: 1},400);
                      });
                    });
        };
      var d1=new dialog(400,480);
      d1.dialogo('#contact');
      d1.abrir("#final");
       

      d1.ancho=400;
      d1.alto=350;
      d1.dialogo("#proxima");
      d1.abrir('.prox');
      d1.abrir('.flechap');
       
      d1.ancho=400;
      //d1.alto=485;
      d1.alto=400;
      d1.dialogo("#registra");
      d1.abrir("#registro");

       
    });


 function dialog(ancho,
                alto,
                elemento
                )
 {

    this.ancho=ancho;
    this.alto=alto;
    this.elemento='';
    this.dialogo=function(elemento){
      this.elemento=elemento;
       $(elemento).dialog({
            height: this.alto,
            autoOpen:false,
            modal: true,
            width:this.ancho,
            resizable:false,
            show: "clip",
            hide: "clip"
        });      
    };
    this.abrir=function(opener){
      var elemento=this.elemento;
      $( opener ).on('click',function(e) 
        {  
         console.log(elemento);
          e.preventDefault();
          $(elemento).dialog( "open" );
        });
    };

 }

  /*<form action='/registro/' method="post" id='register-form2' accept-charset="utf-8">
      {% csrf_token %}
      {{ form.non_field_errors }}
      <div id="form">
        {{form.as_p}}
        <input type="submit" class='boton'  value='Registrar'>
    <form>*/