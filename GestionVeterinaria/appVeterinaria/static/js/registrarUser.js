
function verificacionDatos(){
    nombre = document.getElementById("txtNombre").value
    apellido = document.getElementById("txtApellido").value
    identificacion = document.getElementById("txtIdentificacion").value
    correo = document.getElementById("txtCorreo").value
    contraseña = document.getElementById("txtContraseña").value
    telefono = document.getElementById("txtTelefono").value
    op =document.getElementById("cbIdentificacioon").value
    estado = true
    if ((nombre == "") || (apellido == "") ||  (identificacion == "") || (correo== "") ||  (contraseña == "") ||   (op == "")) {
        estado = false
    }

    return estado
}

function agregarUsuario() {
    verificar = verificacionDatos()
    console.log(verificar)
    if (verificar == true) {
        let data ={
            "nombre": document.getElementById("txtNombre").value,
            "apellido": document.getElementById("txtApellido").value,
            "identificacion": parseInt(document.getElementById("txtIdentificacion").value),
            "correo": document.getElementById("txtCorreo").value,
            "contra": document.getElementById("txtContraseña").value,
            "Telefono": parseInt(document.getElementById("txtTelefono").value),
            "tipoIde": document.getElementById("cbIdentificacioon").value
        }
        let options = {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                "Content-Type": "application/json"
            }
        }
        url = '/registrarseUser/'

        fetch(url, options)
        .then(res => res.json())
        .then(data => {
            if (data.estado == 0) {
                Swal.fire({
                    title: 'Eres Un Nuevo Usuario',
                    text: data.mensaje,
                    icon: 'Succes',               
                    confirmButtonColor: '#3085d6',             
                    confirmButtonText: 'Aceptar'
                }).then((result) => {
                    if (result.isConfirmed) {           
                        location.href="/inicio/"
                    }
                });
            }else{
                Swal.fire(
                    'Error',
                    data.mensaje,
                    'error'
                )
            }
        })
    } else {
        Swal.fire({
            title: 'Faltan Datos',
            text: 'Digita Todos Lo Campos Requridos',
            icon: 'error',                          
            confirmButtonText: 'Aceptar',
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