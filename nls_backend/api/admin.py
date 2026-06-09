from django.contrib import admin

from .models import About,AboutImage,PrivacyPolicy
from .models import Sliders,Contact
from .models import Services,Products
from .models import Faqs,Clients
from .models import BoardMembers,ManComs,Teams
from .models import Teams,Offers,Category, DownloadFile, Research
from .models import Events,Features,IPO_Offer,MarketNews,Branch

admin.site.register(Sliders)
admin.site.register(Faqs)


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['id' ,'title','description']

@admin.register(AboutImage)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['id' ,'about','image']

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['id' ,'title','description','image']

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id' ,'title','description']

@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['id' ,'title','description','image']

@admin.register(MarketNews)
class MarketNewsAdmin(admin.ModelAdmin):
    list_display = ['id' ,'market','trading_code','title','news','publish_date']

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ['id' ,'title','description']

@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','image']

@admin.register(BoardMembers)
class BoardMembersAdmin(admin.ModelAdmin):
    list_display = ['id','name','designation','biodata','image','order']

@admin.register(ManComs)
class ManComsAdmin(admin.ModelAdmin):
    list_display = ['id','name','designation','biodata','image','order']

@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ['id','name','designation','image','order']

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ['id','name','image']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','phone','project','subject','message']

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['id','title','description']

@admin.register(IPO_Offer)
class IPO_OfferAdmin(admin.ModelAdmin):
    list_display = ['id','company','href']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id','category','office','address','contact','email','lat','lng']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

@admin.register(DownloadFile)
class DownloadFileAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "uploaded_at", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title",)

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "file", "published_at")
    list_filter = ("category", "published_at")
    search_fields = ("title",)