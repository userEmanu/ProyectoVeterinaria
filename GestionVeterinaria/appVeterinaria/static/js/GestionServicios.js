


function preparareditarServicio(id) {
    const ide = id
    url = '/editarServicioAdminInfo/'+ide+'/'
    console.log(url)
        try {
            fetch(url)
               .then((response) => response.json())
               .then(data => {
                        estado = data.estado 
                        if(estado = true) {
                            document.getElementById("bodyEditarServicio").innerHTML = ""
                            document.getElementById("botonesIdServicio").innerHTML = ""
                            mostrardetServi(data.servicio, data.lista, data.empleado, data.animalDirigido)
                            console.log(data.animalDirigido)
                        } else {
                            Swal.fire({
                                title: 'Sistema veterinaria animalgro',
                                text: 'Algo salio mal, intenta mas tarde',
                                icon: 'error',                          
                                confirmButtonText: 'Aceptar'
                            })
                        }
                    }
                )                
        }
        catch (error) {
            console.log(error)
        }
}

function mostrardetServi(servicio, lista, empleado, animal) {

    
    document.getElementById("bodyEditarServicio").innerHTML = `
        
        <form class="row g-3 was-validated" enctype="multipart/form-data" id="formEditarServicio" >
                <div class="col-md-12">
                  <div class="form-floating">
                    <input type="text" class="form-control" id="nombreEdit" name="nombreEdit" placeholder="Nombre del servicio" value="${servicio.serNombre}" required>
                    <label for="nombreEdit">Nombre</label>
                  </div>
                </div>

                <div class="col-md-12">
                  <div class="form-floating">
                    <input type="text" class="form-control" id="tipoEdit" name="tipoEdit" placeholder="Tipo Servicio" value="${servicio.serTipo}" required>
                    <label for="tipoEdit">Tipo Servicio</label>
                  </div>
                </div>

                <div class="col-12">
                  <div class="form-floating">
                    <textarea class="form-control" required placeholder="descripcionEdit" id="descripcionEdit" name="descripcionEdit"style="height: 100px;">${servicio.serDescripcion}</textarea>
                    <label for="descripcionEdit">Descripcion</label>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="col-md-12">
                    <div class="form-floating">
                      <input type="number" class="form-control" required id="precioEdit" name="precioEdit" placeholder="Precio" value="${servicio.serPrecio}">
                      <label for="precioEdit">Precio</label>
                    </div>
                  </div>
                </div>
                <div class="col-md-6" id="selectEstadoServicio">
                  <div class="form-floating mb-3">
                    <select class="form-select" id="estadoEdit" aria-label="State" name="estadoEdit" required>
                    <option value ="0" required selected>Seleccione Estado</option>
                    </select>
                    <label for="estadoEdit">Estado</label>
                  </div>
                </div>

                <div class="col-12">
                  <div class="form-floating">
                  <select class="form-select" id="empleadoEdit" aria-label="State" name="empleadoEdit" required>
                  <option value ="0" required selected>Seleccione Empleado</option>
                  <option value ="9999999999999" required>Sin Empleado</option>
                  </select>
                  <label for="empleadoEdit">Empleado</label>
                  </div>
                </div>

                <div class="col-12">
                  <div class="form-floating">
                  <select class="form-select" id="animalEdit" aria-label="State" name="animalEdit" required>
                  </select>
                  <label for="animalEdit">Servicio Dirigido a tipo animal</label>
                  </div>
                </div>
                
              </form>
    `
    document.getElementById("botonesIdServicio").innerHTML = `
        <div class="text-center">
            <button type="button" class="btn btn-success" onclick="editarServicio(${servicio.id})">Editar</button>
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cerrar</button>
        </div>
    `

    lista.forEach(e => {
        if (e[0] === servicio.serEstado) {
            document.getElementById("estadoEdit").innerHTML += `
            <option value="${servicio.serEstado}" selected >${servicio.serEstado}</option>   
            `;
        } else {
            document.getElementById("estadoEdit").innerHTML += `
            <option value="${e[0]}">${e[0]}</option>   
            `;
        }
    });
    
    if (servicio.serEmpleado !== null) {
        empleado.forEach(e => {
            if (e.id === servicio.serEmpleado) {
                document.getElementById("empleadoEdit").innerHTML += `
                <option value="${servicio.serEmpleado}" selected >${servicio.serNombreEmpleado} - ${servicio.serEmpleadoCargo}</option>   
                `;
            } else {
                document.getElementById("empleadoEdit").innerHTML += `
                <option value="${e.id}">${e.nombre} - ${e.cargo}</option>   
                `;
            }
        });
    } else {
        empleado.forEach(e => {
            document.getElementById("empleadoEdit").innerHTML += `
            <option value="${e.id}">${e.nombre} - ${e.cargo}</option>   
            `;
        });
    }
    

    animal.forEach(a => {
        if (a[0] === servicio.serDirigido) {
            document.getElementById("animalEdit").innerHTML += `
            <option value="${servicio.serDirigido}" selected >${servicio.serDirigido}</option>   
            `;
        } else {
            document.getElementById("animalEdit").innerHTML += `
            <option value="${a[0]}">${a[1]}</option>   
            `;
        }
    });
}

