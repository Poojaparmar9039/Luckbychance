# Generated by Django 5.2.1 on 2025-05-22 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sell', '0007_remove_ad_uuid_alter_ad_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='seller_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
