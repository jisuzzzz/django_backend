#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

class Sudoku {
public:
	int grid[9][9];
	int K;
	int N;

	Sudoku(int K) :N(9){
		this->K = K;
		for (int i = 0; i < 9; ++i)
			for (int j = 0; j < 9; ++j)
				grid[i][j] = 0;
	}

	void fillValues() {
		fillDiagonal();
		fillRemaining(0, 3);
		removeKDigits();
	}

	void fillDiagonal() {
		for (int i = 0; i < 9; i = i + 3)
			fillBox(i, i);
	}

	bool unUsedInBox(int rowStart, int colStart, int num) {
		for (int i = 0; i < 3; i++)
			for (int j = 0; j < 3; j++)
				if (grid[rowStart + i][colStart + j] == num)
					return false;
		return true;
	}

	void fillBox(int row, int col) {
		int num;
		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				do {
					num = randomGenerator(N);
				}
				while (!unUsedInBox(row, col, num));
				grid[row + i][col + j] = num;
			}
		}
	}

	int randomGenerator(int num) {
		return (rand() % num) + 1;
	}

	bool CheckIfSafe(int i, int j, int num) {
		return (unUsedInRow(i, num) && unUsedInCol(j, num) &&
			unUsedInBox(i - i % 3, j - j % 3, num));
	}

	bool unUsedInRow(int i, int num) {
		for (int j = 0; j < 9; j++)
			if (grid[i][j] == num)
				return false;
		return true;
	}

	bool unUsedInCol(int j, int num) {
		for (int i = 0; i < 9; i++)
			if (grid[i][j] == num)
				return false;
		return true;
	}

	bool fillRemaining(int i, int j) {
		if (i == 8 && j == 9)
			return true;

		if (j == 9) {
			i++;
			j = 0;
		}

		if (grid[i][j] != 0)
			return fillRemaining(i, j + 1);

		for (int num = 1; num <= 9; num++) {
			if (CheckIfSafe(i, j, num)) {
				grid[i][j] = num;
				if (fillRemaining(i, j + 1))
					return true;
			}
			grid[i][j] = 0;
		}
		return false;
	}

	void removeKDigits() {
		int count = K;
		while (count) {
			int cellId = randomGenerator(9 * 9) - 1;
			int i = (cellId / 9);
			int j = cellId % 9;

			if (grid[i][j] != 0) {
				count--;
				grid[i][j] = 0;
			}
		}
	}

	void printSudoku() {
		for (int i = 0; i < 9; i++) {
			for (int j = 0; j < 9; j++) {
				cout << grid[i][j] << " ";
			}
			cout << endl;
		}
	}
};

int main() {
	int K = 50;
	srand(time(0));
	Sudoku sudoku(K);
	sudoku.fillValues();
	sudoku.printSudoku();
	return 0;
}
