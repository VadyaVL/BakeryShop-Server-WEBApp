"""BakeryShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
import views
import settings
from django.conf.urls.static import static
from tastypie.api import Api
from api import UserApi, BarCodeApi, SendToShopApi, ProductApi, InvoiceApi, ProductToShopApi, ShopApi

v1_api = Api(api_name='v1')
v1_api.register(UserApi())
v1_api.register(BarCodeApi())
v1_api.register(SendToShopApi())
v1_api.register(ProductApi())
v1_api.register(InvoiceApi())
v1_api.register(ShopApi())
v1_api.register(ProductToShopApi())


urlpatterns = []

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^invoices/', views.invoices),
    url(r'^shops/', views.shops),
    url(r'^view_shop/(?P<pk>\d+)/$', views.view_shop),
    url(r'^products/', views.products),
    url(r'^vendors/', views.vendors),
    url(r'^edit_shop/(?P<pk>\d+)/$', views.editShop),
    url(r'^edit_product/(?P<pk>\d+)/$', views.editProduct),
    url(r'^view_send_to_shop/(?P<pk>\d+)/$', views.view_send_to_shop),
    url(r'^create_new_send/', views.create_new_send),
    url(r'^revisions/', views.revisions),
    url(r'^view_revision_info/(?P<pk>\d+)/$', views.view_revision_info),




    url(r'^home/', views.home),
    url(r'^', views.home),
]

