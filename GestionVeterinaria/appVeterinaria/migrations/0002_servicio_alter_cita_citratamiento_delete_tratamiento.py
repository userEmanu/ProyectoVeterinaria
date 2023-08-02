# Generated by Django 4.2.2 on 2023-07-29 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appVeterinaria', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serNombre', models.CharField(db_comment='Nombre del tratamiento', max_length=30, unique=True)),
                ('serTipo', models.CharField(db_comment='Tipo de tratamiento, si es cirugia, revision', max_length=40)),
                ('serPrecio', models.IntegerField(db_comment='Precio del Tratamiento')),
                ('serDescripcion', models.TextField(db_comment='Descripcion Del servicio')),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('serEmpleado', models.ForeignKey(db_comment='El empleado que atiende este servicio', null=True, on_delete=django.db.models.deletion.PROTECT, to='appVeterinaria.empleado')),
            ],
        ),
        migrations.AlterField(
            model_name='cita',
            name='ciTratamiento',
            field=models.ForeignKey(db_comment='Tratmiento', null=True, on_delete=django.db.models.deletion.PROTECT, to='appVeterinaria.servicio'),
        ),
        migrations.DeleteModel(
            name='Tratamiento',
        ),
    ]
