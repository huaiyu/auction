from django.contrib import admin

# Register your models here.

from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "address", "wallet")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category",)

class GoodsAdmin(admin.ModelAdmin):
    list_display = ("goods_id", "status", "deal_price")

class SellCaseAdmin(admin.ModelAdmin):
    list_display = ("sell_case_id", "online_price","description",
                    "category", "seller")

class BuyCaseAdmin(admin.ModelAdmin):
    list_display = ("buy_case_id", "online_price", "offline_price", "buyer", "description")

class DealAdmin(admin.ModelAdmin):
    list_display = ("deal_id", "deal_time", "deal_price")

class ShowAdmin(admin.ModelAdmin):
    list_display = ("show_id", "show_name", "position", "price_choices", "damai_url")

admin.site.register(Action_User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(SellCase, SellCaseAdmin)
admin.site.register(BuyCase, BuyCaseAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(Show, ShowAdmin)