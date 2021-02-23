# Generated by Django 3.1.6 on 2021-02-22 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210210_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pila',
            name='estado',
            field=models.CharField(choices=[(1, 'Fase I: mesófila'), (2, 'Fase II: termófila'), (3, 'Fase III: enfriamiento'), (4, 'Fase IV: maduración')], max_length=50),
        ),
    ]