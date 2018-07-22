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

  function searchByTag() {
    var a = $("#search").val();

    if (a && a.length >=1)
      window.location.href = a;
    else
      $("#backToAll").submit();
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

function checkdate() {
        var text_datum = $(this).val();
        console.log(text_datum)
        var m = text_datum.match(/^\s*(3[01]|[12][0-9]|0?[1-9])\/(1[012]|0?[1-9])\/((?:19|20)\d{2})\s*$/g);

        if (m == null) {
            $(this)[0].setCustomValidity("Nepravilen vnos datuma");
        }
        else {
            $(this)[0].setCustomValidity(""); //more bit!
            split = text_datum.split('/');
            datum_tabela = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

            var stDni_meseca = datum_tabela[split[1] - 1];


            if (split[0] > stDni_meseca) {
                element.setCustomValidity("Nepravilen vnos datuma za ta mesec.");
                return
            }
            
        }
    }
  
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

  $( ".date-menu" ).on('input', checkdate );

  $(".date-menu").datepicker({
  firstDay: 1 ,
  dayNamesMin: [ 'Ne', 'Po', 'To', 'Sr', 'Če', 'Pe', 'So'],
   showOtherMonths: true,
    selectOtherMonths: true,
    dateFormat: 'dd/mm/yy'
  });

}); 
