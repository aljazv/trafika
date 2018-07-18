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




  $(document).ready(function(){
    resize();
   $("#info-text").hide();

///verlic
    //http://coreymaynard.com/blog/performing-ajax-post-requests-in-django/
    // stvar deluje, poslje tudi ok csrf kodo, tako da se uporabnika avtenticira lahko

  $(".dodaj").click(function(e) {
          
          e.preventDefault();

          if ($(this).hasClass("disabled"))
            return;

          var inp = $(this).parent().parent().find(':input[name="kolicina"]');
          var button= $(this);
          console.log(inp)
          var data = {
              'id_izdelka': inp.attr('id'),
              'kolicina' : inp.val()
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
      });
  });

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
    console.log(a);
    window.location.href = a; 
    }
///verlic end


  window.onresize = function() {
   
    resize();
  }
