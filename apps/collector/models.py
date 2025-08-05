from django.db import models
from users.models import User, TimeStampedModel
from contents.models import Content

class Collector(TimeStampedModel):
    """
    유저가 콘텐츠를 인증(수집)한 기록
    ERD 상의 collector 테이블에 매핑됩니다.
    """
    class VerificationMethod(models.TextChoices):
        GPS   = 'GPS',   'GPS'
        PHOTO = 'Photo', 'Photo'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collector',
        help_text="인증한 사용자"
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='collector',
        help_text="인증된 콘텐츠"
    )
    verified_by = models.CharField(
        max_length=10,
        choices=VerificationMethod.choices,
        help_text="인증 방식(GPS or Photo)"
    )
    verified_lat = models.FloatField(
        help_text="인증 위도"
    )
    verified_lng = models.FloatField(
        help_text="인증 경도"
    )
    image_url = models.URLField(
        blank=True,
        help_text="사진 인증 URL (Photo 방식일 때)"
    )
    verified_at = models.DateTimeField(
        help_text="인증 시각"
    )

    class Meta:
        db_table = 'collector'
        unique_together = ('user', 'content')
        ordering = ['-verified_at']
        indexes = [
            models.Index(fields=['verified_at']),
        ]

    def __str__(self):
        return f"{self.user.nickname} ▶ {self.content.title} @ {self.verified_at:%Y-%m-%d %H:%M}"


class Badge(TimeStampedModel):
    """
    도감 배지 정의 (변경 없음)
    """
    badge_id = models.CharField(
        max_length=50,
        primary_key=True,
        help_text="뱃지 고유 ID"
    )
    name = models.CharField(
        max_length=100,
        help_text="뱃지명"
    )
    image_url = models.URLField(
        help_text="뱃지 이미지 URL"
    )
    condition = models.JSONField(
        help_text="획득 조건(JSON 예: {'region':'서울','collector_count':5})"
    )
    description = models.TextField(
        help_text="뱃지 설명"
    )

    class Meta:
        db_table = 'badge'
        ordering = ['badge_id']

    def __str__(self):
        return self.name


class UserBadge(TimeStampedModel):
    """
    유저가 획득한 뱃지 기록 (변경 없음)
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='badges',
        help_text="뱃지를 획득한 사용자"
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name='awarded_users',
        help_text="획득한 뱃지"
    )
    awarded_at = models.DateTimeField(
        help_text="뱃지 획득 시각"
    )

    class Meta:
        db_table = 'user_badge'
        unique_together = ('user', 'badge')
        ordering = ['-awarded_at']
        indexes = [
            models.Index(fields=['awarded_at']),
        ]

    def __str__(self):
        return f"{self.user.nickname} 🏅 {self.badge.name}"
