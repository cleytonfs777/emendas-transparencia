# Generated by Django 4.1.7 on 2023-04-12 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastrar', '0003_remove_assessor_telefone_remove_titular_telefone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titular',
            name='id_chat_d',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
