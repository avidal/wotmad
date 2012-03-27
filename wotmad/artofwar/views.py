from django.contrib import messages
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from .forms import LogForm
from .models import Log


class SubmitLog(CreateView):
    model = Log
    form_class = LogForm

    def form_valid(self, form):
        request = self.request

        log = form.save(commit=False)
        log.slug = slugify(log.title)
        log.submitter = request.user

        log.save()

        messages.success(request, "Score!")
        return redirect(log.get_absolute_url())


class LogDetail(DetailView):
    model = Log


class LogList(ListView):
    model = Log

    def get_queryset(self):
        return Log.objects.order_by('date_submitted')