function editarServicio(id) {
    try {
        Swal.fire({
            title: 'Confirmar Edicion',
            text: '¿Estas seguro de editar el servicio?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, editar el servicio',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                idServicio = id
                let url = '/editarServicioAdmin/'+idServicio+'/'
                let formData = new FormData(document.getElementById('formEditarServicio'));

                let options = {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    }
                };

                fetch(url, options)
                    .then(res => res.json())
                    .then(data => {
                        if(estado = true) {
                            Swal.fire({
                                title: 'Sistema Veterinaria Animalagro',
                                text: data.mensaje,
                                icon: 'success',               
                                confirmButtonColor: '#3085d6',             
                                confirmButtonText: 'Aceptar'
                            }).then((result) => {
                                if (result.isConfirmed) {           
                                    window.location.reload();
                                }});
                        } else {
                            Swal.fire({
                                title: 'Sistema veterinaria animalgro',
                                text: 'Algo salio mal, intenta mas tarde',
                                icon: 'error',                          
                                confirmButtonText: 'Aceptar'
                            })
                        }
                    })
                    .catch(error => {
                        console.log(error);
                    });
                }
        });
    } catch (error) {
        console.log(error)
    }
}

function agregarServicio() {
    let nombre =  document.getElementById("txtNombreServicio").value
    let tipo = document.getElementById("txtTiposer").value
    let descripcion = document.getElementById('txtDescripcionser').value
    let precio = document.getElementById('txtPrecioSer').value
    let empleado = document.getElementById('cbEmpleado').value
    let animal = document.getElementById('cbTipoAnimalDirigido').value
    let foto = document.getElementById('fileFotoSer')
    const selectedFile = foto.files[0];

    if ((nombre != '') && (descripcion != '') && (precio != '') && (tipo != "") && (animal != '') ) {
        if (selectedFile) {
            let formData = new FormData(document.getElementById('idAgregarServicio'));

            let options = {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            };
            
            let url = '/agregarServicio/'
            try {
                fetch(url, options)
                .then((response) => response.json())
                .then(data => {
                            estado = data.estado 
                            if(estado = true) {
                                Swal.fire({
                                    title: 'Sistema Veterinaria Animalagro',
                                    text: data.mensaje,
                                    icon: 'success',               
                                    confirmButtonColor: '#3085d6',             
                                    confirmButtonText: 'Aceptar'
                                }).then((result) => {
                                    if (result.isConfirmed) {           
                                        window.location.reload();
                                    }});
                            } else {
                                Swal.fire({
                                    title: 'Sistema veterinaria animalgro',
                                    text: 'Algo salio mal, intenta mas tarde',
                                    icon: 'error',                          
                                    confirmButtonText: 'Aceptar'
                                })
                            }
                        }
                    )                
            }
            catch (error) {
                console.log(error)
            }
        } else {
            Swal.fire({
                title: 'Faltan Datos',
                text: 'Escoge una foto para el servicio, ¡la foto es unica, no la puedes editar!',
                icon: 'error',                          
                confirmButtonText: 'Aceptar'
            })
        }
        
    } else {
        Swal.fire({
            title: 'Faltan Datos',
            text: 'Digita Todos Lo Campos Requridos',
            icon: 'error',                          
            confirmButtonText: 'Aceptar'
        })
    } 
}

function asignarEmpleado() {
    let servicio = document.getElementById('cbservicio').value
    let empleado= document.getElementById('cbempleado').value
    if ((servicio != 0) && (empleado != 0)) {
        let data ={
            "servicio": servicio,
            "empleado": empleado,
        }
        let options = {
            method: 'POST',
            body: JSON.stringify(data),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    "Content-Type": "application/json"
                }
            }
        let url = '/asignarservicio/'
        try {
            fetch(url, options).then((response) => response.json()).then(data => {
                        console.log(data)
                        estado = data.estado 
                        if(estado = true) {
                            Swal.fire({
                                title: 'Sistema veterinaria animalgro',
                                text: data.mensaje,
                                icon: 'success',                          
                                confirmButtonText: 'Aceptar'
                            }).then((result) => {
                                if (result.isConfirmed) {           
                                    window.location.reload();
                                }});
                            
                        } else {
                            Swal.fire({
                                title: 'Sistema veterinaria animalgro',
                                text: 'Algo salio mal, intenta mas tarde',
                                icon: 'error',                          
                                confirmButtonText: 'Aceptar'
                            })
                        }
                    }
                )                
        } catch (error) {
            console.log(error)
        }
    }
    else{
        Swal.fire({
            title: 'Faltan Datos',
            text: 'Digita Todos Lo Campos Requridos',
            icon: 'error',                          
            confirmButtonText: 'Aceptar'
        })
    }
}



function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                return cookieValue;
            }
        }
    }
}


