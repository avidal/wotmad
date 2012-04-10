from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from braces.views import LoginRequiredMixin

from .forms import ScriptForm
from .models import Script, CLIENT_CHOICES


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
        qs = Script.objects.order_by('-date_submitted')

        client = self.kwargs.get('client', None)
        if not client:
            return qs

        # Uppercase the client and see if its in the client list
        clients_dict = dict(CLIENT_CHOICES)
        if client.upper() not in clients_dict:
            raise Http404

        if client:
            qs = qs.filter(client=client.upper())

        return qs
