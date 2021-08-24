import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    
    dependencies = [ migrations.swappable_dependency(settings.AUTH_USER_MODEL), ]

