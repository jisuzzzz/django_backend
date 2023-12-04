#include <iostream>
using namespace std;
int grid[9][9];

void printGrid() {
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            cout << grid[i][j] << " ";
        }
        cout << endl;
    }
}

bool isPossible(){
    int row, col;
    int filled_cell = 0;
    
    for(row =0; row<9; row++){
        for(col=0; col<9; col++){
            if(grid[row][col] != 0) filled_cell++;
        }
    }
    return filled_cell >= 17;
}
// 최소 17개의 cell이 채워져 있어야 스도쿠가 가능

bool isRow(int row, int num){
    for(int i=0; i<9; i++){
        if(num == grid[row][i]) return true;
    }
    return false;
}

bool isCol(int col, int num){
    for(int i=0; i<9; i++){
        if(num == grid[i][col]) return true;
    }
    return false;
}

/*
주어진 행 row에 num이 이미 존재하는지 찾는 함수 -> isRow
주어진 열 col에 num이 이미 존재하는지 찾는 함수 -> isCol
*/

bool isSubGrid(int start_row, int start_col, int num){
    int i, j;
    for (i=start_row; i<start_row+3; i++){
        for(j=start_col; j<start_col+3; j++){
            if(grid[i][j]==num) return true;
        }
    }
    return false;
}
/*
3x3 sub gird에 num이 이미 존재하는지 찾는 함수
밑에 함수에서 start_row, start_col을 정의함
start_row = row - row%3
start_col = col - col%3
이렇게 정의하면 
0~2까지는 0
3~5까지는 3
6~8까지는 6
이라서 3x3 sub grid에서 시작 지점이 항상 일정함
*/ 

bool isVaild(int row, int col, int num){
    int start_row = row - row%3;
    int start_col = col - col%3;
    
    return !isRow(row, num) && !isCol(col, num) && !isSubGrid(start_row, start_col, num);
}
/*
유효성 검사 주어진 행, 열 row, col에 주어진 숫자 num이 이미 존재 하지 않고
sub gird 3x3에도 존재 하지 않아야 함
*/

bool findEmptyCell(int &row, int &col){
    for(row=0; row<9; row++){
        for(col=0; col<9; col++){
            if(grid[row][col]==0) return true;
        }
    }
    return false;
}
/*
gird 내에 빈 cell 즉 채워지지 않은 cell을 찾는 함수
비어 있는 cell을 찾으면 그 cell에 row, col을 외부에 참조 매개변수로 반환
모든 cell이 채워져 있다면 == 수도쿠 풀이 완료!
*/

bool solve_sudoku(int &call_count){
    int row, col;
    call_count++;
    if(!findEmptyCell(row, col)) return true;

    for(int num=1; num<=9; num++){
        if(isVaild(row, col, num)){
            grid[row][col] = num;
            if(solve_sudoku(call_count)) return true;
            grid[row][col] = 0;
        }
    }
    return false;
}
/*
findEmptyCell함수를 호출해 비어있는 cell에 (row,col)을 찾고 반환
for루프는 1부터 9까지의 숫자를 시도 == 이 숫자는 그리드에 배치할 후보 숫자
isValid 함수를 호출해 (row,col)에 숫자를 배치할 수 있는지 확인
-> isValid함수는 특정 숫자가 해당 행, 열, 서브 그리드에 이미 존재하는지 확인하는 함수
isVaild 함수가 true를 반환하면 == 그 위치에 숫자를 배치하고 solve_sudoku함수를 재귀적으로 호출
이 과정속에서 모든 비어있는 cell에 대한 시도가 이루어짐
재귀 호출에서 solve_sudoku가 ture를 반환하면 유효한 숫자가 유효한 자리에 배치된 것
만약 현재 위치(row,col)에 숫자를 배치하고 solve_sudoku함수에서 fales가 반환되었다면,
현재 위치에 배치된 숫자를 0으로 설정 == 빈 cell로 초기화 하고 다음 숫자를 시도함
*/

int main() {
    int call_count = 0;
    int filled = 0;

    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            scanf("%d", &grid[i][j]);
            if (grid[i][j] > 0) {
                filled++;
            }
        }
    }

//    cout << "채워진 셀의 수: " << filled << endl;

    if (!isPossible()) {
        printf("불가능한 스도쿠 퍼즐입니다.");
    } else {
        if (solve_sudoku(call_count)) {
//            printf("성공!");
            printGrid();
//            cout << "재귀 함수 호출 횟수: " << call_count << endl;
        } else {
            printf("실패!");
        }
    }

    return 0;
}
