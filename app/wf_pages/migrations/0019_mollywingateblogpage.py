# Generated by Django 4.2.1 on 2023-05-18 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wf_pages", "0018_rename_mollywingateblogindex_mollywingateblogindexpage"),
    ]

    operations = [
        migrations.CreateModel(
            name="MollyWingateBlogPage",
            fields=[
                (
                    "wfpage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wf_pages.wfpage",
                    ),
                ),
                ("publication_date", models.DateField(verbose_name="Publication date")),
            ],
            options={
                "verbose_name": "Molly Wingate Blog Post",
                "verbose_name_plural": "Molly Wingate Blog Posts",
            },
            bases=("wf_pages.wfpage",),
        ),
    ]
