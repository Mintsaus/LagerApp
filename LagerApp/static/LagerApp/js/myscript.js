/**
 * Created by Ludwig on 2016-02-26.
 */
$(function(){
    $('#main').on('submit', function(e){
        e.preventDefault();
        var $form = $('#add_form');
        var data = $form.serialize();
        $.post($form.attr('action'), data, function(){
            alert("posted");
        });
    });

});