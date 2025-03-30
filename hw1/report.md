# Report

Содержит результаты CLI работы утилит: nl_script.py, tail_script.py, and wc_script.py.

## 1. nl_script.py (1.1)

### Test Case 1: reading from a file
```bash
echo -e "Line 1\nLine 2\nLine 3\n\nLine 5" > test_file.txt
./hw1/nl_script.py test_file.txt
```
output:
```
     1	Line 1
     2	Line 2
     3	Line 3
     4	
     5	Line 5
```

### Test Case 2: reading from stdin
```bash
echo -e "Line 1\nLine 2\nLine 3" | ./hw1/nl_script.py
```
output:
```
     1	Line 1
     2	Line 2
     3	Line 3
```

### Test Case 3: file not found
```bash
./hw1/nl_script.py non_existent_file.txt
```
output:
```
non_existent_file.txt: No such file or directory
```

## 2. tail_script.py (1.2)

### Test Case 1: reading from a file
```bash
for i in {1..20}; do echo "Line $i" >> test_file_long.txt; done
./hw1/tail_script.py test_file_long.txt
```
output (последние 10 строк):
```
Line 11
Line 12
Line 13
Line 14
Line 15
Line 16
Line 17
Line 18
Line 19
Line 20
```

### Test Case 2: reading from many files
```bash
for i in {1..5}; do echo "File2 Line $i" >> test_file2.txt; done
./hw1/tail_script.py test_file_long.txt test_file2.txt
```
output:
```
==> test_file_long.txt <==
Line 11
Line 12
Line 13
Line 14
Line 15
Line 16
Line 17
Line 18
Line 19
Line 20

==> test_file2.txt <==
File2 Line 1
File2 Line 2
File2 Line 3
File2 Line 4
File2 Line 5
```

### Test Case 3: reading from stdin
```bash
for i in {1..20}; do echo "Line $i"; done | ./hw1/tail_script.py
```
output (последние 17 строк):
```
Line 4
Line 5
Line 6
Line 7
Line 8
Line 9
Line 10
Line 11
Line 12
Line 13
Line 14
Line 15
Line 16
Line 17
Line 18
Line 19
Line 20
```

### Test Case 4: file not found
```bash
./hw1/tail_script.py non_existent_file.txt
```
output:
```
cannot open 'non_existent_file.txt' for reading: No such file or directory
```

## 3. wc_script.py (1.3)

### Test Case 1: reading from file
```bash
./hw1/wc_script.py test_file_long.txt
```
output (формат: строки слова байты файл):
```
     20       40      151 test_file_long.txt
```

### Test Case 2: reading from many files
```bash
./hw1/wc_script.py test_file_long.txt test_file2.txt
```
output:
```
     20       40      151 test_file_long.txt
      5       15       65 test_file2.txt
     25       55      216 total
```

### Test Case 3: reading from stdin
```bash
echo -e "Line 1\nLine 2\nLine 3" | ./hw1/wc_script.py
```
output:
```
      3        6       21
```

### Test Case 4: file not found
```bash
./hw1/wc_script.py non_existent_file.txt
```
output:
```
non_existent_file.txt: No such file or directory
```

## Cleanup (удаляем файлы созданные все)
```bash
rm test_file.txt test_file_long.txt test_file2.txt
```
