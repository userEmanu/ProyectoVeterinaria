




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

function detallepedido(id) {
    const ide = id
    url = '/detPedidoUser/'+ide+'/'
    console.log(url)
        try {
            fetch(url)
               .then((response) => response.json())
               .then(data => {
                        estado = data.estado 
                        if(estado = true) {
                            document.getElementById("detalle").innerHTML = ""
                            document.getElementById("detalleEnvioUser").innerHTML = ""
                            document.getElementById("botonesId").innerHTML = ""

                            mostrarDet(data.detalle, data.ped, data.envio)
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



function mostrarDet(detalle, pedido, envio) {

    

    detalle.forEach(det => {
        document.getElementById("detalle").innerHTML += `
        <tr>
            <td>${det.Nombre}</td>
            <td>${det.precioUni}</td>
            <td>${det.descuento}</td>
            <td>${det.porcentaje} %</td>
            <td>${det.cantidad}</td>
            <td>${det.precio}</td>
        </tr>`;
    });

    envio.forEach(en => {
        document.getElementById("detalleEnvioUser").innerHTML += `
        <tr>
            <td>${en.detNombre}</td>
            <td>${en.detTelefono}</td>
            <td>${en.detCorreo}</td>
            <td>${en.detDireccion} %</td>
            <td>${en.detUbicacion}</td>
        </tr>`;
    });


    const estado = "Solicitado"
    if (pedido.estado === estado ) {
        document.getElementById("botonesId").innerHTML = `
        <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cerrar</button>
        <form enctype="multipart/form-data" id="formComprobante">
        <button type="button" class="btn btn-success" onclick="cargarImagenComprobante(${pedido.idPedido})">Subir Imagen</button>
        <label class="btn btn-warning " title="Subir comprobante de pago, Imagen" style="color: rgb(255, 255, 255);" >
            <input type="file" id="fileFoto" name="fileFoto" style="display: none;">
            <i class="bi bi-upload"></i> Cargar Comprobante
        </label>
        </form>
        <button type="button" class="btn btn-danger" onclick="cancelarPedido(${pedido.idPedido})">Cancelar Pedido</button>
    `;
    } else {
        document.getElementById("botonesId").innerHTML = `
        <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cerrar</button>
    `;
    }
}

function cancelarPedido(id) {
    try {
        Swal.fire({
            title: 'Confirmar cancelacion de pedido',
            text: '¿Estás seguro de que quieres cancelar el pedido?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, cancelar pedido',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {

                url = "/cancelarPedidoUser/"+id+"/"
                fetch(url)
               .then((response) => response.json())
               .then(data => {
                        if(data.estado) {
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
        });
    } catch (error) {
        console.log(error)
    }
}

function cargarImagenComprobante(id) {
    try {
        const fileInput = document.getElementById("fileFoto");
        const selectedFile = fileInput.files[0];

        if (selectedFile) {
            const imageUrl = URL.createObjectURL(selectedFile);
            Swal.fire({
                title: 'Confirmar cargar comprobante',
                text: '¿Estás seguro de que quieres cargar el comprobante?',
                icon: 'question',
                imageUrl: imageUrl,
                imageAlt: 'Vista previa de la imagen',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, cargar comprobante',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    
                    let formData = new FormData(document.getElementById('formComprobante'));

                    let options = {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                        }
                    };

                    let url = "/subirImagenComprobante/" + id + "/";
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
        } else {
            Swal.fire({
                title: 'Carga la imagen',
                text: 'Carga la imagen del comprobante',
                icon: 'error',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Aceptar'
            });
        }
    } catch (error) {
        console.log(error);
    }
}

function agregarMascota() {
    try {

        let formData = new FormData(document.getElementById('formAgregarMascota'));

        let options = {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        };

        let url = "/agregarMacota/";
        fetch(url, options)
            .then(res => res.json())
            .then(data => {
                if(data.estado) {
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
                        text: data.mensaje,
                        icon: 'error',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'Aceptar'
                    });                    
                }
            })
            .catch(error => {
                console.log(error);
            });

    } catch (error) {
        console.log(error)
    }
}

function registrarseComoUsuario() {
    try {
        
        let formData = new FormData(document.getElementById('idFormRegistrarse'));

        let options = {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        };

        let url = "/registrarseUser/";
        fetch(url, options)
            .then(res => res.json())
            .then(data => {
                if(data.estado) {
                    Swal.fire({
                        title: 'Sistema Veterinaria Animalagro',
                        text: data.mensaje,
                        icon: 'success',               
                        confirmButtonColor: '#3085d6',             
                        confirmButtonText: 'Aceptar'
                    }).then((result) => {
                        if (result.isConfirmed) {           
                            window.location.href="/inicio/"
                        }});
                } else {
                    Swal.fire({
                        title: 'Sistema veterinaria animalgro',
                        text: data.mensaje,
                        icon: 'error',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'Aceptar'
                    });                    
                }
            })
            .catch(error => {
                console.log(error);
            });
    } catch (error) {
        console.log(error)
    }
}


function subirImagenPerfil(id) {
    try {
        const fileInput = document.getElementById("FilefotoPerfil");
        const selectedFile = fileInput.files[0];

        if (selectedFile) {
            Swal.fire({
                title: 'Confirmar actualizacion de foto',
                text: '¿Estás seguro de que deseas cambiar la foto de perfil?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, actualizar foto',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    let formData = new FormData(document.getElementById('imagenPerfil'));

                    let options = {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                        }
                    };

                    let url = "/subirImagenPerfil/" + id + "/";
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
        } else {
            Swal.fire({
                title: 'Carga la imagen',
                text: 'Carga la imagen',
                icon: 'error',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Aceptar'
            });
        }
    } catch (error) {
        console.log(error)
    }
}

function actualizarperfil(id) {
    try {
        const nombre = document.getElementById("nombreEdit").value
        const apellido = document.getElementById("apellidoEdit").value
        const email = document.getElementById("emailEdit").value
        const telefono = document.getElementById("telefonoEdit").value
        const numero = document.getElementById("noDocEdit").value
        const tipo = document.getElementById("cbTipoEdit").value

        if (nombre, apellido, email, telefono, numero, tipo != "") {
            Swal.fire({
                title: 'Confirmar actualizacion de Datos',
                text: '¿Estás seguro de que deseas actualizar tu informacion?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, actualizar datos',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    let formData = new FormData(document.getElementById('editarperfil'));
    
                    let options = {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                        }
                    };
    
                    let url = "/actualizarDatosPerfil/" + id + "/";
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
        } else {
            Swal.fire({
                title: 'Faltan Datos',
                text: 'Faltan Datos',
                icon: 'error',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Aceptar'
            });
        }
    } catch (error) {
        console.log(error)
    }
}



function mascotaDetalleCita(id) {
    const ide = id
    url = '/detalleCitaMascota/'+ide+'/'
    console.log(url)
        try {
            fetch(url)
               .then((response) => response.json())
               .then(data => {
                        estado = data.estado 
                        if(estado === true) {
                            document.getElementById("citasMascota").innerHTML = ""
                            mostarDetCita(data.cita)
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

function mostarDetCita(cita) {
    cita.forEach(ci => {
        if (ci.ciPdf === true) {
            document.getElementById("citasMascota").innerHTML += `
                <tr>
                    <td>${ci.ciServicio}</td>
                    <td>${ci.ciPrecio}</td>
                    <td>${ci.ciFecha}</td>
                    <td>${ci.ciEstado} </td>
                    <td>${ci.ciVeterinario}</td>
                    <td>No hay Pdf</td>
                </tr>`;
        } else {
            document.getElementById("citasMascota").innerHTML += `
                <tr>
                    <td>${ci.ciServicio}</td>
                    <td>${ci.ciPrecio}</td>
                    <td>${ci.ciFecha}</td>
                    <td>${ci.ciEstado} </td>
                    <td>${ci.ciVeterinario}</td>
                    <td><a href="https://veterinariaanimalagro.pythonanywhere.com/${ci.ciPdf}">Ver Historial</a></td>
                </tr>`;
        }
    });
}

// 
// Perfil
// Administrador
// 

