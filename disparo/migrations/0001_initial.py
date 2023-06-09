# Generated by Django 4.1.7 on 2023-04-10 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Imagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='imagem_disparo/')),
            ],
        ),
        migrations.CreateModel(
            name='RegAssessor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_cat', models.CharField(blank=True, max_length=40)),
                ('nome_ass', models.CharField(blank=True, max_length=50)),
                ('id_a', models.CharField(blank=True, default='', max_length=15)),
                ('nome_tit', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RegTitular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_cat', models.CharField(blank=True, max_length=40)),
                ('nome_tit', models.CharField(blank=True, max_length=50)),
                ('id_t', models.CharField(blank=True, default='', max_length=15)),
                ('only_assec', models.BooleanField(default=False)),
            ],
        ),
    ]
