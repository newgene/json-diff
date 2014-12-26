var data = new Object();
var back_data = new Object();

$(document).ready(function(){
    $("#search").click(function(){
        var posstart = document.getElementById("posstart").value;
        var posend = document.getElementById("posend").value;
        var chr = $("#genechr").val();
        var vartype = $("#vartype").val();
        var pagesize = $("#items_per_page").val();

        var let_num = /^([A-Za-z0-9])+$/;    //letter and number
        var number = /^([\0-9])+$/;    //only number

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
                back_data = eval('(' + e + ')');
                if (back_data['counts']==" "){
                    no_values();
                }else{
                    table_result(back_data,Number(pagesize));
                    $('#tableandjson').html("<input id='getjson' style='margin-left:2em;width:16em' class='pure-button pure-button-primary' onclick='getJson()' value='Click here to get Json of this page' type='button'>");
                }

            }else{
                no_values();
                }
        });
    })
})

function no_values(){
    $('#Searchresult').html("<div><h2 class='post-title'>There is no data, change the conditions please.</h2></div>");    
    $('#tableandjson').html(" ");
}

function table_result(data,pagesize){
    var total_lines = data['counts'];
    var total_pages = data['pages'];
    var results = data['value'];
    var current_page = data['currentpage'];
    var new_table = "<div class='post-description'><table class='pure-table'><thead><tr><th>chr</th><th>pos</th><th>vartype</th><th>ref</th><th>genotypes</th><th>genotype_freqs</th><th>allele_freqs</th></tr></thead><tbody>";
    
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
            new_tr = "<tr class='pure-table-odd'><td>"+results[i]['chr']+"</td><td>"+results[i]['pos']+"</td><td>"+results[i]['vartype']+"</td><td>"+results[i]['ref']+"</td><td>"+genotypes(results[i]['genotypes'])+"</td><td>"+freqs(results[i]['genotype_freqs'])+"</td><td>"+freqs(results[i]['allele_freqs'])+"</td></tr>";
            new_table += new_tr;
            }else{
            new_tr ="<tr><td>"+results[i]['chr']+"</td><td>"+results[i]['pos']+"</td><td>"+results[i]['vartype']+"</td><td>"+results[i]['ref']+"</td><td>"+genotypes(results[i]['genotypes'])+"</td><td>"+freqs(results[i]['genotype_freqs'])+"</td><td>"+freqs(results[i]['allele_freqs'])+"</td></tr>";
            new_table += new_tr;
                }
        }
        new_table +="</tbody></table></div></div>"
    $('#Searchresult').html(title_html+new_table);
}

function genotypes(data_object){
    var result = "";
    for(var key in data_object){
        result += key + ": " + data_object[key].length + "<br>";
        }
    return result;
    }

function freqs(data_object){
    var result = "";
    for (var key in data_object){
        result += key + ": " + data_object[key] + "<br>";
        }
    return result;
    }

function rangePage(current_page,total_lines,total_pages,page_size){
    if (Number(current_page)<Number(total_pages)){
        return Number(page_size);
        }
    if (Number(current_page)==Number(total_pages)){
        var range_line = Number(total_lines) - Number(page_size)*(Number(current_page)-1);
        return range_line;
        }
}

function nextPage(){
    var pagesize = data['pagesize'];
    var nowpage = Number(data['nowpage'])+1;
    data['nowpage'] = nowpage.toString();
    $.post("/", {"data":JSON.stringify(data)}, function(e){
        if (e!="0"){
            var back_data = eval('(' + e + ')');
            alert(back_data['counts']);
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
function prevPage(){
    var pagesize = data['pagesize'];
    var nowpage = Number(data['nowpage'])-1;
    data['nowpage'] = nowpage.toString();
    $.post("/", {"data":JSON.stringify(data)}, function(e){
        if (e!="0"){
            var back_data = eval('(' + e + ')');
            alert(back_data['counts']);
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


$(document).ready(function(){
    $("#items_per_page").change(function(){
        if (not_empty(data) && data['format']=="table"){
            pagesize = $(this).children('option:selected').val();
            data['pagesize'] = pagesize;
            data['nowpage'] = '1';
            $.post("/", {"data":JSON.stringify(data)}, function(e){
                if (e!="0"){
                    var back_data = eval('(' + e + ')');
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



function not_empty(obj){
    for (var name in obj){
        return true;
        }
    return false;
    };


function getJson(){
        if (not_empty(data)){
            data['format'] = 'json';
            $.post("/", {"data":JSON.stringify(data)}, function(e){
                if (e != "0"){
                    disp_json = "<pre>"+e+"</pre>"
                    $('#Searchresult').html(disp_json);
                    $('#tableandjson').html("<input style='margin-left:2em;width:16em' class='pure-button pure-button-primary' onclick='backTable()' value='Go back TABLE' type='button'>");
                }else{
                    no_values();
                }
                });
        }
    }


function backTable(){
        pagesize = data['pagesize'];
        data['format'] = "table";
        table_result(back_data,Number(pagesize));
        $('#tableandjson').html("<input id='getjson' style='margin-left:2em;width:16em' class='pure-button pure-button-primary' onclick='getJson()' value='Click here to get Json of this page' type='button'>");
}
