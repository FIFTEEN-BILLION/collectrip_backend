from django.db import models
from apps.users.models import TimeStampedModel 

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
        max_length=255,
        help_text="주소"
    )
    addr2            = models.CharField(
        max_length=255,
        blank=True,
        help_text="상세주소"
    )
    map_x            = models.FloatField(
        help_text="GPS X좌표"
    )
    map_y            = models.FloatField(
        help_text="GPS Y좌표"
    )
    tel              = models.CharField(
        max_length=50,
        blank=True,
        help_text="연락처"
    )
    title            = models.CharField(
        max_length=255,
        help_text="제목"
    )
    dong_region_code = models.IntegerField(
        help_text="법정동(시도) 코드"
    )
    dong_sigungu_code= models.IntegerField(
        help_text="법정동(시군구) 코드"
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
    booking_place  = models.CharField(max_length=255, blank=True, help_text="예매처")
    discount_info  = models.TextField(blank=True, help_text="할인 정보")
    event_homepage = models.URLField(blank=True, help_text="행사 홈페이지")
    event_startdate= models.DateField(null=True, blank=True, help_text="행사 시작일")
    event_enddate  = models.DateField(null=True, blank=True, help_text="행사 종료일")
    place_info     = models.TextField(blank=True, help_text="행사장 위치 안내")
    play_time      = models.CharField(max_length=100, blank=True, help_text="공연 시간")
    program        = models.TextField(blank=True, help_text="행사 프로그램")
    use_time       = models.CharField(max_length=100, blank=True, help_text="이용 요금")

    class Meta:
        db_table = 'festival'


class Info(ContentDetailBase):
    """
    ERD 상 'info' / alias 'food_store' 테이블
    """
    chk_credit     = models.CharField(max_length=100, blank=True, help_text="신용카드 가능정보")
    discount_info  = models.TextField(blank=True, help_text="할인 정보")
    open_time      = models.CharField(max_length=100, blank=True, help_text="영업일")
    packing        = models.BooleanField(default=False, help_text="포장 가능 여부")
    parking        = models.CharField(max_length=100, blank=True, help_text="주차 시설")
    reservation    = models.CharField(max_length=255, blank=True, help_text="예약 안내")
    rest_date      = models.CharField(max_length=100, blank=True, help_text="쉬는 날")
    scale          = models.CharField(max_length=100, blank=True, help_text="규모")
    treat_menu     = models.TextField(blank=True, help_text="취급 메뉴")

    class Meta:
        db_table = 'info'


class Course(ContentDetailBase):
    distance       = models.CharField(max_length=100, blank=True, help_text="코스 총 거리")
    info_center    = models.CharField(max_length=100, blank=True, help_text="문의 및 안내")
    take_time      = models.CharField(max_length=100, blank=True, help_text="총 소요 시간")
    theme          = models.CharField(max_length=100, blank=True, help_text="코스 테마")

    class Meta:
        db_table = 'course'


class TouristAttraction(ContentDetailBase):
    chk_credit     = models.CharField(max_length=100, blank=True, help_text="신용카드 가능정보")
    info_center    = models.CharField(max_length=100, blank=True, help_text="문의 및 안내")
    open_date      = models.DateField(null=True, blank=True, help_text="개장일")
    parking        = models.CharField(max_length=100, blank=True, help_text="주차 시설")
    rest_date      = models.CharField(max_length=100, blank=True, help_text="쉬는 날")
    use_time       = models.CharField(max_length=100, blank=True, help_text="이용 시간")

    class Meta:
        db_table = 'tourist_attraction'


class Culture(ContentDetailBase):
    chk_credit     = models.CharField(max_length=100, blank=True, help_text="신용카드 가능정보")
    discount_info  = models.TextField(blank=True, help_text="할인 정보")
    info_center    = models.CharField(max_length=100, blank=True, help_text="문의 및 안내")
    parking        = models.CharField(max_length=100, blank=True, help_text="주차 시설")
    rest_date      = models.CharField(max_length=100, blank=True, help_text="쉬는 날")
    use_fee        = models.CharField(max_length=100, blank=True, help_text="이용 요금")
    use_time       = models.CharField(max_length=100, blank=True, help_text="이용 시간")

    class Meta:
        db_table = 'culture'


class Shopping(ContentDetailBase):
    chk_credit     = models.CharField(max_length=100, blank=True, help_text="신용카드 가능정보")
    fair_day       = models.CharField(max_length=100, blank=True, help_text="장 서는 날")
    info_center    = models.CharField(max_length=100, blank=True, help_text="문의 및 안내")
    open_date      = models.DateField(null=True, blank=True, help_text="개장일")
    open_time      = models.CharField(max_length=100, blank=True, help_text="영업 시간")
    parking        = models.CharField(max_length=100, blank=True, help_text="주차 시설")
    rest_date      = models.CharField(max_length=100, blank=True, help_text="쉬는 날")
    sale_item      = models.CharField(max_length=255, blank=True, help_text="판매 품목")
    sale_item_cost = models.CharField(max_length=255, blank=True, help_text="판매 품목별 가격")
    shop_guide     = models.TextField(blank=True, help_text="매장 안내")

    class Meta:
        db_table = 'shopping'


class Leports(ContentDetailBase):
    accom_count    = models.IntegerField(null=True, blank=True, help_text="수용 인원")
    chk_credit     = models.CharField(max_length=100, blank=True, help_text="신용카드 가능정보")
    exp_age_range  = models.CharField(max_length=100, blank=True, help_text="체험 가능 연령")
    info_center    = models.CharField(max_length=100, blank=True, help_text="문의 및 안내")
    open_period    = models.CharField(max_length=100, blank=True, help_text="운영 기간")
    parking_fee    = models.CharField(max_length=100, blank=True, help_text="주차 요금")
    parking        = models.CharField(max_length=100, blank=True, help_text="주차 시설")
    reservation    = models.CharField(max_length=255, blank=True, help_text="예약 안내")
    rest_date      = models.CharField(max_length=100, blank=True, help_text="쉬는 날")
    use_fee        = models.CharField(max_length=100, blank=True, help_text="입장료")
    use_time       = models.CharField(max_length=100, blank=True, help_text="이용 시간")

    class Meta:
        db_table = 'leports'
