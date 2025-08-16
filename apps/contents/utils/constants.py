# contents/utils/constants.py

ALL_AREAS = [1, 2, 3, 4, 5, 6, 7, 8, 31, 32, 33, 34, 35, 36, 37, 38, 39]
ALL_CONTENT_TYPES = [12, 14, 15, 25, 28, 32, 38, 39]  # 관광지, 문화시설, 축제, 여행코스, 레포츠, 숙박, 쇼핑, 음식점

# 서비스 분류 코드 조회 결과를 최종 반영한 매핑 정보
CONTENT_TYPE_MAPPING = {
    '12': {  # 관광지 (Attraction)
        'A0101': 'TouristAttraction', # 자연관광지
        'A0201': 'TouristAttraction', # 역사관광지
        'A0202': 'TouristAttraction', # 휴양관광지
        'A0203': 'TouristAttraction', # 체험관광지
        # 'A0204' (산업관광지) 등은 필요에 따라 추가
    },
    '14': {  # 문화시설 (Culture)
        'A0206': 'Culture',
    },
    '15': {  # 행사/공연/축제 (Festival)
        'A0207': 'Festival', # 축제
        'A0208': 'Festival', # 공연/행사
    },
    '25': {  # 여행 코스 (Course)
        'C0112': 'Course', # 가족코스
        'C0113': 'Course', # 나홀로코스
        'C0114': 'Course', # 힐링코스
        'C0115': 'Course', # 도보코스
        'C0116': 'Course', # 캠핑코스
        'C0117': 'Course', # 맛코스
    },
    '28': {  # 레포츠 (Leports)
        'A0302': 'Leports', # 육상 레포츠
        'A0303': 'Leports', # 수상 레포츠
        'A0304': 'Leports', # 항공 레포츠
        'A0305': 'Leports', # 복합 레포츠
    },
    '38': {  # 쇼핑 (Shopping)
        'A0401': 'Shopping',
    },
    '39': {  # 음식점 (FoodStore)
        'A0502': 'FoodStore',
    }
}