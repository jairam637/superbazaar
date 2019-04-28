from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^login$', views.login1, name="login"),
    url(r'^log_out$', views.logout_view, name="log_out"),
    url('register/', views.register, name='register'),
    url('cashier1/', views.cashier1, name='cashier1'),
    url(r'^catagories$', views.get_catagories),
    url(r'^brands/(?P<catagory>[^/]*)', views.get_brands),
    url(r'^item/(?P<catagory>[^/]*)/(?P<brand>[^/]*)', views.get_item),
    url(r'^store/', views.store_data),
]
