# Generated by Django 4.1.7 on 2023-04-23 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disparo', '0003_editassessor'),
    ]

    operations = [
        migrations.AddField(
            model_name='editassessor',
            name='telefone',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
