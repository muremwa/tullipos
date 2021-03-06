# Generated by Django 2.1.2 on 2018-11-12 13:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20181112_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorder',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shoe',
            name='name_slug',
            field=models.SlugField(blank=True, help_text="how do you want the url to appear don't edit. An automatic one is generated from name"),
        ),
    ]
