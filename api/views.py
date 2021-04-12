from rest_framework import viewsets, generics
# JWTトークンがなくても大丈夫なページの箇所につけていく
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment, Cart, User
import logging

class CreateUserView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    # perform_createメソッドをオーバーライド
    # read_onlyにしたのでそのためにオーバーライドする必要がある
    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)

class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    # ログインしているユーザだけを返す
    # userProfileに一致しているユーザだけを返す
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)

class PostDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Cart.objects.all()

    serializer_class = serializers.CartSerializer

    def perform_create(self, serializer):
        # UserPost = User.objects.filter(id=self.request.data['cartUserPost'])
        # print(UserPost.get().id)
        serializer.save(cartUserPost=User.objects.get(pk=self.request.data['cartUserPost']))
        serializer.save(cartUserProfile=User.objects.get(pk=self.request.data['cartUserProfile']))

class CartListView(generics.ListAPIView):
    permission_classes = (AllowAny,)

    queryset = Cart.objects.select_related('cartUserPost').select_related('post').select_related('profile').all()
    serializer_class = serializers.CartListSerializer

    # ログインしているユーザだけを返す
    # userProfileに一致しているユーザだけを返す
    # def get_queryset(self):
    #     print(self.request.data)
    #     return self.queryset.filter(userProfile=self.request.data['cartUserProfile'])