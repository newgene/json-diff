var data = new Object();        //post to tornado
var nowpage = 1;                //current page

$body = $("body");

//contruct the Object data 
function DataKeyValue(key, value, format){    //format is "number" or "letter"
    var letter_number = /^([A-Z-a-z0-9])+$/;
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
        }else{
            DataKeyValue('gene', '-1', 'number');
        }

        if (posstart){
            DataKeyValue('posstart', posstart, 'number');
        }else{
            DataKeyValue('posstart', '-1', 'number');
        }
        
        if (posend){
            DataKeyValue('posend', posend, 'number');
        }else{
            DataKeyValue('posend', '-1', 'number');
        }
        
        if (vartype != '0'){
            DataKeyValue('vartype', vartype, 'letter');
        }else{
            DataKeyValue('vartype', '-1', 'number');
        }

        data['pagesize'] = pagesize;
        data['nowpage'] = '1';
        nowpage = 1;
        data['format'] = 'table';
        data['bysort'] = 'chr,pos';
        
        if (posstart || posend){
            if (chr=="-1"){
                document.getElementById("chrerror").style.display='inline';
            }else{
                DataKeyValue('chr', chr, 'number');
                document.getElementById("chrerror").style.display='none';
                $body.addClass("loading");
                $.get("/search", {"data":JSON.stringify(data)}, function(e){
                    $body.removeClass("loading");
                    display_table(e, pagesize);
                });
            }
        }else{
            data['chr'] = chr;    
            document.getElementById("chrerror").style.display='none';
            $body.addClass("loading");
            $.get("/search", {"data":JSON.stringify(data)}, function(e){
                $body.removeClass("loading");
                display_table(e, pagesize);
            });
        }
    })
});

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
            + "<th style='width:5em; cursor:pointer;' onclick='javascript:sortCol(0)' >chr&nbsp;<img src='./static/images/up.png'></th>"
            + "<th style='cursor:pointer' onclick='javascript:sortCol(1)'>pos&nbsp;<img src='./static/images/up.png'></th>"
            + "<th style='cursor:pointer' onclick='javascript:sortCol(2)'>gene&nbsp;<img src='./static/images/up.png'></th>"
            + "<th style='width:7em;cursor:pointer' onclick='javascript:sortCol(3)'>vartype&nbsp;<img src='./static/images/up.png'></th>"
            + "<th style='width:4.5em;cursor:pointer' onclick='javascript:sortCol(4)'>ref&nbsp;<img src='./static/images/up.png'></th>"
            + "<th style='width:4.5em;cursor:pointer' onclick='javascript:sortCol(5)'>alt&nbsp;<img src='./static/images/up.png'></th>"
            + "<th style='width:9em'>genotypes</th>"
            + "<th>alleles</th>"
            + "<th style='color:blue; width:6em;'>OPTION</th>"
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
                + "<td style='word-break:break-all;word-wrap:break-word;'>"+display_array_element(results[i]['gene'],'<br>')+"</td>"
                + "<td>"+results[i]['vartype']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word'>"+results[i]['ref']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word'>"+results[i]['alt']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word;'>"+fgenotypes(results[i]['genotypes'], '<br>')+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word;'>"+falleles(results[i]['alleles'], '<br>')+"</td>"
                + "<td style='color:red;cursor:pointer' onclick='javascript:MoreGeneInfo("+JSON.stringify(results[i])+")'>More...</td>"
                + "</tr>";
            new_table += new_tr;
            }else{
            new_tr ="<tr>"
                + "<td>"+results[i]['chr']+"</td>"
                + "<td>"+results[i]['pos']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word;'>"+display_array_element(results[i]['gene'],'<br>')+"</td>"
                + "<td>"+results[i]['vartype']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word'>"+results[i]['ref']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word'>"+results[i]['alt']+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word'>"+fgenotypes(results[i]['genotypes'], '<br>')+"</td>"
                + "<td style='word-break:break-all;word-wrap:break-word;'>"+falleles(results[i]['alleles'], '<br>')+"</td>"
                + "<td style='color:green;cursor:pointer;' onclick='javascript:MoreGeneInfo("+JSON.stringify(results[i])+")'>More...</td>"
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
    var gene = display_array_element(gene_object["gene"], ","); // "RAP1GAP", 
    var vartype = gene_object['vartype'];  // "snp", 
    var genotypes = fgenotypes(gene_object['genotypes'], ', ');  // [{"count": 5,"freq": 0.025, "genotype": "T/C"}, {"count": 195, "freq": 0.975,"genotype": "T/T"}]
    var alleles = falleles(gene_object['alleles'], ', ');  // [{"allele": "C", "freq": 0.0125}, {"allele": "T", "freq": 0.9875 }]
    var protein_pos = display_array_element(gene_object['protein_pos'], ', ');  // ["694", "673", "635", "609"],
    var polyphen = display_array_element(gene_object['polyphen'], ', ');  //["possibly damaging", "probably damaging"], 
    var sift = display_array_element(gene_object['sift'], ', '); // "INTOLERANT", 
    var original_aa = display_array_element(gene_object['original_aa'], ', '); //"Y", 
    var alt = display_array_element(gene_object['alt'], ', ');  // "C", 
    var ref = display_array_element(gene_object["ref"], ', ');  // "T", 
    var allele_aa = display_array_element(gene_object["allele_aa"], ', ');  // "C", 
    var coding_impact = display_array_element(gene_object["coding_impact"], ', ');  // "Nonsynonymous"
    var splice_site_pred = display_array_element(gene_object["splice_site_prd"],', ');
    var adviser_score = display_array_element(gene_object["adviser_score"], ', ');
    var clinvar = display_array_element(gene_object['clinvar'], ', ');
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
                + "<tr><td>splice_site_pred</td><td>" + splice_site_pred + "</td></tr>"
                + "<tr><td>adviser_score</td><td>" + adviser_score + "</td></tr>"
                + "<tr><td>clinvar</td><td>" + clinvar + "</td></tr>"
                + "</table></div></div>";

    var pagei = $.layer({
           type: 1,   //0-4的选择,
           title: 'DETAIL->POS: ' + pos,
           offset: ['30px',''],
           border: [0],
           closeBtn: [1,true],
           shadeClose: true,
           area: ['600px', '770px'],
           page: {
                 html: innhtml
                 }
        });
}

