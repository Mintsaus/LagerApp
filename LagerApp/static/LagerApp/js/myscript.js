/**
 * Created by Ludwig on 2016-02-26.
 */

$(function(){
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
        $.get($a.attr('href'), function(data){
            $('div#main').html(data);
            window.history.pushState({'title': $a.text(), 'href':$a.attr('href')}, $a.text(), $a.attr('href'));
            if($.attr('href') == "/add/"){

                set_default_date();
            }
        });
    });

    $('img#home_button').on('click', function(event){
        event.preventDefault();
        $a = $(this).parent();
        $.get($a.attr('href'), function(data){
            $('div#main').html(data);
            window.history.pushState({'title': 'Home', 'href':$a.attr('href')}, 'Home', $a.attr('href'));
        });
        $('ul.navbar-nav li').removeClass('active');
    })

    window.onpopstate = function(event){
        $.get(event.state.href, function(data){
            $('div#main').html(data);
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

    $('#main').on('click', '.paginator', function(event){
        event.preventDefault();
        var $a = $(this);
        $.get($a.attr('href'), function(data){
            $('div#main').html(data);
            window.history.pushState({'title': $a.text(), 'href':$a.attr('href')}, $a.text(), $a.attr('href'));
        });
    });


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

