from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Base_App.views import *  # Imports all views, including get_product_detail if defined

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView, name='home'),
    path('about/', AboutView, name='about'),
    path('menu/', MenuView, name='menu'),
    path('book/', BookTableView, name='book'),
    path('review/', ReviewView, name='review'),
    path('get-product/<int:pk>/', get_product_detail, name='get_product_detail'),
    path('process-checkout/', process_checkout, name='process_checkout'),
    path('test-checkout/', test_checkout_url, name='test_checkout'),
    path('submit_review/', submit_review, name='submit_review'),

] 
# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)