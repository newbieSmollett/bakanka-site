from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import render
from django.utils import timezone

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from core.models import BasePage


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@register_setting(icon="cog")
class SiteContactSettings(BaseSiteSetting):
    company_name = models.CharField(max_length=255, blank=True, default="ООО «Баканка»", verbose_name="Название компании")
    phone = models.CharField(max_length=100, blank=True, default="+7 (999) 999-99-99", verbose_name="Телефон")
    email = models.EmailField(blank=True, default="info@example.com", verbose_name="Email")
    address = models.CharField(max_length=255, blank=True, default="Краснодарский край, станица Нижнебаканская", verbose_name="Адрес")
    city = models.CharField(max_length=100, blank=True, default="Новороссийск", verbose_name="Город")

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
    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_NEW, "Новая"),
        (STATUS_IN_PROGRESS, "В работе"),
        (STATUS_DONE, "Обработана"),
        (STATUS_REJECTED, "Отклонена"),
    ]

    company = models.CharField(max_length=255, blank=True, verbose_name="Компания")
    name = models.CharField(max_length=255, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=100, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    source = models.CharField(max_length=100, blank=True, default="homepage", verbose_name="Источник")
    page_url = models.CharField(max_length=500, blank=True, verbose_name="URL страницы")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP-адрес")
    user_agent = models.TextField(blank=True, verbose_name="User-Agent")
    consent_personal_data = models.BooleanField(
        default=False,
        verbose_name="Согласие на обработку ПДн",
    )
    consent_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата согласия",
    )
    consent_policy_version = models.CharField(
        max_length=100,
        blank=True,
        default="policy_2026_04_27",
        verbose_name="Версия политики",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        company_part = f" / {self.company}" if self.company else ""
        return f"{self.name} — {self.phone}{company_part}"


class LeadFormMixin:
    lead_source = "site_form"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.setdefault("form_data", {
            "company": "",
            "name": "",
            "phone": "",
            "comment": "",
        })
        context.setdefault("form_errors", {})
        context.setdefault("form_success", False)
        return context

    def serve(self, request):
        if request.method != "POST":
            return super().serve(request)

        company = request.POST.get("company", "").strip()
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        comment = request.POST.get("comment", "").strip()
        personal_data_consent = request.POST.get("personal_data_consent") == "on"

        form_data = {
            "company": company,
            "name": name,
            "phone": phone,
            "comment": comment,
            "personal_data_consent": personal_data_consent,
        }

        form_errors = {}

        if not name:
            form_errors["name"] = "Укажите контактное лицо."
        elif len(name) < 2:
            form_errors["name"] = "Имя слишком короткое."

        if not phone:
            form_errors["phone"] = "Укажите телефон."
        else:
            phone_digits = "".join(ch for ch in phone if ch.isdigit())
            if len(phone_digits) < 10:
                form_errors["phone"] = "Введите корректный телефон."

        if form_errors:
            context = self.get_context(request)
            context["form_data"] = form_data
            context["form_errors"] = form_errors
            context["form_success"] = False
            return render(request, self.get_template(request), context)

        phone_digits = "".join(ch for ch in phone if ch.isdigit())

        if phone_digits.startswith("8"):
            phone_digits = "7" + phone_digits[1:]

        if not phone_digits.startswith("7"):
            phone_digits = "7" + phone_digits

        phone_digits = phone_digits[:11]
        normalized_phone = "+" + phone_digits

        if not personal_data_consent:
            form_errors["personal_data_consent"] = "Необходимо дать согласие на обработку персональных данных."
 

        lead = Lead.objects.create(
            company=company,
            name=name,
            phone=normalized_phone,
            comment=comment,
            source=self.lead_source,
            page_url=request.build_absolute_uri(),
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            consent_personal_data=personal_data_consent,
            consent_at=timezone.now() if personal_data_consent else None,
            consent_policy_version="policy_2026_04_27",
        )

        subject = f"Новая заявка с сайта: {name}"
        message = (
            f"Новая заявка с сайта.\n\n"
            f"Страница: {self.title}\n"
            f"Компания: {company or '—'}\n"
            f"Контактное лицо: {name}\n"
            f"Телефон: {normalized_phone}\n"
            f"Комментарий: {comment or '—'}\n"
            f"Источник: {self.lead_source}\n"
            f"URL страницы: {request.build_absolute_uri()}\n"
            f"IP: {get_client_ip(request) or '—'}\n"
            f"User-Agent: {request.META.get('HTTP_USER_AGENT', '') or '—'}\n"
            f"ID заявки: {lead.id}\n"
            f"Согласие на обработку ПДн: {'да' if personal_data_consent else 'нет'}\n"
            f"Версия политики: policy_2026_04_27\n"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.LEAD_NOTIFICATION_EMAIL],
                fail_silently=False,
            )
        except Exception:
            pass

        context = self.get_context(request)
        context["form_success"] = True
        context["form_data"] = {
            "company": "",
            "name": "",
            "phone": "",
            "comment": "",
        }
        context["form_errors"] = {}

        return render(request, self.get_template(request), context)


