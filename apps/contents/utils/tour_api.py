# contents/utils/tourapi.py
import os
import requests
import logging
from django.conf import settings

# 로거 인스턴스 생성
logger = logging.getLogger(__name__)

class TourAPI:
    def __init__(self, api_key=None): # api_key를 인자로 받을 수 있도록 변경
        """
        TourAPI 클래스 초기화.
        api_key가 주어지면 그 값을 사용하고, 없으면 Django settings에서 가져옵니다.
        """
        if api_key:
            self.api_key = api_key
        else:
            # Django settings에 의존하는 부분을 fallback(대안)으로 변경
            self.api_key = getattr(settings, 'TOUR_API_KEY', None)

        # os.environ을 직접 사용하는 방법 (참고용)
        # self.api_key = api_key or os.environ.get('TOUR_API_KEY')
        
        if not self.api_key:
            raise ValueError("TourAPI API Key가 없습니다. 클래스에 직접 전달하거나 settings.py에 설정해주세요.")
            
        self.base_url = "http://apis.data.go.kr/B551011/KorService2"
        self.default_params = {
            "serviceKey": self.api_key,
            "MobileOS": "ETC",
            "MobileApp": "Collectrip",
            "_type": "json",
            "numOfRows": 100,
        }

    def _make_request(self, endpoint_url, params):
        """
        실제 API 요청을 보내고 응답을 처리하는 내부 메소드
        """
        try:
            response = requests.get(endpoint_url, params=params, timeout=10)
            response.raise_for_status()  # 200 OK가 아닐 경우 HTTPError 발생
            
            data = response.json()
            # 2버전은 응답 구조가 약간 다를 수 있으나, 일반적으로 동일한 헤더 구조를 가집니다.
            if data.get('response', {}).get('header', {}).get('resultCode') != '0000':
                error_msg = data.get('response', {}).get('header', {}).get('resultMsg', 'Unknown API Error')
                logger.error(f"TourAPI 에러: {error_msg} (URL: {response.url})")
                return None

            return data.get('response', {}).get('body', {})

        except requests.exceptions.RequestException as e:
            logger.error(f"TourAPI 요청 중 에러 발생: {e}")
            return None
        except ValueError: # JSON 디코딩 에러
            logger.error("TourAPI 응답 JSON 파싱 중 에러 발생")
            return None

    def get_area_based_list2(self, area_code=None, content_type_id=None, cat1=None, cat2=None, cat3=None, page_no=1):
        """
        areaBasedList2 (지역기반 관광정보조회) API 호출
        """
        endpoint = f"{self.base_url}/areaBasedList2"
        params = {
            **self.default_params,
            "areaCode": area_code,
            "contentTypeId": content_type_id,
            "cat1": cat1,
            "cat2": cat2,
            "cat3": cat3,
            "pageNo": page_no,
        }
        # 값이 없는 파라미터는 제거하여 API 요청 URL을 깔끔하게 유지
        params = {k: v for k, v in params.items() if v is not None}
        
        logger.info(f"areaBasedList2 호출: page={page_no}, area_code={area_code}, cat2={cat2}")
        return self._make_request(endpoint, params)

    def get_detail_intro2(self, content_id, content_type_id):
        """
        detailIntro2 (소개정보조회) API 호출
        """
        endpoint = f"{self.base_url}/detailIntro2" 
        params = {
            **self.default_params,
            "contentId": content_id,
            "contentTypeId": content_type_id,
        }
        
        logger.info(f"detailIntro2 호출: content_id={content_id}, content_type_id={content_type_id}")
        return self._make_request(endpoint, params)
    
    def get_category_codes(self, content_type_id=None, cat1=None, cat2=None):
        """
        categoryCode2 (서비스 분류코드 조회) API 호출
        """
        # 2버전 API의 기본 URL을 사용합니다.
        endpoint = f"{self.base_url}/categoryCode2"
        params = {
            **self.default_params,
            "contentTypeId": content_type_id,
            "cat1": cat1,
            "cat2": cat2,
        }
        # 값이 없는 파라미터는 제거
        params = {k: v for k, v in params.items() if v is not None and v != ''}
        
        logger.info(f"categoryCode2 호출: contentTypeId={content_type_id}, cat1={cat1}")
        return self._make_request(endpoint, params)