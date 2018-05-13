$(document).ready(function() {
    $('input[name=opt]').attr('checked', false);
    $('form#search').click(function() {
      $.getJSON('/search', {
        for: $('input').val()
      })
    });
    //  event.preventDefault()
  });