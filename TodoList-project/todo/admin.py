from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('timecreate',)


admin.site.register(Todo, TodoAdmin)
