# Generated by Django 5.1.6 on 2025-02-24 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
