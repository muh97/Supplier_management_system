# Generated by Django 3.2 on 2021-08-10 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_supplier_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partyplaner',
            name='price_small',
        ),
    ]
