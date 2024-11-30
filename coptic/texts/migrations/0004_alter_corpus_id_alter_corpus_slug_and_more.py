# Generated by Django 4.2.16 on 2024-11-30 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0003_html_visualization_updates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corpus',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='corpus',
            name='slug',
            field=models.SlugField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='htmlvisualization',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='metaorder',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='text',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='textmeta',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
