from django.contrib import admin
from .models import CustomUser, Vendor, Package, Booking



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name','approved')
    list_filter = ('approved',)
    search_fields = ('user__username', 'company_name')
    actions = ['approve_vendors', 'reject_vendors'] 

    def approve_vendors(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} vendor(s) approved.")
    approve_vendors.short_description = "Approve selected vendors"

    def reject_vendors(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f"{updated} vendor(s) rejected.")
    reject_vendors.short_description = "Reject selected vendors"   


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor', 'price', 'approved')
    list_filter = ('approved', 'vendor')
    search_fields = ('title', 'vendor__user__username')
    actions = ['approve_packages', 'reject_packages']

    def approve_packages(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} package(s) approved.")
    approve_packages.short_description = "Approve selected packages"

    def reject_packages(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f"{updated} package(s) rejected.")
    reject_packages.short_description = "Reject selected packages"


admin.register(Booking)
