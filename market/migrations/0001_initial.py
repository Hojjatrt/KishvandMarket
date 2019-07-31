# Generated by Django 2.2.3 on 2019-07-29 15:09

from django.db import migrations, models
import django.db.models.deletion
import market.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('image', models.ImageField(blank=True, null=True, upload_to=market.models.PathAndRename('Categories/2019/07/29', 'Category'), verbose_name='Image')),
                ('thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to=market.models.PathAndRename('Categories/thumbnails/2019/07/29', 'Category'), verbose_name='Thumbnail')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Order')),
            ],
            options={
                'verbose_name': 'MainCategory',
                'verbose_name_plural': 'MainCategories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Order')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='market.MainCategory', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'SubCategory',
                'verbose_name_plural': 'SubCategories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Active'), (0, 'DeActive')], default=1, help_text='Status of Product', verbose_name='Status')),
                ('unit', models.PositiveSmallIntegerField(choices=[(0, 'Number'), (1, 'Box'), (2, 'Liter'), (3, 'MiliLiter'), (4, 'Cc'), (5, 'KiloGram'), (6, 'Gram'), (7, 'MiliGram')], default=0, help_text='Unit of Product', verbose_name='Unit')),
                ('price', models.BigIntegerField(help_text='Sell in Toman', verbose_name='Price')),
                ('discount_ratio', models.PositiveSmallIntegerField(help_text='Discount percent', verbose_name='Discount Ratio')),
                ('image', models.ImageField(blank=True, null=True, upload_to=market.models.PathAndRename('products/2019/07/29', 'Product'), verbose_name='Image')),
                ('thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to=market.models.PathAndRename('products/thumbnails/2019/07/29', 'Product'), verbose_name='Thumbnail')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('capacity', models.PositiveIntegerField(default=0, verbose_name='Capacity')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Products', to='market.SubCategory', verbose_name='Category')),
                ('tags', models.ManyToManyField(to='market.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
