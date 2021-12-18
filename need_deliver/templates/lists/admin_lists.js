{% load staticfiles %}

$(function(){
    $("body").on("click", ".send_mail", function(){
        clearFormData('send_mail_popupForm');
        var rcvDetails = $( this ).attr("data-rcv");
        var id = $( this ).attr("data-id");
        $("#send_mail_popupForm").find("input[name=to_send]").val(rcvDetails).trigger("change");
        $("#send_mail_popupForm").find('input:hidden[name=id]').val(id);
    });
   
    var hash = window.location.hash;
    
    if(hash){

        $(".modal-body").hide();
        $(".edit-data-load-content").show();
        clearFormData('add_popupForm');
        var action = $(this).attr('data-action');
        $('#createModal').find('#modal_label').html("View Details");
        $(".add_popupForm").find('input,select').prop('disabled', true);
        $(".add_popupForm").find('#submit-btn-form').hide();
        $(".add_popupForm").find('#pass-blk').hide();
        $(".add_popupForm").find('#pass-blk').hide();
        $(".add_popupForm").find(".not-editable").prop('disabled', true);
        var id = window.location.hash.substring(1)
        $(".add_popupForm").find('input:hidden[name=id]').val(id);
        var url = "{{ settings.REST_URL }}" + "adminuser-details/"+ id 
        serverCall(url, null, 'get', true, null, null, null, function (res) {
            $(".modal-body").show();
            $(".edit-data-load-content").hide();
            // console.log(res);return false;
            if (res.length>0) {
                // var resp = $.parseJSON(data);alert(1);
                $.each(res, function(key, val){
                    $.each(val, function(key1, val1){
                        if(key1 == 'status' && val1 == true){
                            // alert(JSON.stringify(val.data.country));
                            $( "input[name=first_name]" ).val(val.data.first_name).trigger("change");
                            $( "input[name=last_name]" ).val(val.data.last_name).trigger("change");
                            $( "input[name=email_id]" ).val(val.data.email_id).trigger("change");
                            $( "select[name=duration]" ).val(val.data.duration).trigger("change");   

                            $( "#password" ).val(val.data.password).trigger("change");    
                            $( "textarea[name=description]" ).val(val.data.description).trigger("change");                      
                            if(val.data.country!= null){$( "select[name=country]" ).val(val.data.country.id).trigger("change");}
                            
                            
                            $( "input[name=city]" ).val(val.data.city).trigger("change");
                            $( "select[name=language]" ).val(val.data.language.id).trigger("change");
                            if( val.data.profile_picture != null || val.data.profile_picture ==''){
                                $(".add_popupForm").find('#users_av ').attr('src',  val.data.profile_picture + "?time="+ new Date($.now()) );
                            }else{
                                $(".add_popupForm").find('#users_av ').attr('src', "{% static 'images/avatar.jpg' %}"); 
                            }
                            if( val.data.image_file != null || val.data.image_file ==''){
                                $(".add_popupForm").find('#vehicle_preview ').attr('src', "{{settings.AWS_S3_BUCKET_URL}}{{settings.AWS_USERS_IMAGES}}" + val.data.image_file + "?time="+ new Date($.now()) );
                            }else{
                                $(".add_popupForm").find('#vehicle_preview ').attr('src', "{% static 'images/no_car_image.png' %}"); 
                            }
                            $(".add_popupForm").find('.big-img-loader').each(function(){
                                $(this).after('<img class="rounded-circle z-depth-1-half avatar-pic" src="{% static 'images/big-img-loader.gif'%} height="100px;" width="100px;"/>') // some preloaded "loading" image
                               .hide()
                               .attr('src',this.src)
                               .one('load', function() {
                                  $(this).fadeIn().next().remove();
                               });
                            });
                        }
                    });    
                });
            }
        });
           $('#createModal').modal('show'); 

    }
    

    $( "body" ).on("click", "#groupCheck", function(){
        if($(this).is(':checked')){
            $( ".multi_action" ).show('slow');
            $( ".single_action" ).hide('slow');
            var count = $( "#tblCustomer" ).find('.singleCheck').length;
            $("#selected_records").html(count);
            $( "#tblCustomer" ).find('input[name="id[]"]').prop( "checked", true );
        } else{
            $( ".multi_action" ).hide('slow');
            $( ".single_action" ).hide('slow');
            $("#selected_records").html(0);
            $( "#tblCustomer" ).find('input[name="id[]"]').prop( "checked", false );
        }
    });
    $( "body" ).on("click", ".action", function(){
        $( "#upRecords" ).find('#popup_title').html($(this).attr('data-title'));
        $( "#upRecords" ).find('input[name=data-action]').val($(this).attr('data-action'))
        $( "#upRecords" ).find('input[name=data-value]').val($(this).attr('data-value'))
    });
    $( "body" ).on("click", ".action-btn", function(){
        var thisVal = $(this);
        thisVal.attr('disabled',true);
        var idsArray = []
        $('input[name="id[]"]:checked').each(function(){
            idsArray.push($(this).val());
        });
        var action = $( "#upRecords" ).find('input[name=data-action]').val();
        var value = $( "#upRecords" ).find('input[name=data-value]').val();
        var role = "{{ settings.IS_CUSTOMER }}";
        var data = {'ids': JSON.stringify(idsArray), 'action' : action, 'value' : value, 'role' : role};
        

        var url = "updateAdminUserMulRecords";
        serverCall(url, data, 'post', true, 'updateloader', null, null, function (res) {
            thisVal.attr('disabled',false);
            if(action == 'update' || action == 'rm'){refreshData();}
            if (res.length>0) {
                        if(res[0].status == true){
                            // console.log(res[key].countingInfo['allTeacher'])
                            if(action == 'update'){ 
                              
                            }
                            $('#upRecords').modal('hide'); 
                            $('.multi_action').hide(); 
                            refreshData();
                            if( action == 'send_cred' ){
                                $(".singleCheck").prop("checked", false);
                                $('.multi_action').hide();   
                            }

                        } else if(res[0].status == false){
                            if(action != 'update'){alert(val['msg']);}
                        }
                    
            }
            
        });
    });
   
    refreshData();
    $('.date-picker').datepicker({
        format: 'yyyy-mm-dd',
        }).on('changeDate', function(e){
            $(this).datepicker('hide');
    });

    $( "body" ).on("click", ".btn-add-new", function(event){
        $(".modal-body").show();
        openTab(event, 'basicinfo');
        $(".edit-data-load-content").hide();
        clearFormData('add_popupForm');
        var getOperation = $( this ).attr("data-operation");
        if(getOperation == "create_user"){
            $('#createModal').modal('show'); 
        }
    });
    $( "body" ).on("click", ".editView", function(){
        $(".modal-body").hide();
        $(".edit-data-load-content").show();
        clearFormData('add_popupForm');
        var action = $(this).attr('data-action');
        if( action == 'view' ){
            $('#createModal').find('#modal_label').html("View Details");
            $(".add_popupForm").find('input,select').prop('disabled', true);
            $(".add_popupForm").find('#submit-btn-form').hide();
            $(".add_popupForm").find('#pass-blk').hide();
        } else if( action == 'edit' ){
            $('#createModal').find('#modal_label').html("Update details");
            $(".add_popupForm").find('input,select').prop('disabled', false);
            $(".add_popupForm").find('#submit-btn-form').show();
            $(".add_popupForm").find('#pass-blk').show();
        }
        $(".add_popupForm").find('#pass-blk').hide();
        $(".add_popupForm").find(".not-editable").prop('disabled', true);
        var id = $( "#tblCustomer" ).find('input:hidden[name="id[]"]:checked').val();
        $(".add_popupForm").find('input:hidden[name=id]').val(id);
        var url = "adminuser-details/"+ id ;
        serverCall(url, null, 'get', true, null, null, null, function (res) {
            $(".modal-body").show();
            $(".edit-data-load-content").hide();
          
           // return false;
            if (res.length>0) {
                // var resp = $.parseJSON(res);
                
                // return false;
                // $.each(res, function(key, val){
                //     $.each(val, function(key1, val1){
                        if(res[0].status == true){

                            // if( res[0].data.details_data.profile_picture != null || res[0].data.details_data.profile_picture ==''){
                                
                            //     $('#users_av').attr('src', res[0].data.details_data.profile_picture+ "?time="+ new Date($.now()) );
                                
                            //     var only_profile_pic = res[0].data.details_data.profile_picture.replace("https://diaxrbad0p1f6.cloudfront.net/static/", '');
                                

                            //     $( "input:hidden[name=profile_img_prev]" ).val(only_profile_pic).trigger("change");

                            // }else{
                            //     $('#users_av').attr('src', "{% static 'images/avatar.jpg' %}"); 
                            // }
                            // alert(JSON.stringify(res[0].data));
                            $( "input[name=first_name]" ).val(res[0].data.first_name).trigger("change");
                            $( "input[name=last_name]" ).val(res[0].data.last_name).trigger("change");
                            $( "input[name=email_id]" ).val(res[0].data.email_id).trigger("change");
                            $( "input[name=phone_number]" ).val(res[0].data.phone_number).trigger("change");
                            // $( "input[name=dob]" ).val(res[0].data.dob).trigger("change");
                            // $( "#password" ).val(res[0].data.password).trigger("change");   
                           
                          
                            // res[0].data.driverAttachments['img'].forEach(function(theDonut, index) {
                            //         alert(theDonut);
                            //     });
                            // $( "textarea[name=description]" ).val(val.data.description).trigger("change");
                            setTimeout(function(){

                            if(res[0].data.state!= null){
                                //alert("hi");
                                $( "select[name=state]" ).val(res[0].data.state.id).trigger("change");}     
                            },2000);
                            
                            
                            
                            // $( "select[name=language]" ).val(val.data.language.id).trigger("change");
                            // if( val.data.profile_picture != null || val.data.profile_picture ==''){
                            //     $(".add_popupForm").find('#users_av ').attr('src', "{{settings.AWS_S3_BUCKET_URL}}{{settings.AWS_USERS_IMAGES}}" + val.data.profile_picture + "?time="+ new Date($.now()) );
                            // }else{
                            //     $(".add_popupForm").find('#users_av ').attr('src', "{% static 'images/avatar.jpg' %}"); 
                            // }
                            $(".add_popupForm").find('.big-img-loader').each(function(){
                                $(this).after('<img class="rounded-circle z-depth-1-half avatar-pic" src="{% static 'images/big-img-loader.gif'%}" height="100px" width="100px"/>') // some preloaded "loading" image
                               .hide()
                               .attr('src',this.src)
                               .one('load', function() {
                                  $(this).fadeIn().next().remove();
                               });
                            });
                        }
                //     });    
                // });
            }
        });
           $('#createModal').modal('show'); 
    });


    $( "body" ).on("click", ".singleCheck", function(){
        var count = 1;
        var count = $('input[name="id[]"]:checked').length;
        var countCheckbox = $('input[name="id[]"]').length;
        $("#selected_records").html(count);
        if(count == countCheckbox){
            $("#groupCheck").prop("checked", true);
        } else{
            $("#groupCheck").prop("checked", false);
        }
        if(count == 1){
            $( ".multi_action" ).show('slow');
            $( ".single_action" ).show('slow');
        } else if( count> 1 ){
            $( ".multi_action" ).show('slow');
            $( ".single_action" ).hide('slow');
        } else{
            $( ".multi_action" ).hide('slow');
            $( ".single_action" ).hide('slow');
        }
    });
    $('body').on('submit', '.add_popupForm', function (e) { 
        $(".add_popupForm").find('.eq-ui-input').removeClass('eq-ui-input invalid')
        $(".add_popupForm").find('#msg-res').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
        var thisVal =  $( this );
        thisVal.find('[type=submit]').prop('disabled', true);
        
        if(formValidation("add_popupForm") == false){
            
            thisVal.find('[type=submit]').prop('disabled', false);
            return false;
        }
        $('.error-input').remove();
        $('.add_popupForm').find('.formResponse').removeClass('success-msg').removeClass('error-input').html("");
        var url =  "updateAdminUserRecords/";
        var method = 'POST';
        

        var id = $(this).find('input:hidden[name=id]').val();
        
        if(id != ""){
            url += id+"/";
            method = 'PUT';
        }
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();

        var myForm = document.getElementById('driver_form');
        var formData = new FormData(this);
        
        formData.append('is_status', 'TRUE');
        formData.append('csrfmiddlewaretoken', csrftoken);

       // alert(JSON.stringify(formData));
       console.log(formData);

        serverCall(url, formData, method, true, 'formloader', null, true, function (res) {    
            thisVal.find('[type=submit]').prop('disabled', false);
            if (res.length>0) {
                // var resp = $.parseJSON(data);alert(1);
                $.each(res, function(key, val){
                    $.each(val, function(key1, val1){
                        if(key1 == 'status' && val1 == true){
                            $(".add_popupForm").find('#msg-res').addClass('alert alert-success');
                            if( id!= '' ){
                                thisVal.find('input:hidden[name=id]').val("");
                            }
                            $('.add_popupForm').find('.formResponse').addClass('success-msg').html(res[key].msg);
                            setTimeout(function(){
                                if( id == '' ){
                                    $( ".all-users" ).html(val.updated_record['allTeachers']);
                                    $( ".all-active-member" ).html(val.updated_record['totalActiveTeachers']);
                                    $( ".all-deactive-member" ).html(val.updated_record['totalDeactiveTeachers']);
                                    $( ".multi_action" ).hide('slow');
                                    $( ".single_action" ).hide('slow'); 
                                }
                                $(".add_popupForm").find('#msg-res').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
                                refreshData();
                                $('#createModal').modal('hide');
                                clearFormData('add_popupForm');
                                window.location.reload();
                            },2000);
                        } else if(key1 == 'status' && val1 == false){
                            $(".add_popupForm").find('#msg-res').addClass('alert alert-danger');
                            
                            if( res[key].field != 'mainError'){  
                               
                                openTab(e, 'basicinfo');
                                $('.add_popupForm').find('[name=' + res[key].field + ']').addClass('eq-ui-input invalid')
                                // $('.add_popupForm').find('.formResponse').addClass('error-msg').html("Please check there is some error in validation!");
                                // $('.add_popupForm').find('.formResponse').addClass('error-msg').html("Please check there is some error in validation!");
                                $('.add_popupForm').find('[name=' + res[key].field + ']').after("<span class='error-input'>" + res[key].msg + "</span>");
                            }else{
                                $('.add_popupForm').find('.formResponse').addClass('error-msg').html(res[key].msg);
                            }
                        }
                    });    
                });
            }
              
        }, csrftoken);

        e.preventDefault();
    });
    
    
});
function deleteAttachment(val, params){
    var split_val = val.split('/');
    var length = split_val.length;
    var attached_file = split_val[length-2]+"/"+split_val[length-1];
     
    var data = {'attached_file': attached_file,'params': params};
    var url = "deleteAttacment";
    serverCall(url, data, 'post', true, 'updateloader', null, null, function (res) {
        thisVal.attr('disabled',false);
        
        if (res.length>0) {
            alert(res[0].status );
                   
        }
        
    });
}
// function mail_send_validator( idVal ){
//    $( "#" + idVal ).find('.eq-ui-input').removeClass('eq-ui-input invalid');
//    $("#" + idVal).find('#send-mail-msg-res').removeClass('alert').removeClass('alert-success').removeClass('alert-danger'); 
//    var errorFields = {
//         'subject' : 'Subject',
//         'description'  : 'Mail body',
        
