# Generated manually to fix price column type

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Base_App', '0010_convert_price_to_text'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward SQL: Convert integer column to text
            sql="ALTER TABLE \"Base_App_items\" ALTER COLUMN price TYPE text USING price::text;",
            # Reverse SQL: Convert text column back to integer (if needed)
            reverse_sql="ALTER TABLE \"Base_App_items\" ALTER COLUMN price TYPE integer USING price::integer;",
        ),
    ] 