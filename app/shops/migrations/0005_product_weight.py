# Generated by Django 5.0.6 on 2024-07-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_translations'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.PositiveIntegerField(default=1000, help_text='Weight in grams'),
            preserve_default=False,
        ),
    ]
