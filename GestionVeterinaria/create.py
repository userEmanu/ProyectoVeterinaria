import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionVeterinaria.settings')
django.setup()

from appVeterinaria.models import User, Group  

def crearRole():
    try:
        Group.objects.get_or_create(name='Usuario')
        Group.objects.get_or_create(name='Administrador')
        Group.objects.get_or_create(name='Asistente')
        Group.objects.get_or_create(name='Medico')
        return True
    except Exception as e:
        print(e)
        
def create_super_user(username, email, password):
    try:
        k = crearRole()
        user = User.objects.create_superuser(username, email, password, first_name ="Super Administrador", userTipo ="Administrador", userTelefono = 3114921996)
        rol = Group.objects.get(pk=2)
        user.groups.add(rol)
        print(f"Superusuario '{username}' creado exitosamente.")
    except Exception as e:
        print(f"Error al crear el superusuario: {e}")

if __name__ == '__main__':
    create_super_user('veterinariaanimalagro@gmail.com', 'veterinariaanimalagro@gmail.com', 'admin')
