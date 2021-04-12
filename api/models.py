from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ファイルのパス取得メソッド
def upload_avatar_path(instance, filename):
    # 拡張子取得
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])

def upload_post_path(instance, filename):
    # 拡張子取得
    ext = filename.split('.')[-1]
    return '/'.join(['posts', str(instance.userPost.id)+str(instance.title)+str(".")+str(ext)])


# Create your models here.
# 元からあるUserManagerクラスをオーバーライド
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('email is must')

        # インスタンス作成
        user = self.model(email=self.normalize_email(email))
        # パスワードをハッシュ化してから生成
        user.set_password(password)
        user.save(using=self._db)

        return user

    # カスタムでユーザーモデルを作成するのでスーパーユーザー用のメソッドもオーバーライドする
    def create_superuser(self, email, password):
        # インスタンス作成
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

# Userモデルをオーバーライド
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=58, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # UserManagerクラスを呼び出し
    objects = UserManager()

    # USERNAME_FIELDをオーバーライド
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Profile(models.Model):
    nickName = models.CharField(max_length=30)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="userProfile",
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)
    postCode = models.CharField(max_length=7, null=True)
    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True)
    phoneNumber = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.nickName

class Post(models.Model):
    title = models.CharField(max_length=100)
    # DBのOneToMany用にForeignKeyを使用
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="userPost",
        on_delete=models.CASCADE
    )
    price =models.IntegerField(default=0, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked", blank=True)
    description = models.CharField(max_length=400, null=True)

    def __str__(self):
        return self.title

class Cart(models.Model):
    cartUserProfile = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="cartUserProfile",
        on_delete=models.CASCADE
    )
    cartUserPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="cartUserPost", db_column='cartUserPost_id',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.user.id

# class Purchase(models.Model):
#     buyerUserProfile = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name="buyerUserProfile",
#         on_delete=models.CASCADE
#     )
#     sellerUserProfile = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name="sellerUserProfile",
#         on_delete=models.CASCADE
#     )
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     buyerUserProfile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     typeOfPayment =
#     created_on = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.CharField(max_length=100)
    # DBのOneToMany用にForeignKeyを使用
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="userComment",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