//     }
//     $("#" + idVal).find(".error-input").remove();
//     $("#" + idVal).find(".error-input-text").remove();
//     var flag = false;
//     $( "#" + idVal ).find("input, textarea").not(":hidden").each(function( value){
//         var fieldName = $(this).attr("name");
//         // alert(fieldName)
//         var fieldVal = $(this).val();
//         if(fieldName && (fieldVal == "" || fieldVal == 0) ){
//             $( "#" + idVal ).find('[name=' + fieldName + ']').addClass('eq-ui-input invalid');
//             $( "#" + idVal ).find("[name="+ fieldName +"]").after("<span class='error-input' >" + errorFields[fieldName] + " can not be blank.<span>");
//             flag = true;


//         }
        
//     });
//     if($("[name=description]").val() == ""){
//         $( "#" + idVal ).find('[name=description]').addClass('eq-ui-input invalid');
//         $( "#" + idVal ).find("#cke_mail_description").after("<span class='error-input-text' style='color: red;font-size: 12px;'>Mail body can not be blank<span>");
//         flag = true;
//     }
//     if(flag){

//         $( "#" + idVal ).find('#send-mail-msg-res').addClass('alert alert-danger');
//         $( "#" + idVal ).find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
//         return false;
//     } else{
//         $( "#" + idVal ).find('.eq-ui-input').removeClass('eq-ui-input invalid');
//         $( "#" + idVal ).find('.formResponse').removeClass('error-msg').html("");
//         return true;
//     }
// } 
function formValidation( idVal ){
    $( "." + idVal ).find('.eq-ui-input').removeClass('eq-ui-input invalid')
    $("." + idVal).find('#msg-res').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
    var errorFields = {
        'first_name' : 'First Name',
        'last_name'  : 'Last Name',
        'email_id' : 'Email ID',
        'phone_number' : 'Phone number',
        'password' : 'Password',

    }

    var fields = $('input.required');
    var select_fields = $('select.required');
    $("." + idVal).find(".error-input").remove();
    var flag = false;
    for(var i=0;i<fields.length;i++){
        var fieldName = fields[i].name;
        var fieldId = fields[i].id;
        var fieldVal = $(fields[i]).val();
        // alert("fields[i]).val() = "+$(fields[i]).val());
        
        
        if( fieldName == "email_id"){
            if(fieldVal== ''){
                // alert("in email blank");
                $( "#"+fieldId).addClass('eq-ui-input invalid');
                $( "#"+fieldId).after("<span class='error-input'>" + errorFields[fieldId] + " can not be blank.<span>");
                flag = true;
            }
            else if(emailRestrict(fieldVal) == false){
                // alert("in email restrict");
                $( "input[name='"+fieldName+"']" ).addClass('eq-ui-input invalid');
                $( "input[name='"+fieldName+"']" ).after("<span class='error-input'>Please enter valid Email Id</span>");
                flag = true;

            } else {
                // alert("in email exist");
                // flag = true;
                // if($( "#user_id").val() ==""){
                var data = {'email_id': fieldVal};
                var url = "checkUniqueEmail";
                $.ajax({
                type: "POST",
                url: url,
                data: data,
                async: false,
                success: function (res) { 
                    if (res[0].status == false) {
                        $( "input[name='email_id']" ).addClass('eq-ui-input invalid');
                        $( "input[name='email_id']" ).after("<span class='error-input'>Email Id already exist</span>");
                        flag = true;
                    } else {
                        flag = false;
                    }
                },
                
            });
                //  serverCall(url, data, 'post', true, 'updateloader', null, null, function (res) {
                //     alert("res[0].status "+res[0].status);
                //     if (res[0].status == false) {

                //         // alert(JSON.stringify(res[0].msg));

                //         document.getElementById("basicinfo_tab").className += " active";
                //         // document.getElementById("driverinfo_tab").className   = document.getElementById("driverinfo_tab").className.replace(" active", "");
                //         // document.getElementById("basicinfo").style.display = "block";
                //         // document.getElementById("driverinfo").style.display = "none";
                //         // document.getElementById("vehicleinfo").style.display = "none";
                //         // alert("res.status= "+JSON.stringify(res));
                       
                       
                        
                        
                //         setTimeout(function(){  
                //             $( "input[name='email_id']" ).addClass('eq-ui-input invalid');
                //             $( "input[name='email_id']" ).after("<span class='error-input'>Email Id already exist</span>");
                //             flag = true;
                //          }, 3000);
                //         alert("flag = "+flag);
                               
                //     } else {
                //         flag = false;
                //         // document.getElementById("next").style.display = "block";
                //     }
                    
                // });

            }
        }
        if(fieldName != "email_id" && $(fields[i]).val() == ''){
            $( "#"+fieldId).addClass('eq-ui-input invalid');
            $( "#"+fieldId).after("<span class='error-input'>" + errorFields[fieldId] + " can not be blank.<span>");
            flag = true;
        }
        // }
    }

    // for(var i=0;i<select_fields.length;i++){
    //     var fieldName = select_fields[i].name;
    //     alert("fieldName = "+fieldName);
    //     var fieldId = select_fields[i].id;
    //     var fieldVal = $(select_fields[i]).val();
    //     if($(select_fields[i]).val() == 0){
    //         $( "#"+fieldId).css("border","solid 1px red");
    //         $( "#"+fieldId).after("<span class='error-input'>" + errorFields[fieldId] + " can not be blank.<span>");
            
    //         flag = true;
    //     } else {
    //         $( "#"+fieldId).css("border","solid 1px ##cccccc");
    //         $( "#"+fieldId).after("<span class='error-input'><span>");
    //         flag = false;
    //     }
    // }


    
    
   // alert("flag = "+flag);
    if(flag){
        $( "." + idVal ).find('#msg-res').addClass('alert alert-danger');
        $( "." + idVal ).find('.formResponse').addClass('error-msg').html("Please check fields");
        return false;
    } else{
        $( "." + idVal ).find('.eq-ui-input').removeClass('eq-ui-input invalid');
        $( "." + idVal ).find('.formResponse').removeClass('error-msg').html("");
        return true;
    }
}
function refreshData(){
    // $("#tblCustomer").append('<tbody class="tblCustomer-error"><img src="{{ settings.BASE_URL }}/static/images/dataloader.gif"></tbody>');
    var dataTable = $('#tblCustomer').DataTable( {
        "stateSave": true,
        "destroy": true,
        "serverSide": true,
        "aaSorting": [],
        "order": [[0,'desc']],
        "aoColumns":[
            {"bSortable": true},
            {"bSortable": false},
            {"bSortable": false},
            {"bSortable": false},
            {"bSortable": false},
        ],
        'columnDefs': [{
            'targets': 0,
            'searchable':true,
            'orderable':true,
            'responsive': true,
            "processing": true,
            
            'className': 'dt-center',
            'render': function (data, type, full, meta){
                    return '<label class="checkbox text-primary " ><input type="checkbox" class="singleCheck" name="id[]" value="' + $('<div/>').text(data).html() + '"><span class="check"></span></label>';
                }
        }],
        "drawCallback": function () {
            $('.dataTables_paginate > .pagination').addClass('pagination-circle pg-blue mb-0 justify-content-end');
            $('.dataTables_paginate > .pagination').find('li').addClass('page-item');
            $('.dataTables_paginate > .pagination').find('li>a').addClass('page-link waves-effect waves-effect');
        },
        "ajax":{
            beforeSend : function(data){
                $("#tblCustomer").append('<tbody class="preloader-loader-content"><tr><th class="preload-datatable" colspan="10"><img class="datatable-loader" src="{% static 'images/dataloader.gif' %}"></th></tr></tbody>');
            },
            url :"adminuser_list_json",
            type: "get",  // method  , by default get
            error: function(){  // error handling
                $(".tblCustomer-error").html("");
                $("#tblCustomer").append('<tbody class="tblCustomer-error"><tr><th colspan="10">No data found in the server</th></tr></tbody>');
                $("#tblCustomer_processing").css("display","none");
            },
            complete: function(data) {
                // alert("conp"+JSON.stringify(data));
                $("#selected_records").html(0);
                $("#groupCheck").prop("checked", false);
                $( ".multi_action" ).hide('slow');
                $( ".single_action" ).hide('slow');
                $("#tblCustomer").find(".preload-datatable").remove();
                $("#tblCustomer").find(".preloader-loader-content").remove();
                $('.big-img-loader').each(function(){
                    $(this).after('<img width="50" height="50" src="{% static 'images/big-img-loader.gif'%}" />') // some preloaded "loading" image
                   .hide()
                   .attr('src',this.src)
                   .one('load', function() {
                      $(this).fadeIn().next().remove();
                   });
                });
            }
        },
    } );


}

