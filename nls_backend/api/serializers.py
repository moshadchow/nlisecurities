from rest_framework import serializers

from .models import About,AboutImage,Sliders,Services,Products,Events,\
    Features,Offers,BoardMembers,Clients,Faqs,Contact,PrivacyPolicy,\
    ManComs,Teams,IPO_Offer,MarketNews,Branch,Category,DownloadFile,Research

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['title','description']

class AboutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutImage
        fields = ['about','image']

class SlidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sliders
        fields = ['title','description','layout','animation','image']

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id','title','description','image']

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id','title','description']

class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields=['id','title','description']

class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = ['id','title','description','image']

class BoardMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMembers
        fields = ['id','name','designation','biodata','image']

class ManComsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManComs
        fields = ['id','name','designation','biodata','image']

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['id','name','designation','image']

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id','title','description','image','publish_date']

class MarketNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketNews
        fields = ['id','market','trading_code','title','news','publish_date']

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['id','name','image']

class FaqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = ['id','question','answer']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id','name','email','phone','project','subject','message']

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['title','description']

class IPO_OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPO_Offer
        fields = ['id','company','href']

    def get_change_percent(self, obj):
        try:
            return round((obj.change_val / obj.ycp) * 100, 2)
        except (ZeroDivisionError, TypeError):
            return None
        
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id','category','office','address','email','contact','lat','lng']

class DownloadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadFile
        fields = [
            "id",
            "title",
            "file",
            "description",
            "uploaded_at",
            "is_active",
        ]

class CategorySerializer(serializers.ModelSerializer):
    # Nested files
    files = DownloadFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "files",
        ]

class ResearchFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = [
            "id",
            "title",
            "file",
            "description",
            "published_at",
        ]

class ResearchGroupedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    files = ResearchFileSerializer(many=True)
