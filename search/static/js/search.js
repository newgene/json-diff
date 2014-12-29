var data = new Object();        //post to tornado
//var result = new Object();      
var nowpage = 1;                //current page

//click query button to search and display the result in webpage

$(document).ready(function(){
    $("#search").click(function(){
        var posstart = document.getElementById("posstart").value;
        var posend = document.getElementById("posend").value;
        var chr = $("#genechr").val();
        var vartype = $("#vartype").val();
        var pagesize = $("#items_per_page").val();

        var let_num = /^([A-Za-z0-9])+$/;    //letter and number
        var number = /^([\0-9])+$/;          //only number

        if (posstart){
            check_posstart = number.test(posstart);
            if (check_posstart){
                data['posstart']=posstart;
                }else{
                data['posstart']="-1";
                }
        }else{data['posstart']='-1';}
        
        if (posend){
            check_posend = number.test(posend);
            if (check_posstart){
                data['posend']=posend;
                }else{
                data['posend']='-1';
                }
        }else{data['posend']='-1';}
        
        if (vartype != '0'){
            data['vartype']=vartype;
        }else{
            data['vartype']='-1';
        }

        data['chr'] = chr;
        data['pagesize'] = pagesize;
        data['nowpage'] = '1';
        data['format'] = 'table';
        data['bysort'] = 'pos';
    
        $.post("/", {"data":JSON.stringify(data)}, function(e){
            if (e!="0"){
                var back_data = eval('(' + e + ')');
                var cur_page = back_data['currentpage'];
                //result = {};
                //result[Number(cur_page)] = back_data;
                if (back_data['counts']==" "){
                    no_values();
                }else{
                    table_result(back_data,Number(pagesize));
                    $('#tableandjson').html("<input id='getjson' style='margin-left:2em;width:16em' class='pure-button pure-button-primary' onclick='getJson()' value='Click here to get JSON' type='button'>");
                }
            }else{
                no_values();
                }
        });
    })
})

//query nothing, then do this

function no_values(){
    $('#Searchresult').html("<div><h2 class='post-title'>Opps, the data you want was not found.</h2></div>");    
    $('#tableandjson').html(" ");
}

//display the result of query in web

function table_result(data,pagesize){
    var total_lines = data['counts'];
    var total_pages = data['pages'];
    var results = data['value'];
    var current_page = data['currentpage'];
    var new_table = "<div class='post-description'><table style='width:100%;table-layout:fixed;' class='pure-table'><thead><tr><th style='width:4em;'>chr</th><th style='width:7em; cursor:pointer' onclick='javascript:sortCol(1)'>pos</th><th style='width:6em; cursor:pointer' onclick='javascript:sortCol(2)'>vartype</th><th style='cursor:pointer' onclick='javascript:sortCol(3)'>ref</th><th style='cursor:pointer' onclick='javascript:sortCol(4)'>genotypes</th><th style='cursor:pointer' onclick='javascript:sortCol(5)'>genotype_freqs</th><th style='cursor:pointer' onclick='javascript:sortCol(6)'>allele_freqs</th></tr></thead><tbody>";
    
    if (Number(total_pages)==1){
        title_html = "<div><div class='content-subhead'><span class='post-meta'>TOTAL LINES:"+total_lines+"&nbsp;&nbsp;TOTAL PAGES:"+total_pages+"</span></div>"
        }
    else if (Number(current_page)==1 && Number(total_pages)>1){
        title_html = "<div><div class='content-subhead'><input type='button' class='post-category' value='Next Page' onclick='nextPage()'>&nbsp;&nbsp;&nbsp;<span class='post-meta'>TOTAL LINES:"+total_lines+"&nbsp;&nbsp;TOTAL PAGES:"+total_pages+"</span></div>"
        }
    else if (Number(current_page)<Number(total_pages)){
        title_html = "<div><div class='content-subhead'><input type='button' class='post-category' value='Prev Page' onclick='prevPage()'>&nbsp;&nbsp;<input type='button' class='post-category' value='Next Page' onclick='nextPage()'>&nbsp;&nbsp;&nbsp;<span class='post-meta'>TOTAL LINES: "+total_lines+"&nbsp;&nbsp;TOTAL PAGES: "+total_pages+"</span></div>"
        }
    else if (Number(current_page)==Number(total_pages)){
        title_html = "<div><div class='content-subhead'><input type='button' class='post-category' value='Prev Page' onclick='prevPage()'>&nbsp;&nbsp;&nbsp;<span>TOTAL LINES: "+total_lines+"&nbsp;&nbsp;TOTAL PAGES: "+total_pages+"</span></div>"
        }
    else{
        title_html = "<div><div class='content-subhead'>There is No Data. Maybe it has some bugs.</div>"
        }
    
    circle_num = rangePage(current_page,total_lines,total_pages,pagesize)
    for (var i=0; i<circle_num; i++ ){
        if (i%2!=0){
            new_tr = "<tr class='pure-table-odd'><td>"+results[i]['chr']+"</td><td>"+results[i]['pos']+"</td><td>"+results[i]['vartype']+"</td><td>"+wordBreak(results[i]['ref'])+"</td><td>"+genotypes(results[i]['genotypes'])+"</td><td>"+freqs(results[i]['genotype_freqs'])+"</td><td>"+freqs(results[i]['allele_freqs'])+"</td></tr>";
            new_table += new_tr;
            }else{
            new_tr ="<tr><td>"+results[i]['chr']+"</td><td>"+results[i]['pos']+"</td><td>"+results[i]['vartype']+"</td><td>"+wordBreak(results[i]['ref'])+"</td><td>"+genotypes(results[i]['genotypes'])+"</td><td>"+freqs(results[i]['genotype_freqs'])+"</td><td>"+freqs(results[i]['allele_freqs'])+"</td></tr>";
            new_table += new_tr;
                }
        }
        new_table +="</tbody></table></div></div>"
    $('#Searchresult').html(title_html+new_table);
}

