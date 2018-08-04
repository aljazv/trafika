function getBootstrapDeviceSize() {
      return $('#users-device-size').find('div:visible').first().attr('id');
    }

  function resize(){
    var size = getBootstrapDeviceSize();
    var nav = $('#sidenav');
    var main = $('#main');
    var logo = $('#logo-white');
    if (size == "xs" || size == "sm" || size == "md"){

      if (nav.hasClass('sidenav')){
        nav.removeClass('sidenav');
        main.removeClass('main');
        logo.removeClass('logo-expand')
        $(".card.p-3.mb-3.item-card").addClass("auto-m");
      }
    }

    else{

      if (! nav.hasClass('sidenav')){
        nav.addClass('sidenav');
        main.addClass('main')
        logo.addClass('logo-expand')
        $(".card.p-3.mb-3.item-card").removeClass("auto-m");
      }
    }
  }

  function checkNum(el, e){

    e.preventDefault();

    val = el.siblings(":input[name='kolicina']").val()
    var isnum = /^\d+$/.test(val);

    if (! isnum){
      $("#warning-text").addClass("show");
    
      return;
    }

    if ($("#warning-text").hasClass("show"))
      $("#warning-text").removeClass("show");


    if (el.data("min") > val){
      $("#warning-text2").text("Minimalna količina za ta izdelek je "+ el.data("min")+".")
      $("#warning-text2").addClass("show");
      return;
    }

    if ($("#warning-text2").hasClass("show"))
      $("#warning-text2").removeClass("show");


    var fname = el.data("form");
    $('form[name="'+fname+'"]').submit();
  
  
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


  function addToBasket(button, e){
    e.preventDefault();


    if ($("#danger-text").hasClass("show"))
      $("#danger-text").removeClass("show");

    if ($("#info-text").hasClass("show"))
      $("#info-text").removeClass("show");

    if (button.hasClass("disabled"))
      return;


    var itemId = button.attr('id');
    var inp = button.parent().parent().find(':input[name="group-'+itemId+'"]:checked');

    if (inp.length==0){
      inp = button.parent().parent().find(':input[name="kolicina"]');   
    }

    var isnum = /^\d+$/.test(inp.val());
    if (! isnum){
     
      $("#warning-text").addClass("show");
      return;
    }

    if ($("#warning-text").hasClass("show"))
      $("#warning-text").removeClass("show");

    value = parseInt(inp.val());

    if (button.data("min") > value ){
      $("#warning-text2").addClass("show");
      return;
    }

    if ($("#warning-text2").hasClass("show"))
      $("#warning-text2").removeClass("show");


    var data = {
        'id_izdelka': itemId,
        'kolicina' : value
    }

    $.ajax({
        "type": "POST",
        "dataType": "json",
        "url": "/",
        "data": data,
        "success": function(result) {
      
            button.text("Dodano")
            $("#group-"+itemId).addClass("disabled-buttons")

            $("#info-text").addClass("show");

        },
        "error": function(result) {
            $("#danger-text").addClass("show");
        },
    });
};


function showPerPage(){

  if ($("#danger-text").hasClass("show"))
    $("#danger-text").removeClass("show");

  data = {
    'perpage-select': $("#perpage-select").val()
  }
  $.ajax({
    "type": "POST",
    "dataType": "json",
    "url": "/session/",
    "data": data,
    "success": function(result) {
        location.reload();

    },
    "error": function(result) {
        $("#danger-text").addClass("show");
    },
});
}

function checkdate() {
    var text_datum = $(this).val();

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


function checkNumInOrder(el, e){
    e.preventDefault();

    if ($("#warning-text2").hasClass("show"))
      $("#warning-text2").removeClass("show");

    val = el.siblings(":input[name='kolicina']").val()
    var isnum = /^\d+$/.test(val);

    if (! isnum){

      $("#warning-text").addClass("show");
    
      return;
    }

    if ($("#warning-text").hasClass("show"))
      $("#warning-text").removeClass("show");


    if (el.data("min") > val){
      $("#warning-text2").text("Minimalna količina za ta izdelek je "+ el.data("min")+".")
      $("#warning-text2").addClass("show");
      return;
    }

    if ($("#warning-text2").hasClass("show"))
      $("#warning-text2").removeClass("show");


    var fname = el.data("form");
    $('form[name="'+fname+'"]').submit();
}

$(document).ready(function(){
  resize();

  $(':input[name="kolicina"]').on("focus", removeActive);

  $('#perpage-select').on("change", showPerPage);


  $('.obdelaj').on("click", function(event){
      event.preventDefault();
      var form = "#"+ $(this).data("form");

      $('#mainModal').modal("show");
      $('#mainModal button.ok').on("click", function(){
        $(form).submit();
        
      });
    
  });

  $(".dodaj").on('click', function(event){
    addToBasket($(this), event);
  }); 

  $(".spremeni_kolicino").on('click', function(event){
    checkNum($(this), event);
  }); 

  $(".spremeni_kolicino_admin").on('click', function(event){
    checkNumInOrder($(this), event);
  }); 

  $(".dodaj_izdelek_admin").on('click', function(event){
    checkNumInOrder($(this), event);
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
