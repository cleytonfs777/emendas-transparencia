# Generated by Django 4.2.8 on 2024-10-17 12:33

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
                ('nome_cat', models.CharField(blank=True, max_length=100)),
                ('nome_ass', models.CharField(blank=True, max_length=100)),
                ('id_a', models.CharField(blank=True, default='', max_length=50)),
                ('nome_tit', models.CharField(blank=True, max_length=100)),
                ('ddd', models.CharField(blank=True, max_length=2, null=True)),
                ('telfnumber', models.CharField(blank=True, max_length=300, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegTitular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_cat', models.CharField(blank=True, max_length=100)),
                ('nome_tit', models.CharField(blank=True, max_length=100)),
                ('id_t', models.CharField(blank=True, default='', max_length=30)),
                ('only_assec', models.BooleanField(default=False)),
                ('ddd', models.CharField(blank=True, max_length=2, null=True)),
                ('telfnumber', models.CharField(blank=True, max_length=250, null=True, unique=True)),
            ],
        ),
    ]
