# Generated by Django 4.2 on 2023-04-06 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Robot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('type', models.CharField(blank=True, max_length=30)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('ip', models.CharField(blank=True, max_length=30)),
                ('port', models.IntegerField(blank=True)),
                ('online', models.BooleanField(default=False)),
                ('status', models.JSONField(blank=True, default=dict)),
                ('task', models.CharField(blank=True, max_length=100, null=True)),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
    ]