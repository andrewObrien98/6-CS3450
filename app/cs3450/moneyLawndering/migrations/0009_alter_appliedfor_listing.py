# Generated by Django 4.0.2 on 2022-03-15 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moneyLawndering', '0008_alter_appliedfor_listing_alter_appliedfor_worker_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedfor',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='moneyLawndering.listing'),
        ),
    ]
