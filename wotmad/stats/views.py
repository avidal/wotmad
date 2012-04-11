from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, View

from annoying.decorators import JsonResponse

from .models import Stat, CLASS_CHOICES, FACTION_CHOICES, SEX_CHOICES


class StatList(ListView):
    model = Stat

    def get_queryset(self):
        return Stat.objects.order_by('-date_submitted')


class ContributeStat(TemplateView):
    template_name = 'stats/contribute.html'


class SubmitStat(View):

    def get(self, *args, **kwargs):
        request = self.request
        print request.GET

        def make_response(data, code=200):
            resp = JsonResponse(data)
            resp.status_code = code
            return resp

        def make_error(msg):
            return make_response(dict(error=msg), 400)

        # First, make sure all of these fields are actually available
        required = ['apikey', 'sex', 'faction', 'class', 'homeland',
                    'hitpoints', 'moves', 'strength', 'intel', 'wil', 'dex',
                    'con']
        for field in required:
            if not request.GET.get(field, None):
                return make_error("Missing argument {0}".format(field))

        # Validate the incoming data
        sex = request.GET['sex']
        if sex not in dict(SEX_CHOICES).keys():
            return make_error("Unrecognized sex {0}".format(sex))

        klass = request.GET['class']
        if klass not in dict(CLASS_CHOICES).keys():
            return make_error("Unrecognized class {0}".format(klass))

        faction = request.GET['faction']
        if faction not in dict(FACTION_CHOICES).keys():
            return make_error("Unrecognized faction {0}".format(faction))

        # If the klass is C the faction must be H
        if klass == 'C' and faction != 'H':
            return make_error("Invalid class for this faction.")

        # If the klass is C spellpoints must be submitted
        if klass == 'C' and not request.GET.get('spellpoints', None):
            return make_error("Channelers must provide spell points.")

        # All integer fields must be 0 or greater
        intfields = ['hitpoints', 'moves', 'spellpoints', 'strength', 'intel',
                     'wil', 'dex', 'con']
        for field in intfields:
            v = request.GET.get(field, 0)
            try:
                v = int(v)
            except ValueError:
                msg = "{0} must be an integer 0 or greater.".format(field)
                return make_error(msg)

        # TODO: Perform better validations on the submitted data
        # eg; min/max for stats

        # See if they submitted with a valid API key
        apikey = request.GET.get('apikey', None)

        # Try to find a user with this API key
        try:
            user = User.objects.get(apikey__key=apikey, is_active=True)
        except User.DoesNotExist:
            return make_error("Invalid API key.")

        # At this point, we have valid data and a valid user, so just
        # create the stat and let them know it was done!
        try:
            Stat.objects.create(submitter=user,
                                name=request.GET.get('name', ''),
                                sex=sex,
                                faction=faction,
                                klass=klass,
                                homeland=request.GET['homeland'],
                                hitpoints=int(request.GET['hitpoints']),
                                moves=int(request.GET['moves']),
                                spellpoints=int(request.GET.get('spellpoints', 0)),
                                strength=int(request.GET['strength']),
                                intel=int(request.GET['intel']),
                                wil=int(request.GET['wil']),
                                dex=int(request.GET['dex']),
                                con=int(request.GET['con']),
                               )
        except:
            return make_error("Something went wrong accepting your stat.")

        return make_response(dict(success="Ok"))
