from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "account"
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('cart/', views.user_cart, name='user_cart'),
    path('logout/', views.user_logout, name='user_logout'),
    path('search/' , views.index , name="search"),
    path('update_item/' , views.update_item , name="update_item"),
    path('category/' , views.category_view , name="category_view"),
    path('tag/<slug:tag_slug>' , views.index , name="tag_view"),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
