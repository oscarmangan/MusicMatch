from django.contrib import admin
from musicapp import models


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class InstrumentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class GenreAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    readonly_fields = ('id', 'lat_long')


class UserGenreAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    readonly_fields = ('user', 'genre')


# Register your models here.
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Instrument, InstrumentAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.UserInstrument, admin.ModelAdmin)
admin.site.register(models.UserGenre, admin.ModelAdmin)
admin.site.register(models.UserImage, admin.ModelAdmin)
