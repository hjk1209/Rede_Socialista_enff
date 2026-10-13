from django.contrib import admin

from .models import InfraCalendarEvent, InfraRequest, InfraRequestUpdate, TiInventoryItem, TiNetworkNode


class InfraRequestUpdateInline(admin.TabularInline):
    model = InfraRequestUpdate
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(InfraRequest)
class InfraRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'sector', 'status', 'priority', 'requester', 'assigned_to', 'scheduled_for', 'updated_at')
    list_filter = ('sector', 'status', 'priority', 'created_at', 'scheduled_for')
    search_fields = ('title', 'location', 'asset_identifier', 'requester__display_name', 'requester__username')
    inlines = [InfraRequestUpdateInline]


@admin.register(InfraCalendarEvent)
class InfraCalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'sector', 'start_at', 'responsible', 'status')
    list_filter = ('sector', 'status', 'start_at')
    search_fields = ('title', 'location', 'responsible__display_name')


@admin.register(TiInventoryItem)
class TiInventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'asset_code', 'location', 'assigned_to', 'status', 'updated_at')
    list_filter = ('kind', 'status', 'location')
    search_fields = ('name', 'asset_code', 'location', 'ip_address', 'mac_address', 'assigned_to__display_name')


@admin.register(TiNetworkNode)
class TiNetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'location', 'ip_address', 'ssid', 'status', 'updated_at')
    list_filter = ('kind', 'status', 'location')
    search_fields = ('name', 'location', 'ip_address', 'ssid', 'vlan', 'upstream')
