from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import View, FormView, RedirectView
from django.shortcuts import redirect

from django_browserid.base import get_audience
from django_browserid.views import Verify as MozVerify

from .forms import AccountSetupForm


class Verify(MozVerify):

    def form_valid(self, form):
        """Handles the return post request from the browserID form and puts
        interesting variables into the class. If everything checks out, then
        we call handle_user to decide how to handle a valid user
        """
        self.assertion = form.cleaned_data['assertion']
        self.audience = get_audience(self.request)
        self.user = auth.authenticate(
                assertion=self.assertion,
                audience=self.audience)

        if self.user:
            messages.success(self.request, "Holy shit! That worked!")
            return self.login_success()

        return self.login_failure()


class Logout(View):

    def dispatch(self, request, *args, **kwargs):
        # Log the user out
        auth.logout(request)

        messages.info(request, "Thank you come again.")

        return redirect('home')


class LoginRedirect(RedirectView):

    def get_redirect_url(self, **kwargs):
        """Take the user to the homepage or to the account setup page.

        If the user is already active, they go to the homepage, otherwise
        they need to pick their username!

        """
        if self.request.user.is_active:
            return reverse('home')

        return reverse('account-setup')


class AccountSetup(FormView):
    template_name = 'account-setup.html'
    form_class = AccountSetupForm

    def get_success_url(self):
        return reverse("home")

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(AccountSetup, self).get_form_kwargs(*args,
                                                                **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def get_initial(self):
        return dict(username=self.request.user.username)

    def form_valid(self, form):
        # If the form is valid, let's update the username
        # and mark them active
        username = form.cleaned_data['username']

        self.request.user.username = username
        self.request.user.is_active = True
        self.request.user.save()

        return super(AccountSetup, self).form_valid(form)
