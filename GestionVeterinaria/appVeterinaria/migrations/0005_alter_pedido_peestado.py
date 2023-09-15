# Generated by Django 4.2.2 on 2023-08-25 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appVeterinaria', '0004_alter_pedido_peestado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='peEstado',
            field=models.CharField(choices=[('Enviado', 'Enviado'), ('Entregado', 'Entregado'), ('Solicitado', 'Solicitado'), ('Rechazado', 'Rechazado'), ('Cancelado', 'Cancelado'), ('Pago Cargado', 'Pago Cargado')], db_comment='estado del pedido', max_length=14),
        ),
    ]
