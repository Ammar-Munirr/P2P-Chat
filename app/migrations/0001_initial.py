# Generated by Django 5.0.4 on 2024-05-16 17:21

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
            name='MyChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.JSONField(default=dict)),
                ('frnd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frnd', to=settings.AUTH_USER_MODEL)),
                ('me', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='me', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
