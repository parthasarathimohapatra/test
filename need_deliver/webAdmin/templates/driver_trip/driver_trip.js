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
        var url = "updateCancellationReasonActionRecords";
        serverCall(url, data, 'post', true, 'updateloader', null, null, function (res) {
            thisVal.attr('disabled',false);
            if(action == 'update' || action == 'rm'){refreshData('no');}
            if (res.length>0) {
                if(res[0].status == true){
                    $('#upRecords').modal('hide'); 
                    $('.multi_action').hide(); 
                    refreshData('no');
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
    refreshData('no');
    $('#start_date').datepicker({
        format: 'yyyy-mm-dd'
        }).on('changeDate', function(selected){
            $("#end_date").datepicker("option","minDate", selected);
            $(this).datepicker('hide');
    });
    $('#end_date').datepicker({
        format: 'yyyy-mm-dd'
        }).on('changeDate', function(selected){
            $(this).datepicker('hide');
            $("#start_date").datepicker("option","maxDate", selected)
    });
    // Date wise search call start
    $('#search').click(function(){
      var start_date = $('#start_date').val();
      var end_date = $('#end_date').val();
      if(start_date != '' && end_date !='')
      {
        if(start_date > end_date ) {
            alert("End date can not be less than start date");
        } else {
            $('#order_data').DataTable().destroy();
            refreshData('yes', start_date, end_date);
        }
       
      }
      else
      {

       alert("Both Date is Required");
      }
     });
    // Date wise search call end


    $('.date-picker').datepicker({
        format: 'yyyy-mm-dd',
        }).on('changeDate', function(e){
            $(this).datepicker('hide');
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
            $('#createModal').find('#modal_label').html("Update details");
            $(".add_popupForm").find('input,select').prop('disabled', false);
            $(".add_popupForm").find('#submit-btn-form').show();
            $(".add_popupForm").find('#pass-blk').show();
        }
        $(".add_popupForm").find('#pass-blk').hide();
        $(".add_popupForm").find(".not-editable").prop('disabled', true);
        var id = $( "#tblCustomer" ).find('input:hidden[name="id[]"]:checked').val();
        $(".add_popupForm").find('input:hidden[name=id]').val(id);
        var url = "drivertrip-details/"+ id ;
        serverCall(url, null, 'get', true, null, null, null, function (res) {
            $(".modal-body").show();
            $(".edit-data-load-content").hide();
          
           // return false;
            if (res.length>0) {
                if(res[0].status == true){
                    $( "input[name=contact_name]" ).val(res[0].data['order_details'].contact_name).trigger("change");
                    $( "input[name=contact_number]" ).val(res[0].data['order_details'].contact_number).trigger("change");
                    $( "input[name=supplier_name]" ).val(res[0].data['order_details'].supplier.first_name).trigger("change");
                    $( "input[name=driver_name]" ).val(res[0].data['order_details'].driver.first_name).trigger("change");
                    $( "input[name=location]" ).val(res[0].data['order_details'].location).trigger("change");

                    $( "input[name=location_1]" ).val(res[0].data['order_drop_off_location1'].location).trigger("change");
                    $( "input[name=item_name_1]" ).val(res[0].data['order_drop_off_location1'].item_name).trigger("change");
                    $( "input[name=contact_name_1]" ).val(res[0].data['order_drop_off_location1'].contact_name).trigger("change");
                    $( "input[name=contact_number_1]" ).val(res[0].data['order_drop_off_location1'].contact_number).trigger("change");
                    $( "input[name=note_to_driver_1]" ).val(res[0].data['order_drop_off_location1'].note_to_driver).trigger("change");
                    $( "input[name=cash_collection_1]" ).val(res[0].data['order_drop_off_location1'].cash_collection).trigger("change");

                    $( "input[name=location_2]" ).val(res[0].data['order_drop_off_location2'].location).trigger("change");
                    $( "input[name=item_name_2]" ).val(res[0].data['order_drop_off_location2'].item_name).trigger("change");
                    $( "input[name=contact_name_2]" ).val(res[0].data['order_drop_off_location2'].contact_name).trigger("change");
                    $( "input[name=contact_number_2]" ).val(res[0].data['order_drop_off_location2'].contact_number).trigger("change");
                    $( "input[name=note_to_driver_2]" ).val(res[0].data['order_drop_off_location2'].note_to_driver).trigger("change");
                    $( "input[name=cash_collection_2]" ).val(res[0].data['order_drop_off_location2'].cash_collection).trigger("change");
                    

                    $(".add_popupForm").find('.big-img-loader').each(function(){
                        $(this).after('<img class="rounded-circle z-depth-1-half avatar-pic" src="{% static 'images/big-img-loader.gif' %}" />') // some preloaded "loading" image
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
        var url =  "updateCancellationReasonRecords/";
        var method = 'POST';
        var reason = $("input[name=reason]").val();
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();

        var id = $(this).find('input:hidden[name=id]').val();
        
        if(id != ""){
            url += id+"/";
            method = 'PUT';
        }
        // var role = "{{ settings.IS_CUSTOMER }}";
        // alert(role);
        var data = {
            'reason': reason, 
            'is_status': 'TRUE',
            'csrftoken':csrftoken
        };
         serverCall(url, (data), method, true, 'formloader', null, null, function (res) {

            thisVal.find('[type=submit]').prop('disabled', false);
            if (res.length>0) {
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
                                refreshData('no');
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
function refreshData(is_date_search, start_date='', end_date=''){
    // $("#tblCustomer").append('<tbody class="tblCustomer-error"><img src="{{ settings.BASE_URL }}/static/images/dataloader.gif"></tbody>');
    var dataTable = $('#tblCustomer').DataTable( {
        "stateSave": false,
        "destroy": true,
        "serverSide": true,
        "order": [[0, "desc" ]],
        "aoColumns":[
            {"bSortable": false },
            {"bSortable": true},
            {"bSortable": false},
            {"bSortable": false},
            {"bSortable": true},
            {"bSortable": false},
            {"bSortable": true},
            {"bSortable": true},
            {"bSortable": true},
            {"bSortable": false},
         ],
        // "order": [ [0,'desc'] ],
        'columnDefs': [{
            'targets': 0,
            'searchable':true,
            'orderable':false,
            'responsive': true,
            "processing": true,
            "orderSequence": [ "desc" ], 
            'className': 'dt-center',
            'render': function (data, type, full, meta){
                    return '<label class="checkbox text-primary " ><input type="checkbox" class="singleCheck" name="id[]" value="' + $('<div/>').text(data).html() + '"><span class="check"></span></label>';
                }
        }],
        'columnDefs': [{ targets: [1], type: 'date'}],
        "drawCallback": function () {
            $('.dataTables_paginate > .pagination').addClass('pagination-circle pg-blue mb-0 justify-content-end');
            $('.dataTables_paginate > .pagination').find('li').addClass('page-item');
            $('.dataTables_paginate > .pagination').find('li>a').addClass('page-link waves-effect waves-effect');
        },
        "ajax":{
            beforeSend : function(data){
                $('.preloader-loader-content').remove();
                $("#tblCustomer").append('<tbody class="preloader-loader-content"><tr><th class="preload-datatable" colspan="10"><img class="datatable-loader" src="{% static 'images/dataloader.gif' %}"></th></tr></tbody>');
            },
            url :"drivertrip-list-json",
            type: "get",  // method  , by default get
            data:{
                 "is_date_search":is_date_search, "start_date":start_date, "end_date":end_date
                },
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
                    $(this).after('<img width="50" height="50" src="{% static 'images/big-img-loader.gif' %}" />') // some preloaded "loading" image
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
$( "body" ).on("click", ".btn-booking-details", function(){
        $(".modal-body").hide();
        $(".edit-data-load-content").show();
        $("#call_details").html('');
        var id = $(this).attr('data-id');
       
        // $('#createModal').find('#modal_label').html("Update language details");
        // alert("{{ settings.REST_URL }}")
        var url = "{{ settings.REST_URL }}" + "order_summary/"
        var dataVal = {"order_id": id }
        serverCall(url, dataVal, 'POST', true, null, null, null, function (res) {
            $(".modal-body").show();
            $(".edit-data-load-content").hide();
            // console.log(res.html_data);return false;
            $("#call_details").html(res.html_data)
            // if (res.length>0) {
            //     // var resp = $.parseJSON(data);alert(1);
            //     $.each(res, function(key, val){
            //         $.each(val, function(key1, val1){
            //             if(key1 == 'status' && val1 == true){
            //                 console.log(val1.html_data)
            //                 $("#call_details").html(val.html_data)
            //                 // $("#call_details").find('.big-img-loader').each(function(){
            //                 //     $(this).after('<img class="rounded-circle z-depth-1-half avatar-pic" src="{{ settings.BASE_URL }}/static/images/big-img-loader.gif" />') // some preloaded "loading" image
            //                 //    .hide()
            //                 //    .attr('src',this.src)
            //                 //    .one('load', function() {
            //                 //       $(this).fadeIn().next().remove();
            //                 //    });
            //                 // });
            //             }
            //         });    
            //     });
            // }
        });
        $('#createModal').modal('show'); 
    });
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

/* Custom filtering function which will filter data in column four between two values */
$.fn.dataTableExt.afnFiltering.push(
    function( oSettings, aData, iDataIndex ) {
        var iMin = document.getElementById('min').value * 1;
        var iMax = document.getElementById('max').value * 1;
        var iVersion = aData[5] == "-" ? 0 : aData[5]*1;
        if ( iMin == "" && iMax == "" )
        {
            return true;
        }
        else if ( iMin == "" && iVersion < iMax )
        {
            return true;
        }
        else if ( iMin < iVersion && "" == iMax )
        {
            return true;
        }
        else if ( iMin < iVersion && iVersion < iMax )
        {
            return true;
        }
        return false;
    }
);
