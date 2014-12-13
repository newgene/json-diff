$(document).ready(function(){
    $("#search").click(function(){
        var posstart = document.getElementById("posstart").value;
        var posend = document.getElementById("posend").value;
        var chr = $("#genechr").val();
        var vartype = $("#vartype").val();
        var ref = document.getElementById("generef").value;

        var let_num = /^([A-Za-z0-9])+$/;    //letter and number
        var number = /^([\0-9])+$/;    //only number

        var data = new Object();

        if (posstart){
            check_posstart = number.test(posstart);
            if (check_posstart){data.posstart=posstart;}else{
                $(".error").css('display','inline');
                document.getElementById("error").innerHTML="POS should be inter";
                }
        }
        if (posend){
            check_posend = number.test(posend);
            if (check_posstart){data.posend=posend;}else{
                $(".error").css('display','inline');
                document.getElementById("error").innerHTML="POS should be inter";
                }
        }
        if (chr != '0'){
            check_chr = let_num.test(chr);
            if (check_chr){data.chr=chr;}else{
                $(".error").css('display','inline');
                document.getElementById("error").innerHTML="CHR should be letter or inter";
                }
        }
        if (vartype != '0'){
            check_vartype = let_num.test(vartype);
            if (check_vartype){data.vartype=vartype;}else{
                $(".error").css('display','inline');
                document.getElementById("error").innerHTML="VARTYPE should be letter or inter";
                }
        }
        if (ref){
            check_ref = let_num.test(ref);
            if (check_ref){data.ref=ref;}else{
                $(".error").css('display','inline');
                document.getElementById("error").innerHTML="REF should be letter or inter";
                }
        }

        $.post( "/query", {"data":JSON.stringify(data)}, function( e ) {
            if (e!="0"){
                page = 1
                search_str = "?q="+JSON.stringify(data)+"&j="+e+"&p="+page;
                window.location.href="/search"+search_str;
            }else{
            $(".error").css("display","inline");
            document.getElementById("error").innerHTML="There is no data, please change condition."
            }
        });
    })

})

function nextPage(){
    url_search = window.location.search;
    search_lst = url_search.split("&");
    current_page = search_lst[2].split('=')[1];
    var page = new Number(current_page); 
    next_page = page + 1;
    search_str = search_lst[0]+"&"+search_lst[1]+"&p="+next_page;
    window.location.href="/search"+search_str;
}
function prePage(){
    url_search = window.location.search;
    search_lst = url_search.split("&");
    current_page = search_lst[2].split('=')[1];
    var page = new Number(current_page); 
    pre_page = page - 1;
    search_str = search_lst[0]+"&"+search_lst[1]+"&p="+pre_page;
    window.location.href="/search"+search_str;
}

