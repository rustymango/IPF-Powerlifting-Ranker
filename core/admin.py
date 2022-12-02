from django.contrib import admin
from .models import Powerlifting

# Register your models here.
class PowerliftingAdmin(admin.ModelAdmin):
    list_display = ("weight", "gender", "age")

admin.site.register(Powerlifting, PowerliftingAdmin)