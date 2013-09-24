import csv
from datetime import datetime
import re

from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, ListView, View

from annoying.decorators import JsonResponse

from .forms import SubmitStatForm
from .models import Stat


class StatList(ListView):
    model = Stat
    mine = False

    def get_initial_queryset(self):
        qs = Stat.objects.select_related('submitter')

        if self.mine and self.request.user.is_anonymous():
            raise Http404

        if self.mine:
            return qs.filter(submitter=self.request.user)

        return qs

    def get_queryset(self):
        qs = self.get_initial_queryset()

        return qs.order_by('-date_submitted')[:100]

    def get_context_data(self, *args, **kwargs):
        ctx = super(StatList, self).get_context_data(*args, **kwargs)

        ctx.update(mine=self.mine)

        total = self.get_initial_queryset().count()

        if total > 999:
            total = "{0:0.1f}K".format(total / 1000.)

        ctx.update(total=total)

        return ctx


class ContributeStat(TemplateView):
    template_name = 'stats/contribute.html'


class ExportStats(View):

    def get(self, *args, **kwargs):
        request = self.request
        mine = 'mine' in request.GET

        response = HttpResponse(mimetype="text/csv")
        response['Content-Disposition'] = 'attachment; filename=stats.csv'

        writer = csv.writer(response)

        header = [
            ('Submitted', 'date_submitted'),
            ('Faction', 'get_faction_display'),
            ('Class', 'get_klass_display'),
            ('Sex', 'get_sex_display'),
            ('Homeland', 'get_homeland_display'),
            ('Strength', 'strength'),
            ('Intelligence', 'intel'),
            ('Willpower', 'wil'),
            ('Dexterity', 'dex'),
            ('Constitution', 'con'),
        ]

        stats = Stat.objects.order_by('-date_submitted')

        if mine:
            stats = stats.filter(submitter=request.user)
            header.insert(0, ('Name', 'name'))

        labels = [r[0] for r in header]
        fields = [r[1] for r in header]

        writer.writerow(labels)

        for stat in stats.all():
            row = []
            for f in fields:
                attr = getattr(stat, f)
                if callable(attr):
                    value = attr()
                else:
                    value = attr

                # If the value is a datetime object
                # then we need to do some quick formatting
                if isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")

                row.append(value)

            writer.writerow(row)

        return response


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
                    out.append("<p>The following errors were encountered "
                               "while validating your submission:</p>")
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

        # First, let's normalize all of the input: lowercase and strip
        # punctuation
        for k, v in formdata.iteritems():
            if not v:
                continue

            v = v.lower()

            if k == 'homeland':
                if v.endswith(' trolloc'):
                    v = v[:-8]
                if v.startswith('the '):
                    v = v[4:]

            v = re.sub(r'[^a-z]', '', v)
            formdata[k] = v

        # Next, allow some common shorthands for inputs
        fulltext_maps = {
            'sex': {
                'm': 'male',
                'f': 'female',
            },
            'faction': {
                'h': 'human',
                's': 'seanchan',
                't': 'darkside',
                'd': 'darkside',
            },
            'klass': {
                'h': 'hunter',
                'r': 'rogue',
                'w': 'warrior',
                'c': 'channeler',
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
                                con=clean.get('con'))
        except:
            return make_error("Something went wrong accepting your stat.")

        return make_response(dict(success="Ok"))
