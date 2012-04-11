from django.views.generic import ListView

from .models import Stat


class StatList(ListView):
    model = Stat

    def get_queryset(self):
        return Stat.objects.order_by('-date_submitted')
