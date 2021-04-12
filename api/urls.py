from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

app_name = 'user'

router = DefaultRouter()
# viewsetの登録
router.register('profile', views.ProfileViewSet)
router.register('post', views.PostViewSet)
router.register('comment', views.CommentViewSet)
router.register('cart', views.CartViewSet)

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('post/detail/<int:id>', views.PostDetailView.as_view()),
    path('cart/items', views.CartListView.as_view()),
    path('', include(router.urls)),

]