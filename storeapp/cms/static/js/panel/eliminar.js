$(document).on('ready',comenzar);
var elemento;
function comenzar(){
	$('.delete').on('click',confirmar);

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

	$(function() {
    $( "#confirmacion" ).dialog({
      resizable: false,
      height:210,
      width:380,
      modal: true,
      autoOpen:false,
      show: "clip",
      hide: "clip",
      buttons: {
        "SI, estoy seguro": function() {
        if($(elemento).data('elemento')=='PaquetesFormaenvio'){
          console.log($(elemento).data('id'));
          var producto={
              iditem:$(elemento).data('id'),
              elemento:$(elemento).data('elemento'),
              forma:$(elemento).data('forma')
            };
        }
        else
        {
            var producto={
              iditem:$(elemento).data('id'),
              elemento:$(elemento).data('elemento')
            };
        }
     
	
			$.ajax(
			   {
			        url: "/Eliminar/",
			        type: "POST",
			        data:  producto,
			        dataType: 'json',
			        async: false,
			        success: function(data) {
			        	if(data.Error==false)
			        		eliminar();
                else
                  console.log(data.Error);
			        }

			    }
			);
        },
        'Cancelar': function() {
          $( this ).dialog( "close" );
        }
      }
    });
  });

}
function confirmar(){
	elemento=$(this);
	$('#confirmacion').dialog( "open" );

	
}

function eliminar(){

	$('#confirmacion').dialog( "close" );
	elemento.parent().parent().fadeOut('slow',console.log(2));
}