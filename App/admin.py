from django.contrib import admin

# Register your models here.

from App.models import Goods, UserModel


class MyAdmin(admin.AdminSite):
    site_header = 'AXF后台'
    site_title = 'AXF后台管理系统'
    site_url = '/axf/home'


site = MyAdmin()

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


site.register(Goods, GoodsAdmin)


class UserAdmin(admin.ModelAdmin):

    def active(self):
        if self.is_active:
            return '已激活'
        else:
            return '未激活'
    active.short_description = '激活状态'

    def delete(self):
        if not self.is_delete:
            return '账号在使用'
        else:
            return '账号已注销'
    delete.short_description = '使用状态'

    fieldsets = (
        ('姓名', {'fields': ('u_name', 'u_email', 'is_active', 'is_delete',)}),
    )

    list_display = ['u_name', 'u_email', active, delete]


site.register(UserModel, UserAdmin)

