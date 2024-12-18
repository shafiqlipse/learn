# Generated by Django 5.1.2 on 2024-12-17 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainee',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.discipline'),
        ),
        migrations.RemoveField(
            model_name='level',
            name='course',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='discipline',
        ),
        migrations.AddField(
            model_name='level',
            name='discipline',
            field=models.ManyToManyField(to='training.discipline'),
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
