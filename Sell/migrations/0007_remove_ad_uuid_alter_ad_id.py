# Generated by Django 5.2.1 on 2025-05-22 10:35

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sell', '0006_alter_ad_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='uuid',
        ),
        migrations.AlterField(
            model_name='ad',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
