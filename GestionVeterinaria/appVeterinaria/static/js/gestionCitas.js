function cancelar(id) {
    const ide = id
    url = '/cancelarCita/'+ide
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
}