//the values of genotypes filed: key:len(values)

function genotypes(data_object){
    var geno_result = "";
    for(var key in data_object){
        geno_result += wordBreak(key) + ": " + data_object[key].length + "<br>";
        }
    return geno_result;
    }

//the values of genotype_freqs and allele_freqs, and the decimal is less 4, and the letter of one line less 10

function freqs(data_object){
    var freqs_result = "";
    for (var key in data_object){
        freqs_result += wordBreak(key) + ": " + changeDecimal(data_object[key],4) + "<br>";
        }
    return freqs_result;
    }

//in one page, the range of lines

function rangePage(current_page,total_lines,total_pages,page_size){
    if (Number(current_page)<Number(total_pages)){
        return Number(page_size);
        }
    if (Number(current_page)==Number(total_pages)){
        var range_line = Number(total_lines) - Number(page_size)*(Number(current_page)-1);
        return range_line;
        }
}

//if the letter is more than 10, then break and turn to next line

function wordBreak(word_string){
    var breaked = '';
    var word_length = word_string.length;
    if (word_length<11){
        return word_string;
    }else{
        var n = parseInt(word_length/10);
        var poi = 0;
        for(var i=0; i<n; i++){
            breaked += word_string.substr(poi,10) +"<br>";
            poi +=10;
        }
        breaked += word_string.substr(poi);
        return breaked;
    }
}

//The argument('num_string') is a decimal or not, if is, then return it and less 'n' of its decimal

function changeDecimal(num_string,n){  //n is the length of decimal, 3.14=>n=2
    if (String(num_string).indexOf(".")>-1){
        var decimal_string = String(num_string).split(".")[1];
        var decimal_length = decimal_string.length;
        if (decimal_length>n){
            return parseFloat(num_string).toFixed(n);
        }else{
            return num_string;
        }
    }else{
        return num_string;
    }
}

//next page

function nextPage(){
    var pagesize = data['pagesize'];
    nowpage += 1;
//    if (nowpage in result){
//        table_result(result[nowpage], Number(pagesize));
//    }else{
    data['nowpage'] = nowpage.toString();
    $.post("/", {"data":JSON.stringify(data)}, function(e){
        if (e!="0"){
            var back_data = eval('(' + e + ')');
            //var cur_page = back_data['currentpage'];
            //result[Number(cur_page)] = back_data;
            if (back_data['counts']==" "){
                no_values();
            }else{
                table_result(back_data,Number(pagesize));
            }

        }else{
            no_values();
            }
        });
    //}
}

//prev page

function prevPage(){
    nowpage -= 1;
    var pagesize = data['pagesize']
    data['nowpage'] = nowpage.toString();
    //var back_data = result[nowpage];
    $.post("/", {"data":JSON.stringify(data)}, function(e){
        if(e != "0"){
            var back_data = eval('(' + e + ')');
            if (back_data['counts']==" "){
                no_values();
            }else{
                table_result(back_data,Number(pagesize));
            }
        }else{no_values();}
    });
    //table_result(back_data,Number(data['pagesize']));
}

//change the iterms per page, then return the call in webpage

$(document).ready(function(){
    $("#items_per_page").change(function(){
        if (not_empty(data) && data['format']=="table"){
            pagesize = $(this).children('option:selected').val();
            data['pagesize'] = pagesize;
            data['nowpage'] = '1';
            $.post("/", {"data":JSON.stringify(data)}, function(e){
                if (e!="0"){
                    var back_data = eval('(' + e + ')');
                    //var cur_page = back_data['currentpage'];
                    //result = {};
                    //result[Number(cur_page)] = back_data;
                    if (back_data['counts']==" "){
                        no_values();
                    }else{
                        table_result(back_data,Number(pagesize));
                    }

                }else{
                    no_values();
                    }
            });
        }
        });
    });

//judge an object is empty or not

function not_empty(obj){
    for (var name in obj){
        return true;
        }
    return false;
    };

//return the Json of result

function getJson(){
    data['format'] = 'json';
    $.post("/", {"data":JSON.stringify(data)}, function(e){
        if (e!="0"){
            document.write(e);
        }
        else{
            no_values();
        }
    });
}



function backTable(){
        var back_data = result[nowpage];
        var pagesize = back_data['pagesize'];
        table_result(back_data,Number(pagesize));
        $('#tableandjson').html("<input id='getjson' style='margin-left:2em;width:16em' class='pure-button pure-button-primary' onclick='getJson()' value='Click here to get Json' type='button'>");
}

function sortCol(n){
    var title = document.getElementsByTagName('th')[n].innerHTML ;
    data['bysort'] = title;
    data['nowpage'] = '1';
    $.post("/", {"data":JSON.stringify(data)}, function(e){
        if (e!="0"){
            var back_data = eval('(' + e + ')');
            if (back_data['counts']==" "){
                no_values();
            }else{
                var pagesize = data['pagesize'];
                table_result(back_data,Number(pagesize));
            }
        }else{
            no_values();
        }
    });
}
