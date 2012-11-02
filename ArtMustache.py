# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Art Mustache Templates for Python

~~~~~~~~~~~~~~~~~~~~~~~~~~~

Art Mustache is simple and it was designed as an easy to learn, compact and expressive template engine that enables a fluid coding workflow.

Art Mustache is not a new programming language itself, but uses native language(just like python) syntax for having code.

## know some simple rules ##

1. '@' is the magic character that precedes code instructions in the following contexts:
    1. '@' For a single code line/values:
        A single code line inside the markup:

        <p>Hello @variable</p>
    
    2. '@{...}' For a single code line/python code:
    
        @{my_name = 'I am art mustache.'}
    
    3. '@{...}' For code blocks with multiple lines:
    
        @{
            def say_hello(name):
                return 'hello %s' % name
            name = 'Hyson'
            
            say_hello(name)
            
            if name == 'Hyson':
                for n in ['hello',name]:
                    @:<li>@n</li> # @: syntax
            else:
                say_hello('world')
         
        }
    
    4. '@:' For single plain text to be rendered in '@{}' in template:
    
        @{
            for i in range(10):
                @:this is a single plain text,this is @i line.
        }
        
2. plain text or HTML markup can be included at any part of the code:

    It is no need to open or close code blocks to write HTML inside a page. If you want to add a code instruction inside HTML, you will need to use ‘@’ before the code:

    @if status == 1 {
        <span>Hello,what's are you doing?</span>
    }@elif status == 2 {
        <span>Hello guy,do you like a simple template engine?</span>
    }@else{
        <span>I am sorry to that.</span>
    }

    @for i in range(20){
        @if i % 2 {
            <li class="odd">@i</li>
        }@else{
            <li class="even">@i</li>
        }
    }

3. How to use Art Mustache

    tpl = '''
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
    @say_hello('world')
    '''
    t = ArtMustache(tpl)
    print t.render(
        name='Art Mustache',
        numbers=[1,2,3,4,5,6]
        )


:copyright: 2012 by Hyson Wu.

:license: MIT License.

