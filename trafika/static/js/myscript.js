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
      }
    }

    else{
      var nav = $('#sidenav');
      var main = $('#main');
      if (! nav.hasClass('sidenav')){
        nav.addClass('sidenav');
        main.addClass('main')
      }
    }
  }




  $(document).ready(function(){
    resize();
   $("#info-text").hide();

///verlic
    //http://coreymaynard.com/blog/performing-ajax-post-requests-in-django/
    // stvar deluje, poslje tudi ok csrf kodo, tako da se uporabnika avtenticira lahko

  $("#post").click(function(e) {
          e.preventDefault();
          var data = {
              'id_izdelka': 1,
              'kolicina' : 25
          }

          
          $.ajax({
              "type": "POST",
              "dataType": "json",
              "url": "/1/",
              "data": data,
              "success": function(result) {
                  $("#info-text").show();
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
///verlic end


  window.onresize = function() {
   
    resize();
  }