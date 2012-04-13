from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, View

from annoying.decorators import JsonResponse

from .forms import SubmitStatForm
from .models import Stat


class StatList(ListView):
    model = Stat

    def get_queryset(self):
        return Stat.objects.order_by('-date_submitted')


class ContributeStat(TemplateView):
    template_name = 'stats/contribute.html'


class SubmitStat(View):

    def get(self, *args, **kwargs):
        request = self.request
        ashtml = 'ashtml' in request.GET

        def make_response(data, code=200):
            if ashtml:
                out = []
                if 'error' in data:
                    out.append("<h1>Error receiving stat</h1>")
                    out.append("<p>{0}</p>".format(data['error']))
                if 'errors' in data:
                    out.append("<p>The following errors were encountered while "
                               "validating your submission:</p>")
                    for field, errors in data['errors'].iteritems():
                        l = "<li>{0}<ul><li>{1}</li></ul></li>"
                        out.append(l.format(field, "</li><li>".join(errors)))
                if 'success' in data:
                    out.append("<h1>Success! Your stat was accepted.</h1>")

                out.append("<br/><br/>")
                out.append("You may close this window at any time.")

                resp = HttpResponse("\n".join(out))
            else:
                resp = JsonResponse(data)

            resp.status_code = code
            return resp

        def make_error(msg, errors=None):
            errors = errors or {}
            return make_response(dict(error=msg, errors=errors), 400)

        formdata = request.GET.copy()
        formdata['klass'] = formdata.get('class', None)

        # Allow the user to submit full versions of the sex, faction, and class
        fulltext_maps = {
            'sex': {
                'male': 'M',
                'female': 'F',
            },
            'faction': {
                'human': 'H',
                'seanchan': 'S',
                'trolloc': 'D',
            },
            'klass': {
                'hunter': 'H',
                'rogue': 'R',
                'warrior': 'W',
                'channeler': 'C',
            },
        }

        for k, map_ in fulltext_maps.iteritems():
            v = formdata.get(k, None)
            if v and v in map_:
                formdata[k] = map_[v]

        # Create the form instance
        form = SubmitStatForm(formdata)

        # And see if it's valid
        if not form.is_valid():
            # Rename any errors for `klass` to `class`
            if form.errors.get('klass'):
                form.errors['class'] = form.errors['klass']
                del form.errors['klass']

            return make_error("Submitted data is invalid.", form.errors)

        # Pull the user out of the form
        user = form.user
        clean = form.cleaned_data

        # At this point, we have valid data and a valid user, so just
        # create the stat and let them know it was done!
        try:
            Stat.objects.create(submitter=user,
                                name=clean.get('name'),
                                sex=clean.get('sex'),
                                faction=clean.get('faction'),
                                klass=clean.get('klass'),
                                homeland=clean.get('homeland'),
                                strength=clean.get('strength'),
                                intel=clean.get('intel'),
                                wil=clean.get('wil'),
                                dex=clean.get('dex'),
                                con=clean.get('con'),
                               )
        except:
            return make_error("Something went wrong accepting your stat.")

        return make_response(dict(success="Ok"))
