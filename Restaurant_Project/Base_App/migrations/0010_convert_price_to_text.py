# Generated manually to convert price field to text for encryption

from django.db import migrations, models
import Base_App.encryption


class Migration(migrations.Migration):

    dependencies = [
        ('Base_App', '0009_alter_booktable_email_alter_order_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='price',
            field=Base_App.encryption.EncryptedIntegerField(db_index=True),
        ),
    ] 