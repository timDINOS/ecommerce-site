from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='Address',
            options={'verbose_name_plural': 'Addresses'},
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]