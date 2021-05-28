from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(News)
admin.site.register(Opinions)
admin.site.register(Film)
admin.site.register(Staff)
admin.site.register(Cinema)
