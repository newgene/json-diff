var data = new Object();        //post to tornado
var nowpage = 1;                //current page

$body = $("body");
//click query button to search and display the result in webpage


//contruct the Object data 
function DataKeyValue(key, value, format){    //format is "number" or "letter"
    var letter_number = /^([A-Za-z0-9])+$/;
    var number = /^([\0-9])+$/;
    if (format == "number") {
        var check_value = number.test(value);
    }
    if (format == "letter") {
        var check_value = letter_number.test(value);
    }

    if (check_value){
        data[key] = value;
    }else{
        data[key] = '-1';
    }
}

//click query button to search as the condition, then display the result in webpage
$(document).ready(function(){
    $("#search").click(function(){
        var gene = document.getElementById("gene").value;
        var chr = $("#genechr").val();
        var posstart = document.getElementById("posstart").value;
        var posend = document.getElementById("posend").value;
        var vartype = $("#vartype").val();
        var pagesize = $("#items_per_page").val();

        if (gene){
            DataKeyValue('gene', gene.toUpperCase(), 'letter');
        }else{data['gene']='-1';}

        if (posstart){
            DataKeyValue('posstart', posstart, 'number');
        }else{data['posstart']='-1';}
        
        if (posend){
            DataKeyValue('posend', posend, 'number');
        }else{data['posend']='-1';}
        
        if (vartype != '0'){
            data['vartype']=vartype;
        }else{
            data['vartype']='-1';
        }

        if (posstart || posend){
            if (chr=="-1"){
                data['chr'] = '1';
                //alert("Please choose chr");
            }else{
            data['chr'] = chr;
            }
        }else{
            data['chr'] = chr;    
        }

        data['pagesize'] = pagesize;
        data['nowpage'] = '1';
        nowpage = 1;
        data['format'] = 'table';
        data['bysort'] = 'pos';
        
        $body.addClass("loading");
        $.get("/search", {"data":JSON.stringify(data)}, function(e){
            $body.removeClass("loading");
            display_table(e, pagesize);
        });
    })
})

//judge the return data and display table
function display_table(re_data, pagesize){            //'re_data' is the data from server
    if (re_data != '0'){
        var back_data = eval('(' + re_data + ')');
        var cur_page = back_data['currentpage'];
        if (back_data['counts']==" "){
            no_values();
        }
        else{
            table_result(back_data,Number(pagesize));
            $('#tableandjson').html("<a id='getjson' style='margin-left:2em;width:16em; cursor:pointer; color:white' onclick='getJson()'> Click here to get JSON </a>");
        }
    }
    else{
        no_values();
    } 
}


//query nothing, then do this

function no_values(){
    $('#Searchresult').html("<div><h2 class='post-title'>No variants match your query.</h2></div>");    
    $('#tableandjson').html(" ");
}

//display the result of query in web

