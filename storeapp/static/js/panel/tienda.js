 $(document).on('ready',iniciar);


 function iniciar(){
 	$(".editor").jqte({sub: false,
                        sup:false,
                        outdent: false,
                        indent: false,
                        format: false,
                        rule: false,
                        unlink: false,
                        source: false,
                        remove: false,
                        strike: false,
                        titletext:[
                                    {title:"Text Format"},
                                    {title:"Tamaño de letra"},
                                    {title:"Color de la letra"},
                                    {title:"Negritas",hotkey:"B"},
                                    {title:"Italica",hotkey:"I"},
                                    {title:"Subrayado",hotkey:"U"},
                                    {title:"Lista Ordenada",hotkey:"."},
                                    {title:"Lista Desordenada",hotkey:","},
                                    {title:"Subscript",hotkey:"down arrow"},
                                    {title:"Superscript",hotkey:"up arrow"},
                                    {title:"Outdent",hotkey:"left arrow"},
                                    {title:"Indent",hotkey:"right arrow"},
                                    {title:"Alinear Izquierda"},
                                    {title:"Centrar"},
                                    {title:"Alinear derecha"},
                                    {title:"Strike Through",hotkey:"K"},
                                    {title:"Hipervinculo",hotkey:"L"},
                                    {title:"Remove Link",hotkey:""},
                                    {title:"Cleaner Style",hotkey:"Delete"},
                                    {title:"Horizontal Rule",hotkey:"H"},
                                    {title:"Source",hotkey:""}
                                ]});

 	var imagenes= new uploadImagenes();
     $('#add-imagen').on('change',imagenes.uploadImage);
 }

  