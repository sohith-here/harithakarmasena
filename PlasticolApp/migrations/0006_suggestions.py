# Generated by Django 5.0 on 2024-01-08 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlasticolApp', '0005_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=300)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
    ]
