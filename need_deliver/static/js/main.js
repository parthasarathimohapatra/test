function CloseWithWindowOpenTrick() {
    var objWindow = window.open(location.href, "_self");
    objWindow.close();
}
function serverCall(url, data, method, loader, loaderClass, loaderId, fileUpload, cb, csrf_token) {
        if (fileUpload == null) {
            $.ajax({
                type: method,
                url: url,
                data: data,
                
                headers:{"X-CSRFToken": csrf_token},
                beforeSend: function () {
                    if (loader != null) {
                        $('.' + loaderClass).show();
                    }
                    if (loaderId != '') {
                        $('#' + loaderId).show();
                    }
                },
                success: function (res) { 
                    cb(res);
                },
                complete: function (xhr) {
                    if (xhr.readyState == 4) {
                        if (loader != null) {
                            $('.' + loaderClass).hide();
                        }
                        if (loaderId != '') {
                            $('#' + loaderId).hide();
                        }
                    }
                }
            });

        } else {
            $.ajax({
                type: method,
                url: url,
                data: data,
                headers:{"X-CSRFToken": csrf_token},
                contentType: false,
                cache: false,
                // dataType: "json",
                // contentType: "application/json",
                processData: false,
//                timeout: 100000,
//                tryCount: 0,
//                retryLimit: 1,
                beforeSend: function () {
                    if (loader != null) {
                        $('.' + loaderClass).show();
                    }
                    if (loaderId != '') {
                        $('#' + loaderId).show();
                    }
                },
//                error: function (xhr, status1) {
//                    if (xhr.status == 0) {
//                        this.tryCount++;
//                        if (this.tryCount <= this.retryLimit) {
//                            //try again
////                            $.ajax(this);
//                            return;
//                        } else {
//                            if (loader != null) {
//                                $('.' + loaderClass).hide();
//                            }
//                            if (loaderId != '') {
//                                $('#' + loaderId).hide();
//                            }
//                            //alert('Sorry! No internet connection available');
//                            cb(JSON.stringify({'status': false, 'msg': 'no net'}));
//                        }
//                    }
//                },
                success: function (res) {
//                    console.log(res);
                    cb(res);
                },
                complete: function (xhr) {
                    if (xhr.readyState == 4) {
                        if (loader != null) {
                            $('.' + loaderClass).hide();
                        }
                        if (loaderId != '') {
                            $('#' + loaderId).hide(); 
                        }
                    }
                }
            });
        }
    }


    function userAjaxCall(url, data, method, loader, loaderClass, buttonId, fileUpload, cb) {
        if (fileUpload == null) {
            $.ajax({
                type: method,
                url: url,
                data: data,
                
                // headers:{"X-CSRFToken": csrf_token},
                beforeSend: function () {
                    if (loader != null) {
                        $('.' + loaderClass).show();
                        $('#' + buttonId).hide();
                    }
                },
                success: function (res) { 
                    cb(res);
                },
                complete: function (xhr) {
                    if (xhr.readyState == 4) {
                        if (loader != null) {
                            $('.' + loaderClass).hide();
                            $('#' + buttonId).show();
                        }
                    }
                }
            });

        } 
    }

