function cancelar(id) {
    const ide = id
    url = '/cancelarCita/'+ide+'/'
    console.log(url)
        try {
            Swal.fire({
            title: 'Confirmacion para cancelar cita',
            text: '¿Estás seguro de que deseas cancelar la cita?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, cancelar cita',
            cancelButtonText: 'Cancelar'
                }).then((result) => {
                    if (result.isConfirmed) {
                        fetch(url)
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
                                                        location.href="/gestionCitas/"
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
        }
        catch (error) {
            console.log(error)
        }
}

function cancelarDescripcion(id) {
    const ide = id
    url = '/cancelarCita/'+ide+'/'
    console.log(url)
        try {
            Swal.fire({
                title: 'Confirmacion para cancelar cita',
                text: '¿Estás seguro de que deseas cancelar la cita?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, cancelar cita',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(url)
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
                                                    location.href="/gestionCitas/"
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
        }
        catch (error) {
            console.log(error)
        }
}

function realizarCita(id) {
    let descripcion = document.getElementById('descripcion').value
    if (descripcion != "") {
        let data ={
            "descripcion": descripcion
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
        let url = '/realizarCita/'+id
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
    } else {
        Swal.fire({
            title: 'Faltan Datos',
            text: 'Digita Todos Lo Campos Requridos',
            icon: 'error',                          
            confirmButtonText: 'Aceptar'
        })
    }
}

function generarPdf(id) {
    const ide = id
    url = '/generarPDFHistorialEnviar/'+ide+'/'
    console.log(url)
        try {
            fetch(url)
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
