# Generated by Django 3.2 on 2021-08-10 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_musician_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musician',
            name='price_small',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='price/small'),
        ),
        migrations.AlterField(
            model_name='musician',
            name='tool',
            field=models.CharField(choices=[('keyboard', 'keyboard'), ('singer', 'singer'), ('guitar', 'guitar'), ('saxophone', 'saxophone'), ('trumped', 'trumped')], max_length=15, null=True),
        ),
    ]
