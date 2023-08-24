import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionVeterinaria.settings')
django.setup()

from appVeterinaria.models import User, Group  

def create_super_user(username, email, password):
    try:
        user = User.objects.create_superuser(username, email, password)
        rol = Group.objects.get(pk=2)
        user.groups.add(rol)
        print(f"Superusuario '{username}' creado exitosamente.")
    except Exception as e:
        print(f"Error al crear el superusuario: {e}")

if __name__ == '__main__':
    create_super_user('veterinariaanimalagro@gmail.com', 'veterinariaanimalagro@gmail.com', 'admin')
