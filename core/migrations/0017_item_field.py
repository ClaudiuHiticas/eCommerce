# Generated by Django 2.2.4 on 2020-04-21 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20200421_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='field',
            field=models.CharField(default='text', max_length=100),
            preserve_default=False,
        ),
    ]
