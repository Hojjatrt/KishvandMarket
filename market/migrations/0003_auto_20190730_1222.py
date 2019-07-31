# Generated by Django 2.2 on 2019-07-30 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_auto_20190730_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categories',
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(null=True, related_name='Products', to='market.Category', verbose_name='Categories'),
        ),
    ]