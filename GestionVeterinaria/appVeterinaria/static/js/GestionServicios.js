



function agregarServicio() {
    let nombre =  document.getElementById("txtNombreser").value
    let tipo = document.getElementById("txtTiposer").value
    let descripcion = document.getElementById('txtDescripcionser').value
    let precio = document.getElementById('txtPrecioSer').value
    let empleado = document.getElementById('cbEmpleado').value

    if ((nombre != '') && (descripcion != '') && (precio != '') ) {
        let data ={
            "nombre": nombre,
            "empleado": empleado,
            "precio": parseInt(precio),
            "descripcion": descripcion,
            "tipo": tipo
        }
        
        let options = {
        method: 'POST',
        body: JSON.stringify(data),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                "Content-Type": "application/json"
            }
        }
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
                                icon: 'Succes',               
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
            text: 'Digita Todos Lo Campos Requridos',
            icon: 'error',                          
            confirmButtonText: 'Aceptar'
        })
    } 
}

function asignarEmpleado() {
    console.log('holaaaaaaaaaaaaa')
    let servicio = document.getElementById('cbservicio').value
    let empleado= document.getElementById('cbempleado').value
    console.log('holaaaaaaaaaaaaa')
    if ((servicio != 0) && (empleado != 0)) {
        let data ={
            "servicio": servicio,
            "empleado": empleado,
        }
        console.log('holaaaaaaaaaaaaa')
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
                                icon: 'Succes',                          
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
