# Generated by Django 5.1.2 on 2024-12-17 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('discipline', models.ManyToManyField(to='training.discipline')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('course', models.ManyToManyField(to='training.course')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('venue', models.ManyToManyField(to='training.season')),
            ],
        ),
        migrations.CreateModel(
            name='Trainee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=50)),
                ('place', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('tid', models.EmailField(blank=True, max_length=50, null=True)),
                ('date_of_birth', models.DateField()),
                ('entry_date', models.DateField(auto_now_add=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('designation', models.CharField(choices=[('Student', 'Student'), ('Primary Teacher', 'Primary Teacher'), ('Secondary Teacher', 'Secondary Teacher'), ('Other', 'Other')], max_length=20)),
                ('photo', models.ImageField(upload_to='trainee_photos/')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=10)),
                ('residence_type', models.CharField(choices=[('Residential', 'Residential'), ('Non Residential', 'Non Residential')], max_length=20)),
                ('is_paid', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.course')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.discipline')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.district')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.level')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='training.season')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.venue')),
            ],
        ),
        migrations.AddField(
            model_name='discipline',
            name='venue',
            field=models.ManyToManyField(to='training.venue'),
        ),
    ]