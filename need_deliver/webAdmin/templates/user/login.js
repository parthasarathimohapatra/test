$(document).ready(function () {
    $( "body" ).on("click", ".forgot-password-sign-in-btn", function(){
        $("#login-blk").toggle();
        $("#forgot-blk").toggle(); 
    });

    $('#loginForm').on('submit', function (e) {
        var thisVal = $(this);
        var uid = $("input[name=email_id]").val();
        var pwd = $("input[name=password]").val();
        var role = $("input[name=role]").val();
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
        var url =  "{{ settings.REST_URL }}" + "login";
        // var data = {'email_id': uid, 'password': pwd, 'role': role,'csrftoken':csrftoken};
        var data = {'email_id': uid, 'password': pwd, 'role': role};
        
        // userAjaxCall(url, (data), 'post', true, 'formloader', null, null, function (data) {
        serverCall(url, (data), 'post', true, 'formloader', null, null, function (data) {

            thisVal.find('[type=submit]').prop('disabled', false);
            if (data.length>0) {
                // var resp = $.parseJSON(data);alert(1);
                $.each(data, function(key, val){
                    $.each(val, function(key1, val1){

                        if(key1 == 'status' && val1 == true){
                            $("#loginForm").find('#msg-res-login').addClass('alert alert-success');
                            $('#loginForm').find('.formResponse').addClass('success-msg').html(data[key].msg);
                            setTimeout(function(){
                                window.location.href = "{{ settings.BASE_URL }}"  + '/dashboard';
                            },1000);
                        } else if(key1 == 'status' && val1 == false){
                            $( "#loginForm" ).find('.eq-ui-input').removeClass('eq-ui-input invalid');
                                $("#loginForm").find('#msg-res-login').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
                                $("#loginForm").find(".error-input").remove();               
                                 $("#loginForm").find('#msg-res-login').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
                            if( data[key].field != 'mainError'){
                                $('#loginForm').find('[name=' + data[key].field + ']').addClass('eq-ui-input invalid');
                                $('#loginForm').find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
                                $('#loginForm').find('input[name=' + data[key].field + ']').after("<span class='error-input'>" + data[key].msg + "</span>");
                            }else{
                                $("#loginForm").find('#msg-res-login').addClass('alert alert-danger');
                                $('#loginForm').find('.formResponse').addClass('error-msg').html(data[key].msg);

                            }
                        }
                    });    
                });
            }
           
        }, csrftoken);

        e.preventDefault();
    });
    $('#forgotPassForm').on('submit', function (e) {
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
        $("#forgotPassForm").find('.eq-ui-input').removeClass('eq-ui-input invalid');
        $("#forgotPassForm").find('#msg-res-forgot').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
        var thisVal =  $( this );
        $('#forgotPassForm').find('.error-input').remove();
        thisVal.find('[type=submit]').attr('disabled','disabled');
        var forgot_username = $("input[name=forgot_username]").val();

        if(forgot_username == ""){
            $('#forgotPassForm').find('#forgot_username').addClass('eq-ui-input invalid');
            thisVal.find('[type=submit]').prop('disabled', false);
            $('#forgotPassForm').find('#msg-res-forgot').addClass('alert alert-danger');
            $('#forgotPassForm').find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
            $( 'input[name=forgot_username]').after("<span class='error-input'>Email ID can not be blank</span>");
            return false; 
        } 
        else if( $("#forgot_username").attr("data-validation") == "email"){
            if(emailRestrict( $("#forgot_username").val()) == false){
                $('#forgotPassForm').find('#forgot_username').addClass('eq-ui-input invalid');
                // $('#forgotPassForm').find('#msg-res-forgot').addClass('alert alert-danger');
                // $('#forgotPassForm').find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
                $('#forgotPassForm').find('.formResponse').removeClass('alert alert-danger').removeClass('error-msg').html("");
                $( 'input[name=forgot_username]').after("<span class='error-input'>Please enter valid Email Id</span>");
                thisVal.find('[type=submit]').prop('disabled', false);
                return false; 
            }
        }

        $("#forgotPassForm").find('#msg-res-forgot').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
        $('.error-input').remove();
        $('#forgotPassForm').find('.formResponse').removeClass('success-msg').removeClass('error-input').html("")
        
//         var forgot_username = $("input[name=forgot_username]").val();
// alert("forgot_username"+forgot_username);exit();
        // var url = "{{ settings.REST_URL }}" + "forgot_password_mail_sendl/";
        var url = "forgot_password_mail_send";
        // alert("forgot_username 1 = "+forgot_username+"URL = "+url);exit();
        var data = {'forgot_username': forgot_username};
        userAjaxCall(url, (data), 'post', true, 'formloader', "forgotPassButtId", null, function (data) {
            thisVal.find('[type=submit]').prop('disabled', false);
            if (data.length>0) {
                // var resp = $.parseJSON(data);alert(1);
                
                if(data[0].status == true) {
                     $("#forgotPassForm").find('#msg-res-forgot').addClass('alert alert-success');
                            $('#forgotPassForm').find('.formResponse').addClass('success-msg').html(data[0].msg);
                            setTimeout(function(){
                                window.location.reload();
                                $("#forgotPassForm").find('#msg-res-forgot').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
                            },1000);
                } else if(data[0].status == false){
                    $("#forgotPassForm").find('#msg-res-forgot').addClass('alert alert-danger');
                    if( data[0].field != 'mainError'){
                        $('#forgotPassForm').find('[name=' + data[0].field + ']').addClass('eq-ui-input invalid');
                        $('#forgotPassForm').find('.formResponse').addClass('error-msg').html(data[0].msg);
                        $('#forgotPassForm').find('input[name=' + data[0].field + ']');
                        // $('#forgotPassForm').find('input[name=' + data[0].field + ']').after("<span class='error-input'>" + data[0].msg + "</span>");
                        
                    }else{
                        $('#forgotPassForm').find('.formResponse').addClass('error-msg').html(data[0].msg);
                    }
                }

                // $.each(data, function(key, val){
                //     $.each(val, function(key1, val1){
                //         if(key1 == 'status' && val1 == true){   
                //             $("#forgotPassForm").find('#msg-res-forgot').addClass('alert alert-success');
                //             $('#forgotPassForm').find('.formResponse').addClass('success-msg').html(data[key].msg);
                //             setTimeout(function(){
                //                 window.location.reload();
                //                 $("#forgotPassForm").find('#msg-res-forgot').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
                //             },1000);
                //         } else if(key1 == 'status' && val1 == false){
                //             $("#forgotPassForm").find('#msg-res-forgot').addClass('alert alert-danger');
                //             if( data[key].field != 'mainError'){
                //                 $('#forgotPassForm').find('[name=' + data[key].field + ']').addClass('eq-ui-input invalid');
                //                 $('#forgotPassForm').find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
                //                 $('#forgotPassForm').find('input[name=' + data[key].field + ']').after("<span class='error-input'>" + data[key].msg + "</span>");
                //             }else{
                //                 $('#forgotPassForm').find('.formResponse').addClass('error-msg').html(data[key].msg);
                //             }
                //         }
                //     });    
                // });
            }
           
        });

        e.preventDefault();
    });
});
function formValidation( idVal ){

    $( "#" + idVal ).find('.eq-ui-input').removeClass('eq-ui-input invalid');
    $("#" + idVal).find('#msg-res-login').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
    $("#" + idVal).find(".error-input").remove();
    var flag = false;
    $( "#" + idVal ).find("input, select").each(function( value){
        var fieldName = $(this).attr("name");
        var fieldVal = $(this).val();
        if(fieldName && fieldVal == ""){
            $( "#" + idVal ).find('[name=' + fieldName + ']').addClass('eq-ui-input invalid');
            var fieldTxt = fieldName.replace("_", " ");
            fieldTxt = fieldTxt.toLowerCase().replace(/\b[a-z]/g, function(letter) {
                            return letter.toUpperCase();
                    });
            $( "#" + idVal ).find("input[name="+ fieldName +"]").after("<span class='error-input'>" + fieldTxt + " can not be blank.<span>");
            flag = true;
        }
        if( $(this).attr("data-validation") == "password"){
            if(passwordRestrict(fieldVal) == false){
                $( "#" + idVal ).find('[name=' + fieldName + ']').addClass('eq-ui-input invalid');
                $( "#" + idVal ).find("input[name="+ fieldName +"]").after("<span class='error-input'>Password must contain one upper case, one lower case, one digit, one special character and 8 - 20 chanracters.</span>");
                flag = true;
            }
        }
        if( $(this).attr("data-validation") == "email"){
            if(emailRestrict(fieldVal) == false){
                $( "#" + idVal ).find('[name=' + fieldName + ']').addClass('eq-ui-input invalid');
                $( "#" + idVal ).find("input[name="+ fieldName +"]").after("<span class='error-input'>Please enter valid Email Id</span>");
                flag = true;
            }
        }
    });

    if(flag){
        $( "#" + idVal ).find('#msg-res-login').addClass('alert alert-danger');
        $('#' + idVal) .find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
        return false;
    }else{

    }
}

