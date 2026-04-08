from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class BasePage(Page):
    seo_title_custom = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="SEO title",
    )
    seo_description = models.TextField(
        blank=True,
        verbose_name="SEO description",
    )

    content_panels = Page.content_panels + []

    promote_panels = Page.promote_panels + [
        FieldPanel("seo_title_custom"),
        FieldPanel("seo_description"),
    ]

    class Meta:
        abstract = True