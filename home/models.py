from core.models import BasePage


class HomePage(BasePage):
    template = "home/home_page.html"

    subpage_types = []

    parent_page_types = ["wagtailcore.Page"]