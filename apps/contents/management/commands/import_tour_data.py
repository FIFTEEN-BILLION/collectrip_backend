# apps/contents/management/commands/import_tour_data.py

import logging
from django.core.management.base import BaseCommand, CommandParser
from django.apps import apps
from django.db import transaction

from apps.contents.utils.tour_api import TourAPI
from apps.contents.utils.constants import ALL_AREAS, ALL_CONTENT_TYPES, CONTENT_TYPE_MAPPING
from apps.contents.models import Content

logger = logging.getLogger('collectrip_importer')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'TourAPI로부터 관광 정보를 가져와 DB에 저장합니다.'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('--all', action='store_true', help='상수 파일에 정의된 모든 지역과 콘텐츠 타입의 데이터를 가져옵니다.')
        parser.add_argument('--area', type=int, help='데이터를 가져올 지역 코드를 지정합니다.')
        parser.add_argument('--sigungu-code', type=int, help='데이터를 가져올 시군구 코드를 지정합니다.')
        parser.add_argument('--content-type-id', type=int, help='데이터를 가져올 콘텐츠 타입 ID를 지정합니다.')
        parser.add_argument('--dry-run', action='store_true', help='DB에 실제로 저장하지 않고, API 호출 및 데이터 처리 과정만 테스트합니다.')

    def handle(self, *args, **options):
        is_dry_run = options.get('dry_run')
        self.stdout.write(self.style.SUCCESS('🚀 TourAPI 데이터 적재를 시작합니다.'))
        if is_dry_run:
            self.stdout.write(self.style.WARNING('*** DRY RUN 모드로 실행됩니다. DB 변경사항이 없습니다. ***'))

        if options.get('all'):
            self.stdout.write(self.style.SUCCESS('--all 옵션으로 전체 데이터 적재를 시작합니다.'))
            for area_code in ALL_AREAS:
                for content_type_id in ALL_CONTENT_TYPES:
                    if str(content_type_id) not in CONTENT_TYPE_MAPPING:
                        continue
                    self.stdout.write(f"\n--- 처리 중: 지역코드={area_code}, 콘텐츠타입={content_type_id} ---")
                    self._process_data(area_code=area_code, content_type_id=content_type_id, is_dry_run=is_dry_run)
        else:
            self._process_data(
                area_code=options.get('area'),
                sigungu_code=options.get('sigungu_code'),
                content_type_id=options.get('content_type_id'),
                is_dry_run=is_dry_run
            )
        self.stdout.write(self.style.SUCCESS('\n✅ 모든 데이터 적재 작업이 완료되었습니다.'))

    def _process_data(self, **kwargs):
        api = TourAPI()
        stats = {'total': 0, 'created': 0, 'updated': 0, 'skipped': 0, 'failed': 0}
        page_no = 1

        is_dry_run = kwargs.get('is_dry_run', False)
        api_kwargs = {k: v for k, v in kwargs.items() if k != 'is_dry_run' and v is not None}

        while True:
            body = api.get_area_based_list2(page_no=page_no, **api_kwargs)
            if not body or 'items' not in body or not body.get('items'):
                break

            items = body['items']['item']
            if not isinstance(items, list): items = [items]

            for item in items:
                stats['total'] += 1
                content_id = item.get('contentid')
                content_type_id = item.get('contenttypeid')

                if not content_id or not content_type_id:
                    stats['skipped'] += 1
                    continue

                logger.info(f"[{stats['total']}/{body.get('totalCount', 0)}] 처리 중: {item.get('title')} (ID: {content_id})")

                try:
                    content_defaults = {
                        'content_type_id': content_type_id,
                        'title': item.get('title', ''),
                        'addr1': item.get('addr1', ''),
                        'addr2': item.get('addr2', ''),
                        'cat1': item.get('cat1'),
                        'cat2': item.get('cat2'),
                        'cat3': item.get('cat3'),
                        'areacode': item.get('areacode'),
                        'sigungu_code': item.get('sigungucode'),
                        'map_x': item.get('mapx'),
                        'map_y': item.get('mapy'),
                        'image2': item.get('firstimage2', ''),
                    }

                    if not is_dry_run:
                        with transaction.atomic():
                            content_obj, created = Content.objects.update_or_create(content_id=content_id, defaults=content_defaults)
                            stats['created' if created else 'updated'] += 1
                    else:
                        content_obj = Content(content_id=content_id, **content_defaults)
                        logger.info(f"[Dry Run] Content 저장 예정: '{content_obj.title}'")

                    cat2_code = item.get('cat2')
                    content_type_id_str = str(content_type_id)
                    model_name = CONTENT_TYPE_MAPPING.get(content_type_id_str, {}).get(cat2_code)
                    
                    if model_name:
                        detail_body = api.get_detail_intro2(content_id=content_id, content_type_id=content_type_id)
                        if detail_body and 'items' in detail_body and detail_body.get('items'):
                            detail_item = detail_body['items']['item']
                            if isinstance(detail_item, list): detail_item = detail_item[0]
                            
                            DetailModel = apps.get_model('contents', model_name)
                            detail_defaults = self.map_detail_fields(model_name, detail_item)
                            
                            if not is_dry_run:
                                with transaction.atomic():
                                    detail_defaults['content_type_id'] = content_type_id
                                    detail_obj, detail_created = DetailModel.objects.update_or_create(
                                        content=content_obj, 
                                        defaults=detail_defaults
                                    )
                            else:
                                logger.info(f"[Dry Run] {model_name} 상세 정보 저장 예정: '{content_obj.title}'")
                except Exception as e:
                    stats['failed'] += 1
                    logger.error(f"오류 발생 (ID: {content_id}): {e}") # exc_info=True로 다시 변경하여 상세 오류 확인

            if page_no * body.get('numOfRows', 100) >= body.get('totalCount', 0):
                break
            page_no += 1

        self.stdout.write(f"처리 결과 -> 총 시도: {stats['total']}, 신규: {stats['created']}, 업데이트: {stats['updated']}, 스킵: {stats['skipped']}, 실패: {stats['failed']}")

    # 👇 2. `map_detail_fields` 함수를 대폭 수정!
    def map_detail_fields(self, model_name, detail_item):
        """
        detailIntro2 API의 응답(`detail_item`)을 각 상세 모델 필드에 맞게 매핑합니다.
        이제 이 함수는 '상세 정보'만 책임집니다.
        """
        specific_details = {}
        if model_name == 'Festival':
            specific_details = {
                'event_place': detail_item.get('eventplace'),
                'event_startdate': detail_item.get('eventstartdate') or None, # 날짜 필드는 None으로 처리
                'event_enddate': detail_item.get('eventenddate') or None,
                'play_time': detail_item.get('playtime'),
                'use_fee': detail_item.get('usetimefestival'),
            }
        elif model_name == 'FoodStore':
            specific_details = {
                'first_menu': detail_item.get('firstmenu'),
                'treat_menu': detail_item.get('treatmenu'),
                'info_center': detail_item.get('infocenterfood'),
                'open_time': detail_item.get('opentimefood'),
                'rest_date': detail_item.get('restdatefood'),
                'chk_credit': detail_item.get('chkcreditcardfood'),
                'parking': detail_item.get('parkingfood'),
            }
        elif model_name == 'Course':
            specific_details = {
                'distance': detail_item.get('distance'),
                'take_time': detail_item.get('taketime'),
                'info_center': detail_item.get('infocentertourcourse'),
            }
        elif model_name == 'TouristAttraction':
            specific_details = {
                'chk_credit': detail_item.get('chkcreditcard'),
                'parking': detail_item.get('parking'),
                'rest_date': detail_item.get('restdate'),
                'use_time': detail_item.get('usetime'),
                'info_center': detail_item.get('infocenter'),
            }
        elif model_name == 'Culture':
            specific_details = {
                'chk_credit': detail_item.get('chkcreditcardculture'),
                'info_center': detail_item.get('infocenterculture'),
                'parking': detail_item.get('parkingculture'),
                'rest_date': detail_item.get('restdateculture'),
                'use_fee': detail_item.get('usefee'),
                'use_time': detail_item.get('usetimeculture'),
            }
        elif model_name == 'Shopping':
            specific_details = {
                'chk_credit': detail_item.get('chkcreditcardshopping'),
                'fair_day': detail_item.get('fairday'),
                'info_center': detail_item.get('infocentershopping'),
                'open_time': detail_item.get('opentime'),
                'parking': detail_item.get('parkingshopping'),
                'rest_date': detail_item.get('restdateshopping'),
                'sale_item': detail_item.get('saleitem'),
            }
        elif model_name == 'Leports':
            specific_details = {
                'chk_credit': detail_item.get('chkcreditcardleports'),
                'info_center': detail_item.get('infocenterleports'),
                'parking': detail_item.get('parkingleports'),
                'rest_date': detail_item.get('restdateleports'),
                'use_time': detail_item.get('usetimeleports'),
            }

        return specific_details