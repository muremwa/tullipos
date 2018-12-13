# Generated by Django 2.1.2 on 2018-11-12 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20181112_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoe',
            name='image',
        ),
        migrations.AddField(
            model_name='shoeimages',
            name='shoe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shoe'),
        ),
    ]
