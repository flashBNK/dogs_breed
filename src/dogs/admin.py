from django.contrib import admin

from .models import Dog, Breed

admin.site.register(Dog)
admin.site.register(Breed)