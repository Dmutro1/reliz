from django.urls import path
from .views import content_list, home, detail_view
from app import views

urlpatterns = [
    path('', home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('mods/', content_list, {'model_name': 'mods'}, name='mods_list'),
    path('mods/<slug:slug>/', detail_view, {'model_name': 'mods'}, name='mod_detail'),
    path('texture-packs/', content_list, {'model_name': 'texture-packs'}, name='texture_packs_list'),
    path('texture-packs/<slug:slug>/', detail_view, {'model_name': 'texture-packs'}, name='texture_pack_detail'),
    path('modpacks/', content_list, {'model_name': 'modpacks'}, name='modpacks_list'),
    path('modpacks/<slug:slug>/', detail_view, {'model_name': 'modpacks'}, name='modpack_detail'),
    path('worlds/', content_list, {'model_name': 'worlds'}, name='worlds_list'),
    path('worlds/<slug:slug>/', detail_view, {'model_name': 'worlds'}, name='world_detail'),
    path('shaders/', content_list, {'model_name': 'shaders'}, name='shaders_list'),
    path('shaders/<slug:slug>/', detail_view, {'model_name': 'shaders'}, name='shader_detail'),
    path('api/mods/', views.ModListApiView.as_view(), name='api_mods_list'),
    path('api/mods/update/<int:pk>/', views.ModDetailApiView.as_view(), name='api_mod_update'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
