from django.db import models


class Page(models.Model):
    """Класс для хранения страниц."""

    url = models.URLField(null=False)
    h1_count = models.PositiveIntegerField(default=0)
    h2_count = models.PositiveIntegerField(default=0)
    h3_count = models.PositiveIntegerField(default=0)
    a_links = models.JSONField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
