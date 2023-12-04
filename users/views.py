from django.shortcuts import render
import json, re, traceback, bcrypt, jwt  # 각종 Python 라이브러리
from django.http import JsonResponse  # Django의 JsonResponse 클래스
from django.views import View  # Django의 View 클래스
from django.db.models import Q  # Django의 쿼리 생성기
from .models import Account, PlayTime
from django.db.models import Min
from django.db.models.functions import Trunc
from django.core.exceptions import ObjectDoesNotExist
import datetime

import my_settings

# 패스워드의 최소 길이를 전역 변수로 설정
minimum_password_length = 8


# 이메일 유효성 검사 함수
# def valid_email(email):
#     # 이메일 정규 표현식 패턴
#     pattern = re.compile('^.+@+.+\.+.+$')
#     # 정규 표현식에 맞지 않으면 유효하지 않은 이메일
#     if not pattern.match(email):
#         return False, JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
#     return True, None

def valid_email(email):
    # 이메일 정규 표현식 패턴
    pattern = re.compile('^.+@+.+\.+.+$')
    # 정규 표현식에 맞지 않으면 유효하지 않은 이메일
    if not pattern.match(email):
        return False, JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
    return True, None


# 패스워드 길이 검사 함수
def valid_password(password):
    # 패스워드 길이가 최소 길이보다 짧으면 유효하지 않음
    if len(password) < minimum_password_length:
        return False, JsonResponse({'message': 'SHORT_PASSWORD'}, status=400)
    return True, None


# 전화번호 유효성 검사 함수
# def valid_phone(phone):
#     # 전화번호 정규 표현식 패턴
#     pattern = re.compile('^[0]\d{9,10}$')
#     # 정규 표현식에 맞지 않으면 유효하지 않은 전화번호
#     if not pattern.match(phone):
#         return False, JsonResponse({'message': 'INVALID_PHONE_NUMBER'}, status=400)
#     return True, None


# 회원가입을 처리하는 클래스
class SignUpView(View):
    # POST 요청을 처리하는 메서드
    def post(self, request):
        # 클라이언트로부터 받은 JSON 데이터를 파싱
        data = json.loads(request.body)
        try:
            # 각 필드의 데이터를 가져옴
            email = data.get('email', None)
            password = data.get('password', None)
            # name = data.get('name', None)
            # nickname = data.get('nickname', None)
            # phone = data.get('phone', None)

            # 필수 데이터가 없으면 400 에러 반환
            if not (password and email):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            # 유효성 검사
            valid, response = valid_email(email)
            if not valid:
                return response

            valid, response = valid_password(password)
            if not valid:
                return response

            # valid, response = valid_phone(phone)
            # if not valid:
            #     return response

            # 이미 존재하는 계정인지 검사
            if Account.objects.filter(Q(email=email)).exists():
                return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status=409)

            # 새 계정 생성
            Account.objects.create(
                email=email,
                # name=name,
                # phone=phone,
                # nickname=nickname,
                password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            )
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            # KeyError 예외 처리
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


# 로그인을 처리하는 클래스
class LoginView(View):
    # POST 요청을 처리하는 메서드
    def post(self, request):
        # 클라이언트로부터 받은 JSON 데이터를 파싱
        data = json.loads(request.body)
        try:
            # 각 필드의 데이터를 가져옴
            email = data.get('email')
            # phone = data.get('phone')
            password = data.get('password')

            # 이메일 또는 전화번호로 계정을 찾음
            if Account.objects.filter(Q(email=email)).exists():
                account = Account.objects.get(Q(email=email))

                # 비밀번호가 맞는지 검사
                if bcrypt.checkpw(password.encode('utf-8'), account.password.encode('utf-8')):
                    # JWT 토큰 생성
                    token = jwt.encode({'email': email}, my_settings.SECRET['secret'], algorithm='HS256')
                    # 토큰을 클라이언트에 반환
                    return JsonResponse({'message': 'SUCCESS', 'token': token, 'email': email}, status=200)

                # 비밀번호가 틀린 경우
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)

            # 계정이 존재하지 않는 경우
            return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            # KeyError 예외 처리
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class RankingDB(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email = data.get('email')
            duration = data.get('duration')

            # 이메일 유효성 검사
            valid, response = valid_email(email)
            if not valid:
                return response

            # 이메일을 사용하여 Account 모델에서 사용자 조회
            if Account.objects.filter(Q(email=email)).exists():
                account = Account.objects.get(Q(email=email))

                # duration 문자열을 datetime 객체로 변환
                duration_datetime = datetime.datetime.strptime(duration, '%Y-%m-%d %H:%M:%S')

                # PlayTime 인스턴스 생성
                PlayTime.objects.create(
                    account_id=account.id,
                    duration=duration_datetime
                )
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message': 'Account not found'}, status=404)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except ValueError:
            return JsonResponse({"message": "Invalid date format"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)



class RankingView(View):
    def post(self, request):
        data = json.loads(request.body)  # JSON 데이터 로드
        try:
            email = data.get('email')

            if not email:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            # 이메일을 사용하여 Account 모델에서 사용자 조회
            if Account.objects.filter(Q(email=email)).exists():
                account = Account.objects.get(Q(email=email))
                # 관련된 PlayTime 데이터 조회
                play_times = PlayTime.objects.filter(Q(account_id=account.id))

                durations = sorted([play_time.duration.strftime('%H:%M:%S') for play_time in play_times if play_time.duration is not None])[:5]
                return JsonResponse({'durations': durations, 'email': email}, status=200)
            else:
                return JsonResponse({'message': 'ACCOUNT_NOT_FOUND'}, status=404)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "ACCOUNT_NOT"}, status=403)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)


class Ranking_all_View(View):
    def post(self, request):
        try:
            # 각 유저별로 가장 짧은 duration과 관련된 Account 정보를 함께 찾음
            shortest_durations_per_user = PlayTime.objects.select_related('account').annotate(
                shortest_duration=Min('duration')
            ).values('account__email', 'shortest_duration')

            # 전체에서 가장 짧은 상위 5개의 durations을 가진 유저 선택
            top_users = (
                shortest_durations_per_user
                .order_by('shortest_duration')[:5]
                .annotate(duration_str=Trunc('shortest_duration', 'second'))
            )

            result = [
                {
                    'email': user['account__email'],
                    'duration': user['duration_str'].strftime('%H:%M:%S')
                } for user in top_users
            ]

            return JsonResponse({'top_users': result}, status=200)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)


