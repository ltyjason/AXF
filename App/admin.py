from django.contrib import admin

# Register your models here.

from App.models import Goods, UserModel


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['productlongname', 'price']
    list_filter = ['childcidname']
    search_fields = ['productlongname']
    list_per_page = 20
    ordering = ['price']
    fieldsets = (
        ('商品分类', {'fields': ('childcidname',)}),
        ('基本信息', {'fields': ('productlongname', 'price',)}),
    )


admin.site.register(Goods, GoodsAdmin)

admin.site.register(UserModel)

