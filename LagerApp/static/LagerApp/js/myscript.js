/**
 * Created by Ludwig on 2016-02-26.
 */


$(function(){

    var $main = $('div#main');

    /** Handles click-events on the navbar.
     * Switches "active" tab, fetches new content with ajax-call and applies it to #main,
     * pushes state to browser history and reapplies the datepicker
     * for the "new transactions" page.
     */
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

    /** Handles the home-button.
     *  Clears "active" from all tabs, fetches new content with ajax-call and applies it to #main
     */
    $('img#home_button').on('click', function(event){
        event.preventDefault();
        var $a = $(this).parent();
        $.get($a.attr('href'), function(data){
            $('div#main').html(data);
            window.history.pushState({'title': 'Home', 'href':$a.attr('href')}, 'Home', $a.attr('href'));
        });
        $('ul.navbar-nav li').removeClass('active');
    });

    /** Handles the back-button functionality of the browser
     * Fetches previous state and calls corresponding route
     * with an ajax-call and applies response to #main
     * @param event
     */
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
        $list.removeClass('active');
        $contains_title.parent().addClass('active');
    };

    /** Handles the pages of the "Transactions" table
     * Makes ajax GET call with information about sorting.
     * Finds this information through the current url
     */
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

    /**Clears the message from posting a new transaction when
     * the user changes any field in the form.
     */
    $main.on('change', 'form#add_form', function(){
        $('p.msg').hide();
    });

    /** Handles the sorting by column for "transactions" table.
     * Fetches data with ajax-call and applies it to #main.
     */
    $main.on('click', 'thead a', function(event){
        event.preventDefault();
        var $a = $(this);
        var url = $a.attr('href');
        $.get(url, function(data){
            $('div#main').html(data);
            window.history.pushState({'title': $a.text(), 'href':url}, $a.text(), url);
        });
    });


    /** Very bare-bones form validation.
     */
    $main.on('submit', 'form#add_form', function(event){
        var elements = this.elements;
        var $form = $(this);
        var msg = '';
        alert(elements.datepicker.value);
        if(elements.datepicker.value == ''){
            alert('in datepicker.value');
            event.preventDefault();
            msg = msg + 'Date is required';
        }
        if(elements.quantity == ''){
            event.preventDefault();
            msg = msg + 'Quantity is required';
        }
        $form.prepend('<p class=\"msg\">' + msg + '</p>');
    });


    /**Initializes the datepicker on page load
     */
    $.datepicker.setDefaults(
        $.extend( $.datepicker.regional[ 'swe' ] )
    );

    $( '#datepicker' ).datepicker({
          dateFormat: 'dd-mm-yy',
          onClose: function(dateText, inst) { $(this).attr("disabled", false); },
          beforeShow: function(dateText, inst) { $(this).attr("disabled", true); } }
    );

});

