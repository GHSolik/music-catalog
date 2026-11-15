
from django.db import migrations


def add_track_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    database = schema_editor.connection.alias

    group, created = Group.objects.using(database).get_or_create(
        name="Moderators"
    )

    content_type, created = ContentType.objects.using(
        database
    ).get_or_create(
        app_label="catalog",
        model="track"
    )

    for action in ["change", "delete"]:
        permission, created = Permission.objects.using(
            database
        ).get_or_create(
            content_type=content_type,
            codename=f"{action}_track",
            defaults={
                "name": f"Can {action} track"
            }
        )

        group.permissions.add(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_albumrating"),
    ]

    operations = [
        migrations.RunPython(
            add_track_permissions,
            migrations.RunPython.noop,
        ),
    ]
