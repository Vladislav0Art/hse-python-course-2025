import os
from typing import Any, Generator

import numpy as np

from hw3.utils import create_artifacts_dir, save_at
from matrix import Matrix, save_matrix


def has_collision(a: Matrix, b: Matrix) -> bool:
    if a.shape != b.shape:
        raise ValueError("Matrices must have the same shape")
    return hash(a) == hash(b)


def generate_row(length: int, begin: int, end: int) -> Generator[list[int]]:
    """
    Generates all possible lists of given length with elements in the range [begin, end).
    :param length: Length of the list.
    :param begin: Start of the range (inclusive).
    :param end: End of the range (exclusive).
    :return: A generator yielding lists conforming to the specified constraints.
    """
    if length == 0:
        yield []
        return

    for value in range(begin, end):
        for tail in generate_row(length - 1, begin, end):
            yield [value] + tail


def main():
    length = 2
    begin = 1
    end = 10

    matrices: list[Matrix] = []

    for row1 in generate_row(length, begin, end):
        for row2 in generate_row(length, begin, end):
            matrix = Matrix(np.array([row1, row2]))
            matrices.append(matrix)

    A = None
    C = None
    found = False

    for a in matrices:
        if found: break
        for c in matrices:
            if found: break
            if a == c: continue
            if has_collision(a, c):
                print("Collision found:")
                print(f"hash={hash(a)}:")
                print(a)
                print()
                print(f"hash={hash(c)}:")
                print(c)
                A = a
                C = c
                found = True

    if not found:
        raise ValueError("No collisions found")

    B = None
    D = None
    for b in matrices:
        # B is just the same as D, so we only search for B
        if b != A and b != C and (A @ b != C @ b):
            # equivalent to `(B == D) and (A @ B != C @ D)`
            B = D = b
            break

    if B is None or D is None:
        raise ValueError("No B or D found")

    # save found matrices into txt-files
    artifacts_dir = create_artifacts_dir(dirname="task3")

    # save A, B, C, D
    save_matrix(A, artifacts_dir, "A.txt")
    save_matrix(B, artifacts_dir, "B.txt")
    save_matrix(C, artifacts_dir, "C.txt")
    save_matrix(D, artifacts_dir, "D.txt")

    # save products
    AB = A @ B
    CD = C @ D
    save_matrix(AB, artifacts_dir, "AB.txt")
    save_matrix(CD, artifacts_dir, "CD.txt")

    # save hash
    content = f"""A's hash: {hash(A)}
B's hash: {hash(B)}
C's hash: {hash(C)}
AB's hash: {hash(AB)}
CD's hash: {hash(CD)}
"""
    save_at(content, artifacts_dir, filename="hash.txt")

if __name__ == "__main__":
    main()