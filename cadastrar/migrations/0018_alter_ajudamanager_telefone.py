# Generated by Django 4.1.7 on 2023-05-15 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastrar', '0017_alter_ajudamanager_categoria_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ajudamanager',
            name='telefone',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]