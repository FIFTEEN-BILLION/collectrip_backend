from django.db import models
from apps.users.models import TimeStampedModel 

# 공통 상수
LEN_CODE_SHORT = 10
LEN_CAT = 10
LEN_TITLE = 255
LEN_SMALL = 100
LEN_MED = 255

class Content(TimeStampedModel):
    """
    모든 관광 콘텐츠의 공통 정보
    """
    content_id       = models.IntegerField(
        primary_key=True,
        help_text="TourAPI 콘텐츠 ID"
    )
    content_type_id  = models.IntegerField(
        help_text="TourAPI 관광타입 ID"
    )
    addr1            = models.CharField(
        max_length=LEN_TITLE,
        help_text="주소"
    )
    addr2            = models.CharField(
        max_length=LEN_SMALL,
        blank=True,
        help_text="상세주소"
    )
    cat1             = models.CharField(
        max_length=LEN_CAT,
        help_text="대분류"
    )
    cat2             = models.CharField(
        max_length=LEN_CAT,
        help_text="중분류"
    )
    cat3             = models.CharField(
        max_length=LEN_CAT,
        help_text="소분류"
    )
    areacode         = models.CharField(
        max_length=LEN_CODE_SHORT,
        help_text="지역 코드"
    )
    sigungu_code     = models.CharField(
        max_length=LEN_CODE_SHORT,
        help_text="시군구코드"
    )
    map_x            = models.FloatField(
        help_text="GPS X좌표"
    )
    map_y            = models.FloatField(
        help_text="GPS Y좌표"
    )
    title            = models.CharField(
        max_length=255,
        help_text="제목"
    )
    dong_region_code = models.CharField(
        max_length=LEN_CODE_SHORT,
        help_text="법정동(시도) 코드"
    )
    dong_sigungu_code= models.CharField(
        max_length=LEN_CODE_SHORT,
        help_text="법정동(시군구) 코드"
    )
    image2           = models.URLField(
        max_length=LEN_MED, blank=True,
        help_text="썸네일 이미지 URL"
    )

    class Meta:
        db_table = 'content'
        ordering = ['content_id']

    def __str__(self):
        return f"{self.title} ({self.content_id})"


class ContentDetailBase(TimeStampedModel):
    """
    상세정보 모델들의 공통 필드:
    - 1:1 관계로 Content를 참조
    - content_type_id: ERD에 중복 기재된 필드
    """
    content        = models.OneToOneField(
        Content,
        primary_key=True,
        on_delete=models.CASCADE,
        help_text="연결된 콘텐츠(ID)",
    )
    content_type_id= models.IntegerField(
        help_text="TourAPI 관광타입 ID"
    )

    class Meta:
        abstract = True


class Festival(ContentDetailBase):
    event_place    = models.CharField(max_length=LEN_MED, null=True, blank=True, help_text="행사 장소")
    event_startdate= models.DateField(null=True, blank=True, help_text="행사 시작일")
    event_enddate  = models.DateField(null=True, blank=True, help_text="행사 종료일")
    play_time      = models.CharField(max_length=LEN_SMALL, blank=True, help_text="공연 시간")
    use_fee        = models.CharField(max_length=LEN_SMALL, blank=True, help_text="이용 요금")

    class Meta:
        db_table = 'festival'


class FoodStore(ContentDetailBase):
    first_menu     = models.TextField(blank=True, help_text="대표 메뉴")
    treat_menu     = models.TextField(blank=True, help_text="취급 메뉴")
    info_center    = models.CharField(max_length=LEN_SMALL, blank=True, help_text="문의 및 안내")
    open_time      = models.CharField(max_length=LEN_SMALL, blank=True, help_text="영업일")
    rest_date      = models.CharField(max_length=LEN_SMALL, blank=True, help_text="쉬는 날")
    chk_credit     = models.CharField(max_length=LEN_SMALL, blank=True, help_text="신용카드 가능정보")
    parking        = models.CharField(max_length=LEN_SMALL, blank=True, help_text="주차 시설")

    class Meta:
        db_table = 'food_store'


class Course(ContentDetailBase):
    distance       = models.CharField(max_length=LEN_SMALL, blank=True, help_text="코스 총 거리")
    take_time      = models.CharField(max_length=LEN_SMALL, blank=True, help_text="총 소요 시간")
    info_center    = models.CharField(max_length=LEN_SMALL, blank=True, help_text="문의 및 안내")

    class Meta:
        db_table = 'course'


class TouristAttraction(ContentDetailBase):
    chk_credit     = models.CharField(max_length=LEN_SMALL, blank=True, help_text="신용카드 가능정보")
    parking        = models.CharField(max_length=LEN_SMALL, blank=True, help_text="주차 시설")
    rest_date      = models.CharField(max_length=LEN_SMALL, blank=True, help_text="쉬는 날")
    use_time       = models.CharField(max_length=LEN_SMALL, blank=True, help_text="이용 시간")
    info_center    = models.CharField(max_length=LEN_SMALL, blank=True, help_text="문의 및 안내")

    class Meta:
        db_table = 'tourist_attraction'


class Culture(ContentDetailBase):
    chk_credit     = models.CharField(max_length=LEN_SMALL, blank=True, help_text="신용카드 가능정보")
    info_center    = models.CharField(max_length=LEN_SMALL, blank=True, help_text="문의 및 안내")
    parking        = models.CharField(max_length=LEN_SMALL, blank=True, help_text="주차 시설")
    rest_date      = models.CharField(max_length=LEN_SMALL, blank=True, help_text="쉬는 날")
    use_fee        = models.CharField(max_length=LEN_SMALL, blank=True, help_text="이용 요금")
    use_time       = models.CharField(max_length=LEN_SMALL, blank=True, help_text="이용 시간")

    class Meta:
        db_table = 'culture'


class Shopping(ContentDetailBase):
    chk_credit     = models.CharField(max_length=LEN_SMALL, blank=True, help_text="신용카드 가능정보")
    fair_day       = models.CharField(max_length=LEN_SMALL, blank=True, help_text="장 서는 날")
    info_center    = models.CharField(max_length=LEN_SMALL, blank=True, help_text="문의 및 안내")
    open_time      = models.CharField(max_length=LEN_SMALL, blank=True, help_text="영업 시간")
    parking        = models.CharField(max_length=LEN_SMALL, blank=True, help_text="주차 시설")
    rest_date      = models.CharField(max_length=LEN_SMALL, blank=True, help_text="쉬는 날")
    sale_item      = models.CharField(max_length=LEN_MED, blank=True, help_text="판매 품목")

    class Meta:
        db_table = 'shopping'


class Leports(ContentDetailBase):
    chk_credit     = models.CharField(max_length=LEN_SMALL, blank=True, help_text="신용카드 가능정보")
    info_center    = models.CharField(max_length=LEN_SMALL, blank=True, help_text="문의 및 안내")
    parking        = models.CharField(max_length=LEN_SMALL, blank=True, help_text="주차 시설")
    rest_date      = models.CharField(max_length=LEN_SMALL, blank=True, help_text="쉬는 날")
    use_time       = models.CharField(max_length=LEN_SMALL, blank=True, help_text="이용 시간")

    class Meta:
        db_table = 'leports'