# Generated by Django 2.1.2 on 2018-11-12 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoeImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='shoes/')),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='shoe',
            name='image',
        ),
        migrations.AlterField(
            model_name='shoe',
            name='name_slug',
            field=models.SlugField(default=models.CharField(max_length=50), help_text='how do you want the url to appear'),
        ),
        migrations.AddField(
            model_name='shoe',
            name='image',
            field=models.ManyToManyField(to='shop.ShoeImages'),
        ),
    ]
