# Generated by Django 4.1.7 on 2023-04-14 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastrar', '0004_alter_titular_id_chat_d'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessor',
            name='ddd',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='titular',
            name='ddd',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
