from django.db import models
from wagtail.admin.panels import FieldPanel

from core.models import BasePage
from home.models import LeadFormMixin


class ServicePage(LeadFormMixin, BasePage):
    lead_source = "service_page"

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    hero_badge = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Бейдж в hero",
    )
    hero_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Заголовок hero",
    )
    hero_description = models.TextField(
        blank=True,
        verbose_name="Описание hero",
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение hero",
    )

    intro_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Заголовок блока описания",
    )
    intro_text = models.TextField(
        blank=True,
        verbose_name="Текст описания",
    )

    feature_1_title = models.CharField(max_length=255, blank=True, verbose_name="Преимущество 1 — заголовок")
    feature_1_text = models.TextField(blank=True, verbose_name="Преимущество 1 — текст")

    feature_2_title = models.CharField(max_length=255, blank=True, verbose_name="Преимущество 2 — заголовок")
    feature_2_text = models.TextField(blank=True, verbose_name="Преимущество 2 — текст")

    feature_3_title = models.CharField(max_length=255, blank=True, verbose_name="Преимущество 3 — заголовок")
    feature_3_text = models.TextField(blank=True, verbose_name="Преимущество 3 — текст")

    step_1_title = models.CharField(max_length=255, blank=True, verbose_name="Этап 1 — заголовок")
    step_1_text = models.TextField(blank=True, verbose_name="Этап 1 — текст")

    step_2_title = models.CharField(max_length=255, blank=True, verbose_name="Этап 2 — заголовок")
    step_2_text = models.TextField(blank=True, verbose_name="Этап 2 — текст")

    step_3_title = models.CharField(max_length=255, blank=True, verbose_name="Этап 3 — заголовок")
    step_3_text = models.TextField(blank=True, verbose_name="Этап 3 — текст")

    cta_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="CTA заголовок",
    )
    cta_text = models.TextField(
        blank=True,
        verbose_name="CTA текст",
    )
    cta_button_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Текст кнопки CTA",
    )
    cta_button_link = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Ссылка кнопки CTA",
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("hero_badge"),
        FieldPanel("hero_title"),
        FieldPanel("hero_description"),
        FieldPanel("hero_image"),

        FieldPanel("intro_title"),
        FieldPanel("intro_text"),

        FieldPanel("feature_1_title"),
        FieldPanel("feature_1_text"),
        FieldPanel("feature_2_title"),
        FieldPanel("feature_2_text"),
        FieldPanel("feature_3_title"),
        FieldPanel("feature_3_text"),

        FieldPanel("step_1_title"),
        FieldPanel("step_1_text"),
        FieldPanel("step_2_title"),
        FieldPanel("step_2_text"),
        FieldPanel("step_3_title"),
        FieldPanel("step_3_text"),

        FieldPanel("cta_title"),
        FieldPanel("cta_text"),
        FieldPanel("cta_button_text"),
        FieldPanel("cta_button_link"),
    ]

    class Meta:
        verbose_name = "Страница услуги"