from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from supportAPI.views import ProjectViewset, IssueViewset, CommentViewset


# Ici nous créons notre routeur
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register('project', ProjectViewset, basename='project')
router.register('issue', IssueViewset, basename='issue')
router.register('comment', CommentViewset, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # Il faut bien penser à ajouter les urls du router dans la liste des urls disponibles.
    path('api/', include(router.urls))
    ]