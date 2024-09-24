from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.forms import (AdminPasswordChangeForm, UserChangeForm,
                          UserCreationForm)

from .models import Order

admin.site.unregister(User)

@register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form= UserChangeForm
    add_form= UserCreationForm
    change_password_form= AdminPasswordChangeForm


class OrderAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display=['id', 'user', 'status', 'created_at', 'updated_at']
    actions= ['order_delivered_action', 'order_shipped_action']
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_filter= (
        'status',
        ('created_at', RangeDateFilter)
    )
    list_filter_submit= True

    @admin.action(description='Mark selected orders as delivered')
    def order_delivered_action(self, request, queryset):
        orders_to_deliver= queryset.exclude(status= Order.StatusChoice.DELIVERED)
        orders_to_deliver.update(status= Order.StatusChoice.DELIVERED)
        orders= list(orders_to_deliver)
        for order in orders:
            user= order.user
            user.email_user(
                'Your order has been delivered',
                f'Dear {user.username}\n\n Your order has been delivered',
                'admin@example.com',
                fail_silently= False
            )
        self.message_user(
            request,
            'Selected orders has been marked as delivered and users has been notified'
        )
    @admin.action(description='Mark selected orders as shipped')
    def order_shipped_action(self, request, queryset):
        orders_to_ship= queryset.exclude(status= Order.StatusChoice.SHIPPED)
        orders_to_ship.update(status= Order.StatusChoice.SHIPPED)
        orders= list(orders_to_ship)
        for order in orders:
            user= order.user
            user.email_user(
                'Your order has been delivered',
                f'Dear {user.username}\n\n Your order has been delivered',
                'admin@example.com',
                fail_silently= False
            )
        self.message_user(
            request,
            'Selected orders has been marked as delivered and users has been notified'
        )

admin.site.register(Order, OrderAdmin)