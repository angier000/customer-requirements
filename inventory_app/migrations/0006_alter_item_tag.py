# Generated by Django 4.2.6 on 2023-11-25 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_app', '0005_tag_item_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='inventory_app.tag'),
        ),
    ]