# Generated by Django 3.2.18 on 2023-05-15 09:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0002_auto_20230515_0908"),
    ]

    operations = [
        migrations.CreateModel(
            name="PNGImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="PNGs/")),
                ("name", models.CharField(max_length=255)),
                ("size", models.IntegerField()),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name="Image",
        ),
    ]
