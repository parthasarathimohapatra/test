
$(function(){

    /*------------------------------------ Order Bookings by Vehicle chart -------------------------------*/
    var vehicleNames = '{{vehicleTypeName}}';
    vehicleNames = vehicleNames.split("||")
    tmpData = []
    for (var i = 0; i < vehicleNames.length; i++) {
       tmpRow =  vehicleNames[i].split('~')

       tmpData.push({'name' : tmpRow[1], 'y' : parseInt(tmpRow[0]) })
    }
    Highcharts.chart('container', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Bookings by Vehicle Type'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: 'Orders',
            colorByPoint: true,
            data: tmpData

        }]
    });
    /*------------------------------------ Order Bookings by Vehicle chart End -------------------------------*/
    /*------------------------------------ No of calls From --------------------------------------------------*/


    var start = moment().subtract(6, 'days');
    var end = moment();

    function cb(start, end) {
        // $("#no_of_call_graph").hide();
        $('#reportrange_pie span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        // console.log(start.format('Y-MM-DD') + "~~~"+ end.format('Y-MM-DD'))
        // refreshData(start.format('Y-MM-DD'), end.format('Y-MM-DD'));
        $("#daterange_pie").val(start.format('Y-MM-DD')+ "||" +end.format('Y-MM-DD'))
        var startDate = start.format('Y-MM-DD');
        var endDate = end.format('Y-MM-DD');
        var data = { 'startDate' : startDate, 'endDate': endDate, 'graph_type' : 2};
        var url = "regTimeInterval";
        $(".no_of_call_graph_loader").show()
        serverCall(url, data, 'post', true, null, null, null, function (res) {
            if (res.length>0) {
                $(".no_of_call_graph_loader").hide()
                $.each(res, function(key, val){
                    $.each(val, function(key1, val1){
                        if(key1 == 'status' && val1 == true){
                            no_of_booking_with_timeInterval(val.data, startDate, endDate)
                            $("#no_of_call_graph").show();

                        } 
                    });    
                });
            }
                
        });
    }
    $('#reportrange_pie').daterangepicker({

        opens: 'left',
        startDate: start,
        endDate: end,
        maxDate: new Date(),
        "maxSpan": {
            "days": 60
        },
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);

    function no_of_booking_with_timeInterval(dataVal, startDate, endDate ){
// Create the chart
        Highcharts.chart('no_of_call_graph', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'No of calls From '+ startDate + ' To '+ endDate
            },
            // subtitle: {
            //     text: 'Click the columns to view versions. Source: <a href="http://statcounter.com" target="_blank">statcounter.com</a>'
            // },
            xAxis: {
                type: 'category'
            },
            yAxis: {
                title: {
                    text: 'Total calls'
                }

            },
            legend: {
                enabled: false
            },
            plotOptions: {
                series: {
                    borderWidth: 0,
                    dataLabels: {
                        enabled: true,
                        format: '{point.y}'
                    }
                }
            },

            tooltip: {
                headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
            },

            "series": [
                {
                    "name": "Languages",
                    "colorByPoint": true,
                    "data": dataVal
                }
            ],
        
        });
    }
/*------------------------------------ No of calls From End --------------------------------------------------*/
/*------------------------------------ Percentage of payment w.r.t Payment Gateways --------------------------------------------------*/
//     toGetPercentageOfPaymentByGateway()
//     function toGetPercentageOfPaymentByGateway(){
        
//         var data = { 'graph_type' : 3};
//         var url = "regTimeInterval";
//         $(".no_of_call_graph_payment_loader").show()
//         serverCall(url, data, 'post', true, null, null, null, function (res) {
//             if (res.length>0) {
//                 $(".no_of_call_graph_payment_loader").hide()
//                 $.each(res, function(key, val){
//                     $.each(val, function(key1, val1){
//                         if(key1 == 'status' && val1 == true){
//                            persentage_payment_each_gateway(val.data)

//                         } 
//                     });    
//                 });
//             }
                
//         });
//     }
//     function persentage_payment_each_gateway( dataVal ){
// // Create the chart
//         Highcharts.chart('persentage_payment_each_gateway', {
//             chart: {
//                 type: 'column'
//             },
//             title: {
//                  text: 'Percentage of payment w.r.t Payment Gateways'
//             },
//             // subtitle: {
//             //     text: 'Click the columns to view versions. Source: <a href="http://statcounter.com" target="_blank">statcounter.com</a>'
//             // },
//             xAxis: {
//                 type: 'category'
//             },
//             yAxis: {
//                 title: {
//                     text: 'Percentage amount'
//                 }

