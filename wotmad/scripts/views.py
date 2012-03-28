from django.contrib import messages
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from braces.views import LoginRequiredMixin

from .forms import ScriptForm
from .models import Script


class SubmitScript(LoginRequiredMixin, CreateView):
    model = Script
    form_class = ScriptForm

    def form_valid(self, form):
        request = self.request

        script = form.save(commit=False)
        script.slug = slugify(script.title)
        script.submitter = request.user

        script.save()

        messages.success(request, "Score!")
        return redirect(script.get_absolute_url())


class ScriptDetail(DetailView):
    model = Script


class ScriptList(ListView):
    model = Script

    def get_queryset(self):
        return Script.objects.order_by('-date_submitted')
