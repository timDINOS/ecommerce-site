from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20190616_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name="AccountProfile",
            fields = [
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(blank=True, max_length=100, null=True)),
                ('pay_with_click', models.BooleanField()),
            ],
        ),
    ]