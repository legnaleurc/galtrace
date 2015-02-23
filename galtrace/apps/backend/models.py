from django.contrib import admin

from galtrace.libs.core.models import Order


class OrderAdmin(admin.ModelAdmin):

    list_display = ('title', 'vendor', 'date', 'user')

admin.site.register(Order, OrderAdmin)
