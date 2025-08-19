# contents/management/commands/lookup_codes.py

from django.core.management.base import BaseCommand, CommandParser
from apps.contents.utils.tour_api import TourAPI
from apps.contents.utils.constants import ALL_CONTENT_TYPES

class Command(BaseCommand):
    help = 'TourAPI로부터 카테고리 또는 지역/시군구 코드를 조회합니다.'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--type', type=str, choices=['category', 'area'], required=True,
            help="조회할 코드 종류 ('category' 또는 'area')"
        )
        parser.add_argument(
            '--content-type-id', type=int,
            help='카테고리 조회 시 사용할 콘텐츠 타입 ID'
        )
        parser.add_argument(
            '--area-code', type=int,
            help='시군구 코드 조회 시 사용할 상위 지역 코드'
        )

    def handle(self, *args, **options):
        lookup_type = options['type']
        
        if lookup_type == 'category':
            self._lookup_categories(**options)
        elif lookup_type == 'area':
            self._lookup_area_codes(**options)
            
    def _lookup_area_codes(self, **options):
        """지역 또는 시군구 코드를 조회하여 출력합니다."""
        api = TourAPI()
        area_code = options.get('area_code')
        
        if area_code:
            self.stdout.write(self.style.SUCCESS(f"🚀 [지역코드: {area_code}]의 시군구 코드 조회를 시작합니다."))
        else:
            self.stdout.write(self.style.SUCCESS("🚀 광역 지역 코드 조회를 시작합니다."))
        self.stdout.write("="*50)

        body = api.get_area_codes(area_code=area_code)

        if not body or 'items' not in body or not body.get('items'):
            self.stdout.write(self.style.WARNING("코드 정보를 가져오지 못했습니다."))
            return
            
        items = body['items']['item']
        if not isinstance(items, list): items = [items]

        for item in sorted(items, key=lambda x: int(x['rnum'])):
            self.stdout.write(f"- {item['name']} (코드: {item['code']})")
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS("✅ 조회 완료."))

    def _lookup_categories(self, **options):
        api = TourAPI()
        content_type_id_option = options.get('content_type_id')
        content_types_to_fetch = [content_type_id_option] if content_type_id_option else ALL_CONTENT_TYPES
        
        self.stdout.write(self.style.SUCCESS("🚀 서비스 분류 코드 조회를 시작합니다."))
        self.stdout.write("="*50)
        
        for content_type_id in content_types_to_fetch:
            self.stdout.write(self.style.HTTP_INFO(f"\n[ ContentTypeID: {content_type_id} ]"))
            
            body_cat1 = api.get_category_codes(content_type_id=content_type_id)
            if not body_cat1 or 'items' not in body_cat1 or not body_cat1.get('items'):
                self.stdout.write(self.style.WARNING("  - 해당 콘텐츠 타입의 카테고리 정보가 없습니다."))
                continue

            items_cat1 = body_cat1['items']['item']
            if not isinstance(items_cat1, list): items_cat1 = [items_cat1]

            for cat1_item in items_cat1:
                self.stdout.write(f"  - 대분류: {cat1_item['name']} ({cat1_item['code']})")
                body_cat2 = api.get_category_codes(content_type_id=content_type_id, cat1=cat1_item['code'])
                if not body_cat2 or 'items' not in body_cat2 or not body_cat2.get('items'):
                    continue
                items_cat2 = body_cat2['items']['item']
                if not isinstance(items_cat2, list): items_cat2 = [items_cat2]
                for cat2_item in items_cat2:
                    self.stdout.write(f"    - 중분류: {cat2_item['name']} ({cat2_item['code']})")

        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS("✅ 조회 완료."))