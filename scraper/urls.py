from django.urls import path
from .views import earning_page
from django.conf import settings
from django.conf.urls.static import static
from .views import secFillings_report

urlpatterns = [
    path('earning/', earning_page, name='earning_page'),
    path('secFillings/', secFillings_report, name='secFillings')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)