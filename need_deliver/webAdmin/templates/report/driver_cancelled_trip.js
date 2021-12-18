{% load staticfiles %}

$(function(){
    $("body").on("click", ".send_mail", function(){
        clearFormData('send_mail_popupForm');
        var rcvDetails = $( this ).attr("data-rcv");
        var id = $( this ).attr("data-id");
        $("#send_mail_popupForm").find("input[name=to_send]").val(rcvDetails).trigger("change");
        $("#send_mail_popupForm").find('input:hidden[name=id]').val(id);
    });
    
    
    // $("#profile_picture").change(function(){
    //     $("#users_av").hide();
    //     picture(this);
    // });
    // var picture_width;
    // var picture_height;
    // var crop_max_width = 300;
    // var crop_max_height = 300;
    // function picture(input) {
    //     if (input.files && input.files[0]) {
    //         var reader = new FileReader();
    //         reader.onload = function (e) {
    //             $("#jcrop, #preview").html("").append("<img src=\""+e.target.result+"\" alt=\"\" />");
    //             picture_width = $("#preview img").width();
    //             picture_height = $("#preview img").height();
    //             $("#jcrop  img").Jcrop({
    //                 onChange: canvas,
    //                 onSelect: canvas,
    //                 boxWidth: 300,
    //                 boxHeight: 300,
    //                 setSelect: [0,0,300,300],
    //                 aspectRatio: 300/300
    //             });
    //         }
    //         reader.readAsDataURL(input.files[0]);
    //     }

    // }
    // function canvas(coords){
    //     var imageObj = $("#jcrop img")[0];
    //     var canvas = $("#canvas")[0];
    //     canvas.width  = coords.w;
    //     canvas.height = coords.h;
    //     var context = canvas.getContext("2d");
    //     context.drawImage(imageObj, coords.x, coords.y, coords.w, coords.h, 0, 0, canvas.width, canvas.height);
    //     png();
    // }
    // function png() {
    //   var png = $("#canvas")[0].toDataURL('image/png');
    //   $("#profile_img_base").val(png);
    // }
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
        var url = "{{ settings.REST_URL }}" + "users_record_details/"+ id 
        serverCall(url, null, 'get', true, null, null, null, function (res) {
            $(".modal-body").show();
            $(".edit-data-load-content").hide();
            // console.log(res);return false;
            if (res.length>0) {
                // var resp = $.parseJSON(data);alert(1);
                $.each(res, function(key, val){
                    $.each(val, function(key1, val1){
                        if(key1 == 'status' && val1 == true){
                            alert(JSON.stringify(val.data.country));
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
        

        var url = "updateDriverUsersRecords";
        serverCall(url, data, 'post', true, 'updateloader', null, null, function (res) {
            thisVal.attr('disabled',false);
            if(action == 'update' || action == 'rm'){refreshData();}
            if (res.length>0) {
               

                // $.each(res, function(key, val){
                //     $.each(val, function(key1, val1){
                        if(res[0].status == true){
                            // console.log(res[key].countingInfo['allTeacher'])
                            if(action == 'update'){ 
                                //     $.each(res[0].countingInfo, function(key2, val2){
                                //     $.each(val2, function(key3, val3){
                                //         if(key3 == 'allTeachers'){
                                //             $( ".all-users" ).html(val3);
                                //         }
                                //         if(key3 == 'totalActiveTeachers'){
                                //             $( ".all-active-member" ).html(val3);
                                //         }
                                //         if(key3 == 'totalDeactiveTeachers'){
                                //             $( ".all-deactive-member" ).html(val3); 
                                //         }
                                //     });
                                //     $( "#selected_records" ).html(0);
                                // });
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
    $( "body" ).on("click", ".featured-btn", function(){
       
        var id = $(this).attr('data-id');
        var checkedVal = 0;
        if( $( this ).is(':checked') ){
            checkedVal = 1
        }
        var data = {'id' : id, 'is_featured' : checkedVal};
        var url = "{{ settings.REST_URL }}" + "teachers/" + id;
        serverCall(url, (data), 'patch', true, null, null, null, function (res) {
            if (res.length>0) {
                // var resp = $.parseJSON(data);alert(1);
                
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
            $('#createModal').find('#modal_label').html("Update driver details");
            $(".add_popupForm").find('input,select').prop('disabled', false);
            $(".add_popupForm").find('#submit-btn-form').show();
            $(".add_popupForm").find('#pass-blk').show();
        }
        $(".add_popupForm").find('#pass-blk').hide();
        $(".add_popupForm").find(".not-editable").prop('disabled', true);
        var id = $( "#tblCustomer" ).find('input:hidden[name="id[]"]:checked').val();
        $(".add_popupForm").find('input:hidden[name=id]').val(id);
        var url = "details_popup/"+ id ;
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

                            if( res[0].data.details_data.profile_picture != null || res[0].data.details_data.profile_picture ==''){
                                
                                $('#users_av').attr('src', res[0].data.details_data.profile_picture+ "?time="+ new Date($.now()) );
                                
                                var only_profile_pic = res[0].data.details_data.profile_picture.replace("https://diaxrbad0p1f6.cloudfront.net/static/", '');
                                

                                $( "input:hidden[name=profile_img_prev]" ).val(only_profile_pic).trigger("change");

                            }else{
                                $('#users_av').attr('src', "{% static 'images/avatar.jpg' %}"); 
                            }
                            // alert(JSON.stringify(res[0].data));
                            $( "input[name=first_name]" ).val(res[0].data.details_data.first_name).trigger("change");
                            $( "input[name=last_name]" ).val(res[0].data.details_data.last_name).trigger("change");
                            $( "input[name=email_id]" ).val(res[0].data.details_data.email_id).trigger("change");
                            $( "input[name=phone_number]" ).val(res[0].data.details_data.phone_number).trigger("change");
                            $( "input[name=dob]" ).val(res[0].data.details_data.dob).trigger("change");
                            $( "#password" ).val(res[0].data.password).trigger("change");   
                            // $( "select[name=duration]" ).val(val.data.duration).trigger("change");       
                            $( "textarea[name=description]" ).val(res[0].data.details_data.description).trigger("change");                      
                            // if(res[0].data.details_data.gender!= null){$( "select[name=gender]" ).val(res[0].data.details_data.gender.id).trigger("change");}
                            $( "input[name=city]" ).val(res[0].data.city).trigger("change");
                            $( "input[name=zipcode]" ).val(res[0].data.zipcode).trigger("change");
                            if(res[0].data.details_data.gender!= null){$( "select[name=gender]" ).val(res[0].data.details_data.gender).trigger("change");}
                            // alert(JSON.stringify(res[0].data.details_data));
                            // alert(JSON.stringify(res[0].data.details_data.country));
                            if(res[0].data.details_data.country!= null){$( "select[name=country]" ).val(res[0].data.details_data.country.id).trigger("change");}
                            // ############## driver_details ##############
                            $( "input[name=driving_licence_expiry_date]" ).val(res[0].data.driver_details.driving_licence_expiry_date).trigger("change");
                            if(res[0].data.driver_details.vehicle_type!= null){$( "select[name=vehicle_type]" ).val(res[0].data.driver_details.vehicle_type.id).trigger("change");}
                            // ############## vehicle_details ##############
                            if( res[0].data.vehicle_details.image_file != null || res[0].data.vehicle_details.image_file ==''){
                                
                                $('#vehicle_preview').attr('src', res[0].data.vehicle_details.image_file+ "?time="+ new Date($.now()) );
                                
                            }else{
                                $('#vehicle_preview').attr('src', "{% static 'images/avatar.jpg' %}"); 
                            }
                            // $( "input[name=wheel_chair_support]" ).attr("checked",false);
                            // $( "input[name=booster_seat_support]" ).attr("checked",false);
                            // alert("wheel "+res[0].data.vehicle_details.wheel_chair_support);
                            // alert("booster_seat_support "+res[0].data.vehicle_details.booster_seat_support);
                            
                            if(res[0].data.vehicle_details.vehicle_model!= null){$( "select[name=vehicle_model]" ).val(res[0].data.vehicle_details.vehicle_model.id).trigger("change");}
                            $( "input[name=plate_number]" ).val(res[0].data.vehicle_details.plate_number).trigger("change");
                            $( "input[name=registration_expiry_date]" ).val(res[0].data.vehicle_details.registration_expiry_date).trigger("change");
                            $( "input[name=insurance_expiry_date]" ).val(res[0].data.vehicle_details.insurance_expiry_date).trigger("change");
                            if(res[0].data.vehicle_details.year!= null){$( "select[name=year]" ).val(res[0].data.vehicle_details.year).trigger("change");}
                            if(res[0].data.vehicle_details.wheel_chair_support== true){$( '#wheel_chair_support' ).prop("checked",true);}
                            if(res[0].data.vehicle_details.booster_seat_support== true){$( '#booster_seat_support' ).prop("checked",true);}
                        
                            // ############## Start Driver licence multiple file show ##########
                            $("#driver_licence_files" ).empty();
                            $("#driver_licence_existing_files" ).empty();
                            var driver_licence_existing_file_count = 0;
                            $.each(res[0].data.driverAttachments[0], function( key, file_value ) {
                                if(key == 1) {
                                    $.each(file_value, function(key, value){
                                        driver_licence_existing_file_count++;
                                        
                                        $( "#driver_licence_existing_files" ).append($("<div class=\"ins_pip\">" +
                                        "<img class=\"imageThumb\" src=\"{% static 'images/pdf.png' %}\" height=\"100px\" width=\"100px\">" +
                                        "<br/><span class=\"remove\" onclick=\"deleteAttachment('"+value+"','driving_licence')\">x</span>" +
                                        "</div>"));
                                      $(".remove").click(function(){
                                        $(this).parent(".ins_pip").remove();
                                      });
                                    });
                                }
                            });
                            $.each(res[0].data.driverAttachments[1], function( key, file_value ) {
                                if(key == 1) {
                                    $.each(file_value, function(key, value){
                                        driver_licence_existing_file_count++;
                                        $( "#driver_licence_existing_files" ).append( $("<div class=\"ins_pip\">" +
                                        "<img class=\"imageThumb\" src=\"" + value + "\"  height=\"100px\" width=\"100px\">" +
                                        "<span class=\"remove\" onclick=\"deleteAttachment('"+value+"','driving_licence')\">x</span>" +
                                        "</div>") );
                                      $(".remove").click(function(){
                                        $(this).parent(".ins_pip").remove();
                                      });
                                    });
                                }
                            });

                            // ############## Start vehicle Registration multiple file show ##########
                             
                            $( "#vehicle_reg_files" ).empty();
                            $( "#vehicle_reg_existing_files" ).empty();
                            var vehicle_existing_file_count = 0;
                            $.each(res[0].data.vehicleRegistration[0], function( key, file_value ) {
                                if(key == 1) {
                                    $.each(file_value, function(key, value){
                                        vehicle_existing_file_count++;
                                        
                                        $( "#vehicle_reg_existing_files" ).append($("<div class=\"ins_pip\">" +
                                        "<img class=\"imageThumb\" src=\"{% static 'images/pdf.png' %}\" height=\"100px\" width=\"100px\">" +
                                        "<br/><span class=\"remove\" onclick=\"deleteAttachment('"+value+"','vehicle_reg')\">x</span>" +
                                        "</div>"));
                                      $(".remove").click(function(){
                                        $(this).parent(".ins_pip").remove();
                                      });
                                    });
                                }
                            });
                            $.each(res[0].data.vehicleRegistration[1], function( key, file_value ) {
                                if(key == 1) {
                                    $.each(file_value, function(key, value){
                                        vehicle_existing_file_count++;
                                        $( "#vehicle_reg_existing_files" ).append($("<div class=\"ins_pip\">" +
                                        "<img class=\"imageThumb\" src=\"" + value + "\"  height=\"100px\" width=\"100px\">" +
                                        "<br/><span class=\"remove\" onclick=\"deleteAttachment('"+value+"','vehicle_reg')\">x</span>" +
                                        "</div>"));
                                      $(".remove").click(function(){
                                        $(this).parent(".ins_pip").remove();
                                      });
                                    });
                                }
                            });

                            
                            // ############## Start Vehicle Insurance multiple file show ##########
                            // $('.add_popupForm').find('.vehicle_ins').removeClass('vehicle_ins');
                            $( "#vehicle_insurance_files" ).empty();
                            $( "#vehicle_insurance_existing_files" ).empty();
                            var vehicle_insurance_files_count = 0;
                            $.each(res[0].data.vehicleInsurance[0], function( key, file_value ) {
                                if(key == 1) {
                                    $.each(file_value, function(key, value){
                                        vehicle_insurance_files_count++;
                                        
                                        $( "#vehicle_reg_existing_files" ).append($("<div class=\"vehicle_ins\">" +
                                        "<img class=\"imageThumb\" src=\"{% static 'images/pdf.png' %}\" height=\"100px\" width=\"100px\">" +
                                        "<br/><span class=\"remove\" onclick=\"deleteAttachment('"+value+"','vehicle_ins')\">x</span>" +
                                        "</div>"));
                                      $(".remove").click(function(){
                                        $(this).parent(".vehicle_ins").remove();
                                      });
                                    });
                                }
                            });
                            $.each(res[0].data.vehicleInsurance[1], function( key, file_value ) {
                                if(key == 1) {
                                    $.each(file_value, function(key, value){
                                        vehicle_insurance_files_count++;
                                      $( "#vehicle_insurance_existing_files" ).append($("<div class=\"vehicle_ins\">" +
                                        "<img class=\"imageThumb\" src=\"" + value + "\"  height=\"100px\" width=\"100px\">" +
                                        "<br/><span class=\"remove\" onclick=\"deleteAttachment('"+value+"','vehicle_ins')\">x</span>" +
                                        "</div>"));
                                      $(".remove").click(function(){
                                        $(this).parent(".vehicle_ins").remove();
                                      });
                                    });
                                }
                            });

                             // alert("vehicle_existing_file = "+vehicle_existing_file_count);
                            $('#count_of_driver_licence_existing_files').val(driver_licence_existing_file_count);
                            $('#count_of_vehicle_reg_existing_files').val(vehicle_existing_file_count);
                            $('#count_of_vehicle_insurance_existing_files').val(vehicle_insurance_files_count);

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
        var url =  "updateCustomerRecords/";
        var method = 'POST';
        // var first_name = $("input[name=first_name]").val();
        // var last_name = $("input[name=last_name]").val();
        // var email_id = $("input[name=email_id]").val();
        // var phone_number = $("input[name=phone_number]").val();
        // var country = $("select[name=country]").val();
        // var state = $("select[name=state]").val();
        // var city = $("input[name=city]").val();
        // var zipcode = $("input[name=zipcode]").val();
        // // var description = $("textarea[name=description]").val();
        // var description = $('textarea#description').val();

        // var vehicle_type = $("select[name=vehicle_type]").val();
        // var vehicle_number = $("input[name=vehicle_number]").val();
        // var vehicle_note = $('textarea#vehicle_note').val();


        var id = $(this).find('input:hidden[name=id]').val();
        
        if(id != ""){
            url += id+"/";
            method = 'PUT';
        }
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();

        // var data = {
        //     'email_id': email_id, 
        //     'first_name': first_name, 
        //     'last_name': last_name, 
        //     'phone_number': phone_number, 
        //     'country': country,
        //     'state': state,
        //     'city': city,
        //     'zipcode': zipcode,
        //     'description': description,
        //     'csrftoken':csrftoken,

        //     'vehicle_type': vehicle_type,
        //     'vehicle_number': vehicle_number,
        //     'vehicle_note': vehicle_note
        // };
       
        //  console.log(data);
        //  serverCall(url, (data), method, true, 'formloader', null, null, function (res) {

        var myForm = document.getElementById('driver_form');
        var formData = new FormData(this);
        // formData.append('is_status', 'TRUE');
        // formData.append('csrfmiddlewaretoken', csrftoken);
        // formData.append('profile_picture', $('#profile_picture')[0].files[0]);



        formData.append('is_status', 'TRUE');
        formData.append('is_phone_no_verified', 'TRUE');
        formData.append('csrfmiddlewaretoken', csrftoken);

        formData.append('profile_picture', $('#profile_picture')[0].files[0]);
        formData.append('image_file', $('#image_file')[0].files[0]);
        if( $('#wheel_chair_support').is(":checked"))
        {
            formData.append('wheel_chair_support', 'TRUE');
        }
        if( $('#booster_seat_support').is(":checked"))
        {
            formData.append('booster_seat_support', 'TRUE');
        }


        var ins = document.getElementById('driver_licence').files.length;
        for (var x = 0; x < ins; x++) {
            formData.append("driver_licence", document.getElementById('driver_licence').files[x]);
        }

        var ins_no = document.getElementById('vehicle_insurance').files.length;
        for (var x = 0; x < ins_no; x++) {
            formData.append("vehicle_insurance", document.getElementById('vehicle_insurance').files[x]);
        }

        var ins_no = document.getElementById('vehicle_registration').files.length;
        for (var x = 0; x < ins_no; x++) {
            formData.append("vehicle_registration", document.getElementById('vehicle_registration').files[x]);
        }


        // serverCall(url, formData, method, true, 'formloader', null, true, function (res) {
        
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
        'country' : 'Country'
    }

    var fields = $('input.required');
    var select_fields = $('select.required');
    $("." + idVal).find(".error-input").remove();
    var flag = false;
    for(var i=0;i<fields.length;i++){
        var fieldName = fields[i].name;
        var fieldId = fields[i].id;
        var fieldVal = $(fields[i]).val();

        // if($(fields[i]).val() == ''){
        //     $( "input[name='"+fieldName+"']" ).addClass('eq-ui-input invalid');
        //     $( "input[name='"+fieldName+"']").after("<span class='error-input'>" + errorFields[fieldName] + " can not be blank.<span>");
        //     flag = true;
        // }
        if($(fields[i]).val() == ''){
            $( "#"+fieldId).addClass('eq-ui-input invalid');
            $( "#"+fieldId).after("<span class='error-input'>" + errorFields[fieldId] + " can not be blank.<span>");
            flag = true;
        }
        else if(fieldName == "phone_number" && fieldVal!= '') {
            if($( "#user_id").val() ==""){
                var data = {'phone_number': fieldVal};
                var url = "checkUniquePhone";
                
                // document.getElementById("next").style.display = "none";
                 serverCall(url, data, 'post', true, 'updateloader', null, null, function (res) {
                    // thisVal.attr('disabled',false);
                    
                    // alert("res.status= "+res[0].status);
                    
                    // alert("res.msg= "+res.msg);
                    if (res[0].status == false) {
                        document.getElementById("basicinfo_tab").className += " active";
                        document.getElementById("driverinfo_tab").className   = document.getElementById("driverinfo_tab").className.replace(" active", "");
                        document.getElementById("basicinfo").style.display = "block";
                        document.getElementById("driverinfo").style.display = "none";
                        document.getElementById("vehicleinfo").style.display = "none";
                        // alert("res.status= "+JSON.stringify(res));
                        $( "#"+fieldId).addClass('eq-ui-input invalid');
                        $( "#"+fieldId).after("<span class='error-input'>" + res[0].msg + "<span>");
                        flag = true;

                               
                    } else {
                        flag = false;
                        // document.getElementById("next").style.display = "block";
                    }
                    
                });

            }
            

        }
        if( fieldName == "email_id" && fieldVal!= ''){
            if(emailRestrict(fieldVal) == false){
                $( "input[name='"+fieldName+"']" ).addClass('eq-ui-input invalid');
                $( "input[name='"+fieldName+"']" ).after("<span class='error-input'>Please enter valid Email Id</span>");
                flag = true;
            }
        }
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
            {"bSortable": false},
        ],
        'columnDefs': [{
            'targets': 0,
            'searchable':true,
            'orderable':true,
            'responsive': true,
            "processing": true,
            
            'className': 'dt-center',
            // 'render': function (data, type, full, meta){
            //         return '<label class="checkbox text-primary " ><input type="checkbox" class="singleCheck" name="id[]" value="' + $('<div/>').text(data).html() + '"><span class="check"></span></label>';
            //     }
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
            url :"driver_cancelled_trip_json",
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

$(document).ready(function() {
    // $("#phone_number").blur(function(){
    //   $.ajax({url: '/my/data', type: 'GET'})
    //   .done(function(response){
    //     $("#my_div").html(response);
    //   })
    // })
    $("body").on('keypress', '.phone-number',function (event) {
     alert(event.which);
        value = $(this).val() //Allowed 0-9 + - back space arrow
        if((event.which >= 48 && event.which <=57) || (event.which == 43) || (event.which == 45)|| (event.which == 0)|| (event.which == 8)) {
          
          return true; 
        } // prevent if not number/dot
        else {
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
        // $(handle).on(eventType, function () {
        //     if ($(target).prop("type") == text) {
        //         $(target).prop("type", typeChange);
        //     } else {
        //         $(target).prop("type", targetType);
        //     }
        // })
    });
  if (window.File && window.FileList && window.FileReader) {
    $("#driver_licence").on("change", function(e) {
        var driver_licence_exisiting_count = $('#count_of_driver_licence_existing_files').val();
        var total_file =  ($("#driver_licence")[0].files.length)+parseInt(driver_licence_exisiting_count);
        if(total_file <= 5) {
          $('#count_of_driver_licence_existing_files').val(total_file);
          document.getElementById("fp").style.display = "none";
     //               alert("You can select only 2 images");
          var files = e.target.files,
            filesLength = files.length;
          for (var i = 0; i < filesLength; i++) {
            var f = files[i];
            filesLength = files.length;
            var file_size = f.size;
            var file_name = f.name;

            var ext = file_name.split('.').pop().toLowerCase();
               
            //Allowed file types
            if($.inArray(ext, ['gif','png','jpg','jpeg', 'pdf']) == -1) {
                    alert('The file type is invalid!');
                    $('#vehicle_registration').val("");
                    document.getElementById('fp').innerHTML ='<span style="color:red;">The file type is invalid</span>';
            }
            var file_size = f.size;
            if(file_size<10000000) {
                if(ext == "pdf") {
                    var fileReader = new FileReader();
                    fileReader.onload = (function(e) {
                        var file = e.target;
                        $( "#driver_licence_files" ).append($("<div class=\"ins_pip\">" +
                "<img class=\"imageThumb\" src=\"{% static 'images/pdf.png' %}\" title=\"" + file.name + "\" height=\"100px\" width=\"100px\">" +
                "<br/><span class=\"remove\">x</span>" +
                "</div>"));
                        $(".remove").click(function(){
                            $(this).parent(".ins_pip").remove();
                        });
                    });

                } else {
                    var fileReader = new FileReader();
                    fileReader.onload = (function(e) {
                      var file = e.target;
                        $( "#driver_licence_files" ).append( $("<div class=\"ins_pip\">" +
                        "<img class=\"imageThumb\" src=\"" + e.target.result + "\" title=\"" + file.name + "\"/ height=\"100px\" width=\"100px\">" +
                        "<br/><span class=\"remove\">x</span>" +
                        "</div>") );
                        $(".remove").click(function(){
                            $(this).parent(".ins_pip").remove();
                          });
                    });
                }
            }
            else {
                document.getElementById("fp").style.display = "block";
                document.getElementById('fp').innerHTML ='<span style="color:red;">You can not upload more than 5 files</span>';
            }

            fileReader.readAsDataURL(f);
          }
      }
      else {
        $("#driver_licence").val(null);
        document.getElementById("fp").style.display = "block";
        document.getElementById('fp').innerHTML ='<span style="color:red;">You can not upload more than 5 files</span>';
      }

    });
    $("#vehicle_insurance").on("change", function(e) {

        var count_of_vehicle_insurance_count = $('#count_of_vehicle_insurance_existing_files').val();
        var total_file =  ($("#vehicle_insurance")[0].files.length)+parseInt(count_of_vehicle_insurance_count);
       
        if(total_file <= 5) {
          $('#count_of_vehicle_insurance_existing_files').val(total_file);
          document.getElementById("err_ins").style.display = "none";
          
          var files = e.target.files,
          filesLength = files.length;
          for (var i = 0; i < filesLength; i++) {
            var f = files[i];
            ext = "";


            var file_size = f.size;
            var file_name = f.name;

            var ext = file_name.split('.').pop().toLowerCase();
               
            //Allowed file types
            if($.inArray(ext, ['gif','png','jpg','jpeg', 'pdf']) == -1) {
                    alert('The file type is invalid!');
                    $('#vehicle_registration').val("");
                    document.getElementById('err_ins').innerHTML ='<span style="color:red;">The file type is invalid</span>';
            }
            var file_size = f.size;
            if(file_size<10000000) {
                if(ext == "pdf") {
                    var fileReader = new FileReader();
                    fileReader.onload = (function(e) {
                        var file = e.target;
                        $( "#vehicle_insurance_files" ).append($("<div class=\"vehicle_ins\">" +
                "<img class=\"imageThumb\" src=\"{% static 'images/pdf.png' %}\" title=\"" + file.name + "\" height=\"100px\" width=\"100px\">" +
                "<br/><span class=\"remove\">x</span>" +
                "</div>"));
                        $(".remove").click(function(){
                            $(this).parent(".vehicle_ins").remove();
                        });
                    });

                } else {
                    var fileReader = new FileReader();
                    fileReader.onload = (function(e) {
                      var file = e.target;

                      $( "#vehicle_insurance_files" ).append($("<div class=\"vehicle_ins\">" +
                        "<img class=\"imageThumb\" src=\"" + e.target.result + "\" title=\"" + file.name + "\"/ height=\"100px\" width=\"100px\">" +
                        "<br/><span class=\"remove\">x</span>" +
                        "</div>"));
                      $(".remove").click(function(){
                        $(this).parent(".vehicle_ins").remove();
                      });
                    });
                }
            }
            else {
                document.getElementById("err_ins").style.display = "block";
                document.getElementById('err_ins').innerHTML ='<span style="color:red;">You can not upload more than 10 mb</span>';
            }

            fileReader.readAsDataURL(f);
          }
      }
      else {
        $("#vehicle_insurance").val(null);
        document.getElementById("err_ins").style.display = "block";
        document.getElementById('err_ins').innerHTML ='<span style="color:red;">You can not upload more than 5 files</span>';
      }

    });
    $("#vehicle_registration").on("change", function(e) {

        var count_of_vehicle_reg_existing_files = $('#count_of_vehicle_reg_existing_files').val();
        var total_file =  ($("#vehicle_registration")[0].files.length)+parseInt(count_of_vehicle_reg_existing_files);
        if(total_file <= 5) {
          $('#count_of_vehicle_reg_existing_files').val(total_file);
          $( "#vehicle_reg_files" ).empty();
            
          document.getElementById("err_reg").style.display = "none";
     //               alert("You can select only 2 images");
          var files = e.target.files,
            filesLength = files.length;
          for (var i = 0; i < filesLength; i++) {
            var f = files[i];
            ext = "";


            var file_size = f.size;
            var file_name = f.name;

            var ext = file_name.split('.').pop().toLowerCase();
               
            //Allowed file types
            if($.inArray(ext, ['gif','png','jpg','jpeg', 'pdf']) == -1) {
                    alert('The file type is invalid!');
                    $('#vehicle_registration').val("");
                    document.getElementById('err_reg').innerHTML ='<span style="color:red;">The file type is invalid</span>';
            }

            if(file_size<10000000) {
                if(ext == "pdf") {
                    var fileReader = new FileReader();
                    fileReader.onload = (function(e) {
                        var file = e.target;
                        $( "#vehicle_reg_files" ).append($("<div class=\"ins_pip\">" +
                "<img class=\"imageThumb\" src=\"{% static 'images/pdf.png' %}\" title=\"" + file.name + "\" height=\"100px\" width=\"100px\">" +
                "<br/><span class=\"remove\">x</span>" +
                "</div>"));
                        $(".remove").click(function(){
                            $(this).parent(".ins_pip").remove();
                        });
                    });

                } else {
                    var fileReader = new FileReader();
                    fileReader.onload = (function(e) {
                    var file = e.target;
                    // var fileType = f["type"];
                        $( "#vehicle_reg_files" ).append($("<div class=\"ins_pip\">" +
                    "<img class=\"imageThumb\" src=\"" + e.target.result + "\" title=\"" + file.name + "\"/ height=\"100px\" width=\"100px\">" +
                    "<br/><span class=\"remove\" >x</span>" +
                    "</div>"));
                    $(".remove").click(function(){
                        $(this).parent(".ins_pip").remove();
                      });
                    });

                }
            }
            else {
                document.getElementById("err_reg").style.display = "block";
                document.getElementById('err_reg').innerHTML ='<span style="color:red;">You can not upload more than 10 mb</span>';
            }

            fileReader.readAsDataURL(f);
          }
      }
      else {
        $("#vehicle_registration").val(null);
        document.getElementById("err_reg").style.display = "block";
        document.getElementById('err_reg').innerHTML ='<span style="color:red;">You can not upload more than 5 files</span>';
      }

    });
  } else {
    alert("Your browser doesn't support to File API")
  }
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