function clearFormData( formClass ){
    $("#jcrop").html("");
    $( "." + formClass ).find('.eq-ui-input').removeClass('eq-ui-input invalid');
    $("." + formClass).find('#msg-res').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
    $('#createModal').find('#modal_label').html("Add New");
// alert("formClass = "+formClass);
    $( "." + formClass ).find("input,textarea,password").not( ":file" ).val('').trigger('change');
    $( "." + formClass ).find("select").val(0).trigger('change');
    $('.error-input').remove();
    $("#driver_licence_existing_files").empty();
    $("#driver_licence_files" ).empty();
    $("#vehicle_insurance_files" ).empty();
    $("#vehicle_reg_files" ).empty();
    $( "#profile_picture" ).val(null);
    $( "#image_file" ).val(null);
    

    $("#driver_licence").val(null);
    $("#vehicle_insurance").val(null);
    $("#vehicle_registration").val(null);

    $("#count_of_driver_licence_existing_files").val(0);
    $("#count_of_vehicle_insurance_existing_files").val(0);
    $("#count_of_vehicle_reg_existing_files").val(0);

    $( "#wheel_chair_support" ).prop("checked",false);
    $( "#booster_seat_support" ).prop("checked",false);
    $('.add_popupForm').find('.formResponse').removeClass('success-msg').removeClass('error-input').html("");
    $(".add_popupForm").find('input,select').prop('disabled', false);
    $(".add_popupForm").find('#submit-btn-form').show();
    $(".add_popupForm").find('#pass-blk').show();
    $(".add_popupForm").find('#users_av ').attr('src', "{% static 'images/avatar.jpg' %}");
    $(".add_popupForm").find('#vehicle_preview ').attr('src', "{% static 'images/no_car_image.png' %}");
    $(".add_popupForm").find(".not-editable").prop('disabled', false);
    $(".add_popupForm").find('[type=submit]').prop('disabled', false);
}
function readURL(input) {
    if (input.files && input.files[0]) {
       
        var type = input.files[0].type; 
        var type_reg = /^image\/(jpg|png|jpeg|bmp|gif|ico)$/;
        if (type_reg.test(type)) {
            var size = parseFloat(input.files[0].size / 1024).toFixed(2);
            if( size > 7000){
                // $('.add_popupForm').find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
                $("#image-up").after("<span class='error-input img-upload'>Max. image upload size is 7MB.</span>");
            } else{
                $(".img-upload").remove();
                var reader = new FileReader();
                reader.onload = function (e) {

                $('#profile_picture').attr('src', e.target.result);
                $('input:hidden[name=profile_picture]').val(e.target.result);
                $('#users_av ').attr('src', e.target.result);
            }
        };
        reader.readAsDataURL(input.files[0]);
        } else{
            $('.add_popupForm').find('#profile_picture').val( "" );
            $('.add_popupForm').find('input:hidden[name=profile_picture]').val( "" );
            $('#users_av ').attr('src', "{% static 'images/avatar.jpg' %}");
        }
        
        
    }
}
function readVehicleImgURL(input) {
    if (input.files && input.files[0]) {
       
        var type = input.files[0].type; 
        var type_reg = /^image\/(jpg|png|jpeg|bmp|gif|ico)$/;
        if (type_reg.test(type)) {
            var size = parseFloat(input.files[0].size / 1024).toFixed(2);
            if( size > 7000){
                // $('.add_popupForm').find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
                $("#image-up").after("<span class='error-input img-upload'>Max. image upload size is 7MB.</span>");
            } else{
                $(".img-upload").remove();
                var reader = new FileReader();
                reader.onload = function (e) {

                $('#image_file').attr('src', e.target.result);
                $('input:hidden[name=image_file]').val(e.target.result);
                $('#vehicle_preview ').attr('src', e.target.result);
            }
        };
        reader.readAsDataURL(input.files[0]);
        } else{
            $('.add_popupForm').find('#image_file').val( "" );
            $('.add_popupForm').find('input:hidden[name=image_file]').val( "" );
            $('#vehicle_preview ').attr('src', "{% static 'images/no_car_image.png' %}");
        }
        
        
    }
}

