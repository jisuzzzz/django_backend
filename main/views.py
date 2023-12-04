import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from algorithm import sudoku_solver, sudoku_maker
from imgtoarr import main

import json
def index(request):
    print(request)
    return render(request, "main/index.html")

def get_sudoku_arr(request):
    arr = sudoku_maker.run_make_arr()
    print(request)
    arr = arr.strip().split("\n")
    arr = [[int(num) for num in line.split()] for line in arr]
    return JsonResponse({'arr' : arr})


def solve_sudoku(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        # .decode('utf-8') -> 바이트 문자열을 'utf-8'인코딩을 사용해 xq표준 python 문자열 str로 디코딩
        # .loads -> JSON 형식의 문자열을 python 딕서너리로 변환
        arr = body.get('arr', [])
        result = sudoku_solver.run_cpp_program(arr)
        return JsonResponse({'result': result})
def img_to_arr(request):
    if request.method == "POST":
        try:
            # 클라이언트에서 전송한 파일은 2'image' 키를 통해 얻을 수 있습니다.
            uploaded_file = request.FILES['image']

            # 서버에 저장할 파일 경로를 지정합니다.
            # 여기서는 'imgtoarr/' 디렉토리에 클라이언트에서 업로드한 파일 이름으로 저장합니다.
            file_path = 'imgtoarr/' + uploaded_file.name

            # 파일을 바이너리 쓰기 모드로 열고, 업로드된 파일의 데이터를 쓰기합니다.
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            arr = main.img_make_arr(file_path)
            arr_list_int = [int(x) for x in arr]
            arr_list_int = [arr_list_int[i:i + 9] for i in range(0, len(arr_list_int), 9)]
            return JsonResponse({'arr': arr_list_int})
        except Exception as e:
            # 예외가 발생한 경우 에러 응답을 반환합니다.
            return JsonResponse({'status': 'error', 'message': str(e)})

    # POST 메서드가 아닌 경우에는 잘못된 요청 메시지를 반환합니다.
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

