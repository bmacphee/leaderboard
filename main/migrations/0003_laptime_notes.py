# Generated by Django 2.1.15 on 2020-01-12 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200112_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptime',
            name='notes',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
