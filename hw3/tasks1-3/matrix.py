import numpy as np
import os

from hw3.utils import save_at, create_artifacts_dir


class MatrixHashMixin:
    _HASH_FIELD_SIZE_MODULO = 13
    _HASH_MULT_COEF = 3
    _HASH_ADD_COEF = 5

    def __hash__(self) -> int:
        """
        calculate the hash using the formula (a * sum + b) % p
        where `sum` is the sum of all elements in the matrix, `a` and `b` are constants defined above.

        The resulting hash is a field element Z_p of power `_HASH_FIELD_SIZE_MODULO`.
        It makes it easier to find a collision.

        :return: hash value of the given matrix
        """
        if not isinstance(self, Matrix):
            raise TypeError(f"can only hash Matrix objects, received {type(self).__name__}")

        sum_ = sum(self.data.flat)
        return int((self._HASH_MULT_COEF * sum_ + self._HASH_ADD_COEF) % self._HASH_FIELD_SIZE_MODULO)


class Matrix(MatrixHashMixin):
    def __init__(self, data):
        """
        Args:
            data: 2D list or numpy array that represents matrix
        """
        if isinstance(data, list):
            self.data = np.array(data)
        elif isinstance(data, np.ndarray):
            self.data = data
        else:
            raise TypeError(f"list or numpy array expected, got {type(data).__name__}")

        if len(self.data.shape) != 2:
            raise ValueError("matrix must be 2-dimensional")

    @property
    def shape(self):
        """Returns matrix shape"""
        return self.data.shape

    def __str__(self):
        """Returns matrix string representation"""
        return str(self.data)

    def __repr__(self):
        """Returns matrix string representation."""
        return f"Matrix({self.data})"

    def __add__(self, other):
        """
        Implement matrix addition (A + B)
        Args:
            other: another Matrix object
        Returns:
            Matrix object representing result after summation
        Raises:
            ValueError: if matrices have different dimensions
            TypeError: if `other` is not `Matrix` object
        """
        if not isinstance(other, Matrix):
            raise TypeError(f"can only add another Matrix object, received {type(other).__name__}")

        if self.shape != other.shape:
            raise ValueError(f"cannot add matrices of shapes {self.shape} (this) and {other.shape} (other)")

        return Matrix(self.data + other.data)

    def __mul__(self, other):
        """
        Implement element-wise multiplication (A * B)
        Args:
            other: another Matrix
        Returns:
            Matrix object representing element-wise product
        Raises:
            ValueError: when matrices have different dimensions
            TypeError: when other is not `Matrix`
        """
        if not isinstance(other, Matrix):
            raise TypeError(f"can only multiply with another Matrix object, received {type(other).__name__}")

        if self.shape != other.shape:
            raise ValueError(f"cannot multiply element-wise matrices of shapes {self.shape} (this) and {other.shape} (other)")

        return Matrix(self.data * other.data)

    def __matmul__(self, other):
        """
        Implement matrix multiplication (A @ B)
        Args:
            other: another Matrix object.
        Returns:
            `Matrix` object representing matrix product
        Raises:
            ValueError: when matrices have incompatible dimensions for multiplication
            TypeError: when other is not Matrix
        """
        if not isinstance(other, Matrix):
            raise TypeError(f"can only matrix-multiply with another Matrix object, received {type(other).__name__}")

        if self.shape[1] != other.shape[0]:
            raise ValueError(f"cannot matrix-multiply matrices of shapes {self.shape} and {other.shape}")

        return Matrix(self.data @ other.data)


def save_matrix(m: Matrix, artifacts_dir: str, filename: str):
    """Saves matrix to a file."""
    save_at(content=str(m), artifacts_dir=artifacts_dir, filename=filename)


def main():
    np.random.seed(0)

    matrix_a = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix_b = Matrix(np.random.randint(0, 10, (10, 10)))

    print(f"Matrix A:\n{matrix_a}")
    print(f"Matrix B:\n{matrix_b}")

    addition_result = matrix_a + matrix_b
    element_wise_mult_result = matrix_a * matrix_b
    matrix_mult_result = matrix_a @ matrix_b

    # we dynamically store the result into artifacts folder, not to do it manually
    artifacts_dir = create_artifacts_dir(dirname="task1")

    # save matrices into files
    save_matrix(addition_result, artifacts_dir, "matrix+.txt")
    save_matrix(element_wise_mult_result, artifacts_dir, "matrix_mult.txt")
    save_matrix(matrix_mult_result, artifacts_dir, "matrix@.txt")

    print("Operations completed and results saved to text files.")


if __name__ == "__main__":
    main()