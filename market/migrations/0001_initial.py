# Generated by Django 2.2.3 on 2019-08-03 16:50

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import market.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=market.models.PathAndRename('Cat/t/2019/08/03'), verbose_name='Thumbnail')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Order')),
                ('param', jsonfield.fields.JSONField(default=dict, max_length=300, verbose_name='Parameters')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='market.Category', verbose_name='Parent Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('status', models.BooleanField(choices=[(True, 'Active'), (False, 'DeActive')], default=True, help_text='Status of Product', verbose_name='Status')),
                ('unit', models.PositiveSmallIntegerField(choices=[(0, 'Number'), (1, 'Box'), (2, 'Liter'), (3, 'MiliLiter'), (4, 'Cc'), (5, 'KiloGram'), (6, 'Gram'), (7, 'MiliGram')], default=0, help_text='Unit of Product', verbose_name='Unit')),
                ('thumb', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='Thumbnail')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('categories', models.ManyToManyField(related_name='Products', to='market.Category', verbose_name='Categories')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='Title')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.BigIntegerField(default=0, help_text='Sell in Toman', verbose_name='Price')),
                ('discount_ratio', models.PositiveSmallIntegerField(default=0, help_text='Discount percent %', verbose_name='Discount Ratio')),
                ('qnt', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.Product', verbose_name='Quantity')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpecie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200, verbose_name='Text')),
                ('product_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='market.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameters', jsonfield.fields.JSONField(default=dict, max_length=300, verbose_name='Parameters')),
                ('product_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='market.Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='market.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to=market.models.PathAndRename('prod/'), verbose_name='Image')),
                ('main', models.BooleanField(default=False, verbose_name='Main Image')),
                ('prod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.Product', verbose_name='Product')),
            ],
        ),
    ]
