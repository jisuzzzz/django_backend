from django.db import models  # Django의 models 모듈을 불러옴


# Account 모델 정의
class Account(models.Model):
    # 이메일 필드 (이메일 형식 검사 포함)
    email = models.EmailField()
    # 전화번호 필드, 최대 길이는 25
    # phone = models.CharField(max_length=25)
    # 비밀번호 필드, 최대 길이는 100
    password = models.CharField(max_length=100)
    # 이름 필드, 최대 길이는 20
    # name = models.CharField(max_length=20)
    # 별명 필드, 최대 길이는 20
    # nickname = models.CharField(max_length=20)
    # 계정이 생성된 시각. 자동으로 현재 시각 저장
    create_at = models.DateTimeField(auto_now_add=True)
    # 계정 정보가 마지막으로 업데이트된 시각. 자동으로 현재 시각 저장
    update_at = models.DateTimeField(auto_now=True)

    # 모델의 매니저 설정.
    objects = models.Manager()

    # 객체를 문자열로 표현할 때의 포맷 지정
    def __str__(self):
        return f'{self.email}'

        # 메타데이터 설정. 여기서는 데이터베이스 테이블 이름을 'accounts'로 지정

    class Meta:
        db_table = 'accounts'

class PlayTime(models.Model):
    objects = None
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DateTimeField(null=True, blank=True)
    # Account 모델과의 일대다 관계 설정
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='playtimes')


    def __str__(self):
        return f'{self.start_time}, {self.end_time}, {self.duration}'
    class Meta:
        db_table = 'playtime'