function table_result(data,pagesize){
    var total_lines = data['counts'];
    var total_pages = data['pages'];
    var results = data['value'];
    var current_page = data['currentpage'];
    var new_table = "<div class='post-description'>"
        + "<table style='width:100%;table-layout:fixed;' class='pure-table'>"
        //+ "<table class='pure-table'>"
        + "<thead>"
        + "<tr>"
            + "<th style='width:4em'>chr</th>"
            + "<th style='cursor:pointer' onclick='javascript:sortCol(1)'>pos</th>"
            + "<th style='cursor:pointer' onclick='javascript:sortCol(2)'>vartype</th>"
            + "<th style='width:4em;cursor:pointer' onclick='javascript:sortCol(3)'>ref</th>"
            + "<th style='width:4em'>alt</th>"
            + "<th style='width:10em'>genotypes</th>"
            + "<th>alleles</th>"
            + "<th>gene</th>"
            + "<th style='color:blue; width:6em;'>OPTION</th>"
            //+ "<th>original_aa</th>"
            //+ "<th>allele_aa</th>"
            //+ "<th>protein_pos</th>"
            //+ "<th>coding_impact</th>"
            //+ "<th>poclyphen</th>"
            //+ "<th>sift</th>"
            //+ "<th>splice_site_pred</th>"
            //+ "<th>adviser_score</th>"
            //+ "<th>clinvar</th>"
        + "</tr>"
        + "</thead><tbody>";
    
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
            new_tr = "<tr class='pure-table-odd'>"
                + "<td>"+results[i]['chr']+"</td>"
                + "<td>"+results[i]['pos']+"</td>"
                + "<td>"+results[i]['vartype']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word'>"+results[i]['ref']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word'>"+results[i]['alt']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word;'>"+fgenotypes(results[i]['genotypes'])+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word;'>"+falleles(results[i]['alleles'])+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word;'>"+results[i]['gene']+"</td>"
                + "<td style='color:red;cursor:pointer' onclick='javascript:MoreGeneInfo("+JSON.stringify(results[i])+")'>More...</td>"
                //+ "<td>"+results[i]['original_aa']+"</td>"
                //+ "<td>"+results[i]['allele_aa']+"</td>"
                //+ "<td>"+display_arry_element(results[i]['protein_pos'])+"</td>"
                //+ "<td style='word-break:break-all;word-wrap:break-word;'>"+results[i]['coding_impact']+"</td>"
                //+ "<td style='word-break:break-all;word-wrap:break-word;'>"+display_arry_element(results[i]['polyphen'])+"</td>"
                //+ "<td style='word-break:break-all;word-wrap:break-word;'>"+results[i]['sift']+"</td>"
                //+ "<td style='word-break:break-all;word-wrap:break-word;'>"+freqs(results[i]['allele_freqs'])+"</td>"
                + "</tr>";
            new_table += new_tr;
            }else{
            new_tr ="<tr>"
                + "<td>"+results[i]['chr']+"</td>"
                + "<td>"+results[i]['pos']+"</td>"
                + "<td>"+results[i]['vartype']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word'>"+results[i]['ref']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word'>"+results[i]['alt']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word'>"+fgenotypes(results[i]['genotypes'])+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word;'>"+falleles(results[i]['alleles'])+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word;'>"+results[i]['gene']+"</td>"
                + "<td style='color:green;cursor:pointer;' onclick='javascript:MoreGeneInfo("+JSON.stringify(results[i])+")'>More...</td>"
                //+ "<td>"+results[i]['original_aa']+"</td>"
                //+ "<td>"+results[i]['allele_aa']+"</td>"
                //+ "<td>"+display_arry_element(results[i]['protein_pos'])+"</td>"
                //+ "<td style='word-break:break-all;word-wrap:break-word;'>"+results[i]['coding_impact']+"</td>"
                //+ "<td style='word-break:break-all;word-wrap:break-word;'>"+display_arry_element(results[i]['polyphen'])+"</td>"
                //+ "<td style='word-break:break-all;word-wrap:break-word;'>"+results[i]['sift']+"</td>"
                //+ "<td style='word-break:break-all;word-wrap:break-word;'>"+freqs(results[i]['allele_freqs'])+"</td>
                + "</tr>";
            new_table += new_tr;
                }
        }
        new_table +="</tbody></table></div></div>"
    $('#Searchresult').html(title_html+new_table);
}

function MoreGeneInfo(gene_object){
    var chr = gene_object['chr'];  //"1",
    var pos = gene_object['pos'];  //21924946
    var gene = gene_object["gene"]; // "RAP1GAP", 
    var vartype = gene_object['vartype'];  // "snp", 
    var genotypes = fgenotypes1(gene_object['genotypes']);  // [{"count": 5,"freq": 0.025, "genotype": "T/C"}, {"count": 195, "freq": 0.975,"genotype": "T/T"}]
    var alleles = falleles1(gene_object['alleles']);  // [{"allele": "C", "freq": 0.0125}, {"allele": "T", "freq": 0.9875 }]
    var protein_pos = display_arry_element1(gene_object['protein_pos']);  // ["694", "673", "635", "609"],
    var polyphen = display_arry_element1(gene_object['polyphen']);  //["possibly damaging", "probably damaging"], 
    var sift = judge_string(gene_object['sift']); // "INTOLERANT", 
    var original_aa = judge_string(gene_object['original_aa']); //"Y", 
    var alt = judge_string(gene_object['alt']);  // "C", 
    var ref = judge_string(gene_object["ref"]);  // "T", 
    var allele_aa = judge_string(gene_object["allele_aa"]);  // "C", 
    var coding_impact = judge_string(gene_object["coding_impact"]);  // "Nonsynonymous"

    var innhtml = "<div background-color:white; color:black;><div style='padding:10px;'><table class='pure-table pure-table-bordered'>"
                + "<tr><td>chr</td><td>" + chr + "</td></tr>"
                + "<tr><td>pos</td><td>" + pos + "</td></tr>"
                + "<tr><td>gene</td><td>" + gene + "</td></tr>"
                + "<tr><td>vartype</td><td>" + vartype + "</td></tr>"
                + "<tr><td>genotypes</td><td>" + genotypes + "</td></tr>"
                + "<tr><td>alleles</td><td>" + alleles + "</td></tr>"
                + "<tr><td>protein_pos</td><td>" + protein_pos + "</td></tr>"
                + "<tr><td>polyphen</td><td>" + polyphen + "</td></tr>"
                + "<tr><td>sift</td><td>" + sift + "</td></tr>"
                + "<tr><td>original_aa</td><td>" + original_aa + "</td></tr>"
                + "<tr><td>alt</td><td>" + alt + "</td></tr>"
                + "<tr><td>ref</td><td>" + ref + "</td></tr>"
                + "<tr><td>allele_aa</td><td>" + allele_aa + "</td></tr>"
                + "<tr><td>coding_impact</td><td>" + coding_impact + "</td></tr>"
                + "</table></div></div>";

    var pagei = $.layer({
           type: 1,   //0-4的选择,
           title: 'DETAIL->POS: ' + pos,
           offset: ['30px',''],
           border: [0],
           closeBtn: [1,true],
           shadeClose: true,
           area: ['460px', '650px'],
           page: {
                 html: innhtml
                 }
        });
}

