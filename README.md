## Introduction
Python binding for C++ implementation of SORT: Simple, online, and real-time tracking of multiple objects in a video sequence.

Kuhn-Munkres (Hungarian) Algorithm in C++ is forked from:
https://github.com/saebyn/munkres-cpp

## Dependencies
- Ubuntu 16.04
- Docker 18.09.4
- OpenCV 3.4.2
- Boost 1.58.0
- Eigen 3.3.7
- pybind11
- scikit-build


## Usage 
```
git clone git@github.com:jenhaoyang/sort-cpp-pybind11.git
cd sort-cpp-pybind11
pip install .
```


# 安裝
pip install .

# 新增類別
在src/cppsort/__init__.py加入class的名稱

# 編譯(Ubuntu)
pip install .

# Windows 編譯whl debug(因為有些編譯器錯誤沒辦法完整顯示)
先切到windows分支 build-for-windows  或   tracking-with-confidence-and-class-id--windows
```bash
 python setup.py bdist_wheel --generator  "Visual Studio 16 2019"
```
# 測試

## References
1. https://github.com/abewley/sort
2. https://github.com/mcximing/sort-cpp
3. https://github.com/saebyn/munkres-cpp
4. https://github.com/yasenh/sort-cpp
