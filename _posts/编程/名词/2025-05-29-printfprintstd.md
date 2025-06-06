---
layout: article
title: Printf、Print、Std
date: 2025-05-29
created: 2025-05-25 13:16
tags: [编程,名词,printf、print、std]
---
# printf、print、std 用法与区别总结

---

## 一、printf（C语言的标准输出函数）

**用途**：格式化输出数据到终端  
**头文件**：`#include <stdio.h>`  
**语法**：
```c
int printf(const char *format, ...);
```
- `format`：格式字符串，可包含普通字符和格式说明符（如 `%d`, `%f`）。
- `...`：可变参数，按顺序与格式说明符对应。

**常用格式说明符**：
| 说明符   | 含义                       | 示例                         |
|----------|----------------------------|------------------------------|
| `%d`     | 十进制整数（int）          | `printf("%d", 42);`          |
| `%f`     | 浮点数（float/double）     | `printf("%.2f", 3.14);`      |
| `%s`     | 字符串（char*）            | `printf("%s", "Hello");`     |
| `%c`     | 单字符                     | `printf("%c", 'A');`         |
| `%x/%X`  | 十六进制整数               | `printf("%x", 255);`         |
| `%p`     | 指针                       | `printf("%p", ptr);`         |
| `%%`     | 输出`%`本身                | `printf("%%");`              |

**格式修饰符**（宽度/精度/对齐/前导零）：
```c
printf("%10d", 42);    // 宽度10，右对齐
printf("%-10d", 42);   // 宽度10，左对齐
printf("%05d", 42);    // 宽度5，前导零
printf("%.2f", 3.1415);// 浮点输出2位小数
```
---
## 二、std（C++标准库输入/输出流）

**用途**：C++标准库的输入/输出操作，包含丰富的容器、算法、字符串、智能指针等  
**头文件**：`#include <iostream>`, `#include <vector>`, `#include <string>` 等

**常见IO流对象**（见`<iostream>`头文件）：
- `std::cout`：标准输出（类似C的`printf`，但类型安全）
- `std::cin`：标准输入
- `std::cerr`：标准错误（无缓冲）
- `std::clog`：标准日志（有缓冲）

**输出语法**：
```cpp
#include <iostream>
int num = 10;
std::cout << "num = " << num << std::endl;
```

- `cout`：C++ 标准输出流对象，表示“输出到终端/控制台”。
- `<<`：插入运算符，把内容写到输出流里。
- `"key: "`：字符串常量，直接输出字面内容。
- `myKey`：你的变量，输出它当前的值。
- `", value: "`：字符串常量，输出这一段字面内容。
- `myValue`：你的变量，输出它当前的值。
- `endl`：表示输出一个换行，相当于“按下回车”。
**主要特点**：
- 使用流式操作符`<<`，类型安全，支持自定义类输出
- 支持链式输出和自动类型转换
- 可与容器、算法等配合使用

**C++标准库（std）其他常用功能**：
- 各类容器：`std::vector`, `std::map`, `std::set`等
- 字符串处理：`std::string`
- 算法库：`std::sort`, `std::find`等
- 智能指针：`std::unique_ptr`, `std::shared_ptr`
- 时间处理：`std::chrono`
- 数学函数：`std::sqrt`, `std::pow`
- 异常处理：`std::exception`, `std::runtime_error`

**优点**：
- 类型安全
- 可扩展（支持自定义类型的输出）
- 适合面向对象编程

---

## 三、print（Python的标准输出函数）

**用途**：向屏幕输出信息或将信息写入文件  
**语法**：
```python
print(*objects, sep=' ', end='\n', file=sys.stdout)
```
- 支持输出一个或多个对象，默认以空格分隔
- `sep`：自定义分隔符
- `end`：自定义结尾字符（默认换行`\n`）
- `file`：输出目标（默认是终端，可指定为文件）

**基本用法**：
```python
print('Hello, World!')
print('a', 'b', 'c', sep=', ')    # a, b, c
print('Done', end='!')            # Done!
```

**格式化输出**：
- 百分号格式化（与C语言类似）：
    ```python
    print('Name: %s, Score: %.2f' % ('Bob', 85.5))
    ```
- `str.format()`方法：
    ```python
    print('{} is {} years old.'.format('Alice', 20))
    ```
- f-string（推荐，Python3.6+）：
    ```python
    name = 'David'; age = 28
    print(f'{name} is {age} years old.')
    ```

**优点**：
- 简单易用，语法简洁
- 支持多种格式化方式
- 自动换行，可灵活控制分隔、结尾和输出目标

---

## 四、区别对比

| 对比项        | printf (C)                  | std::cout (C++/std库)       | print (Python)                  |
|---------------|----------------------------|-----------------------------|---------------------------------|
| 归属          | C标准库 `<stdio.h>`        | C++标准库 `<iostream>`      | Python内置                      |
| 格式化方式    | 格式字符串`%d/%f/...`      | 流操作符`<<`，类型安全      | `%`/`format()`/f-string         |
| 类型安全      | 否（参数和说明符必须严格匹配） | 是（编译器自动检查类型） | 是（自动类型转换）              |
| 输出多对象    | 需指定多个说明符            | 连续写`<<`即可             | 逗号分隔，自动加空格            |
| 扩展性        | 仅限标准类型                | 支持自定义类型的输出        | 支持任意对象                    |
| 控制输出目标  | 仅终端/文件（需`fprintf`）  | 可重定向，自定义流          | 通过`file`参数可输出到文件      |
| 语法简洁性    | 一般                       | 一般                        | 简单（尤其f-string）            |
| 主要适用范围  | C语言程序                  | C++程序（推荐）             | Python程序                      |
