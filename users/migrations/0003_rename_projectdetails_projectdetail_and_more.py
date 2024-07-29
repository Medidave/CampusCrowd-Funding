# Generated by Django 5.0.6 on 2024-07-20 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_projectdetails'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectDetails',
            new_name='ProjectDetail',
        ),
        migrations.AddField(
            model_name='project',
            name='has_details',
            field=models.BooleanField(default=False),
        ),
    ]