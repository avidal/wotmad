from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from braces.views import LoginRequiredMixin

from .forms import CreateScriptForm, NewVersionScriptForm, UpdateScriptForm
from .models import Script, CLIENT_CHOICES


class SubmitScript(LoginRequiredMixin, CreateView):
    model = Script
    form_class = CreateScriptForm

    def form_valid(self, form):
        request = self.request

        script = form.save(commit=False)
        script.slug = slugify(script.title)
        script.submitter = request.user

        script.save()

        # Create a new ScriptSource entry for this script using
        # the latest source
        script.add_version(form.cleaned_data.get('source'))

        messages.success(request, "Score!")
        return redirect(script)


class UpdateScript(LoginRequiredMixin, UpdateView):
    model = Script
    form_class = UpdateScriptForm

    def get_object(self):
        obj = super(UpdateScript, self).get_object()

        # Ensure request.user owns the script
        if obj.submitter != self.request.user:
            raise Http404()

        return obj

    def form_valid(self, form):
        script = form.save(commit=False)

        # We also want to update the script's slug based on the new title
        script.slug = slugify(script.title)
        script.save()

        messages.success(self.request, "Script updated successfully.")
        return redirect(self.get_success_url())


class SubmitScriptVersion(LoginRequiredMixin, UpdateView):
    model = Script
    form_class = NewVersionScriptForm

    def get_object(self):
        obj = super(SubmitScriptVersion, self).get_object()

        # Ensure request.user owns the script
        if obj.submitter != self.request.user:
            raise Http404()

        return obj

    def get_form_kwargs(self):
        # Normally, the UpdateView mixin would pull out the object
        # instance and stick it into the form kwargs. Since this isn't
        # really a model form, we'll remove the instance argument
        kwargs = super(SubmitScriptVersion, self).get_form_kwargs()
        if 'instance' in kwargs:
            del kwargs['instance']

        return kwargs

    def form_valid(self, form):
        # If the form is valid, then pull out the script object
        # and add a new version
        source = form.cleaned_data.get('source')

        # Add a new version to the script we're updating
        script = self.get_object()
        script.add_version(source)

        # Flash a message and take them back to the detail view
        msg = "Version {0} added. Thanks!"
        messages.success(self.request,
                         msg.format(script.latest_version.version))
        return redirect(script)


class ScriptDetail(DetailView):
    model = Script

    def get(self, *args, **kwargs):
        script = self.get_object()

        # If the slug in the URL doesn't match the script slug,
        # then redirect
        if script.slug != kwargs.get('slug'):
            return redirect(script, permanent=True)

        return super(ScriptDetail, self).get(*args, **kwargs)


class ScriptList(ListView):
    model = Script

    def get_queryset(self):
        qs = Script.objects.order_by('-last_modified')

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
