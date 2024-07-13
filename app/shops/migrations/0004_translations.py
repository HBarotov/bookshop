# Generated by Django 5.0.6 on 2024-07-13 15:56

import django.db.models.deletion
import parler.fields
import parler.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shops", "0003_alter_product_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryTranslation",
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
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=200, unique=True)),
            ],
            options={
                "verbose_name": "category Translation",
                "db_table": "shops_category_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name="ProductTranslation",
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
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=200)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "product Translation",
                "db_table": "shops_product_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "category", "verbose_name_plural": "categories"},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={},
        ),
        migrations.RemoveIndex(
            model_name="category",
            name="shops_categ_name_8341e2_idx",
        ),
        migrations.RemoveIndex(
            model_name="product",
            name="shops_produ_id_85f547_idx",
        ),
        migrations.RemoveIndex(
            model_name="product",
            name="shops_produ_name_495435_idx",
        ),
        migrations.RemoveField(
            model_name="category",
            name="name",
        ),
        migrations.RemoveField(
            model_name="category",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="product",
            name="description",
        ),
        migrations.RemoveField(
            model_name="product",
            name="name",
        ),
        migrations.RemoveField(
            model_name="product",
            name="slug",
        ),
        migrations.AddField(
            model_name="categorytranslation",
            name="master",
            field=parler.fields.TranslationsForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="translations",
                to="shops.category",
            ),
        ),
        migrations.AddField(
            model_name="producttranslation",
            name="master",
            field=parler.fields.TranslationsForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="translations",
                to="shops.product",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="categorytranslation",
            unique_together={("language_code", "master")},
        ),
        migrations.AlterUniqueTogether(
            name="producttranslation",
            unique_together={("language_code", "master")},
        ),
    ]
