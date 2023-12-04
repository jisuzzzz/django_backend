import subprocess  # 외부 명령어를 실행하기 위한 모듈을 가져옴

def run_make_arr():
    try:
        # C++ 컴파일러인 g++로 make_arr.cpp를 컴파일하고 실행 파일의 이름을 sudoku_maker로 지정
        subprocess.run(["g++", "algorithm/make_arr.cpp", "-o", "sudoku_maker"], check=True)
        # 컴파일된 실행 파일 sudoku_maker를 실행
        # 실행 결과의 표준 출력과 에러 출력을 가져올 수 있도록 설정
        process = subprocess.Popen(
            ["./sudoku_maker"],
            stdout=subprocess.PIPE,  # 표준 출력을 파이프로 가져옴
            stderr=subprocess.PIPE,  # 에러 출력을 파이프로 가져옴
            text=True  # 출력을 텍스트 형태로 변환
        )
        # 실행 파일의 실행이 완료될 때까지 대기하고, 표준 출력과 에러 출력을 가져옴
        stdout, stderr = process.communicate()
        # 표준 출력 결과를 반환
        return stdout
    # C++ 컴파일 과정에서 문제가 발생한 경우 에러 메시지 반환
    except subprocess.CalledProcessError as e:
        return f"C++ compilation failed: {e}"
    # 그 외 기타 예외가 발생한 경우 에러 메시지 반환
    except Exception as e:
        return f"An error occurred: {e}"


# if __name__ == "__main__":
#     result = run_make_arr()
#     lines = result.strip().split("\n")
#
#     # 각 줄을 공백으로 분리하고, 각 문자열을 int로 변환하여 2차원 리스트로
#     sudoku_int = [[int(num) for num in line.split()] for line in lines]
#
#     # print(type(result))
#     print(result)
#     # print(sudoku_int)
#     output_str = ""
#
#     for row in sudoku_int:
#         row_str = " ".join(map(str, row))
#         output_str += row_str + "\n"  # 줄바꿈 문자를 추가
#
#     print(output_str)
#     print(type(output_str))
