$(document).on('ready',iniciar);

function iniciar()
{
	 $( "#zona" ).dialog({
            width:650,
            modal:true,
            autoOpen:false,
            show: "clip",
            hide: "clip"
      });

      $('.add-item').on('click',agregarItem);
      $('#zone-form').on('submit',addZona);
      $('#pack').on('keyup',getData);
      $(document).on('change','.zona-add',abrirDialogo);
      $(document).on('click','.delete',quitarItem);
      agregarZona();
      estados();


 
}

function getData(e){
  var bandera=true;
  for(i=0;i<=listaPaquetes.length;i++){
    if (listaPaquetes[i] == $(this).val()){
          $('#min').hide('slow').removeAttr("required");
          $('#max').hide('slow').removeAttr("required");
          $('#productos').hide('slow');
          $('#p-c').hide('slow');
          bandera=false;
    }
    else { 
            if(bandera==true){
              $('#min').show('slow');
              $('#max').show('slow');
              $('#productos').show('slow');
              $('#p-c').show('slow');
            }

    }
  }
    
}

function abrirDialogo(){

      console.log($(this).val());
      if($(this).val()=='Nueva')
            $('#zona').dialog('open');
}

function quitarItem(){

	$(this).parent().remove();
	contador--;

}
var contador=1;
function agregarItem()
{

      var render="<li class='container-zone'><select name='zona_"+contador+"'  class='zona-add'></select><input type='text' name='precio_"+contador+"' placeholder='Precio'><label class='icon-cross inline delete color-rojo'></label></li>";

      $('#contenedor-zonas').append(render);

      agregarZonas();

      contador++;

}

function agregarZonas(){

  $('.zona-add').each(function(index){
    if($(this).val()==null || $(this).val()=='Nueva'){
      
      $(this).html(listaZonas);

      $(this).append('<option value="Nueva">Nueva</option>');
    }

  });
  
}

function agregarZona(){
  
  $('.zona-add').html(listaZonas);
  $('.zona-add').append('<option value="Nueva">Nueva</option>');
}

function addZona(e) 
{
        e.preventDefault();

        $.post( "/zona/nuevo/",$(this).serialize(), function( data ) 
        {

             listaZonas+='<option value="'+data.idzona+'">'+data.zona+'</option>';
            agregarZonas();

             if(data.Error==true){
              mensaje="<center><br><h1> Intentalo mas tarde!!<br><label class='icon-sad'></label> </h1></center>";

              $('#zone-form').html(mensaje).animate({opacity: 1},400);
             }
                  
              else{
                    $('#zona').dialog('close');
                    listaEstadosZonas=data.zonas;
                    estados();
              }
         
        });
 }


 function estados(){

    lista=JSON.stringify(listaEstadosZonas).split(",");

    for (l in lista){
        console.log(lista[l]+",");
        var idx = listaEstados.indexOf(lista[l].replace('"',''));
        if(idx!=-1) {
          listaEstados.splice(idx, 1);
        }
        

    }

    $('#zone-form')[0].reset();

    getEstados();

 }


 function getEstados(){

  var renderEstados='';
  contador=0;
   for (e in listaEstados ){
            renderEstados+='<li class="estados"><input type="checkbox" name="estados[]" value="'+listaEstados[e]+'">'+listaEstados[e]+'</span></li>';
            contador++;
      }


      $('#estados').html(renderEstados);       
 }

