# Generated by Django 2.2.4 on 2020-04-22 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_remove_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='camasa.jpg', upload_to=''),
            preserve_default=False,
        ),
    ]