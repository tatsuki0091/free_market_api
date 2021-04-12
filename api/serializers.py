from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment, Cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        # クライアント側から読まれないためにwrite_onlyにする
        # クライアント側からGETでアクセスがきてもpasswordは返さない
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # user情報を作成
        user = get_user_model().objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'img', 'postCode', 'address1', 'address2', 'phoneNumber')
        extra_kwargs = {'userProfile': {'read_only': True}}

class PostSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'userPost', 'created_on', 'img', 'liked', 'price', 'description')
        extra_kwargs = {'userPost': {'read_only': True}}

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment', 'post')
        extra_kwarg = {'userComment': {'read_only':True}}

class CartSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    class Meta:
        model = Cart
        fields = ('id', 'cartUserPost', 'cartUserProfile', 'profile', 'post', 'created_on')
        #extra_kwargs = {'cartUserProfile': {'write_only': True}, 'cartUserPost': {'write_only': True}}

class CartListSerializer(serializers.ModelSerializer):
    cartUserPost = UserSerializer()
    cartUserProfile = UserSerializer()
    post = PostSerializer()
    profile = ProfileSerializer()
    class Meta:
        model = Cart
        fields = ('id', 'cartUserPost', 'cartUserProfile', 'profile', 'post', 'created_on')
        #extra_kwargs = {'cartUserProfile': {'write_only': True}, 'cartUserPost': {'write_only': True}}