
// function verificacionDatos(){
//     nombre = document.getElementById("txtNombre").value
//     apellido = document.getElementById("txtApellido").value
//     identificacion = document.getElementById("txtIdentificacion").value
//     correo = document.getElementById("txtCorreo").value
//     contraseña = document.getElementById("txtContraseña").value
//     telefono = document.getElementById("txtTelefono").value
//     direccion = document.getElementById("txtDireccion").value
//     op =document.getElementById("cbIdentificacioon").value
//     tipo = op.options[op.selectedIndex].value
//     estado = true
//     if ((nombre == "") && (apellido == "") && (identificacion == "")  && (correo== "") && (contraseña == "") && (telefono == "") && (direccion == "") && (tipo == "")) {
//         return false
//     }
// }

// function agregarUsuario() {
//     verificar = verificacionDatos()

//     if (verificar == true) {
//         op =document.getElementById("cbIdentificacioon").value
//         tipo = op.options[op.selectedIndex].value
//         let data ={
//             "nombre": document.getElementById("txtNombre").value,
//             "apellido": document.getElementById("txtApellido").value,
//             "identificacion": parseInt(document.getElementById("txtIdentificacion").value),
//             "correo": document.getElementById("txtCorreo").value,
//             "contraseña": document.getElementById("txtContraseña").value,
//             "Telefono": parseInt(document.getElementById("txtTelefono").value),
//             "Dirrecion": document.getElementById("txtDireccion").value,
//             "tipoIde": tipo
//         }
//         let options = {
//             method: 'POST',
//             body: JSON.stringify(data),
//             headers: {
//                 'X-CSRFToken': getCookie('csrftoken'),
//                 "Content-Type": "application/json"
//             }
//         }
//         url = '/registrarseUser/'
//         fetch(url, options).then(res => res.json).then(
//             data => {
//                 if(data.estado == True){
//                     Swal.fire({
//                         title: 'Bienvenido',
//                         text: 'Felicitaciones Fuiste Agregado A Nuestro Sistema',
//                         icon: 'success',                          
//                         confirmButtonText: 'Aceptar'
//                     })
//                 }
//             }
//         )
//     } else {
//         Swal.fire({
//             title: 'Faltan Datos',
//             text: 'Digita Todos Lo Campos Requridos',
//             icon: 'error',                          
//             confirmButtonText: 'Aceptar'
//         })
//     }
// }

