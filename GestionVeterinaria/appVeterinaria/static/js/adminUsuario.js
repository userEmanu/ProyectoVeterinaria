
window.addEventListener('load', function() {
const switchCheckboxes = document.querySelectorAll('#flexSwitchCheck');
console.log(switchCheckboxes)
switchCheckboxes.forEach(function (switchCheckbox) {
    switchCheckbox.addEventListener('change', function () {
        const userId = this.getAttribute('data-user-id');
        const action = this.checked ? 'Activar' : 'Suspender';
        console.log(userId)
        Swal.fire({
            title: `¿Estás seguro de ${action} esta cuenta?`,
            text: `¿Estás seguro de ${action} esta cuenta?`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: `Sí, ${action} cuenta`,
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                if (action === "Suspender"){

                    const accion = "Suspendido"
                    url = "/suspenderUser/"+userId+"/"+accion+"/"
                    console.log(url)
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
                                        text: data.mensaje,
                                        icon: 'error',                          
                                        confirmButtonText: 'Aceptar'
                                    }).then((result) => {
                                        if (result.isConfirmed) {           
                                            window.location.reload();
                                    }});
                                }
                            }
                        )  

                }
                else{
                    
                    const accion = "Activo"
                    url = "/suspenderUser/"+userId+"/"+accion+"/"
                    console.log(url)
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
                                        text: data.mensaje,
                                        icon: 'error',                          
                                        confirmButtonText: 'Aceptar'
                                    }).then((result) => {
                                        if (result.isConfirmed) {           
                                            window.location.reload();
                                        }});
                                }
                            }
                        )
                }
            } else {
                this.checked = !this.checked;
            }
        });
    });
});
});