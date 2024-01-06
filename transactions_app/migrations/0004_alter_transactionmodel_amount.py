# Generated by Django 4.2.4 on 2023-08-21 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions_app', '0003_alter_transactionmodel_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmodel',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=False, max_digits=12),
        ),
    ]
