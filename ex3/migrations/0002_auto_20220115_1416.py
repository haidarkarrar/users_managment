# Generated by Django 3.2.9 on 2022-01-15 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ex3', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ex3.company'),
        ),
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ex3.currency'),
        ),
    ]