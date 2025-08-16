# contents/management/commands/import_categories.py

from django.core.management.base import BaseCommand, CommandParser
from apps.contents.utils.tour_api import TourAPI
from apps.contents.utils.constants import ALL_CONTENT_TYPES

class Command(BaseCommand):
    """
    TourAPI로부터 서비스 분류 코드(카테고리)를 조회하여 출력하는 Management Command
    """
    help = 'TourAPI로부터 서비스 분류 코드를 조회하여 `CONTENT_TYPE_MAPPING`을 채우는 데 도움을 줍니다.'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--content-type-id',
            type=int,
            help='카테고리를 조회할 콘텐츠 타입 ID를 지정합니다. (예: 39=음식점)'
        )

    def handle(self, *args, **options):
        api = TourAPI()
        content_type_id_option = options.get('content_type_id')

        # 조회할 콘텐츠 타입 목록 설정
        if content_type_id_option:
            content_types_to_fetch = [content_type_id_option]
        else:
            # 옵션이 없으면 상수에 정의된 모든 콘텐츠 타입을 조회
            content_types_to_fetch = ALL_CONTENT_TYPES
        
        self.stdout.write(self.style.SUCCESS("🚀 서비스 분류 코드 조회를 시작합니다."))
        self.stdout.write("="*50)
        
        for content_type_id in content_types_to_fetch:
            self.stdout.write(self.style.HTTP_INFO(f"\n[ ContentTypeID: {content_type_id} ]"))
            
            # 1. 대분류 조회
            body_cat1 = api.get_category_codes(content_type_id=content_type_id)
            if not body_cat1 or 'items' not in body_cat1 or not body_cat1.get('items'):
                self.stdout.write(self.style.WARNING("  - 해당 콘텐츠 타입의 카테고리 정보가 없습니다."))
                continue

            items_cat1 = body_cat1['items']['item']
            if not isinstance(items_cat1, list): items_cat1 = [items_cat1]

            for cat1_item in items_cat1:
                self.stdout.write(f"  - 대분류: {cat1_item['name']} ({cat1_item['code']})")
                
                # 2. 중분류 조회
                body_cat2 = api.get_category_codes(content_type_id=content_type_id, cat1=cat1_item['code'])
                if not body_cat2 or 'items' not in body_cat2 or not body_cat2.get('items'):
                    continue
                
                items_cat2 = body_cat2['items']['item']
                if not isinstance(items_cat2, list): items_cat2 = [items_cat2]

                for cat2_item in items_cat2:
                    self.stdout.write(f"    - 중분류: {cat2_item['name']} ({cat2_item['code']})")

        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS("✅ 조회 완료. 이 정보를 바탕으로 `import_tour_data.py`의 `CONTENT_TYPE_MAPPING`을 수정하세요."))