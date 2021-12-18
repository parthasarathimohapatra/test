{% load staticfiles %}

$(function(){
   
    $( "body" ).on("click", "#groupCheck", function(){
       if($(this).is(':checked')){
           $( ".multi_action" ).fadeIn('slow');
           $( ".single_action" ).fadeOut('slow');
           var count = $( "#tblCustomer" ).find('.singleCheck').length;
           $("#selected_records").html(count);
           $( "#tblCustomer" ).find('input[name="id[]"]').prop( "checked", true );
       } else{
           $( ".multi_action" ).fadeOut('slow');
           $( ".single_action" ).fadeOut('slow');
           $("#selected_records").html(0);
           $( "#tblCustomer" ).find('input[name="id[]"]').prop( "checked", false );
       }
   });
  
    var hash = window.location.hash;
    
    // if(hash){

    //     $(".modal-body").hide();
    //     $(".edit-data-load-content").show();
    //     clearFormData('add_popupForm');
    //     var action = $(this).attr('data-action');
    //     $('#createModal').find('#modal_label').html("View Details");
    //     $(".add_popupForm").find('input,select').prop('disabled', true);
    //     $(".add_popupForm").find('#submit-btn-form').hide();
    //     $(".add_popupForm").find('#pass-blk').hide();
    //     $(".add_popupForm").find('#pass-blk').hide();
    //     $(".add_popupForm").find(".not-editable").prop('disabled', true);
    //     var id = window.location.hash.substring(1)
    //     $(".add_popupForm").find('input:hidden[name=id]').val(id);
    //     var url = "{{ settings.REST_URL }}" + "users_record_details/"+ id 
    //     serverCall(url, null, 'get', true, null, null, null, function (res) {
    //         $(".modal-body").show();
    //         $(".edit-data-load-content").hide();
    //         // console.log(res);return false;
    //         if (res.length>0) {
    //             // var resp = $.parseJSON(data);alert(1);
    //             $.each(res, function(key, val){
    //                 $.each(val, function(key1, val1){
    //                     if(key1 == 'status' && val1 == true){
    //                         $( "input[name=first_name]" ).val(val.data.first_name).trigger("change");
    //                         $( "input[name=last_name]" ).val(val.data.last_name).trigger("change");
    //                         $( "input[name=email_id]" ).val(val.data.email_id).trigger("change");
    //                         $( "select[name=duration]" ).val(val.data.duration).trigger("change");       
    //                         $( "textarea[name=description]" ).val(val.data.description).trigger("change");                      
    //                         if(val.data.country!= null){$( "select[name=country]" ).val(val.data.country.id).trigger("change");}
                            
                            
    //                         $( "input[name=city]" ).val(val.data.city).trigger("change");
    //                         $( "select[name=language]" ).val(val.data.language.id).trigger("change");
    //                         if( val.data.profile_img != null || val.data.profile_img ==''){
    //                             $(".add_popupForm").find('#users_av ').attr('src', "{{settings.AWS_S3_BUCKET_URL}}{{settings.AWS_USERS_IMAGES}}" + val.data.profile_img + "?time="+ new Date($.now()) );
    //                         }else{
    //                             $(".add_popupForm").find('#users_av ').attr('src', "{% static 'images/avatar.jpg' %}"); 
    //                         }
    //                         $(".add_popupForm").find('.big-img-loader').each(function(){
    //                             $(this).after('<img class="rounded-circle z-depth-1-half avatar-pic" src="{{ settings.BASE_URL }}/static/images/big-img-loader.gif" />') // some preloaded "loading" image
    //                            .hide()
    //                            .attr('src',this.src)
    //                            .one('load', function() {
    //                               $(this).fadeIn().next().remove();
    //                            });
    //                         });
    //                     }
    //                 });    
    //             });
    //         }
    //     });
    //        $('#createModal').modal('show'); 

    // }
    

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
        
        var data = {'ids': JSON.stringify(idsArray), 'action' : action, 'value' : value};
        var url = "updatePaymentMethodActionRecords";
        serverCall(url, data, 'post', true, 'updateloader', null, null, function (res) {
            thisVal.attr('disabled',false);
            if(action == 'update' || action == 'rm'){refreshData();}
            if (res.length>0) {
                if(res[0].status == true){
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
	$('#country').on('change',function(){
        var countryID = $(this).val();
        if(countryID !=0 || countryID){
            var data = null;
            var url = "{{ WEBADMIN }}" + "/states/"+ countryID;
            serverCall(url, null, 'get', true, null, null, null, function (res) {
                if (res.length>0) {
                    // var resp = $.parseJSON(data);alert(1);
                    $.each(res, function(key, val){
                        $.each(val, function(key1, val1){
                            if(key1 == 'status' && val1 == true){
                                var html = '<option value="0">-- State --</option>';
                                $.each(res[key].data, function(key2, val2){
                                    html += '<option value="'+ val2['id'] +'">'+ val2['state_name'] +'</option>';
                                });
                                $('#state').html(html); 
                            } else if(key1 == 'status' && val1 == false){
                                $('#state').html('<option value="0">-- State --</option>');
                            }
                        });    
                    });
                }
            });
        }else{
            $('#state').html('<option value="0">-- State --</option>');
        }
    });
	$( "body" ).on("click", ".btn-add-new", function(){
        $(".modal-body").show();
        $(".edit-data-load-content").hide();
        clearFormData('add_popupForm');
		var getOperation = $( this ).attr("data-operation");
		if(getOperation == "create_teacher"){
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
            $('#createModal').find('#modal_label').html("Update vehicle type");
            $(".add_popupForm").find('input,select').prop('disabled', false);
            $(".add_popupForm").find('#submit-btn-form').show();
            $(".add_popupForm").find('#pass-blk').show();
        }
        $(".add_popupForm").find('#pass-blk').hide();
        $(".add_popupForm").find(".not-editable").prop('disabled', true);
        var id = $( "#tblCustomer" ).find('input:hidden[name="id[]"]:checked').val();
        $(".add_popupForm").find('input:hidden[name=id]').val(id);
        var url = "paymentmethod-details/"+ id ;
        serverCall(url, null, 'get', true, null, null, null, function (res) {
            $(".modal-body").show();
            $(".edit-data-load-content").hide();
          
           // return false;
            if (res.length>0) {
                if(res[0].status == true){
                    $( "input[name=name]" ).val(res[0].data.name).trigger("change");
                   
                    if( res[0].data.payment_logo != null || res[0].data.payment_logo !=''){
                        $('#users_av').attr("src", res[0].data.payment_logo );
                    }else{
                         $("#add_popupForm").find('#users_av').attr('src', "{% static 'images/avatar.jpg' %}"); 
                    }
                    $(".add_popupForm").find('.big-img-loader').each(function(){
                        $(this).after('<img class="rounded-circle z-depth-1-half avatar-pic" src="{% static 'images/big-img-loader.gif'%}" />') // some preloaded "loading" image
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
        var url =  "updatePaymentMethod/";
        var method = 'POST';
        // var vehicle_type_name = $("input[name=vehicle_type_name]").val();
        // var base_fare = $("input[name=base_fare]").val();
        // var khr = $("input[name=khr]").val();
        // var person_capcity = $("input[name=person_capcity]").val();
        // var image_file = $("file[name=image_file]").val();


        var id = $(this).find('input:hidden[name=id]').val();
        
        if(id != ""){
            url += id+"/";
            method = 'PUT';
        }
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
        // var role = "{{ settings.IS_CUSTOMER }}";
        // alert(role);
        // var data = {
        //     'vehicle_type_name': vehicle_type_name, 
        //     'khr': khr, 
        //     'person_capcity': person_capcity, 
           
        //     'csrftoken':csrftoken
        // };
        // alert("url = "+url+" method = "+method+" csrftoken = "+csrftoken);
        var formData = new FormData(this);
        formData.append('is_status', 'TRUE');
        formData.append('csrfmiddlewaretoken', csrftoken);
        formData.append('payment_logo', $('#payment_logo')[0].files[0]);
        // serverCall(url, formData, method, true, 'formloader', null, true, function (res) {
         // console.log(formData);
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
                                $('.add_popupForm').find('[name=' + res[key].field + ']').addClass('eq-ui-input invalid')
                                $('.add_popupForm').find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
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

function formValidation( idVal ){
    $( "#" + idVal ).find('.eq-ui-input').removeClass('eq-ui-input invalid')
    $("#" + idVal).find('#msg-res').removeClass('alert').removeClass('alert-success').removeClass('alert-danger');
    var errorFields = {
        'first_name' : 'First Name',
        'last_name'  : 'Last Name',
        'email_id' : 'Email ID',
        'country' : 'Country Name',
        'city' : 'City Name',
        'duration' : 'Call duration',
        'language' : 'Expert language',
        'password' : 'Password',
        'cpassword' : 'Confirm Password'
    }
    $("#" + idVal).find(".error-input").remove();
    var flag = false;
    $( "#" + idVal ).find("input, select").not(":hidden").each(function( value){
        var fieldName = $(this).attr("name");
        // alert(fieldName)
        var fieldVal = $(this).val();
        
        if(fieldName && (fieldVal == "" || fieldVal == 0) ){
            $( "#" + idVal ).find('[name=' + fieldName + ']').addClass('eq-ui-input invalid')
            // var fieldTxt = fieldName.replace("_", " ");
            // fieldTxt = fieldTxt.toLowerCase().replace(/\b[a-z]/g, function(letter) {
            //     return letter.toUpperCase();
            // });
            if(fieldName != 'password' || $("#" + idVal).find('input:hidden[name=id]').val() == '' ){
                $( "#" + idVal ).find("[name="+ fieldName +"]").after("<span class='error-input'>" + errorFields[fieldName] + " can not be blank.<span>");
                flag = true;
            }

        }
        if( $(this).attr("data-validation") == "password" && fieldVal!= '' ){
            if(passwordRestrict(fieldVal) == false){
                $( "#" + idVal ).find('[name=' + fieldName + ']').addClass('eq-ui-input invalid')
                $( "#" + idVal ).find("[name="+ fieldName +"]").after("<span class='error-input'>Password must contain one upper case, one lower case, one digit, one special character and 8 - 20 chanracters.</span>");
                flag = true;
            }
        }

        if( $(this).attr("data-validation") == "email" && fieldVal!= ''){
            if(emailRestrict(fieldVal) == false){
                $( "#" + idVal ).find('[name=' + fieldName + ']').addClass('eq-ui-input invalid')
                $( "#" + idVal ).find("[name="+ fieldName +"]").after("<span class='error-input'>Please enter valid Email Id</span>");
                flag = true;
            }
        }
    });
    if( $("#" + idVal).find("input[name=cpassword]").val() =='' && $("#" + idVal).find('input:hidden[name=id]').val() != ''){
        flag = false;
    }
    if(flag){
        $( "#" + idVal ).find('#msg-res').addClass('alert alert-danger');
        $( "#" + idVal ).find('.formResponse').addClass('error-msg').html("Please fill up all required fields");
        return false;
    } else{
        $( "#" + idVal ).find('.eq-ui-input').removeClass('eq-ui-input invalid');
        $( "#" + idVal ).find('.formResponse').removeClass('error-msg').html("");
        return true;
    }
}

// $('#tblCustomer').on( 'page.dt',   function () { eventFired( 'Page' );
// } );
function refreshData(){
	// $("#tblCustomer").append('<tbody class="tblCustomer-error"><img src="{{ settings.BASE_URL }}/static/images/dataloader.gif"></tbody>');
    var dataTable = $('#tblCustomer').dataTable( {
        "stateSave": true,
        "destroy": true,
        "serverSide": true,
        // "aaSorting": [[0,'desc']],
        "order": [[ 0, 'desc' ]],
        "aoColumns":[
            {"bSortable": true},
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
            url :"paymentmethod_list_json",
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
    $( "." + formClass ).find("input,textarea").not( ":file" ).val('').trigger('change');
    $( "." + formClass ).find("select").val(0).trigger('change');
    $('.error-input').remove();
    $('.add_popupForm').find('.formResponse').removeClass('success-msg').removeClass('error-input').html("");
    $(".add_popupForm").find('input,select').prop('disabled', false);
    $(".add_popupForm").find('#submit-btn-form').show();
    $(".add_popupForm").find('#pass-blk').show();
    $(".add_popupForm").find('#users_av ').attr('src', "{% static 'images/avatar.jpg' %}");
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

                $('#profile_img').attr('src', e.target.result);
                $('input:hidden[name=profile_img]').val(e.target.result);
                $('#users_av ').attr('src', e.target.result);
            }
        };
        reader.readAsDataURL(input.files[0]);
        } else{
            $('.add_popupForm').find('#profile_img').val( "" );
            $('.add_popupForm').find('input:hidden[name=profile_img]').val( "" );
            $('#users_av ').attr('src', "{% static 'images/avatar.jpg' %}");
        }
        
        
    }
}

// $('#country').on('change',function(){
//         var countryID = $(this).val();
//         alert("countryID = "+countryID);
//         if(countryID !=0 || countryID){
//             var data = null;
//             var url = "{{ settings.WEBADMIN_URL }}" + "states/"+ countryID
//             serverCall(url, null, 'get', true, null, null, null, function (res) {
//                 if (res.length>0) {
//                     // var resp = $.parseJSON(data);alert(1);
//                     $.each(res, function(key, val){
//                         $.each(val, function(key1, val1){
//                             if(key1 == 'status' && val1 == true){
//                                 var html = '<option value="0">-- State --</option>';
//                                 $.each(res[key].data, function(key2, val2){
//                                     html += '<option value="'+ val2['id'] +'">'+ val2['state_name'] +'</option>';
//                                 });
//                                 $('#state').html(html); 
//                             } else if(key1 == 'status' && val1 == false){
//                                 $('#state').html('<option value="0">-- State --</option>');
//                             }
//                         });    
//                     });
//                 }
//             });
//         }else{
//             $('#state').html('<option value="0">-- State --</option>');
//         }
//     });