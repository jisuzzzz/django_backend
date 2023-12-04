import subprocess
def run_cpp_program(input_data):
    try:
        # 만약 input_data가 리스트 타입이면, 문자열로 변환
        if isinstance(input_data, list):
            # 각 배열을 문자열로 변환하고 줄바꿈 문자로 연결
            input_data = '\n'.join([' '.join(map(str, arr)) for arr in input_data])
        # C++ 코드 컴파일
        # subprocess.run(["g++", "/path/to/cpp/project/ssudo.cpp", "-o", "sudoku_solver"], check=True)
        subprocess.run(["g++", "algorithm/ssudo.cpp", "-o", "sudoku_solver"], check=True)
        # C++ 프로그램 실행
        process = subprocess.Popen(
            ["./sudoku_solver"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input_data)
        return stdout
    except subprocess.CalledProcessError as e:
        return f"C++ compilation failed: {e}"
    except Exception as e:
        return f"An error occurred: {e}"
if __name__ == "__main__":
    print("스도쿠를 입력하세요 (9x9 숫자 배열, 빈 칸은 0으로 표시):")
    input_data = ""
    for _ in range(9):
        input_row = input()
        input_data += input_row + "\n"

    result = run_cpp_program(input_data)
    print(result)

if __name__ == "__main__":
    print("스도쿠를 입력하세요 (9x9 숫자 배열, 빈 칸은 0으로 표시):")

    sudoku_list = []
    for _ in range(9):
        input_row = input()
        int_row = list(map(int, input_row.split()))
        sudoku_list.append(int_row)

    # 2차원 리스트를 다시 문자열로 변환하여 C++ 프로그램에 입력으로 전달
    input_data = "\n".join([" ".join(map(str, row)) for row in sudoku_list]) + "\n"

    result = run_cpp_program(input_data)
    print(result)
