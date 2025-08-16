import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    생성일(created_at)과 수정일(updated_at)을 자동으로 관리하는
    추상 베이스 모델입니다.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="생성 시각"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="수정 시각"
    )

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """
    커스텀 UserManager:
    - kakao_id와 nickname을 필수로 받고, UUID는 모델 디폴트를 통해 자동 생성됩니다.
    - 비밀번호가 없으면 unusable_password로 처리합니다.
    """
    use_in_migrations = True

    def _create_user(self, kakao_id, nickname, password=None, **extra_fields):
        if not kakao_id:
            raise ValueError('카카오 ID는 필수 항목입니다.')
        user = self.model(
            kakao_id=kakao_id,
            nickname=nickname,
            **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, kakao_id, nickname, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(kakao_id, nickname, **extra_fields)

    def create_superuser(self, kakao_id, nickname, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields['is_staff'] or not extra_fields['is_superuser']:
            raise ValueError('슈퍼유저는 is_staff=True, is_superuser=True 여야 합니다.')
        return self._create_user(kakao_id, nickname, password, **extra_fields)


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    """
    개선된 User 모델:
    - user_id: UUID primary key
    - kakao_id: 카카오 고유 사용자 번호 (unique)
    - nickname, profile_image, last_login, is_staff, is_active
    - created_at/updated_at은 TimeStampedModel에서 상속
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="내부 사용자 식별자 (UUID4)"
    )
    kakao_id = models.BigIntegerField(
        unique=True,
        help_text="카카오 사용자 고유 ID"
    )
    nickname = models.CharField(
        max_length=150,
        help_text="사용자 닉네임"
    )
    profile_image = models.URLField(
        blank=True, null=True,
        help_text="프로필 이미지 URL"
    )
    # AbstractBaseUser가 last_login을 제공.
    is_staff = models.BooleanField(
        default=False,
        help_text="관리자 페이지 접근 권한"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="활성 사용자 여부"
    )

    # 기본 PermissionMixin 필드 재정의 : related_name 충돌 방지
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('사용자가 속한 그룹 목록'),
        related_name='custom_user_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('사용자에게 직접 부여된 권한 목록'),
        related_name='custom_user_permissions',
        related_query_name='user'
    )

    USERNAME_FIELD = 'kakao_id'
    REQUIRED_FIELDS = ['nickname']

    objects = UserManager()

    def __str__(self):
        return f"{self.nickname}({self.kakao_id})"
