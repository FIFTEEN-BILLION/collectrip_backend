# contents/management/commands/import_tour_data.py

import logging
from django.core.management.base import BaseCommand, CommandParser

# 로거 설정
logger = logging.getLogger('collectrip_importer')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Command(BaseCommand):
    """
    TourAPI로부터 관광 정보를 가져와 데이터베이스에 적재하는 Django Management Command
    """
    help = 'TourAPI로부터 지역, 카테고리별 관광 정보를 가져와 DB에 저장합니다.'

    def add_arguments(self, parser: CommandParser):
        """
        커맨드 라인 인자(argument)를 추가합니다.
        """
        parser.add_argument(
            '--area',
            type=int,
            help='데이터를 가져올 지역 코드를 지정합니다. (예: 1=서울, 31=경기)'
        )
        parser.add_argument(
            '--cat2',
            type=str,
            help='데이터를 가져올 중분류 코드를 지정합니다. (예: A04010100=5일장)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',  # 이 옵션이 있으면 True가 저장됩니다.
            help='DB에 실제로 저장하지 않고, API 호출 및 데이터 처리 과정만 테스트합니다.'
        )

    def handle(self, *args, **options):
        """
        커맨드의 메인 로직을 처리합니다.
        """
        # 옵션 값 가져오기
        area_code = options.get('area')
        cat2 = options.get('cat2')
        is_dry_run = options.get('dry_run')

        # 로깅 시작 메시지
        self.stdout.write(self.style.SUCCESS('🚀 TourAPI 데이터 적재를 시작합니다.'))
        if is_dry_run:
            self.stdout.write(self.style.WARNING('*** DRY RUN 모드로 실행됩니다. DB 변경사항이 없습니다. ***'))

        # --- 여기에 STEP 3의 핵심 로직이 들어갈 예정입니다. ---
        
        self.stdout.write(self.style.SUCCESS('✅ 데이터 적재 작업이 완료되었습니다.'))