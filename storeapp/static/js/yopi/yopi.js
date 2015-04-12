var tipo=1;

$(document).on('ready',iniciar);


function iniciar(){


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


	sendAddress();
	
	if(!sessionStorage.getItem('direccion')){
		localizar= new Localizar(sendAddress);
		localizar.coordenadas();
	}

		



	$('#clientes').dialog({

		width: 'auto', // overcomes width:'auto' and maxWidth bug
	    maxWidth: 650,
	    height: 'auto',
	    modal: true,
	    autoOpen:false,
	    fluid: true, //new option
	    resizable: false,
	    hide:'clip'
	});

	$('#vendedores').dialog({

		width: 'auto', // overcomes width:'auto' and maxWidth bug
	    maxWidth: 650,
	    height: 'auto',
	    modal: true,
	    autoOpen:false,
	    fluid: true, //new option
	    resizable: false,
	    hide:'clip'
	});


	$('#buy').on('click',function(){
		$('#clientes').dialog('open');
		tipo=$(this).data('type');

	});

	$('#shop').on('click',function(){
		$('#vendedores').dialog('open');
		tipo=$(this).data('type');
	})



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
	            if (wWidth < (parseInt(dialog.options.maxWidth) + 50))  {
	                // keep dialog from filling entire screen
	                $this.css("max-width", "90%");
	            } else {
	                // fix maxWidth bug
	                $this.css("max-width", dialog.options.maxWidth + "px");
	            }
	            //reposition dialog
	            dialog.option("position", dialog.options.position);
	        }
	    });
	}
}


function sendAddress(){
	var letrero='';
	if(sessionStorage.getItem("direccion")){
		letrero='Usuarios cerca de '+ sessionStorage.getItem('direccion');

		var datos={
			direccion:sessionStorage.getItem('direccion').split(',')[0],
			estado:sessionStorage.getItem('direccion').split(',')[1]
		}



		$.ajax({
		  type: "POST",
		  url: '/yopi/',
		  data:datos,
		  dataType: 'json',
		  success: dataSuccess,
		});

		

	}
	else
		letrero='Usuarios Recientes';


	$('#lugar').html(letrero);
	
}

function dataSuccess(data){

	var content='';


	for( user in data.usuarios){

		nombre=data.usuarios[user].Nombre;
		avatar=data.usuarios[user].Avatar;

		content+='<li><img src="'+avatar+'" alt="'+nombre+'" title="'+nombre+'""></li>';
		
	}

	$('#usuarios ul').html(content);


}