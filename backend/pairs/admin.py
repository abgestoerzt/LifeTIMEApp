from django.contrib import admin

from .models import PaarSession


@admin.register(PaarSession)
class PaarSessionAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "status",
        "setup_kinder",
        "setup_haustiere",
        "created_at",
    ]
    list_filter = ["status", "setup_kinder", "setup_haustiere"]
    readonly_fields = ["invite_code", "created_at"]
