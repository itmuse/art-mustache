/**
art mustache for js

*/
;(function(){
	var cache = {};
	this.artMustache = function artMustache(str,data){
		var parser = function(source){

		},
		tokenize = function(source, yield){
			var 
	        tag_re = /([\s\S]*?)(\@{1}\{{1}[\s\w\.\,\[\]\(\)\<\>\=\!\'\"\+\-\*\/\%]+\}{1}|\@{1}[a-z]+[\s\w\.\,\[\]\(\)\<\>\=\!\'\"\+\-\*\/\%\:\;\&]+\{{1}|\@{1}\{{1}|\@{1}[\_a-zA-Z]{1}[\w\.\[\]\(\)\'\"\,]*|\}\@|\})/g,
	        vars_re = /^\@{1}[\_a-zA-Z]{1}[\w\.\[\]\(\)\'\"\,]*$/,//new RegExp(''+vars_p+'','gim'),
	        block_re = /^\@{1}\{{1}$/,//new RegExp('^'+block_p+'$','gim'),
	        block_single_re = /^\@{1}\{{1}[\ \w\.\,\[\]\(\)\<\>\=\!\'\"\+\-\*\/\%]+\}{1}$/,//new RegExp('^'+block_single_p+'$','gim'),
	        control_re = /^\@{1}[a-z]+[\s\w\.\,\[\]\(\)\<\>\=\!\'\"\+\-\*\/\%\:\;\&]+\{{1}$/,//new RegExp('^'+control_p+'$','gim'),
	        end_re = /[\}(?=\@)|\}]$/,//new RegExp('^'+end_p+'$','gim'),

	        token_type  = [
            [0,'text'],
            [1,'variable in text'],
            [2,'variable in javascript block code'],
            [3,'javascript control expression begin'],
            [4,'javascript control expression end'],
            [5,'javascript block code begin'],
            [6,'javascript block code end'],
            [7,'data is python block code'],
            [8,'data is single javascript block code']
            ],

            remove_newline = false,
	        data_is_block_code = false,
	        rest = "",
	        counter = 0;

	        function syntax_error_line(source,error_start){
	        	var symbol_num = 0,line_num = 0,
	        	lines = source.split('\n');
	        	for(var i=0;i<lines.length;i++){
	        		line_num += 1;
	        		symbol_num += n.length;
	        		if(symbol_num >= error_start){
	        			return line_num;
	        		}
	        	}
	        }

	        var data,tag;
	        var is_end,is_variable,is_block;
	        while (match = tag_re.exec(source)){
	        	console.log('-----------match begin------------');
	        	
	        	data = match[1];
	        	tag = match[2];
	        	yield('<data|'+match[1]+'|data>\n<tag|'+match[2]+'|tag>');

	        	is_end = end_re.test(tag) && counter > 0;
	        	is_variable = vars_re.test(tag);
	        	is_block = block_re.test(tag);

	        	if (remove_newline && data.indexOf('\n')==0){
	        		data = data.substring(1);
	        	}

	        	if (data_is_block_code && is_block){
	        		throw '@{} syntax do not support nested!';
	        	}

	        	if (data_is_block_code && (is_end || is_variable || data.trim().length>0)){
	        		yield(token_type[7], data);
	        	}else{
	        		yield(token_type[0], data);
	        	}

	        	remove_newline = false;

	        	console.log('<control_reg:'+control_re.test(tag)+'/>');

	        	if (block_single_re.test(tag)){
	        		yield(token_type[8], tag);
	        	}else if (is_variable){
	        		if (data_is_block_code && !is_end){
	        			yield(token_type[2], tag);
	        		}else{
	        			yield(token_type[1], tag);
	        		}
	        	}else if (control_re.test(tag)){
	        		remove_newline = true;
	        		counter += 1;
	        		yield(token_type[3],tag);
	        	}else if (end_re.test(tag)){
	        		remove_newline = true;
	        		if (counter > 0){
	        			counter -= 1;
	        			if(data_is_block_code){
	        				data_is_block_code = false;
	        				yield(token_type[6], tag);
	        			}else{
	        				yield(token_type[4], tag);
	        			}
	        		}else{
	        			yield(token_type[0],tag);
	        		}
	        	}else if (is_block){
	        		counter += 1;
	        		data_is_block_code = true;
	        		yield(token_type[5], tag);
	        	}else{
	        		yield(token_type[0], data);
	        	}
	        	// console.log('-----------------');
	        	// console.log(match);
	        	// rest = match[0];
	        }
	        console.log(111111);
	        if (remove_newline && rest.indexOf('\n')==0){
	        	rest = rest.substring(1);
	        }
	        if(rest.length > 0){
	        	yield(token_type[0], rest);
	        }

		},
		// fn = !/W/.test(str) ?
		// 	cache[str] = cache[str] ||
		// 	artMustache(document.getElementById(str).innerHTML):

		// 	new Function("obj","");
		fun = function(){};

		// return data ? fn(data) : fn;
		return tokenize;
	} 
})();