function formValidationForgot( idVal ){
    $( "#" + idVal ).find('.eq-ui-input').removeClass('eq-ui-input invalid');
    $("#" + idVal).find('#msg-res-forgot').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
    var errorFields = {
        'forgot_username' : 'Email ID'
       
    }
    $("#" + idVal).find(".error-input").remove();
    var flag = false;
        $( "#" + idVal ).find("input, select").not(":hidden").each(function( value){
        var fieldName = $(this).attr("name");
        // alert(fieldName)
        var fieldVal = $(this).val();
        if(fieldName && (fieldVal == "" || fieldVal == 0) ){
            // var fieldTxt = fieldName.replace("_", " ");
            // fieldTxt = fieldTxt.toLowerCase().replace(/\b[a-z]/g, function(letter) {
            //     return letter.toUpperCase();
            // });
            if(fieldName != 'password' || $("#" + idVal).find('input:hidden[name=id]').val() == '' ){
                $( "#" + idVal ).find('[name=' + fieldName + ']').addClass('eq-ui-input invalid');
                $( "#forgot_username" ).after("<span class='error-input'>" + errorFields[fieldName] + " can not be blank.<span>");
                flag = true;
            }

        }
      
    });
    if(flag){
        $( "#" + idVal ).find('#msg-res-forgot').addClass('alert alert-danger');
        $('#' + idVal) .find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
        return true;
    }

}

// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }