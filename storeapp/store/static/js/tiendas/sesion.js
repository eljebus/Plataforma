
function comienzo()
{
	$('#sesion').dialog({
            maxWidth:445,
            modal:true,
            width:345,
            autoOpen:false,
            show: "clip",
            hide: "clip",
            fluid:true
      });

	$('#cuenta').on('click',function(){

    if (sesion==false)
		  $('#sesion').dialog('open');
    else
      location.href='/panelUsuario/'
	});

      $('#abrirRegistro').on('click',function(){
            $('#sesion').dialog('close');
            $('#Registro').dialog('open');
            
      });

      $('#Registro').dialog({
            width:600,
            maxWidth:600,
            modal:true,
            autoOpen:false,
            show: "clip",
            hide: "clip",
            fluid:true
      });
      //Inicio de sesion

      $('#iniciarSesion').on('submit',ingresar);
      $('#registro-form').on('submit',registrar);


      //---------------------------------------------

        // on window resize run function
          $(window).resize(function () {
              fluidDialog();
          });

          // catch dialog if opened within a viewport smaller than the dialog width
          $(document).on("dialogopen", ".ui-dialog", function (event, ui) {
              fluidDialog();
          });

          function fluidDialog() {
              var $visible = $(".ui-dialog:visible");
              // each open dialog
              $visible.each(function () {
                  var $this = $(this);
                  var dialog = $this.find(".ui-dialog-content").data("ui-dialog");
                  // if fluid option == true
                  if (dialog.options.fluid) {
                      var wWidth = $(window).width();
                      // check window width against dialog width
                      if (wWidth < dialog.options.maxWidth + 50) {
                          // keep dialog from filling entire screen
                          $this.css("max-width", "90%");
                      } else {
                          // fix maxWidth bug
                          $this.css("max-width", dialog.options.maxWidth);
                      }
                      //reposition dialog
                      dialog.option("position", dialog.options.position);
                  }
              });

          }


      //---------------------------------------------
}
 function ingresar(e){
      e.preventDefault();
       $('#error').html('');
      var datos=$(this).serialize();
            $.ajax({
                    url: '/ClienteLogin/',
                    type: 'POST',
                    dataType: "json",
                    data:datos,
                    success:function(data){
                        if(data.Error==true)
                              $('#error').html('Usuario o Clave Incorrectos <label class="icon-sad"></label>');
                        
                        else
                          location.href='/panelUsuario/';
                                                       
                    }
                  });

 }

 function registrar(e){
    e.preventDefault();
       $('#error').html('');
      var datos=$(this).serialize();
      $.ajax({
              url: '/Registro/',
              type: 'POST',
              dataType: "json",
              data:datos,
              success:function(data){
                  if(data.Error==true)
                        $('#letrero').html(data.letrero+' <label class="icon-sad"></label>');
                  
                  else
                    $('#registro-form').html('<center><label class="icon-happy color-verde"></label><br>Te enviamos un ocrreo con tu clave de ingreso</center>');
                        //location.href='/panelUsuario/';
                                                 
          }
      });

 }