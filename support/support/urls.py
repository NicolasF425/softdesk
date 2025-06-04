from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from supportAPI.views import ContributorViewSet, ProjectViewSet, IssueViewSet, CommentViewSet
from supportAPI.views import ProjectIssueViewSet, IssueCommentViewSet
from user.views import UserViewset


# Création du routeur
router = routers.SimpleRouter()
# Déclaration des url basée sur le mot clé de la classe et de la view
# afin que l’url générée soit celle que nous souhaitons ‘/api/xxxxx/’
router.register('user', UserViewset, basename='user')
router.register('contributor', ContributorViewSet, basename='contributor')
router.register('project', ProjectViewSet, basename='project')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/project/<int:project_pk>/issue/',
         ProjectIssueViewSet.as_view({'get': 'list'}),
         name='project-issues'),
    path('api/issue/<int:issue_pk>/comment/',
         IssueCommentViewSet.as_view({'get': 'list'}),
         name='issue-comments'),
    # urls du router
    path('api/', include(router.urls))
    ]