//             },
//             legend: {
//                 enabled: false
//             },
//             plotOptions: {
//                 series: {
//                     borderWidth: 0,
//                     dataLabels: {
//                         enabled: true,
//                         format: '{point.y:.1f}%'
//                     }
//                 }
//             },

//             tooltip: {
//                 headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
//                 pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.1f}%</b> of total<br/>'
//             },

//             "series": [
//                 {
//                     "name": "Languages",
//                     "colorByPoint": true,
//                     "data": dataVal
//                 }
//             ],
            
//         });
//     }
/*------------------------------------ Percentage of payment w.r.t Payment Gateways End --------------------------------------------------*/
/*------------------------------------ Number of supplier and driver registered on a given time period --------------------------------------------------*/
    $("body").on('click', "input[name=user_filter]", function(){
        var startEnd = $("#no_of_supplier_reg_range_hidden").val();
        var user_type = $("input[name=user_filter]:checked").val();
        startEnd = startEnd.split("||")
        if( user_type == 3){
            chart.title.text ='Some Positive Title';
        }
        var data = { 'startDate' : startEnd[0], 'endDate': startEnd[1], 'graph_type' : 4, 'user_type' : user_type};
        var url =  "regTimeInterval";
        $(".no_of_students_reg_loader").show()
        serverCall(url, data, 'post', true, null, null, null, function (res) {
            if (res.length>0) {
            	// alert("data"+JSON.stringify(res));
                $(".no_of_students_reg_loader").hide()
                $.each(res, function(key, val){
                    $.each(val, function(key1, val1){
                        if(key1 == 'status' && val1 == true){

                            no_of_user_reg_with_timeInterval(val.data, startEnd[0], startEnd[1])
                            $("#no_of_users_reg_graph").show();

                        } 
                    });    
                });
            }
                
        });
    });
    function cb2(start, end) {
        $('#no_of_supplier_reg_range span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        $("#no_of_supplier_reg_range_hidden").val(start.format('Y-MM-DD')+ "||" +end.format('Y-MM-DD'))
        var startDate = start.format('Y-MM-DD');
        var endDate = end.format('Y-MM-DD');
        var user_type = $("input[name=user_filter]:checked").val()
        var data = { 'startDate' : startDate, 'endDate': endDate, 'graph_type' : 4, 'user_type' : user_type};
        var url =  "regTimeInterval";
        $(".no_of_students_reg_loader").show()
        serverCall(url, data, 'post', true, null, null, null, function (res) {
            if (res.length>0) {
                $(".no_of_students_reg_loader").hide()
                $.each(res, function(key, val){
                    $.each(val, function(key1, val1){
                        if(key1 == 'status' && val1 == true){

                            no_of_user_reg_with_timeInterval(val.data, startDate, endDate)
                            $("#no_of_users_reg_graph").show();

                        } 
                    });    
                });
            }
                
        });
    }
    $('#no_of_supplier_reg_range').daterangepicker({
 
        opens: 'right',
        startDate: start,
        endDate: end,
        maxDate: new Date(),
        "maxSpan": {
            "days": 60
        },
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb2);

    cb2(start, end);
    function no_of_user_reg_with_timeInterval(dataVal, startDate, endDate ){
    var user_type = $("input[name=user_filter]:checked").val();
    var someFlag = true;
    var chartTitle =  'No of suppliers registered from '+ startDate + ' - '+ endDate;

    if(user_type == 3){
      chartTitle = 'No of drivers registered from '+ startDate + ' - '+ endDate;
    }

// Create the chart
    chart = Highcharts.chart('no_of_users_reg_graph', {
            chart: {
                type: 'column'
            },
            title: {
                text: chartTitle
            },
            // subtitle: {
            //     text: 'Click the columns to view versions. Source: <a href="http://statcounter.com" target="_blank">statcounter.com</a>'
            // },
            xAxis: {
                type: 'category'
            },
            yAxis: {
                title: {
                    text: 'No of registration'
                }

            },
            legend: {
                enabled: false
            },
            plotOptions: {
                series: {
                    borderWidth: 0,
                    dataLabels: {
                        enabled: true,
                        format: '{point.y}'
                    }
                }
            },

            tooltip: {
                headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
            },

            "series": [
                {
                    "name": "Users",
                    "colorByPoint": true,
                    "data": dataVal,
                    // maxPointWidth: 50
                }
            ],
            
       
        });
    }
    
});
