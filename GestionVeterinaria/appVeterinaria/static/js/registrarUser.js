
function verificacionDatos(){
    nombre = document.getElementById("txtNombre")
    apellido = document.getElementById("txtApellido")
    identificacion = document.getElementById("txtIdentificacion")
    correo = document.getElementById("txtCorreo")
    contraseña = document.getElementById("txtContraseña")
    telefono = document.getElementById("txtTelefono")
    direccion = document.getElementById("txtDireccion")

    if (nombre == "" && apellido == "" && identificacion == ""  && correo== "" && contraseña == "" && telefono == "" && direccion == "") {
        return false
    } else {
        return true
    }
}

function agregarUsuario() {
    verificar = verificacionDatos()

    if (verificar == true) {
        let data ={
            "nombre": document.getElementById("txtNombre").value,
            "apellido": document.getElementById("txtApellido").value,
            "identificacion": parseInt(document.getElementById("txtIdentificacion")),
            "correo": document.getElementById("txtCorreo").value,
            "contraseña": document.getElementById("txtContraseña").value,
            "Telefono": parseInt(document.getElementById("txtTelefono")),
            "Dirrecion": document.getElementById("txtDireccion").value,
            "tipoIde": document.getElementById("cbIdentificacioon")
        }
        option = Ajax(data)
        url = '/registrarse/'
        fetch(url, option).then(res => res.json).then(
            data => {
                
            }
        )
    } else {
        
    }
}

function Ajax(data) {
    let options = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            "Content-Type": "application/json"
        }
    }

    return options
}