from django.contrib import admin
from .models import ResourceCollector
from .models import ReportMaker

# Register your models here.
admin.site.register(ResourceCollector)
admin.site.register(ReportMaker)


# class FlattenJsonWidget(TextInput):
    # def render(self, name, value, attrs=None):
        # if not value is None:
            # parsed_val = ''
            # for k, v in dict(value):
                # parsed_val += " = ".join([k, v])
            # value = parsed_val
        # return super(FlattenJsonWidget, self).render(name, value, attrs)