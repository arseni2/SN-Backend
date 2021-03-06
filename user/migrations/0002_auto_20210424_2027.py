# Generated by Django 3.2 on 2021-04-24 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='userPhoto',
            field=models.ImageField(null=True, upload_to='userPhotos'),
        ),
        migrations.AddField(
            model_name='user',
            name='year',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
