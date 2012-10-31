Art Mustache
===========

##About ArtMustache

Art Mustache was designed as an easy to learn, compact and expressive template engine that enables a fluid coding workflow.

Art Mustache is not a new programming language itself, but uses native language(just like python) syntax for having code.

##ArtMustache Syntax

Before getting introduced to Art Mustache you should first know some simple rules that will help you understand how to write template with python in the same page:

1. '@' is the magic character that precedes code instructions in the following contexts:
    1. '@' For a single code line/values:
    A single code line inside the markup:
    ```html
    <p>Hello @variable</p>
    ```
    
    2. '@{...}' For a single code line/python code:
    ```html
    @{my_name = 'I am art mustache.'}
    @{status = True}
    @{my_name = 'art mustache' if status else 'no art mustache'}
    ```
    
    3. '@{...}' For code blocks with multiple lines:
    ```python
    @{
        def say_hello(name):
            return 'hello %s' % name
        name = 'Hyson'
        
        say_hello(name)
        
        if name == 'Hyson':
            for n in ['hello',name]:
                @:<li>@i</li> # @: syntax
        else:
            say_hello('you have no name.')
         
    }
    ```
    
    4. '@:' For single plain text to be rendered in '@{}' in the template
    
    ```python
    @{
        for i in range(10):
            @:this is a single plain text,this is @i line.
    }
    ```
2. plain text or HTML markup can be included at any part of the code:

It is no need to open or close code blocks to write HTML inside a page. If you want to add a code instruction inside HTML, you will need to use ‘@’ before the code:

```html
@{your_name = 'geeker'}

@def func(name){
    <h1>Hello @name</h1>
}

@{func2 = lambda x,y:x+y}

@if status == 1{
    <span>Hello,what's are you doing?</span>
}@elif status == 1{
    <span>Hello @your_name,do you like a simple template engine?</span>
}@else{
    <span>I am sorry to that.</span>
}

@for i in range(20){
    @if i % 2{
        <li class="odd">@i</li>
    }@else{
        <li class="even">@i</li>
    }
    @func('art mustache'+str(i))
}

@{index=0}

@while index<10{
    @if i % 2{
        <li class="odd">@i</li>
    }@else{
        <li class="even">@i</li>
    }
    @func('art mustache'+str(i))
}

@try{
    @{1+'a'}
}@except Exception as e{
    <span><b style="color:red"></b>@e</span>
}
```

3. How to use Art Mustache
```python
tpl = """
       @name
~~~~~~~~~~~~~~~~~
@{my_name = 'hyson'}
@{
    def say_hello(name):
        return 'hello'+str(name)
}
@for i in numbers{
    <li>line @i</li>
}
@say_hello(my_name)
@sya_hello('hello world')
"""
t = ArtMustache(tpl)
print t.render(
    name='Art Mustache',
    numbers=[1,2,3,4,5,6]
    )
```