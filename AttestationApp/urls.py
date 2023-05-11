"""
URL configuration for AttestationApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app.views import *
from cart.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index_template, name = 'index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', user_reg, name='reg'),
    path('logout/', user_logout, name = 'logout'),
    path('contact/', contact_email, name='contact'),

    path('cart/', cart_detail, name='cart'),
    path('cart/add/<int:pk>/', cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', cart_remove, name='cart_remove'),
    path('cart/remove/all/', cart_remove_all, {'products': 'all'}, name='cart_remove_all'),
    path('cart/order/', order, name = 'order'),

    path('favourite/', favourite_list, name='favourite_list'),
    path('favourite/add/<int:pk>/', favourite_add, name='favourite_add'),

    path('api/list', tour_api_list, name='tour_api_list'),
    path('api/detail/<int:pk>/', tour_api_detail, name = 'tour_api_detail'),

    path('tourlist/', TourList.as_view(), name = 'tour_list'),
    path('touradd/', TourCreate.as_view(), name = 'tour_add'),
    path('tourdetail/<int:pk>', TourDetail.as_view(), name = 'tour_detail'),
    path('edit/<int:pk>/', TourUpdate.as_view(), name = 'tour_update'),
    path('tourdetail/<int:pk>/delete', TourDeleteView.as_view(), name = 'tour_delete'),

    path('fail/', csrf_failure, name = 'csrf_failure'),
    # path('tourdetail/<int:pk>/addtocart', add_to_cart, name = 'add_to_cart'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
