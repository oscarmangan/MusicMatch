from django.contrib import admin
from musicapp import models

# Register your models here.
admin.site.register(models.Profile, admin.ModelAdmin)
admin.site.register(models.Instrument, admin.ModelAdmin)
admin.site.register(models.Genre, admin.ModelAdmin)
admin.site.register(models.UserInstrument, admin.ModelAdmin)
admin.site.register(models.UserGenre, admin.ModelAdmin)