class HomePage(LeadFormMixin, BasePage):
    lead_source = "homepage"
    max_count = 1

    hero_badge = models.CharField(max_length=255, blank=True, default="B2B · Новороссийск · Нижнебаканская", verbose_name="Hero badge")
    hero_title = models.CharField(max_length=255, default="Вывоз и утилизация отходов для бизнеса", verbose_name="Hero title")
    hero_description = models.TextField(blank=True, verbose_name="Hero description")

    hero_primary_button_text = models.CharField(max_length=100, blank=True, default="Получить расчет", verbose_name="Текст основной кнопки")
    hero_primary_button_link = models.CharField(max_length=255, blank=True, default="#request", verbose_name="Ссылка основной кнопки")
    hero_secondary_button_text = models.CharField(max_length=100, blank=True, default="Наши услуги", verbose_name="Текст второй кнопки")
    hero_secondary_button_link = models.CharField(max_length=255, blank=True, default="#services", verbose_name="Ссылка второй кнопки")

    feature_1_title = models.CharField(max_length=255, blank=True, default="Собственный транспорт", verbose_name="Преимущество 1 — заголовок")
    feature_1_text = models.CharField(max_length=255, blank=True, default="Оперативный вывоз по Новороссийску и близлежащим территориям", verbose_name="Преимущество 1 — текст")
    feature_2_title = models.CharField(max_length=255, blank=True, default="Работа по договору", verbose_name="Преимущество 2 — заголовок")
    feature_2_text = models.CharField(max_length=255, blank=True, default="Документальное сопровождение и понятные условия для B2B", verbose_name="Преимущество 2 — текст")
    feature_3_title = models.CharField(max_length=255, blank=True, default="Системный подход", verbose_name="Преимущество 3 — заголовок")
    feature_3_text = models.CharField(max_length=255, blank=True, default="Подбираем решение под тип отходов, объем и специфику объекта", verbose_name="Преимущество 3 — текст")

    panel_label = models.CharField(max_length=255, blank=True, default="Экологические решения", verbose_name="Подпись на правой панели")
    panel_title = models.CharField(max_length=255, blank=True, default="Надежный подрядчик для бизнеса", verbose_name="Заголовок правой панели")
    panel_item_1 = models.CharField(max_length=255, blank=True, default="Строительные отходы", verbose_name="Пункт панели 1")
    panel_item_2 = models.CharField(max_length=255, blank=True, default="Производственные отходы", verbose_name="Пункт панели 2")
    panel_item_3 = models.CharField(max_length=255, blank=True, default="Контейнерный вывоз", verbose_name="Пункт панели 3")
    panel_item_4 = models.CharField(max_length=255, blank=True, default="Сопровождение заявок и документов", verbose_name="Пункт панели 4")

    services_section_title = models.CharField(max_length=255, blank=True, default="Основные направления работы", verbose_name="Заголовок блока услуг")
    services_section_text = models.TextField(blank=True, default="Работаем со стройками, предприятиями, подрядными организациями, складскими и коммерческими объектами.", verbose_name="Описание блока услуг")

    service_1_title = models.CharField(max_length=255, blank=True, default="Вывоз строительных отходов", verbose_name="Услуга 1 — заголовок")
    service_1_text = models.TextField(blank=True, default="Вывоз отходов после строительства, ремонта, демонтажа и расчистки территории.", verbose_name="Услуга 1 — текст")
    service_2_title = models.CharField(max_length=255, blank=True, default="Вывоз производственных отходов", verbose_name="Услуга 2 — заголовок")
    service_2_text = models.TextField(blank=True, default="Решения для производств, цехов, складов и промышленных площадок.", verbose_name="Услуга 2 — текст")
    service_3_title = models.CharField(max_length=255, blank=True, default="Контейнеры и логистика", verbose_name="Услуга 3 — заголовок")
    service_3_text = models.TextField(blank=True, default="Подбор техники, графика вывоза и схемы обслуживания объекта.", verbose_name="Услуга 3 — текст")
    service_4_title = models.CharField(max_length=255, blank=True, default="Документальное сопровождение", verbose_name="Услуга 4 — заголовок")
    service_4_text = models.TextField(blank=True, default="Договоры, заявки, акты и понятный процесс взаимодействия с клиентом.", verbose_name="Услуга 4 — текст")

    about_title = models.CharField(max_length=255, blank=True, default="Не просто вывозим, а выстраиваем сервис", verbose_name="Заголовок блока о компании")
    about_text = models.TextField(blank=True, default="Для B2B-клиента важен не только сам вывоз отходов, но и управляемый процесс: соблюдение графика, наличие транспорта, понятная коммуникация и документы.", verbose_name="Текст блока о компании")

    stat_1_title = models.CharField(max_length=255, blank=True, default="B2B", verbose_name="Статистика 1 — заголовок")
    stat_1_text = models.CharField(max_length=255, blank=True, default="работаем с юридическими лицами", verbose_name="Статистика 1 — текст")
    stat_2_title = models.CharField(max_length=255, blank=True, default="Новороссийск", verbose_name="Статистика 2 — заголовок")
    stat_2_text = models.CharField(max_length=255, blank=True, default="и станица Нижнебаканская", verbose_name="Статистика 2 — текст")
    stat_3_title = models.CharField(max_length=255, blank=True, default="Полный цикл", verbose_name="Статистика 3 — заголовок")
    stat_3_text = models.CharField(max_length=255, blank=True, default="от заявки до сопровождения", verbose_name="Статистика 3 — текст")

    request_title = models.CharField(max_length=255, blank=True, default="Оставьте запрос на расчет", verbose_name="Заголовок блока заявки")
    request_text = models.TextField(blank=True, default="Подготовим предложение под тип отходов, объем работ, адрес объекта и формат взаимодействия.", verbose_name="Текст блока заявки")

    content_panels = BasePage.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_badge"),
            FieldPanel("hero_title"),
            FieldPanel("hero_description"),
            FieldPanel("hero_primary_button_text"),
            FieldPanel("hero_primary_button_link"),
            FieldPanel("hero_secondary_button_text"),
            FieldPanel("hero_secondary_button_link"),
        ], heading="Первый экран"),
        MultiFieldPanel([
            FieldPanel("feature_1_title"),
            FieldPanel("feature_1_text"),
            FieldPanel("feature_2_title"),
            FieldPanel("feature_2_text"),
            FieldPanel("feature_3_title"),
            FieldPanel("feature_3_text"),
        ], heading="Преимущества"),
        MultiFieldPanel([
            FieldPanel("panel_label"),
            FieldPanel("panel_title"),
            FieldPanel("panel_item_1"),
            FieldPanel("panel_item_2"),
            FieldPanel("panel_item_3"),
            FieldPanel("panel_item_4"),
        ], heading="Правая панель hero"),
        MultiFieldPanel([
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
        ], heading="Блок услуг"),
        MultiFieldPanel([
            FieldPanel("about_title"),
            FieldPanel("about_text"),
            FieldPanel("stat_1_title"),
            FieldPanel("stat_1_text"),
            FieldPanel("stat_2_title"),
            FieldPanel("stat_2_text"),
            FieldPanel("stat_3_title"),
            FieldPanel("stat_3_text"),
        ], heading="Блок о компании"),
        MultiFieldPanel([
            FieldPanel("request_title"),
            FieldPanel("request_text"),
        ], heading="Блок заявки"),
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        try:
            from services.models import ServicePage

            context["service_pages"] = (
                ServicePage.objects
                .live()
                .public()
                .child_of(self)
                .order_by("path")
            )
        except Exception:
            context["service_pages"] = []

        return context

    class Meta:
        verbose_name = "Главная страница"