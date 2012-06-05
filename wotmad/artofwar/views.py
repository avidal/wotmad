from django.contrib import messages
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from braces.views import LoginRequiredMixin

from .forms import LogForm
from .models import Log, Category


class SubmitLog(LoginRequiredMixin, CreateView):
    model = Log
    form_class = LogForm

    def form_valid(self, form):
        request = self.request

        log = form.save(commit=False)
        log.slug = slugify(log.title)
        log.submitter = request.user

        log.save()
        form.save_m2m()

        messages.success(request, "Score!")
        return redirect(log.get_absolute_url())


class LogDetail(DetailView):
    model = Log


class LogList(ListView):
    model = Log

    def get_context_data(self, *args, **kwargs):
        ctx = super(LogList, self).get_context_data(*args, **kwargs)
        ctx.update(categories=Category.objects.all())

        return ctx

    def filter_queryset(self, qs):
        # If the category is in request.GET, then filter
        category = self.request.GET.get('category', None)
        if not category:
            return qs
        return qs.filter(categories__slug=category)

    def sort_queryset(self, qs):
        return qs.order_by('-date_submitted')

    def get_queryset(self):
        qs = Log.objects
        qs = self.filter_queryset(qs)
        qs = self.sort_queryset(qs)
        return qs
