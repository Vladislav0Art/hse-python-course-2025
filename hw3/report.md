# Report

## Task 3.1

1. The solution resides at [matrix.py](./tasks1-3/matrix.py).
2. Artifacts are at [artifacts/task1](./artifacts/task1).

## Task 3.2

1. The solution resides at [entity.py](./task2/entity.py) (implementation) and [test_entity.py](./task2/test_entity.py) (saving artifacts into txt-files).
2. Artifacts are at [artifacts/task2](./artifacts/task2).

## Task 3.3

1. The solution resides at [find_collision.py](./tasks1-3/find_collision.py) (it searches for a hash collision in `Matrix` class and saves the matrices with the required property (`(hash(A) == hash(C)) and (A != C) and (B == D) and (A @ B != C @ D)`) into files).
2. Additionally, see the implementation of [MatrixHashMixin](./tasks1-3/matrix.py) (it is a mixin for hash calculation; it maps a sum of `Matrix` elements into the field `Z_13` with some shift; the field is made of a smaller power, namely 13, to ease the collision search).
3. Artifacts reside at [artifacts/task3](./artifacts/task3).