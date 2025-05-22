from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from supportAPI.views import UserViewset, ContributorViewset, ProjectViewset, IssueViewset, CommentViewset


# Création du routeur
router = routers.SimpleRouter()
# Déclaration des url basée sur le mot clé de la classe et de la view
# afin que l’url générée soit celle que nous souhaitons ‘/api/xxxxx/’
router.register('user', UserViewset, basename='user')
router.register('contributor', ContributorViewset, basename='contributor')
router.register('project', ProjectViewset, basename='project')
router.register('issue', IssueViewset, basename='issue')
router.register('comment', CommentViewset, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # urls du router
    path('api/', include(router.urls))
    ]
