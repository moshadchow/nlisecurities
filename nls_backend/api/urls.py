from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('about/', views.Abouts, name="get_about"),
    path('about_image/', views.AboutImages, name="get_about_img"),
    path('about_image/<int:pk>', views.AboutImages, name="get_about_img_single"),
    path('slider/', views.Sliders_view, name="get_slider"),
    path('service/', views.Services_view, name="get_service_all"),
    path('service/<int:pk>', views.Services_view, name="get_service_single"),
    path('product/', views.Products_view, name="get_product_all"),
    path('product/<int:pk>', views.Products_view, name="get_product_single"),
    path('feature/', views.Features_view, name="get_service_all"),
    path('feature/<int:pk>', views.Features_view, name="get_service_single"),
    path('offer/', views.Offers_view, name="get_all_offers"),  # GET all offers
    path('offer/<int:pk>/', views.Offers_view, name="get_single_offer"),
    path('board_member/', views.BoardMembers_view, name="get_member_all"),
    path('board_member/<int:pk>/', views.BoardMembers_view, name="get_member_single"),
    path('mancom/', views.ManComs_view, name="get_mancom_all"),
    path('mancom/<int:pk>/', views.ManComs_view, name="get_mancom_single"),
    path('tech/', views.Teams_view, name="get_team"),
    path('event/', views.Events_view, name="get_event_all"),
    path('event/<int:pk>', views.Events_view, name="get_event_single"),
    path('market_news/', views.News_view, name="get_news_all"),
    path('market_news/<str:pk>', views.News_view, name="get_news_single"),
    path('client/', views.Clients_view, name="get_client"),
    path('faq/', views.Faqs_view, name="get_faq"),
    path('contact/', views.Contact_view, name="post_contact"),
    path('ipo/', views.IPO_view, name="ipo"),
    path('privacy-policy/', views.Policy_view, name="get_policy"),
    path('top_share_price_by/',views.Top_share_price_by,name="get_top_share_price_by"),
    path('top_share_price_by/<str:pk>',views.Top_share_price_by,name="get_top_share_price_by"),
    path('branch/<str:pk>', views.Branch_view, name="branch"),
    path('branch/', views.Branch_view, name="branch_all"),
    path("research/<str:pk>", views.research_grouped_view, name="research-grouped"),
    path('categories/', views.category_list, name="category-list"),
    path('market_info/',views.market_info,name="market_infos"),
    path('market_info/<str:pk>',views.market_info,name="market_info"),
    path('minutes_index/',views.minutes_index,name="minutes_indexes"),
    path('minutes_index/<str:pk>',views.minutes_index,name="minutes_index"),
    path('market_index/',views.market_index,name="market_indexes"),
    path('market_index/<str:pk>',views.market_index,name="market_index"),
    path('sector_wise_inst',views.sector_wise_inst,name="sector_wise_inst"),
    path('ticker_price/<str:pk>',views.ticker_price,name="ticker_price")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)