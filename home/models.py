from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    seo_title_custom = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="SEO Title"
    )
    seo_description = models.TextField(
        blank=True,
        verbose_name="SEO Description"
    )

    hero_badge = models.CharField(
        max_length=255,
        blank=True,
        default="B2B · Новороссийск · Нижнебаканская",
        verbose_name="Hero badge"
    )
    hero_title = models.CharField(
        max_length=255,
        default="Вывоз и утилизация отходов для бизнеса",
        verbose_name="Hero title"
    )
    hero_description = models.TextField(
        blank=True,
        verbose_name="Hero description"
    )

    hero_primary_button_text = models.CharField(
        max_length=100,
        blank=True,
        default="Получить расчет",
        verbose_name="Текст основной кнопки"
    )
    hero_primary_button_link = models.CharField(
        max_length=255,
        blank=True,
        default="#request",
        verbose_name="Ссылка основной кнопки"
    )
    hero_secondary_button_text = models.CharField(
        max_length=100,
        blank=True,
        default="Наши услуги",
        verbose_name="Текст второй кнопки"
    )
    hero_secondary_button_link = models.CharField(
        max_length=255,
        blank=True,
        default="#services",
        verbose_name="Ссылка второй кнопки"
    )

    feature_1_title = models.CharField(max_length=255, blank=True, default="Собственный транспорт")
    feature_1_text = models.CharField(max_length=255, blank=True, default="Оперативный вывоз по Новороссийску и близлежащим территориям")

    feature_2_title = models.CharField(max_length=255, blank=True, default="Работа по договору")
    feature_2_text = models.CharField(max_length=255, blank=True, default="Документальное сопровождение и понятные условия для B2B")

    feature_3_title = models.CharField(max_length=255, blank=True, default="Системный подход")
    feature_3_text = models.CharField(max_length=255, blank=True, default="Подбираем решение под тип отходов, объем и специфику объекта")

    panel_label = models.CharField(
        max_length=255,
        blank=True,
        default="Экологические решения",
        verbose_name="Подпись на правой панели"
    )
    panel_title = models.CharField(
        max_length=255,
        blank=True,
        default="Надежный подрядчик для бизнеса",
        verbose_name="Заголовок правой панели"
    )

    panel_item_1 = models.CharField(max_length=255, blank=True, default="Строительные отходы")
    panel_item_2 = models.CharField(max_length=255, blank=True, default="Производственные отходы")
    panel_item_3 = models.CharField(max_length=255, blank=True, default="Контейнерный вывоз")
    panel_item_4 = models.CharField(max_length=255, blank=True, default="Сопровождение заявок и документов")

    services_section_title = models.CharField(
        max_length=255,
        blank=True,
        default="Основные направления работы"
    )
    services_section_text = models.TextField(
        blank=True,
        default="Работаем со стройками, предприятиями, подрядными организациями, складскими и коммерческими объектами."
    )

    service_1_title = models.CharField(max_length=255, blank=True, default="Вывоз строительных отходов")
    service_1_text = models.TextField(blank=True, default="Вывоз отходов после строительства, ремонта, демонтажа и расчистки территории.")

    service_2_title = models.CharField(max_length=255, blank=True, default="Вывоз производственных отходов")
    service_2_text = models.TextField(blank=True, default="Решения для производств, цехов, складов и промышленных площадок.")

    service_3_title = models.CharField(max_length=255, blank=True, default="Контейнеры и логистика")
    service_3_text = models.TextField(blank=True, default="Подбор техники, графика вывоза и схемы обслуживания объекта.")

    service_4_title = models.CharField(max_length=255, blank=True, default="Документальное сопровождение")
    service_4_text = models.TextField(blank=True, default="Договоры, заявки, акты и понятный процесс взаимодействия с клиентом.")

    about_title = models.CharField(
        max_length=255,
        blank=True,
        default="Не просто вывозим, а выстраиваем сервис"
    )
    about_text = models.TextField(
        blank=True,
        default="Для B2B-клиента важен не только сам вывоз отходов, но и управляемый процесс: соблюдение графика, наличие транспорта, понятная коммуникация и документы."
    )

    stat_1_title = models.CharField(max_length=255, blank=True, default="B2B")
    stat_1_text = models.CharField(max_length=255, blank=True, default="работаем с юридическими лицами")

    stat_2_title = models.CharField(max_length=255, blank=True, default="Новороссийск")
    stat_2_text = models.CharField(max_length=255, blank=True, default="и станица Нижнебаканская")

    stat_3_title = models.CharField(max_length=255, blank=True, default="Полный цикл")
    stat_3_text = models.CharField(max_length=255, blank=True, default="от заявки до сопровождения")

    request_title = models.CharField(
        max_length=255,
        blank=True,
        default="Оставьте запрос на расчет"
    )
    request_text = models.TextField(
        blank=True,
        default="Подготовим предложение под тип отходов, объем работ, адрес объекта и формат взаимодействия."
    )

    company_name = models.CharField(
        max_length=255,
        blank=True,
        default="ООО «Баканка»",
        verbose_name="Название компании для schema.org"
    )
    company_phone = models.CharField(
        max_length=100,
        blank=True,
        default="+7 (999) 999-99-99",
        verbose_name="Телефон"
    )
    company_email = models.EmailField(
        blank=True,
        default="info@example.com",
        verbose_name="Email"
    )
    company_address = models.CharField(
        max_length=255,
        blank=True,
        default="Краснодарский край, станица Нижнебаканская",
        verbose_name="Адрес"
    )
    company_city = models.CharField(
        max_length=100,
        blank=True,
        default="Новороссийск",
        verbose_name="Город"
    )

    content_panels = Page.content_panels + [
        FieldPanel("seo_title_custom"),
        FieldPanel("seo_description"),

        FieldPanel("hero_badge"),
        FieldPanel("hero_title"),
        FieldPanel("hero_description"),
        FieldPanel("hero_primary_button_text"),
        FieldPanel("hero_primary_button_link"),
        FieldPanel("hero_secondary_button_text"),
        FieldPanel("hero_secondary_button_link"),

        FieldPanel("feature_1_title"),
        FieldPanel("feature_1_text"),
        FieldPanel("feature_2_title"),
        FieldPanel("feature_2_text"),
        FieldPanel("feature_3_title"),
        FieldPanel("feature_3_text"),

        FieldPanel("panel_label"),
        FieldPanel("panel_title"),
        FieldPanel("panel_item_1"),
        FieldPanel("panel_item_2"),
        FieldPanel("panel_item_3"),
        FieldPanel("panel_item_4"),

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

        FieldPanel("about_title"),
        FieldPanel("about_text"),
        FieldPanel("stat_1_title"),
        FieldPanel("stat_1_text"),
        FieldPanel("stat_2_title"),
        FieldPanel("stat_2_text"),
        FieldPanel("stat_3_title"),
        FieldPanel("stat_3_text"),

        FieldPanel("request_title"),
        FieldPanel("request_text"),

        FieldPanel("company_name"),
        FieldPanel("company_phone"),
        FieldPanel("company_email"),
        FieldPanel("company_address"),
        FieldPanel("company_city"),
    ]