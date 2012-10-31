handbook
========
* art mustache的语法架构非常简单，包括：
    * @variable
    * @expression{...}
    * @{...}
    * @:string
* @variable 是把变量生成到模板，可以在模板的任意语法结构中使用。列如：
    ```
    <span>@variable</span>
    ---
    @if True{
        <span>@variable</span>
    }
    ---
    @{
        @:<span>@variable</span>
    }
    ```
* 除了"@{...}"之外的其他所有语法，"{...}"内的所有内容都将会生成到模板，并且可以嵌套定义
"@expression{...}"的语法结构，并且可以无限制的使用"@variable"。

'@:'中使用'@variable'时，可以是一个变量，也可以是一个对象中的某个方法或者集合，如：
```
@{
    @:output variable,@obj.fun(var1,var2,var3)
    @:output variabel,@obj.names[10]
}
```
当调用对象的方法时，如果传入的参数是字符串，字符串内容只能是英文字母、数字、和下划线以及”,.[]()“的组合，不能包含其他特殊符号，但@:后面可以是任意字符的内容。