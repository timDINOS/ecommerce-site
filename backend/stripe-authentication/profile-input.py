from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='AccountProfile',
            name="pay_with_click",
            field=models.BooleanField(default=False),
        ),
    ]