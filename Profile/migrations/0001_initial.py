# Generated by Django 3.2.2 on 2021-05-27 17:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likeLike', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('userLike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='reviews')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_children', to='Profile.reviews', verbose_name='Родительский комментарий')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostWall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('des', models.CharField(max_length=256)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='post')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('editMode', models.BooleanField(default=False)),
                ('like', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.likepost')),
                ('reviews', models.ManyToManyField(to='Profile.Reviews')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
