# Generated by Django 4.1.7 on 2023-04-27 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastrar', '0009_alter_ajudamanager_tema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ajudamanager',
            name='tema',
            field=models.CharField(choices=[('DA', 'DIFICULDADE DE ACESSO'), ('NRC', 'NAO SEI REALIZAR O CADASTRO'), ('ED', 'ERRO NOS DADOS'), ('NRD', 'NÃO RECEBO MAIS DADOS'), ('NQD', 'NÃO QUERO MAIS RECEBER DADOS'), ('TT', 'TROQUEI DE TITULAR'), ('OT', 'OUTRO')], max_length=40),
        ),
        migrations.AlterField(
            model_name='registrodisparo',
            name='assessor',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='registrodisparo',
            name='disparador',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='registrodisparo',
            name='titular',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]