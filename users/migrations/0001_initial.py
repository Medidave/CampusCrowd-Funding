# Generated by Django 5.0.6 on 2024-07-16 09:40

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('profile_image', models.ImageField(blank=True, default='profiles/user-default.png', null=True, upload_to='profiles/')),
                ('about_you', models.TextField(blank=True, null=True)),
                ('reference_number', models.IntegerField(blank=True, null=True)),
                ('programme_of_study', models.CharField(blank=True, max_length=250, null=True)),
                ('name_of_institution', models.CharField(blank=True, max_length=250, null=True)),
                ('abbreviation_of_institution', models.CharField(blank=True, max_length=250, null=True)),
                ('college_name', models.CharField(blank=True, max_length=250, null=True)),
                ('category', models.CharField(choices=[('student', 'Student'), ('investor', 'Investor'), ('faculty', 'Faculty')], default='Student', max_length=25)),
                ('contact', models.IntegerField(blank=True, null=True)),
                ('linkedIn_url', models.CharField(blank=True, max_length=300, null=True)),
                ('website_url', models.CharField(blank=True, max_length=250, null=True)),
                ('stars', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_title', models.CharField(blank=True, max_length=250)),
                ('brief_description', models.CharField(max_length=500)),
                ('about_project', models.TextField(blank=True, null=True)),
                ('project_image', models.ImageField(upload_to='project_images/')),
                ('project_target_amount', models.IntegerField(blank=True, null=True)),
                ('target_funding_period_in_days', models.IntegerField(blank=True, null=True)),
                ('amount_raised', models.IntegerField(default=0)),
                ('project_short_demo_video', models.FileField(blank=True, null=True, upload_to='project_videos/')),
                ('project_stars', models.IntegerField(default=0)),
                ('has_update', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('project_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ProjectUpdate',
            fields=[
                ('title', models.CharField(max_length=350)),
                ('update', models.TextField()),
                ('update_number', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.project')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.project')),
            ],
            options={
                'unique_together': {('user', 'project')},
            },
        ),
    ]
