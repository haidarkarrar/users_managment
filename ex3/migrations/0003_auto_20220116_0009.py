# Generated by Django 3.2.9 on 2022-01-15 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ex3', '0002_auto_20220115_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='ex3.company'),
        ),
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency', to='ex3.currency'),
        ),
        migrations.AlterField(
            model_name='item',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='ex3.supplier'),
        ),
    ]
