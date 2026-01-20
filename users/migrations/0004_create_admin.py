from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_admin_user(apps, schema_editor):
    User = apps.get_model('users', 'User')

    if not User.objects.filter(email="admin@example.com").exists():
        User.objects.create(
            username="admin",
            email="admin@example.com",
            password=make_password("admin123"),  # ✅ hash manually
            is_staff=True,
            is_superuser=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_id'),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
