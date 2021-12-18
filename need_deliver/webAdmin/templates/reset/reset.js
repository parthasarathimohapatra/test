{% load staticfiles %}
$(document).ready(function () {
    
    $('#resetPasswordForm').on('submit', function (e) {
        $("#resetPasswordForm").find('.eq-ui-input').removeClass('eq-ui-input invalid')
        $('.error-input').remove();
        var thisVal =  $( this );
        thisVal.find('[type=submit]').prop('disabled', true);
        if(formValidation("resetPasswordForm") == false){
            thisVal.find('[type=submit]').prop('disabled', false);
            return false;
        }
        $('#resetPasswordForm').find('.formResponse').removeClass('success-msg').removeClass('error-input').html("")
        
        // var url = "{{ settings.REST_URL }}" + "reset_password/";
        var url = "reset_password_ajax";
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
        var formData = new FormData(this);
        serverCall(url, formData, "POST", true, 'formloader', null, true, function (res) {
        thisVal.find('[type=submit]').prop('disabled', false);
            if (res.length>0) {
                var myJSON = JSON.stringify(res);

                // alert(myJSON);
                // alert(res[0].msg);
                if(res[0].status == true){

                    $('#resetPasswordForm').find('.formResponse').addClass('success-msg').html(res[0].msg);                           
                    setTimeout(function(){
                        clearFormData('resetPasswordForm');
                        window.location.href= "/";
                    },2000);
                } else if(res[0].status == false){
                    if( res[0].field != 'mainError'){  
                        $('#resetPasswordForm').find('[name=' + res[0].field + ']').addClass('eq-ui-input invalid')
                        $('#resetPasswordForm').find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
                        $('#resetPasswordForm').find('[name=' + res[0].field + ']').after("<span class='error-input'>" + res[0].msg + "</span>");
                    }else{
                        $('#resetPasswordForm').find('.formResponse').addClass('error-msg').html(res[0].msg);
                    }
                }


                // $.each(res, function(key, val){
                //     $.each(val, function(key1, val1){
                //         if(key1 == 'status' && val1 == true){

                //             $('#resetPasswordForm').find('.formResponse').addClass('success-msg').html(res[key].msg);                           
                //             setTimeout(function(){
                //                 clearFormData('resetPasswordForm');
                //                 window.location.href= "/";
                //             },2000);
                //         } else if(key1 == 'status' && val1 == false){
                //             if( res[key].field != 'mainError'){  
                //                 $('#resetPasswordForm').find('[name=' + res[key].field + ']').addClass('eq-ui-input invalid')
                //                 $('#resetPasswordForm').find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
                //                 $('#resetPasswordForm').find('[name=' + res[key].field + ']').after("<span class='error-input'>" + res[key].msg + "</span>");
                //             }else{
                //                 $('#resetPasswordForm').find('.formResponse').addClass('error-msg').html(res[key].msg);
                //             }
                //         }
                //     });    
                // });

            }
           
        },csrftoken);

        e.preventDefault();
    });
    
});
function formValidation( idVal ){
    $( "#" + idVal ).find('.eq-ui-input').removeClass('eq-ui-input invalid');
    var errorFields = {
        'new_password' : 'New Password',
        'confirm_password' : 'Confirm Password',
        
    }
    $("#" + idVal).find(".error-input").remove();
    var flag = false;
    $( "#" + idVal ).find("input, select").not(":hidden").each(function( value){
        var fieldName = $(this).attr("name");
        // alert(fieldName)
        var fieldVal = $(this).val();
        if(fieldName && (fieldVal == "" || fieldVal == 0) ){
            $( "#" + idVal ).find('[name=' + fieldName + ']').addClass('eq-ui-input invalid')
            $( "#" + idVal ).find("[name="+ fieldName +"]").after("<span class='error-input'>" + errorFields[fieldName] + " can not be blank.<span>");
            flag = true;
        }
        if( $(this).attr("data-validation") == "password" && fieldVal!= '' ){
            if(passwordRestrict(fieldVal) == false){
                $( "#" + idVal ).find('[name=' + fieldName + ']').addClass('eq-ui-input invalid')
                $( "#" + idVal ).find("[name="+ fieldName +"]").after("<span class='error-input'>Password must contain one upper case, one lower case, one digit, one special character and 8 - 20 chanracters.</span>");
                flag = true;
            }
        }

    });
    
    if(flag){
        $("#" + idVal).find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
        return false;
    } else{
        $("#" + idVal).find('.formResponse').removeClass('error-msg').html("");
        return true;
    }
}
function clearFormData( formId ){
    $( "#" + formId ).find('.eq-ui-input').removeClass('eq-ui-input invalid');
    $('.error-input').remove();
    $( "#" + formId ).find('.formResponse').removeClass('success-msg').removeClass('error-input').html("");
    $( "#" + formId ).find('input,select').prop('disabled', false);
    $( "#" + formId ).find('[type=submit]').prop('disabled', false);
    $( "#" + formId ).find("input[name=new_password]").val("");
    $( "#" + formId ).find("input[name=confirm_password]").val("");
}