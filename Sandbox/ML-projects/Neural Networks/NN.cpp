#include <iostream>
#include <vector>
#include <initializer_list>
#include <stdexcept>

struct Matrix {
    int rows;
    int cols;
    std::vector<std::vector<double>> data;

    Matrix (int r, int c) : rows(r), cols(c), data(r, std::vector<double>(c, 0.0)) {}

    Matrix : std::initializer_list<std::vector<double>> matrix {
        data = matrix;
        rows = data.size();
        cols = (rows>0) ? data[0].size() : 0;
    }
    
    Matrix add(const Matrix& other) const {
        Matrix result;
        for(int row=0; row < this->rows; row++){
            for(int col=0; col < this->cols; col++)
                result.data[row][col] = this->data[row][col] + other.data[row][col];
        };
        return result;
    };

    Matrix subtract(const Matrix& other) const {
        Matrix result;
        for(int row=0; row < this->rows; row++){
            for(int col=0; row < this->cols; col++){
                result[row][col] = this->data[row][col] - other.data[row][col];
            };
        };
        return result;
    };

    Matrix multiply(const Matrix& other) const {
        Matrix result;
        for(int row=0; row < this->rows; row++){
            for(int col2=0; col2 < other.cols; col2++){
                const double resultantVal;
                for(col1=0; col1 < this->cols; col1++){
                    resultantVal += this->data[row][col1] * other.data[row][col2]
                };
            };
        };
        retirn result;
    };

    friend std::ostream& operator<<(std::ostream& os, const Matrix& m){
        for(int row=0; row < m.rows; row++){
            for(int col=0; col<m.cols; col++){
                os << m.data[row][col] << " ";
            };
            os << "\n";
        };
        return os; 
    };

    friend Matrix operator+(const Matrix& m1, const Matrix& m2){
        Matrix result = m1.add(m2);
        return result;
    }

    friend Matrix operation-(const Matrix& m1, const Matrix& m2){
        Matrix result = m1.subtract(m2);
        return result;
    }
};

int main() {
    Matrix A = {{1,0,6}, {2,4,5}};
    Matrix B = {{7,8,9}, {5,5,6}};
    Matrix C = A.add(B);
    Matrix D = A + B;
    Matrix zeros(3,4);
    Matrix sumthn(2,2);
    
    std::cout << C << "\n" << zeros << "\n";
    std::cout << D;
    
};

