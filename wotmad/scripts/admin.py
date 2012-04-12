from django.contrib import admin

from .models import Script, ScriptSource


admin.site.register(Script)
admin.site.register(ScriptSource)
