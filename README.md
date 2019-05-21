# CompilationDatabase
Clang Compilation Database collections for deepin projects.

对于一些基于`clang`的静态检查工具一般都需要[Clang Compilation Database](https://clang.llvm.org/docs/JSONCompilationDatabase.html)才能正常工作，其中就包括`clazy`。所以，本项目主要用来收集deepin开源项目中基于C++/Qt项目的`compile_commands.josn`文件，以方便对相应的项目做静态检查（目前只有`clazy`）。

# 目录结构
- [db](./db) 目录用来存放各个项目的`compile_commands.json`文件；
- [clazy_enabled.json](./clazy_enabled.json) 文件中声明了需要进行clazy静态检查的项目；

# 使用方式

在使用上，主要分为两个方面，一方面是为项目生成`compile_commands.json`文件；另一方面是为项目启用`clazy`检查。

## 文件生成

使用项目[tools](./tools)目录中的`generate_db.py`生成项目的`compile_commands.json`文件，使用方式为：

```
./tools/generate_db.py path/to/project
```

会在`db`目录创建项目目录，并生成`compile_commands.json`文件。

NOTE: 目前工具支持`cmake`和`qmake`两种项目，`cmake`项目无需编译项目即可生成所需文件，但是`qmake`项目需要对项目进行构建。

工具依赖:

- qmake 
- cmake
- make
- bear

## 启用clazy检查

`jenkins`会根据`clazy_enabled.json`文件中的内容判断是否对相应的项目进行`clazy`检查，需要开启的项目修改`clazy_enabled.json`，增加相应项目即可。
