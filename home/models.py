from django.db import models
from django.shortcuts import render

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting(icon="cog")
class SiteContactSettings(BaseSiteSetting):
    company_name = models.CharField(
        max_length=255,
        blank=True,
        default="ООО «Баканка»",
        verbose_name="Название компании",
    )
    phone = models.CharField(
        max_length=100,
        blank=True,
        default="+7 (999) 999-99-99",
        verbose_name="Телефон",
    )
    email = models.EmailField(
        blank=True,
        default="info@example.com",
        verbose_name="Email",
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        default="Краснодарский край, станица Нижнебаканская",
        verbose_name="Адрес",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        default="Новороссийск",
        verbose_name="Город",
    )

    panels = [
        FieldPanel("company_name"),
        FieldPanel("phone"),
        FieldPanel("email"),
        FieldPanel("address"),
        FieldPanel("city"),
    ]

    class Meta:
        verbose_name = "Контакты сайта"


class Lead(models.Model):
    company = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Компания",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Контактное лицо",
    )
    phone = models.CharField(
        max_length=100,
        verbose_name="Телефон",
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
    )
    source = models.CharField(
        max_length=100,
        blank=True,
        default="homepage",
        verbose_name="Источник",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name="Обработано",
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        company_part = f" / {self.company}" if self.company else ""
        return f"{self.name} — {self.phone}{company_part}"


class HomePage(Page):
    max_count = 1

    seo_title_custom = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="SEO Title",
        help_text="Если заполнено, будет использоваться вместо стандартного title страницы.",
    )
    seo_description = models.TextField(
        blank=True,
        verbose_name="SEO Description",
        help_text="Краткое описание страницы для поисковых систем.",
    )

    hero_badge = models.CharField(
        max_length=255,
        blank=True,
        default="B2B · Новороссийск · Нижнебаканская",
        verbose_name="Hero badge",
    )
    hero_title = models.CharField(
        max_length=255,
        default="Вывоз и утилизация отходов для бизнеса",
        verbose_name="Hero title",
    )
    hero_description = models.TextField(
        blank=True,
        verbose_name="Hero description",
    )

    hero_primary_button_text = models.CharField(
        max_length=100,
        blank=True,
        default="Получить расчет",
        verbose_name="Текст основной кнопки",
    )
    hero_primary_button_link = models.CharField(
        max_length=255,
        blank=True,
        default="#request",
        verbose_name="Ссылка основной кнопки",
    )
    hero_secondary_button_text = models.CharField(
        max_length=100,
        blank=True,
        default="Наши услуги",
        verbose_name="Текст второй кнопки",
    )
    hero_secondary_button_link = models.CharField(
        max_length=255,
        blank=True,
        default="#services",
        verbose_name="Ссылка второй кнопки",
    )

    feature_1_title = models.CharField(
        max_length=255,
        blank=True,
        default="Собственный транспорт",
        verbose_name="Преимущество 1 — заголовок",
    )
    feature_1_text = models.CharField(
        max_length=255,
        blank=True,
        default="Оперативный вывоз по Новороссийску и близлежащим территориям",
        verbose_name="Преимущество 1 — текст",
    )

    feature_2_title = models.CharField(
        max_length=255,
        blank=True,
        default="Работа по договору",
        verbose_name="Преимущество 2 — заголовок",
    )
    feature_2_text = models.CharField(
        max_length=255,
        blank=True,
        default="Документальное сопровождение и понятные условия для B2B",
        verbose_name="Преимущество 2 — текст",
    )

    feature_3_title = models.CharField(
        max_length=255,
        blank=True,
        default="Системный подход",
        verbose_name="Преимущество 3 — заголовок",
    )
    feature_3_text = models.CharField(
        max_length=255,
        blank=True,
        default="Подбираем решение под тип отходов, объем и специфику объекта",
        verbose_name="Преимущество 3 — текст",
    )

    panel_label = models.CharField(
        max_length=255,
        blank=True,
        default="Экологические решения",
        verbose_name="Подпись на правой панели",
    )
    panel_title = models.CharField(
        max_length=255,
        blank=True,
        default="Надежный подрядчик для бизнеса",
        verbose_name="Заголовок правой панели",
    )
    panel_item_1 = models.CharField(
        max_length=255,
        blank=True,
        default="Строительные отходы",
        verbose_name="Пункт панели 1",
    )
    panel_item_2 = models.CharField(
        max_length=255,
        blank=True,
        default="Производственные отходы",
        verbose_name="Пункт панели 2",
    )
    panel_item_3 = models.CharField(
        max_length=255,
        blank=True,
        default="Контейнерный вывоз",
        verbose_name="Пункт панели 3",
    )
    panel_item_4 = models.CharField(
        max_length=255,
        blank=True,
        default="Сопровождение заявок и документов",
        verbose_name="Пункт панели 4",
    )

    services_section_title = models.CharField(
        max_length=255,
        blank=True,
        default="Основные направления работы",
        verbose_name="Заголовок блока услуг",
    )
    services_section_text = models.TextField(
        blank=True,
        default="Работаем со стройками, предприятиями, подрядными организациями, складскими и коммерческими объектами.",
        verbose_name="Описание блока услуг",
    )

    service_1_title = models.CharField(
        max_length=255,
        blank=True,
        default="Вывоз строительных отходов",
        verbose_name="Услуга 1 — заголовок",
    )
    service_1_text = models.TextField(
        blank=True,
        default="Вывоз отходов после строительства, ремонта, демонтажа и расчистки территории.",
        verbose_name="Услуга 1 — текст",
    )

    service_2_title = models.CharField(
        max_length=255,
        blank=True,
        default="Вывоз производственных отходов",
        verbose_name="Услуга 2 — заголовок",
    )
    service_2_text = models.TextField(
        blank=True,
        default="Решения для производств, цехов, складов и промышленных площадок.",
        verbose_name="Услуга 2 — текст",
    )

    service_3_title = models.CharField(
        max_length=255,
        blank=True,
        default="Контейнеры и логистика",
        verbose_name="Услуга 3 — заголовок",
    )
    service_3_text = models.TextField(
        blank=True,
        default="Подбор техники, графика вывоза и схемы обслуживания объекта.",
        verbose_name="Услуга 3 — текст",
    )

    service_4_title = models.CharField(
        max_length=255,
        blank=True,
        default="Документальное сопровождение",
        verbose_name="Услуга 4 — заголовок",
    )
    service_4_text = models.TextField(
        blank=True,
        default="Договоры, заявки, акты и понятный процесс взаимодействия с клиентом.",
        verbose_name="Услуга 4 — текст",
    )

    about_title = models.CharField(
        max_length=255,
        blank=True,
        default="Не просто вывозим, а выстраиваем сервис",
        verbose_name="Заголовок блока о компании",
    )
    about_text = models.TextField(
        blank=True,
        default="Для B2B-клиента важен не только сам вывоз отходов, но и управляемый процесс: соблюдение графика, наличие транспорта, понятная коммуникация и документы.",
        verbose_name="Текст блока о компании",
    )

    stat_1_title = models.CharField(
        max_length=255,
        blank=True,
        default="B2B",
        verbose_name="Статистика 1 — заголовок",
    )
    stat_1_text = models.CharField(
        max_length=255,
        blank=True,
        default="работаем с юридическими лицами",
        verbose_name="Статистика 1 — текст",
    )

    stat_2_title = models.CharField(
        max_length=255,
        blank=True,
        default="Новороссийск",
        verbose_name="Статистика 2 — заголовок",
    )
    stat_2_text = models.CharField(
        max_length=255,
        blank=True,
        default="и станица Нижнебаканская",
        verbose_name="Статистика 2 — текст",
    )

    stat_3_title = models.CharField(
        max_length=255,
        blank=True,
        default="Полный цикл",
        verbose_name="Статистика 3 — заголовок",
    )
    stat_3_text = models.CharField(
        max_length=255,
        blank=True,
        default="от заявки до сопровождения",
        verbose_name="Статистика 3 — текст",
    )

    request_title = models.CharField(
        max_length=255,
        blank=True,
        default="Оставьте запрос на расчет",
        verbose_name="Заголовок блока заявки",
    )
    request_text = models.TextField(
        blank=True,
        default="Подготовим предложение под тип отходов, объем работ, адрес объекта и формат взаимодействия.",
        verbose_name="Текст блока заявки",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("seo_title_custom"),
                FieldPanel("seo_description"),
            ],
            heading="SEO",
        ),
        MultiFieldPanel(
            [
                FieldPanel("hero_badge"),
                FieldPanel("hero_title"),
                FieldPanel("hero_description"),
                FieldPanel("hero_primary_button_text"),
                FieldPanel("hero_primary_button_link"),
                FieldPanel("hero_secondary_button_text"),
                FieldPanel("hero_secondary_button_link"),
            ],
            heading="Первый экран",
        ),
        MultiFieldPanel(
            [
                FieldPanel("feature_1_title"),
                FieldPanel("feature_1_text"),
                FieldPanel("feature_2_title"),
                FieldPanel("feature_2_text"),
                FieldPanel("feature_3_title"),
                FieldPanel("feature_3_text"),
            ],
            heading="Преимущества",
        ),
        MultiFieldPanel(
            [
                FieldPanel("panel_label"),
                FieldPanel("panel_title"),
                FieldPanel("panel_item_1"),
                FieldPanel("panel_item_2"),
                FieldPanel("panel_item_3"),
                FieldPanel("panel_item_4"),
            ],
            heading="Правая панель hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("services_section_title"),
                FieldPanel("services_section_text"),
                FieldPanel("service_1_title"),
                FieldPanel("service_1_text"),
                FieldPanel("service_2_title"),
                FieldPanel("service_2_text"),
                FieldPanel("service_3_title"),
                FieldPanel("service_3_text"),
                FieldPanel("service_4_title"),
                FieldPanel("service_4_text"),
            ],
            heading="Блок услуг",
        ),
        MultiFieldPanel(
            [
                FieldPanel("about_title"),
                FieldPanel("about_text"),
                FieldPanel("stat_1_title"),
                FieldPanel("stat_1_text"),
                FieldPanel("stat_2_title"),
                FieldPanel("stat_2_text"),
                FieldPanel("stat_3_title"),
                FieldPanel("stat_3_text"),
            ],
            heading="Блок о компании",
        ),
        MultiFieldPanel(
            [
                FieldPanel("request_title"),
                FieldPanel("request_text"),
            ],
            heading="Блок заявки",
        ),
    ]

    class Meta:
        verbose_name = "Главная страница"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["form_data"] = {
            "company": "",
            "name": "",
            "phone": "",
            "comment": "",
        }
        context["form_errors"] = {}
        context["form_success"] = False
        return context

    def serve(self, request):
        if request.method == "POST":
            company = request.POST.get("company", "").strip()
            name = request.POST.get("name", "").strip()
            phone = request.POST.get("phone", "").strip()
            comment = request.POST.get("comment", "").strip()

            form_data = {
                "company": company,
                "name": name,
                "phone": phone,
                "comment": comment,
            }
            form_errors = {}

            if not name:
                form_errors["name"] = "Укажите контактное лицо."
            if not phone:
                form_errors["phone"] = "Укажите телефон."

            if form_errors:
                context = self.get_context(request)
                context["form_data"] = form_data
                context["form_errors"] = form_errors
                context["form_success"] = False
                return render(request, "home/home_page.html", context)

            Lead.objects.create(
                company=company,
                name=name,
                phone=phone,
                comment=comment,
                source="homepage",
            )

            context = self.get_context(request)
            context["form_success"] = True
            context["form_data"] = {
                "company": "",
                "name": "",
                "phone": "",
                "comment": "",
            }
            return render(request, "home/home_page.html", context)

        return super().serve(request)