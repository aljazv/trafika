function getBootstrapDeviceSize() {
      return $('#users-device-size').find('div:visible').first().attr('id');
    }

  function resize(){
    var size = getBootstrapDeviceSize();

    if (size == "xs" || size == "sm" || size == "md"){
      var nav = $('#sidenav');
      var main = $('#main');
      if (nav.hasClass('sidenav')){
        nav.removeClass('sidenav');
        main.removeClass('main');
        $(".card.p-3.mb-3.item-card").addClass("auto-m");
      }
    }

    else{
      var nav = $('#sidenav');
      var main = $('#main');
      if (! nav.hasClass('sidenav')){
        nav.addClass('sidenav');
        main.addClass('main')
        $(".card.p-3.mb-3.item-card").removeClass("auto-m");
      }
    }
  }

  function checkNum(el, e){

    e.preventDefault();

    val = el.siblings(":input[name='kolicina']").val()
    var isnum = /^\d+$/.test(val);

    if (! isnum){
      $("#warning-text").show();
    
      return;
    }

    $("#warning-text").hide();

    console.log(el.closest('form[name="change-val"]'));
    el.closest('form[name="change-val"]').submit();
  
  
  }


  function removeActive(){

    $(this).parent().parent()
    .find(':input[name="options"]').prop('checked', false)
    .parent().removeClass("active");

  }


  //dobi csrf kodo
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  //pripravi za avtomatsko posiljanje csfr
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
              // Only send the token to relative URLs i.e. locally.
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          }
      }

    });

  function myFunction() {
    var a = document.getElementById("search").value;

    window.location.href = a; 
  }


  function addToBasket(el, e){
    e.preventDefault();

    if (el.hasClass("disabled"))
      return;

    var inp = el.parent().parent().find(':input[name="options"]:checked');

    if (inp.length==0){
      inp = el.parent().parent().find(':input[name="kolicina"]');   
    }

    var isnum = /^\d+$/.test(inp.val());
    if (! isnum){
     
      $("#warning-text").show();
      return;
    }


    $("#warning-text").hide();

    var button= el;
    value = parseInt(inp.val());

    var data = {
        'id_izdelka': button.attr('id'),
        'kolicina' : value
    }

    $.ajax({
        "type": "POST",
        "dataType": "json",
        "url": "/",
        "data": data,
        "success": function(result) {
      
            button.text("Dodano")
            button.removeClass("btn-primary")
            button.addClass("btn-success disabled")

        },
        "error": function(result) {
            console.log(result);
        },
    });
};
  
  window.onresize = function() {
   
    resize();
  }

$(document).ready(function(){
  resize();
  $("#info-text").hide();
  $("#warning-text").hide();
  $(':input[name="kolicina"]').on("focus", removeActive);


  $(".dodaj").on('click', function(event){
    addToBasket($(this), event);
  }); 

}); 
