# Generated by Django 3.2.12 on 2023-02-07 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caloriescounter_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food_item_gredient',
            name='username',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
