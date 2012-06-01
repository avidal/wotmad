from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class SearchView(TemplateView):
    template_name = "search.html"
