

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
                            document.getElementById("botonesId").innerHTML = ""
                            document.getElementById("ImagenComprobante").innerHTML = ""
                            document.getElementById("detalleEnvioUser").innerHTML = ""
                            mostrarDet(data.detalle, data.ped, data.estado, data.envio)
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

function mostrarDet(detalle, pedido, estado, envio) {
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
    document.getElementById("botonesId").innerHTML = `
    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cerrar</button>
    <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#modalImageComprobante" data-bs-backdrop="true">Visualizar Comprobante</button>
    <select class="form-select" name="cbEstado" id="cbEstado"  required>                                  
    </select>
    <button type="button" class="btn btn-success" onclick="cambiarEstado(${pedido.idPedido}, '${pedido.estado}')" >Cambiar Estado</button>
    `;

    
    estado.forEach(e => {
        if (e[0] === pedido.estado) {
            document.getElementById("cbEstado").innerHTML += `
            <option value="${pedido.estado}" selected >${pedido.estado}</option>   
            `;
        } else {
            document.getElementById("cbEstado").innerHTML += `
            <option value="${e[0]}">${e[0]}</option>   
            `;
        }
    });
    
    document.getElementById("ImagenComprobante").innerHTML= `
        <img class="" src="../media/${pedido.foto}" alt="" id="zoomable-image" >
    `;

    const imageElement = document.querySelector('#zoomable-image');
    imageElement.addEventListener('load', function () {
        mediumZoom(imageElement);
    });
    
}

function cambiarEstado(id, estado) {
    try {
        const ide = id;
        const estadoPedido = estado.toString();
        const estadoElegido = document.getElementById("cbEstado").value;

        if (estadoPedido != estadoElegido) {
            Swal.fire({
                title: 'Confirmar cambio de estado',
                text: '¿Estás seguro de que deseas cambiar el estado?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, cambiar estado',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    let data ={
                        "estado": estadoElegido
                    }
                    let options = {
                        method: 'POST',
                        body: JSON.stringify(data),
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken'),
                                "Content-Type": "application/json"
                            }
                        }
                    let url = '/cambiarEstadoPedido/'+ide+'/'
                    try {
                        fetch(url, options).then((response) => response.json()).then(data => {
                                    if(data.estado) {
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
            });
        } else {
            Swal.fire({
                title: 'Sistema veterinaria animalgro',
                text: 'Elige un estado',
                icon: 'error',                          
                confirmButtonText: 'Aceptar'
            });
        }
    } catch (error) {
        console.log(error);
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