//the values of genotypes filed: key:len(values)

function fgenotypes(data_arry){
    if(typeof data_arry =='undefined'){
        return "";
    }else{
        var geno_result = "";
        for (var i=0; i<data_arry.length; ++i){
            geno_result += data_arry[i]['genotype'] +': ' + data_arry[i]['count'] + '(' + data_arry[i]['freq'].toFixed(2) + ')<br> '
        }
        return geno_result;
    }
}

function fgenotypes1(data_arry){
    if(typeof data_arry =='undefined'){
        return "";
    }else{
        var geno_result = "";
        for (var i=0; i<data_arry.length; ++i){
            geno_result += data_arry[i]['genotype'] +': ' + data_arry[i]['count'] + '(' + data_arry[i]['freq'].toFixed(2) + '), '
        }
        return geno_result;
    }
}

function falleles(data_arry){
    if(typeof data_arry =='undefined'){
        return "";
    }else{
        var geno_result = "";
        for (var i=0; i<data_arry.length; ++i){
            geno_result += data_arry[i]['allele'] +': ' + data_arry[i]['freq'].toFixed(3) + '<br>'
        }
        return geno_result;
    }
}


function falleles1(data_arry){
    if(typeof data_arry =='undefined'){
        return "";
    }else{
        var geno_result = "";
        for (var i=0; i<data_arry.length; ++i){
            geno_result += data_arry[i]['allele'] +': ' + data_arry[i]['freq'].toFixed(3) + ', '
        }
        return geno_result;
    }
}

function display_arry_element(data_arry){
    if (typeof data_arry == 'undefined'){
        return "";
    }
    else{
        var data_result = "";
        for (var i=0; i<data_arry.length; ++i){
            data_result += data_arry[i] +",<br>"
        }
        return data_result;
    }
}

function display_arry_element1(data_arry){
    if (typeof data_arry == 'undefined'){
        return "";
    }
    else{
        var data_result = "";
        for (var i=0; i<data_arry.length; ++i){
            data_result += data_arry[i] +",  "
        }
        return data_result;
    }
}

function judge_string(data_string){
    if (typeof data_string == 'undefined'){
        return "";
    }else{
        return data_string;
    }
}
//the values of genotype_freqs and allele_freqs, and the decimal is less 4, and the letter of one line less 10

function freqs(data_object){
    var freqs_result = "";
    for (var key in data_object){
        freqs_result += key + ": " + changeDecimal(data_object[key],4) + "<br>";
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
    data['nowpage'] = nowpage.toString();
    $body.addClass("loading");
    $.get("/search", {"data":JSON.stringify(data)}, function(e){
        $body.removeClass("loading");
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

//prev page

function prevPage(){
    nowpage -= 1;
    var pagesize = data['pagesize']
    data['nowpage'] = nowpage.toString();
    $body.addClass("loading");
    $.get("/search", {"data":JSON.stringify(data)}, function(e){
        $body.removeClass("loading");
        if(e != "0"){
            var back_data = eval('(' + e + ')');
            if (back_data['counts']==" "){
                no_values();
            }else{
                table_result(back_data,Number(pagesize));
            }
        }else{no_values();}
    });
}

//change the iterms per page, then return the call in webpage

$(document).ready(function(){
    $("#items_per_page").change(function(){
        if (not_empty(data) && data['format']=="table"){
            pagesize = $(this).children('option:selected').val();
            data['pagesize'] = pagesize;
            data['nowpage'] = '1';
            nowpage = 1;
            $body.addClass("loading");
            $.get("/search", {"data":JSON.stringify(data)}, function(e){
                $body.removeClass("loading");
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
    window.location.href="/search?data="+JSON.stringify(data);
    //$.get("/search", {"data":JSON.stringify(data)}, function(e){
        //if (e!="0"){
        //    document.write(e);
        //}
        //else{
        //    no_values();
        //}
    //});
}

//sort by one title

function sortCol(n){
    var title = document.getElementsByTagName('th')[n].innerHTML ;
    data['bysort'] = title;
    data['nowpage'] = '1';
    nowpage = 1;
    $body.addClass("loading");
    $.get("/search", {"data":JSON.stringify(data)}, function(e){
        $body.removeClass("loading");
        if (e!="0"){
            var back_data = eval('(' + e + ')');
            if (back_data['counts']==" "){
                no_values();
            }else{
                var pagesize = data['pagesize'];
                table_result(back_data,Number(pagesize));
                var th = document.getElementsByTagName('th')[n];
                th.style.cssText="background-color: yellow"; 
                $("td").filter(":nth-child(" + (n+1) + ")").css("background-color", "#f3fca4");
                //var td = document.getElementsByTagName('td')[n];
                //td.style.cssText="background-color: #f3fca4";
            }
        }else{
            no_values();
        }
    });
}

