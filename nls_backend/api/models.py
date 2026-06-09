from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import datetime

#from ckeditor_uploader.fields import RichTextUploadingField

class About(models.Model):
    title = models.CharField(max_length=100)
    description = CKEditor5Field('Content', config_name='extends')

    def __str__(self):
        return self.title


class AboutImage(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='about/')

    def __str__(self):
        return f"Image for {self.about.title}"
    
class Sliders(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=1500, blank=False)
    image = models.ImageField(upload_to='slider/', blank=False)
    layout = models.CharField(max_length=10, blank=True)
    animation = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title

class Services(models.Model):
    title = models.CharField(max_length=100,blank=True)
    description = CKEditor5Field('Content', config_name='extends')
    image = models.ImageField(upload_to='service/', blank=False)
    
    def __str__(self):
        return self.title
    
class Products(models.Model):
    title = models.CharField(max_length=100,blank=True)
    description = CKEditor5Field('Content', config_name='extends')
    
    def __str__(self):
        return self.title
    
class Features(models.Model):
    title = models.CharField(max_length=100,blank=True)
    description = CKEditor5Field('Content', config_name='extends')
    
    def __str__(self):
        return self.title
    
class BoardMembers(models.Model):
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    biodata = models.TextField(max_length=1500, blank=False)
    image = models.ImageField(upload_to='board/', blank=True)
    order = models.IntegerField(unique=True)  # Added unique constraint

    class Meta:
        ordering = ['order']  # Optional: to ensure consistent ordering

    def __str__(self):
        return self.name

class ManComs(models.Model):
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    biodata = models.TextField(max_length=2000, blank=False)
    image = models.ImageField(upload_to='mancom/', blank=True)
    order = models.IntegerField(unique=True)  # Added unique constraint

    class Meta:
        ordering = ['order']  # Optional: to ensure consistent ordering

    def __str__(self):
        return self.name

class Teams(models.Model):
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    image = models.ImageField(upload_to='team/', blank=True)
    order = models.IntegerField(unique=True)  # Added unique constraint

    class Meta:
        ordering = ['order']  # Optional: to ensure consistent ordering

    def __str__(self):
        return self.name
    
class Faqs (models.Model):
    question = models.CharField(max_length=200)
    answer =  models.TextField(max_length=1500, blank=False)
    
    def __str__(self):
        return self.question

class Events (models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Content', config_name='extends')
    image = models.ImageField(upload_to='event/', blank=True)
    publish_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.title

class Offers(models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Content', config_name='extends')
    image = models.ImageField(upload_to='offer/', blank = True)
    def __str__(self):
        return self.title

class Clients(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='client/', blank=True)
    def __str__(self):
        return self.name

class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=100)
    description = CKEditor5Field('Content', config_name='extends')
    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100,blank=False)
    email = models.CharField(max_length=100,blank=False)
    phone = models.CharField(max_length=20,blank=False)
    project = models.CharField(max_length=50,blank=False)
    subject = models.CharField(max_length=100,blank=False)
    message = models.TextField(max_length=1500, blank=False)

    def __str__(self):
        return self.subject

class IPO_Offer(models.Model):
    company = models.CharField(max_length=200)
    href = models.ImageField(upload_to='ipo/', blank = True)
    def __str__(self):
        return self.company  
    
class Branch(models.Model):
    BR_CHOICES = [
        ('Branch', 'Branch'),
        ('Extension', 'Extension'),
        ('Booth', 'Booth'),
    ]

    category = models.CharField(max_length=15, choices=BR_CHOICES)
    office = models.CharField(max_length=100)
    address = models.TextField(max_length=500)
    email = models.EmailField(max_length=50)
    contact = models.CharField(max_length=20)
    lat = models.CharField(max_length=50, blank=True, null=True)
    lng = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.category}-{self.office}"

class MarketNews(models.Model):
    MARKET_CHOICES = [
        ('DSE', 'DSE'),
        ('CSE', 'CSE'),
    ]

    market = models.CharField(max_length=3, choices=MARKET_CHOICES)
    trading_code = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    news = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-publish_date']

    def __str__(self):
        return f"{self.trading_code} - {self.title}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class DownloadFile(models.Model):
    MARKET_CHOICES = [
        ('DSE', 'DSE'),
        ('CSE', 'CSE'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="files")
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to="downloads/")
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title
    
class Research(models.Model):
    Category = [
        ('DailyNewsFlash', 'Daily News Flash'),
        ('DailyMarketUpdate', 'Daily Market Update'),
        ('WeeklyMarketReview', 'Weekly Market Review'),
        ('WeeklyMutualFundReport', 'Weekly Mutual Fund Report'),
        ('EquitySnapshot', 'Equity Snapshot'),
        ('IPOInsights', 'IPO Insights'),
        ('EarningUpdates', 'Earning Updates'),
        ('MacroReport', 'Macro Report'),
        ('SectorReport', 'Sector Report'),
    ]
    category = models.CharField(max_length=50, choices=Category)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="research/")
    published_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
    