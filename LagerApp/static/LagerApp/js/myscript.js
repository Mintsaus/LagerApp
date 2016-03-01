/**
 * Created by Ludwig on 2016-02-26.
 */

var transactions_page;
var transactions_order_by;

$(function(){

    var $main = $('div#main');
    function set_default_date() {
        alert('set_date called');
        var $date = $('div#main form#add_form div#add_date');
        var now = new Date();
        $date.children('#add_year').children("option[value|=" + now.getFullYear() + "]").attr('selected', 'selected');
    }

    $('ul.navbar-nav').on('click', 'li a', function(event){
         event.preventDefault();
        var $a = $(this);
        var $li = $a.parent();
        $li.siblings().removeClass('active');
        $li.addClass('active');
        console.log(window.location.pathname);
        $.get($a.attr('href'), function(data){
            $('div#main').html(data);
            window.history.pushState({'title': $a.text(), 'href':$a.attr('href')}, $a.text(), $a.attr('href'));
            if(window.location.pathname == '/add/'){
                $( '#datepicker' ).datepicker({
                  dateFormat: 'dd-mm-yy',
                  onClose: function(dateText, inst) { $(this).attr("disabled", false); },
                  beforeShow: function(dateText, inst) { $(this).attr("disabled", true); }
                });
            }
        });
    });

    $('img#home_button').on('click', function(event){
        event.preventDefault();
        var $a = $(this).parent();
        $.get($a.attr('href'), function(data){
            $('div#main').html(data);
            window.history.pushState({'title': 'Home', 'href':$a.attr('href')}, 'Home', $a.attr('href'));
        });
        $('ul.navbar-nav li').removeClass('active');
    });

    window.onpopstate = function(event){
        $.get(event.state.href, function(data){
            $main.html(data);
        });

        var $list = $('ul.navbar-nav li');
        var $contains_title;
        var title = event.state.title;
        if(title === "Transactions"){
            $contains_title = $list.children('a:contains("Transactions")');
        }else if(title === "Saldo"){
            $contains_title = $list.children('a:contains("Saldo")');
        }else if(title === "New transaction"){
            $contains_title = $list.children('a:contains("New transaction")');
        }
        console.log($list);
        console.log($contains_title);
        $list.removeClass('active');
        $contains_title.parent().addClass('active');
    };

    $main.on('click', '.paginator', function(event){
        event.preventDefault();
        var $a = $(this);
        var curl = window.location.search;
        var order = '';
        var url;

        if(curl.includes('order_by') && curl.includes('page')){
            var oindex = curl.indexOf('order_by');
            var pindex = curl.indexOf('page');
            var aindex = curl.indexOf('&');
            if(oindex < pindex){
                order = curl.substring(oindex, (aindex-1));
            }else{
                order = curl.substring(oindex);
            }
            url = $a.attr('href') + '&' + order;
        }else if(curl.includes('order_by')){
            order = curl.substring(1);
            url = $a.attr('href') + '&' + order;
        }else{
            url = $a.attr('href');
        }

        $.get(url, function(data){
            $('div#main').html(data);
            window.history.pushState({'title': $a.text(), 'href':$a.attr('href')}, $a.text(), url);
        });
    });

    $main.on('change', 'form#add_form', function(){
        $('p.msg').hide();
    });

    $main.on('click', 'thead a', function(event){
        event.preventDefault();
        var $a = $(this);
        transactions_order_by = $a.attr('href');
        var url = $a.attr('href');
        $.get(url, function(data){
            $('div#main').html(data);
            window.history.pushState({'title': $a.text(), 'href':url}, $a.text(), url);
        });
    });

    $main.on('submit', 'form#add_form', function(event){
        elements = this.elements;
        var $form = $(this);
        if(elements.datepicker.value == ''){
            alert('connected' + elements.datepicker.value);
            event.preventDefault();
            $form.find("input[name='datepicker_msg']").removeClass('hidden').text("This field must be filled");
        }
        if(elements.quantity == ''){
            event.preventDefault();
            $form.find("input[name='datepicker_msg']").removeClass('hidden').text("This field must be filled");
        }
    });



    $.datepicker.setDefaults(
        $.extend( $.datepicker.regional[ 'swe' ] )
    );

    $( '#datepicker' ).datepicker({
          dateFormat: 'dd-mm-yy',
          onClose: function(dateText, inst) { $(this).attr("disabled", false); },
          beforeShow: function(dateText, inst) { $(this).attr("disabled", true); } }
    );




    /*
    $('#main').on('submit', function(e){
        e.preventDefault();
        alert('jquery in myscript');
        var $form = $('#add_form');
        var data = $form.serialize();
        $.post($form.attr('action'), data, function(){
            alert("posted");
        });
    });
*/
});