function forceNumber(element) {
  element
    .data("oldValue", '')
    .bind("paste", function(e) {
      var validNumber = /^[-]?\d+(\.\d{1,2})?$/;
      element.data('oldValue', element.val())
      setTimeout(function() {
        if (!validNumber.test(element.val()))
          element.val(element.data('oldValue'));
      }, 0);
    });
  element
    .keypress(function(event) {
      var text = $(this).val();
      if(event.which == 45) {
                return false;
            event.preventDefault();
        } 
      if ((event.which != 46 || text.indexOf('.') != -1) && //if the keypress is not a . or there is already a decimal point
        ((event.which < 48 || event.which > 57) && //and you try to enter something that isn't a number
          (event.which != 45 || (element[0].selectionStart != 0 || text.indexOf('-') != -1)) && //and the keypress is not a -, or the cursor is not at the beginning, or there is already a -
          (event.which != 0 && event.which != 8))) { //and the keypress is not a backspace or arrow key (in FF)
        event.preventDefault(); //cancel the keypress
      }

      if ((text.indexOf('.') != -1) && (text.substring(text.indexOf('.')).length > 2) && //if there is a decimal point, and there are more than two digits after the decimal point
        ((element[0].selectionStart - element[0].selectionEnd) == 0) && //and no part of the input is selected
        (element[0].selectionStart >= element.val().length - 2) && //and the cursor is to the right of the decimal point
        (event.which != 45 || (element[0].selectionStart != 0 || text.indexOf('-') != -1)) && //and the keypress is not a -, or the cursor is not at the beginning, or there is already a -
        (event.which != 0 && event.which != 8)) { //and the keypress is not a backspace or arrow key (in FF)
        event.preventDefault(); //cancel the keypress
      }
    });
}
function quantityChecker(e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        //display error message
        // $("#errmsg").html("Digits Only").show().fadeOut("slow");
               return false;
        // }
    }
}
function isNormalInteger(str) {
    return /^\+?(0|[1-9]\d*)$/.test(str);
}
$(function(){
    // $("body").on('keypress', '.quantity', function (e) {alert(e.which)
    //  //if the letter is not digit then display error and don't type anything
    //     if (e.which != 8 && e.which != 0 && (e.which < 46 || e.which > 57 )) {
    //     //display error message
    //            return false;
    //     }
    // });
    $(document).on("click", "#close-window", function(){
        var hash = window.location.hash;
        if(hash){
            CloseWithWindowOpenTrick();
        }
    });
    $("form").find('input,select,textarea').focusin(function(){
        $(this).parent().find('.error-input').show();
        
    });
    $("form").find('input,select,textarea').focusout(function(){
        $(this).parent().find('.error-input').hide();
        
    });
    $(".menu-left-btn").click(function(){
        $(this).parent().siblings().removeClass('active');
        $(this).parent('li').toggleClass('active');
    });
    $(document).on("keydown", '.price-input', function(){
         forceNumber($(".price-input"));
    } )
   $("body").on('keypress', '.positive-float-input',function (event) {
        value = $(this).val()
        if(value <0){
            return false;
            event.preventDefault();
        }
        if(event.which < 45 || event.which > 58 || event.which == 47 ) {
          return false;
            event.preventDefault();
        } // prevent if not number/dot

        if(event.which == 46 && value.indexOf('.') != -1) {
            return false;
            event.preventDefault();
        } // prevent if already dot
        if(event.which == 45) {
                return false;
            event.preventDefault();
        } 
        if(event.which == 45 && value.indexOf('-') != -1) {
                return false;
            event.preventDefault();
        } // prevent if already dot

        if(event.which == 45 && value.length>0) {
            event.preventDefault();
        } // prevent if already -

        return true;
    });
   $("body").on('keypress', '.float-input',function (event) {
        value = $(this).val()
        if(event.which < 45 || event.which > 58 || event.which == 47 ) {
          return false;
            event.preventDefault();
        } // prevent if not number/dot

        if(event.which == 46 && value.indexOf('.') != -1) {
            return false;
            event.preventDefault();
        } // prevent if already dot

            if(event.which == 45 && value.indexOf('-') != -1) {
                return false;
            event.preventDefault();
        } // prevent if already dot

        if(event.which == 45 && value.length>0) {
            event.preventDefault();
        } // prevent if already -

        return true;
    });
   $("body").on('keypress', '.positive-int-input',function (evt) {
       var charCode = (evt.which) ? evt.which : event.keyCode
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;

         return true;

   });
    // $('img').each(function(i, el){
    //     if (!$(this).is(":hidden")) { 
    //           $(this).after('<img width="50" height="50" src="https://diaxrbad0p1f6.cloudfront.net/static/images/big-img-loader.gif" />') // some preloaded "loading" image
    //                .hide()
    //                .attr('src',this.src)
    //                .one('load', function() {
    //                   $(this).fadeIn().next().remove();
    //           });
    //     }
    // });
   
})
function passwordRestrict(password){
    var regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$@!%&*?])[A-Za-z\d#$@!%&*?]{8,20}$/;
    if (!regex.test(password) && password != "") {
        return false;
    } else {
        return true;
    }
}

function emailRestrict(email){
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (!regex.test(email) && email!= '') {
        return false;
    } else {
        return true;
    }
}