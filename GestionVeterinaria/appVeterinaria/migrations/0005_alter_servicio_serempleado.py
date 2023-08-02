# Generated by Django 4.2.2 on 2023-08-01 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appVeterinaria', '0004_alter_servicio_serempleado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='serEmpleado',
            field=models.ForeignKey(db_comment='El empleado que atiende este servicio', null=True, on_delete=django.db.models.deletion.PROTECT, to='appVeterinaria.empleado'),
        ),
    ]
