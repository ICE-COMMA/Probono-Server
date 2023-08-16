from django.db import models

# DB
from bson.objectid import ObjectId
from bson.json_util import loads, dumps

# User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# 이거 완전 쓸모 없어 형석아 지우자
class CustomUserManager(BaseUserManager):

    def create_user(self, user_id, name, password, sex, birth, disability, custom):

        if not user_id:
            raise ValueError('아이디는 필수입니다.')
        if not name:
            raise ValueError('이름은 필수입니다.')
        if not password:
            raise ValueError('비밀번호는 필수입니다.')
        if sex == 0:
            raise ValueError('성별은 필수입니다.')
        if birth == 0:
            raise ValueError('생년월일은 필수입니다.')
        if disability == 0:
            raise ValueError('장애여부는 필수입니다.')

        user = self.model(user_id = user_id, sex = sex, birth = birth, disability = disability, custom = custom)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 보류
    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser는 is_staff=True여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser는 is_superuser=True여야 합니다.')

        return self.create_user(user_id, password, **extra_fields)

class CustomUser(AbstractBaseUser):

    # user_id
    user_id = models.CharField(max_length=100, unique=True)
    # user name
    name = models.CharField(max_length=100)
    # sex
    sex = models.CharField(max_length=1)
    # birth
    birth = models.DateField()
    # disability
    disability = models.CharField(max_length=10)
    # custom
    custom = models.CharField(max_length=10)

    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'

    # 보류
    REQUIRED_FIELDS = ['user_id']

    # 보류
    def __str__(self):
        return self.user_id
    
