#include <iostream>
#include <vector>
#include <initializer_list>
#include <stdexcept>
#include <sstream>

enum class MultType{
    Dot,
    Hadamard,
    outerprod
};

struct Matrix {
    int rows;
    int cols;
    std::vector<std::vector<double>> data;
    int shape[4];

    Matrix (int r, int c) : rows(r), cols(c), data(r, std::vector<double>(c, 0.0)) {}

    Matrix(std::initializer_list<std::vector<double>> matrix) {
        data = matrix;
        rows = data.size();
        cols = (rows>0) ? data[0].size() : 0;
        shape[0] = rows;
        shape[1] = cols;
    };
    
    Matrix add(const Matrix& other) const {
        if(this->rows != other.rows || this->cols != other.cols){
            std::stringstream ss;
            ss << "Matrix dimensions must match for addition! \n You gave dimensions (" << this->rows << "," << this->cols << ") + (" << other.rows << "," << other.cols << ")";
            throw std::invalid_argument(ss.str());
        }
        Matrix result(rows,cols);
        for(int row=0; row < this->rows; row++){
            for(int col=0; col < this->cols; col++)
                result.data[row][col] = this->data[row][col] + other.data[row][col];
        };
        return result;
    };

    Matrix subtract(const Matrix& other) const {
        Matrix result(rows,cols);
        for(int row=0; row < this->rows; row++){
            for(int col=0; col < this->cols; col++){
                result.data[row][col] = this->data[row][col] - other.data[row][col];
            };
        };
        return result;
    };

    Matrix multiply(const Matrix& other, bool IsScalar = false) const {
        if( IsScalar == false && (this->cols != other.rows)){
            std::stringstream ss;
            ss << "Dimensions are wrong for multiplication. \n, You did (" << this->rows << "," << this->cols << ") * (" << other.rows << "," << other.cols << ")";
            throw std::invalid_argument(ss.str());
        };
        if(IsScalar == false){
            Matrix result(this->rows,other.cols);
            for(int row1=0; row1 < this->rows; row1++){
                for(int col2=0; col2 < other.cols; col2++){
                    double resultantVal = 0.0;
                    for(int col1=0; col1 < this->cols; col1++){
                        resultantVal += this->data[row1][col1] * other.data[col1][col2];
                    };
                    result.data[row1][col2] = resultantVal;
                };
            };
        
            return result;
        } else {
            Matrix result(rows,cols);
            double scalar = other.data[0][0];

            for(int row1=0; row1<this->rows; row1++){
                for(int col1=0; col1<this->cols; col1++){
                    result.data[row1][col1] = this->data[row1][col1] * scalar;
                }
            }
            return result;
        }
    };

    Matrix hadamard(const Matrix& other){
        if(this->rows != other.rows || this->cols != other.cols){
            std::stringstream ss;
            ss << "Dimensions are wrong for hadamard product - They must be equal. \n, You did (" << this->rows << "," << this->cols << ") * (" << other.rows << "," << other.cols << ") - ";
            throw std::invalid_argument(ss.str());
        };
        
        Matrix result(this->rows, this->cols);
        for(int row=0; row<this->rows; row++){
            for(int col=0; col<this->cols; col++){
                result.data[row][col] = this->data[row][col] * other.data[row][col];
            }
        }
        return result;
    }

    Matrix multiplication(const Matrix& other, MultType type = MultType::Dot){}
                          
    //Matrix outerprod()

    Matrix T(){
        Matrix result(cols, rows);
        for(int row=0; row<this->rows; row++){
            for(int col=0; col<this->cols; col++){
                result.data[col][row] = this->data[row][col];
            }
        }
        return result;
    }

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

    friend Matrix operator-(const Matrix& m1, const Matrix& m2){
        Matrix result = m1.subtract(m2);
        return result;
    }

    friend Matrix operator*(const Matrix& m1, double scalar){
        Matrix scalarmtx = {{scalar}};
        Matrix result = m1.multiply(scalarmtx, true);
        return result;
    }

    friend Matrix operator*(double scalar, const Matrix& m1){
        Matrix scalarmtx = {{scalar}};
        Matrix result = m1.multiply(scalarmtx, true);
        return result;
    }

    friend Matrix operator*(const Matrix& m1, const Matrix& m2){
        Matrix result = m1.multiply(m2);
        return result;
    }
};

int main() {
    Matrix A = {{1,0,6}, {2,4,5}};
    Matrix B = {{7,8,9}, {5,5,6}};
    Matrix C = A.add(B);
    Matrix D = A + B;
    Matrix E = A*2;
    Matrix zeros(3,4);
    Matrix sumthn(2,2);

    Matrix m1 = {{0,1}, {1,0}};
    Matrix m2 = {{2,3}, {3,4}};
    
    std::cout << C << "\n" << zeros << "\n";
    std::cout << D << "\n";
    std::cout << "Normal :" << A;
    std::cout << "Multiplied" << E;
    std::cout << "Matrix Multiplied " << m1*m2;
    std::cout << "Transpose " << (m1*m2).T() << "\n";
    std::cout << A.T() << "\n";

    std::cout << B*(A.T()) << "\n";
    
};