"""
import re

class ArtMustache(object):

    def __init__(self, source):
        self.code = None
        self.parser(source)

    def parser(self, source, return_code=None):
        source_lines = []
        block_lines = []
        oneindent = ' '
        indention = 0

        def write(data, offset):
            source_lines.append(( oneindent * (indention - offset)) + data)

        def format_indent(data):
            space_num = 0
            deal_space_num = False
            new_lines = []
            current_indent = oneindent * indention

            for line in data.splitlines():
                if deal_space_num == False and line.strip():
                    space_num = len(line)-len(line.lstrip())
                    deal_space_num = True

                new_lines.append(current_indent+line[space_num:])
            return '\n'.join(new_lines)

        for token_type, data in self.tokenize(source):
            if token_type[0] == 0: # text
                if data:
                    write('__write(%r)' % data, 0)
            elif token_type[0] == 1: # variable in text
                if data:
                    write('__write_var(%s)' % data[1:], 0)
            elif token_type[0] == 2: # variable in python block code
                if data:
                    block_lines.append('$'+data+'$') # it will be proccess in python block code end
            elif token_type[0] == 3: # python control expression begin
                if data:
                    data = data[1:-1].replace('\r','').replace('\n','')
                    if data.endswith(':') == False:
                        data += ':'
                    write(data, 0)
                    indention += 1
            elif token_type[0] == 4: # python control expression end
                indention -= 1
            elif token_type[0] == 5: # python block code begin
                write('# block code begin', 0)
            elif token_type[0] == 6: # python block code end
                block_lines = ''.join(block_lines).splitlines()
                block_lines_num = len(block_lines)
                line_index = 0

                while line_index < block_lines_num:
                    if(block_lines[line_index].lstrip().startswith('@:')):

                        indent_num = len(block_lines[line_index])-len(block_lines[line_index].lstrip())
                        start_indent = block_lines[line_index][:indent_num]

                        f_line = block_lines[line_index].lstrip()[2:] # remove @: symbol
                        f_lines = [start_indent,"__write(''.join(map(str,('\\n',"]

                        for fl in f_line.split('$'):
                            if fl.startswith('@'): # if has variable
                                f_lines.append('__get_var(%s),' % fl[1:])
                            else:
                                f_lines.append("'%s'," % fl.replace("'","\\'"))
                        f_lines.append('))))')
                        block_lines[line_index] = ''.join(f_lines) # reset it with formated string

                    line_index += 1

                write(format_indent('\n'.join(block_lines)), indention)

                block_lines = []
                write('# block code end', 0)
            elif token_type[0] == 7: # data is python block code
                if data:
                    block_lines.append(data)
            elif token_type[0] == 8:
                write('# single block code begin', 0)
                write(data[2:-1], 0)
                write('# single block code end', 0)
        source = '\n'.join(source_lines)
        # print "*"*10+"following is python code"+"*"*10
        # print source
        self.code = compile(source, '<template>', 'exec')
        if return_code:
            return self.code

    def tokenize(self, source):
        vars_p = '\@{1}[\_a-zA-Z]{1}[\w\.\[\]\(\)\'\"\,]*'
        block_p = '\@{1}\{{1}'
        block_single_p = '\@{1}\{{1}[\ \w\.\,\[\]\(\)\<\>\=\!\'\"\+\-\*\/\%]+\}{1}'
        control_p = '\@{1}[a-z]+[\s\w\.\,\[\]\(\)\<\>\=\!\'\"\+\-\*\/\%\:]+\{{1}'
        end_p = '\}(?=\@)|\}$'

        tag_re = re.compile(r'(.*?)('+block_single_p+'|'+control_p+'|'+block_p+'|'+vars_p+'|'+end_p+')(?uism)')
        vars_re = re.compile(r'^'+vars_p+'$')
        block_re = re.compile(r'^'+block_p+'\s*$')
        block_single_re = re.compile(r'^'+block_single_p+'$')
        control_re = re.compile(r'^'+control_p+'$')
        end_re = re.compile(r'^'+end_p+'$')

        token_type  = (
            (0,'text'),
            (1,'variable in text'),
            (2,'variable in python block code'),
            (3,'python control expression begin'),
            (4,'python control expression end'),
            (5,'python block code begin'),
            (6,'python block code end'),
            (7,'data is python block code'),
            (8,'data is single python block code')
            )

        remove_newline = False
        data_is_block_code = False
        rest = ""
        counter = 0

        def syntax_error_line(source, error_start):
            symbol_num = 0
            line_num = 0
            for line in source.splitlines():
                line_num += 1
                symbol_num += len(line)
                if symbol_num >= error_start:
                    return line_num
                    
        for match in tag_re.finditer(source):
            data = match.group(1)
            tag = match.group(2).strip()

            # print '-'*10+'match begin'+'-'*10
            # print '<data %s data>' % data
            # print "<tag %s tag>" % tag

            is_end = (end_re.match(tag) != None and counter > 0)
            is_variable = (vars_re.match(tag) != None)
            is_block = (block_re.match(tag) != None)

            if remove_newline and data.startswith("\n"):
                data = data[1:] # remove \n symbol

            if data_is_block_code and is_block:
                raise SyntaxError('@{} syntax do not support nested! Please checks line %d in your template.' % syntax_error_line(source, match.start(2)))
            
            # block code is end
            # block code there is variable
            # block code there isn't variable
            if data_is_block_code and (is_end or is_variable or data.strip()): 
                yield token_type[7], data
            else:
                yield token_type[0], data

            remove_newline = False

            if block_single_re.match(tag):
                yield token_type[8], tag # data is single python block code
            elif is_variable:
                if data_is_block_code and is_end == False:
                    yield token_type[2], tag # variable in block code
                else:
                    yield token_type[1], tag # variable in text
            elif control_re.match(tag):
                remove_newline = True
                counter += 1
                yield token_type[3], tag # python control expression
            elif end_re.match(tag):
                remove_newline = True
                if counter > 0:
                    counter -= 1
                    if data_is_block_code:
                        data_is_block_code = False
                        yield token_type[6], tag # 'python block code end'
                    else:
                        yield token_type[4], tag # 'python control expression end'
                else:
                    yield token_type[0], tag # make } symbol as text

            elif is_block:
                counter += 1
                data_is_block_code = True
                yield token_type[5], tag # python block code begin 
            rest = source[match.end():]
        print '<rest is %s rest>' % rest
        if remove_newline and rest.startswith('\n'):
            rest = rest[1:]
        if rest:
            yield token_type[0], rest

    def get_variable(self, value):
        if isinstance(value, unicode):
            return value.encode('utf-8')
        elif not isinstance(value, str):
            return str(value)
        return value

    def render(self, *args, **kwargs):
        lines = []
        d = dict(*args, **kwargs)
        d['__write'] = lines.append
        d['__write_var'] = lambda x: lines.append(self.get_variable(x))
        d['__get_var'] = lambda x: self.get_variable(x)

        exec self.code in d
        return ''.join(lines)

def AM(source, *args, **kwargs):
    am = ArtMustache(source)
    if len(args) == 0 and len(kwargs) == 0:
        return am.render
    else:
        return am.render(args, kwargs)

def test():
    tpl = '''
       @name
    ~~~~~~~~~~~~~~~~~
    @{import re}
    @{my_name = 'hyson'}
    @{
        r = re.compile(r'\d+')
        @:output variable @r.sub('_','Hello12345art321mustache')!@#$%^&*()_+
        def say_hello(name):
            return 'hello'+str(name)
    }
    @def fun(name){
        @{
            s = 'hello ' + str(name)
            def fun2(vars):
                return '<b>'+str(vars)+'</b>'
        }
        <h1>@name</h1>
        <h1>@s</h1>
        <h1>@fun2(name)</h1>
    }
    @for i in numbers{
        <li>line @i</li>
        @{fun(i)}
    }
    @say_hello(my_name)
    @say_hello('world')
    <span> span</span>
    '''
    # t = ArtMustache(tpl)
    # print t.render(
    #     name='Art Mustache',
    #     numbers=[1,2,3,4,5,6]
    #     )
    t = AM(tpl)
    print t(
        name='Art Mustache',
        numbers=[1,2,3,4,5,6]
        )
if __name__ == '__main__':
    test()