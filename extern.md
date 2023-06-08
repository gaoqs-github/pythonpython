# extern简介

## 从codecheck看extern

```c++
"header.h"
#define NAMESPACE_SA_START namespace sa { 
#define NAMESPACE_SA_END } 
```

```C++
fileA.cc

#include "header.h"

NAMESPACE_SA_START
extern void func();
void func(){}

NAMESPACE_SA_END
```

```C++
fileB.cc

#include "header.h"

NAMESPACE_SA_START
    extern void print();
    void func(){
        sa::print();
    }
NAMESPACE_SA_END

int main() {
    sa::func();
    return 0;
}
```

编译命令：

g++ -c file_a.cpp -o file_a.o

g++ file_b.cpp -o a.out file_a.o

1. 从代码中看，文件B似乎也没有包含A，为什么能调用func？
2. 下面这几种改法行不行：

```C++
fileB.cc

#include "header.h"

//extern void func();
void use_func() {
    func();
}
```

```C++
fileB.cc

#include "header.h"

void func();
void use_func() {
    func();
}
```
fileB.cc中需要再次声明函数func的原因是因为fileB.cc与fileA.cc是两个独立的源文件，它们无法直接访问彼此的函数定义。尽管它们都包含了相同的命名空间sa，但是在C++中，命名空间无法跨越多个源文件共享定义。

因此，在fileB.cc中，如果要使用func函数，需要在fileB.cc中进行函数的声明。这样可以确保在fileB.cc的其他地方（例如main函数）可以正确地调用func函数。


```C++
fileB.cc

#include "header.h"
#include "fileA.cc"

void use_func() {
    func();
}
```
编译器在处理fileA.cc时会看到对函数func的定义，然后在处理fileB.cc时又看到了另一个对函数func的定义，这就导致了重定义错误。

这种错误是因为你在多个编译单元中都提供了相同名称的函数定义。在C++中，函数的定义只能在一个编译单元中存在，否则就会引起重定义错误。


如果对一个模板进行 extern 声明，意味着该模板不会在当前编译单元中被实例化。这是因为 extern 关键字用于指示编译器，该模板的实例化定义将在其他编译单元中提供。

在 C++ 中，模板的实例化是在使用模板的代码位置进行的。当编译器在某个编译单元中遇到模板的使用时，它会根据使用的具体类型实例化模板，并生成相应的代码。

然而，如果在当前编译单元中使用 extern 声明模板，编译器将不会在该编译单元中实例化模板。相反，编译器期望在其他编译单元中找到该模板的实例化定义。这样做的目的是将模板的实例化延迟到连接阶段，以便在整个程序的链接过程中解析模板的实例化定义。

需要注意的是，模板的声明和实例化定义必须在不同的编译单元中，以避免出现重复定义的错误。在模板的声明所在的编译单元中，使用 extern 关键字告诉编译器模板的实例化定义将在其他编译单元中提供。

这种方式常用于将模板的实现分离到独立的源文件中，以便在需要的时候进行实例化。这有助于减少编译时间和减少生成的目标代码的大小。

总而言之，使用 extern 关键字声明模板可以推迟模板的实例化定义，并将其留给链接阶段进行解析。这样可以提高编译效率和减少重复定义的错误。

当使用 extern 关键字声明模板时，通常需要将模板的声明和实例化定义分离到不同的编译单元中。这样做可以延迟模板的实例化，并将实例化的定义留给链接阶段处理。

下面是一个具体的示例：

假设我们有以下的头文件 mytemplate.h，其中包含一个简单的模板类 MyTemplate 的声明：

```C++
mytemplate.h
#ifndef MYTEMPLATE_H
#define MYTEMPLATE_H

template <typename T>
class MyTemplate {
public:
    void print(const T& value);
};

#endif  // MYTEMPLATE_H
```

然后，在一个源文件 mytemplate.cpp 中，我们提供了模板类 MyTemplate 的实例化定义：
```C++
mytemplate.cpp
#include "mytemplate.h"

template <typename T>
void MyTemplate<T>::print(const T& value) {
// 实现模板类的成员函数
// ...
}

// 显式实例化 MyTemplate<int> 类型
template class MyTemplate<int>;
```
在另一个源文件 main.cpp 中，我们使用了 extern 关键字来声明模板类 MyTemplate：

```C++
main.cpp
#include "mytemplate.h"

// 声明模板类 MyTemplate<int>
extern template class MyTemplate<int>;

int main() {
    MyTemplate<int> obj;
    obj.print(42);

    return 0;
}
```
在这个示例中，模板类 MyTemplate 的实例化定义被放在了 mytemplate.cpp 文件中，并通过 template class MyTemplate<int> 进行了显式实例化。

在 main.cpp 文件中，我们使用 extern 关键字声明了模板类 MyTemplate<int>，告诉编译器该实例化定义将在其他编译单元中提供。然后，我们在 main() 函数中使用 MyTemplate<int> 类型创建了对象，并调用了其中的成员函数。

通过这种方式，模板的实例化被推迟到链接阶段进行处理，以提高编译效率，并避免了重复定义的错误。

3. 为什么使用extern声明模板类不在mytemplate.cpp中呢？

使用 extern 声明模板类的目的是将模板的实例化定义推迟到其他编译单元中提供，以便在链接阶段解析。这种技术通常用于将模板的实现与声明分离，并将实例化的定义放在独立的源文件中。

在示例中，将模板类 MyTemplate 的实例化定义放在了 mytemplate.cpp 中的原因是为了展示模板的完整使用流程，并在同一个文件中提供模板的声明和实例化定义。

然而，在实际项目中，通常会将模板的声明放在头文件中，而将模板的实例化定义放在独立的源文件中，以便在需要时进行实例化。这种做法可以提高编译效率，并减少目标代码的大小。

下面是一个更符合实际项目结构的示例：

假设我们有以下的头文件 mytemplate.h，其中只包含模板类 MyTemplate 的声明：

```C++
// mytemplate.h
// 包含模板的实例化定义
#include "mytemplate_impl.h"

#ifndef MYTEMPLATE_H
#define MYTEMPLATE_H

template <typename T>
class MyTemplate {
public:
void print(const T& value);
};

#endif  // MYTEMPLATE_H
```

然后，在独立的源文件 mytemplate_impl.cpp 中，我们提供了模板类 MyTemplate 的实例化定义：

```C++
// mytemplate_impl.cpp
#include "mytemplate.h"

template <typename T>
void MyTemplate<T>::print(const T& value) {
// 实现模板类的成员函数
// ...
}

// 显式实例化 MyTemplate<int> 类型
template class MyTemplate<int>;
```


在这种结构下，我们可以在其他源文件中直接包含 mytemplate.h 头文件，并使用模板类 MyTemplate，而不需要再使用 extern 声明。
```C++
// main.cpp
#include "mytemplate.h"

int main() {
MyTemplate<int> obj;
    obj.print(42);
    return 0;
}
```

通过将模板的声明放在头文件中，可以使其他源文件能够访问和使用模板类。而将模板的实例化定义放在独立的源文件中，则可以避免重复定义，并在需要时进行显式实例化。

这种分离模板声明和实例化定义的方式可以提高编译效率，避免重复定义的错误，并使代码结构更清晰和可维护。