//the values of genotypes filed: key:len(values)

function fgenotypes(data_arry, space_sign){
    if(typeof data_arry =='undefined'){
        return "";
    }else{
        var geno_result = "";
        for (var i=0; i<data_arry.length; ++i){
            geno_result += data_arry[i]['genotype'] +': ' + data_arry[i]['count'] + '(' + data_arry[i]['freq'].toFixed(2) + ')' + space_sign
        }
        return geno_result;
    }
}


function falleles(data_arry, space_sign){
    if(typeof data_arry =='undefined'){
        return "";
    }else{
        var geno_result = "";
        for (var i=0; i<data_arry.length; ++i){
            geno_result += data_arry[i]['allele'] +': ' + data_arry[i]['freq'].toFixed(3) + space_sign 
        }
        return geno_result;
    }
}

//display array or string in more layer
function display_array_element(data_arry, space_sign){
    if (typeof data_arry == 'undefined'){
        return "";
    }
    else if (data_arry.constructor==String){
        return data_arry;
    }
    else if (data_arry.constructor==Array){
        var data_result = "";
        for (var i=0; i<data_arry.length; ++i){
            data_result += data_arry[i] + space_sign;
        }
        return data_result;
    }
    else{
        return "";
    }
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


//next page

function nextPage(){
    var pagesize = data['pagesize'];
    nowpage += 1;
    data['nowpage'] = nowpage.toString();
    $body.addClass("loading");
    $.get("/search", {"data":JSON.stringify(data)}, function(e){
        $body.removeClass("loading");
        display_table(e, pagesize);
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
        display_table(e, pagesize);
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
                display_table(e, pagesize);
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
            }
        }else{
            no_values();
        }
    });
}

//get json: the url

function getJson(){
    var json_url = "http://myvariant.info/v1/" + getJsonUrl(data);
    window.location.href=json_url;
}


function getJsonUrl(content){
    var q = "query?q=_exists_:wellderly";
    
    var gene = content['gene'];
    var gene_chr = content['chr'];
    var posstart = content['posstart'];
    var posend = content['posend'];
    var vartype = content['vartype'];
    var sort_value = content['bysort'];

    var nowpage = Number(content['nowpage']);
    var pagesize = content['pagesize'];
    var start_page = String((nowpage-1)*Number(pagesize));

    if (gene != '-1'){
        q += " AND wellderly.gene:" + gene
    }

    if (gene_chr != '-1'){
        q += " AND wellderly.chr:" + gene_chr
    }

    if (posstart !="-1" && posend!='-1'){
        q += " AND wellderly.pos:[" + posstart + " TO " + posend +"]"
    }
    else if (posstart !='-1'){
        q += " AND wellderly.pos:" + posstart
    }
    else if (posend !='-1'){
        q += " AND wellderly.pos:" + posend
    }

    if (vartype != '-1'){
        q += " AND wellderly.vartype:" + vartype
    }

    q += "&fields=wellderly&from=" + start_page +"&size=" + pagesize

    if (sort_value.indexOf(",")>=0){
        var sort_lst = sort_value.split(',');
        var wsort_lst= new Array();
        for (var i=0; i<sort_lst.length; ++i){
            var wx = 'wellderly.' + sort_lst[i];
            wsort_lst.push(wx);
        }
        var sort_str = wsort_lst.join(',');
    }
    else{
        var sort_str = 'wellderly.' + sort_value;
    }
    
    q += "&sort=" + sort_str

    return q;
}