$(document).ready(function() {
   
    $("body").on('keypress', '.phone-number',function (event) {
     // alert(event.which);
        value = $(this).val() //Allowed 0-9 + - back space arrow
        if((event.which >= 48 && event.which <=57) || (event.which == 43) || (event.which == 45)|| (event.which == 0)|| (event.which == 8)) {
          $( ".phone-number").removeClass('eq-ui-input invalid');
          $( ".phone-number").removeClass('error-msg').html("");
          return true; 
        } // prevent if not number/dot
        else {
           
            $( ".phone-number").addClass('alert alert-danger');
            $( ".phone-number").addClass('error-msg').html("Please check fields");
            event.preventDefault();
            return false;
        }
    });
    $( "#togglePasswordField" ).click(function() {
      // alert( "Handler for .click() called." );
       var targetType = $('#password').prop("type");
       // alert(targetType);
       if (targetType == "text") {

                $("#password").prop("type", "password");
            } else {
                $("#password").prop("type", "text");
            }
       
    });

});

/* tab js */
function openTab(evt, tabName) {
    if(formValidation("add_popupForm") == false){
        document.getElementById("basicinfo").style.display = "block";
        // document.getElementById("basicinfo_tab").className += " active";
       
    }
    else {
        var i, tabcontent, tablinks;
        if(tabName == "vehicleinfo" || tabName == "basicinfo") {
            if($('#driving_licence_expiry_date').val() == ''){
                $( "input[name='driving_licence_expiry_date']" ).addClass('eq-ui-input invalid');
                $( "input[name='driving_licence_expiry_date']").after("<span class='error-input'>Driving licence exp can not be blank.<span>");
                $( ".add_popupForm" ).find('#msg-res').addClass('alert alert-danger');
                $( ".add_popupForm" ).find('.formResponse').addClass('error-msg').html("Please check fields");
                return false;
            }
        }
        tabcontent = document.getElementsByClassName("tabcontent");

        for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        // alert("tablinks = "+tablinks);
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(tabName).style.display = "block";
        document.getElementById(tabName+"_tab").className += " active";

    }
  
  // evt.currentTarget.className += " active";
}


