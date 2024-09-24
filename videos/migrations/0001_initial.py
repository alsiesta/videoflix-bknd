# Generated by Django 5.0.7 on 2024-09-24 11:44

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(default=datetime.date.today)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos')),
                ('image_file', models.FileField(blank=True, null=True, upload_to='images')),
                ('path', models.CharField(blank=True, max_length=255, null=True)),
                ('imagepath', models.CharField(blank=True, max_length=255, null=True)),
                ('categories', models.ManyToManyField(related_name='videos', to='videos.category')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video')),
            ],
            options={
                'unique_together': {('user', 'video')},
            },
        ),
    ]
