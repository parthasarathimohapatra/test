var app = require("express")();
var http = require("http").Server(app);
var io = require("socket.io")(http, {"pingInterval": 3000, "pingTimeout": 4000});
var diff = require("deep-diff").diff;
var pg = require("pg");
var request = require('request');
var in_array = require("in_array");
var customServices = require("./services/Services.js");
var customModel = require("./model/Model.js");
var constants = require("./constants/Constants.js");
var envConst = require("./constants/env.js");
var restApiBaseUrl = global.REST_URL;
var suplierApiUrl = restApiBaseUrl + "/supplierAppApi/";
var moment = require("moment-timezone");
var now = moment();
var formatted = moment.tz(now,"Asia/Kolkata");
var nodemailer = require('nodemailer');
const interval = require('interval-promise')
var transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'soumya.sengupta@navsoft.in',
    pass: 'zxcvbnm!@'
  }
});

// var sqlite3 = require("sqlite3").verbose();
// var db = new sqlite3.Database(":memory:");
const haversine = require("haversine");
var distance = require("google-distance");
distance.apiKey = "AIzaSyDOZCiwPSXUm58TOjViGXwbsfKYkP6t0jw";
// require("events").EventEmitter.defaultMaxListeners = 0;
// const log = require('simple-node-logger').createSimpleLogger(); 
fs = require('fs');

// require('crashreporter').configure({
//     mailEnabled: true,
//     mailTransportName: 'SMTP',
//     hiddenAttributes: [ 'error', 'dateTime', 'processTitle', 'activeHandle', 'activeRequest'],
//     mailTransportConfig: {
//         service: 'Gmail',
//         auth: {
//             user: "arijit.chandra@navsoft.in",
//             pass: "break690"
//         }
//     },
//     mailSubject: 'NEED DELIVER Crash Report',
//     mailFrom: 'crashreporter <arijit.chandra@navsoft.in>',
//     mailTo: 'arijit.chandra@navsoft.in'
// });
	// abc = moment.utc(formatted.toDate()).toDate().toLocaleString()
// abc = abc.replace("T", " ")
// console.log(abc)
// import HaversineGeolocation from "haversine-geolocation";
// var justAGuy = new Services()
// var conString = "postgres://postgres:navsoftpsql@54.86.98.240/flooant";

// var client = new pg.Client(conString);
// var config = {
//   user: "postgres", //env var: PGUSER
//   database: "flooant", //env var: PGDATABASE
//   password: "navsoftpsql", //env var: PGPASSWORD
//   host: "192.168.0.65", // Server hosting the postgres database
//   port: 5432, //env var: PGPORT
//   max: 10000, // max number of clients in the pool
//   idleTimeoutMillis: 30000, // how long a client is allowed to remain idle before being closed
// };

// console.log(abc)

function remove(array, element) {
    const index = array.indexOf(element);
    array.splice(index, 1);
}
var deleteMe = function( arr, me ){
   var i = arr.length;
   while( i-- ) if(arr[i] === me ) arr.splice(i,1);
}
var users = [];
io.on("connection", function(socket) {
	
	// console.log(socket.id)
/*********************** This event is fired borderStyle: "solid" "dotted" "dashed"  Supplier when he press on the confirm booking( at the time of searching driver api) ************************************/
	socket.on("set_customer_id_before_booking", function(data){
			global.orderUsersIds[data.user_id] = socket.id

			io.emit("testing", global.orderUsersIds);
	});
	socket.on("current_location_after_booking_accpt", function(data){
		// console.log("@@@@@@@@@")
		if(Object.keys(global.orderUsersIds).length>0){
			// console.log(data)
			// if(in_array(data["supplier_id"], global.orderUsersIds)){
				var supplierSocket = global.orderUsersIds[data["supplier_id"]];
				var supplierDatails = {};
				supplierDatails['latitude'] = data["pickup_latitude"]
				supplierDatails['longitude'] = data["pickup_longitude"]
				var driverDetails = {};
				driverDetails['latitude'] = data["driver_latitude"]
				driverDetails['longitude'] = data["driver_longitude"]
				// , driverDetails
				customServices.sendCurrentDriverLocation(supplierDatails, driverDetails, function(res){
					if(res){
						io.to(supplierSocket).emit("track_driver_route", {"latitude": data["driver_latitude"], "longitude" : data["driver_longitude"], "distance":res["driver"]["distance"], 'estimated_time':res["driver"]['estimated_time'], 'vehicle_logo': data["vehicle_logo"] });	
						// io.emit("test_track", {"latitude": data["driver_latitude"], "longitude" : data["driver_longitude"], "distance":res["driver"]['distance'], 'estimated_time':res["driver"]['estimated_time'], 'vehicle_logo': data["vehicle_logo"] });
					}
				});
				
			// }
			// console.log("In");
		}
		// console.log("out");
	});
/*********************** This event is fired by Driver when he reject or accept any booking ************************************/
	async function driver_response_check(data, cb){
		await new Promise(next=> {
		// errorLogMail("driver_response_check start", JSON.stringify(data))
		if(data.response_type === true){
			// console.log("00000")
			var querySelObj = []
	    	querySelObj["select"] = "count(*)"
	    	querySelObj["table_name"] = "nd_order"
	    	querySelObj["condition"] = " ID="+ data["order_id"] +" and booking_status !="+ BOOKING_STATUS_CANCELLED
	    	querySelObj["type"] = "count"
			customModel.selectQuery(querySelObj, async function(res){
				// console.log("11111")
				if(res && parseFloat(res)>0){

						var queryObj = []
						var n = new Date()
				    	// queryObj["select"] = "device_token, id"
				    	queryObj["table_name"] = "nd_order"
				    	queryObj["condition"] = " id="+ data["order_id"]
				    	queryObj["updateStr"] = "driver_id="+data["driver_id"]+ ", booking_time=current_timestamp, booking_status=2, vehicles_type_id="+parseInt(data["vehicle_type"])
						await customModel.updateQuery(queryObj,async  function(res){
							var upsertQueryObj = []
							// console.log("22222")
					    	upsertQueryObj["insertObj"] = parseInt(data["driver_id"])+",0,0,false"
							await customModel.upsertQuery(upsertQueryObj, data["driver_id"], false, async function(resUpsert){
								io.to(global.orderUsersIds[data['supplier_id']]).emit("current_order_status", {"order_id" :data["order_id"], 
								"order_status" : BOOKING_STATUS_PLACED, "driver_response": true, "driver_key": data['driver_id']+"~"+data["vehicle_type"]});
								// console.log("333333")
								// global.ON_GOING_DRIVERS[data["driver_id"]] = {order_id:data["order_id"], "supplier_id":  data["supplier_id"], "socket_id": data['socket_id']}
								// if(Object.keys(global.orderUsersIds).length>0){
								// 	// if(in_array(data["supplier_id"], global.orderUsersIds)){
								// 		console.log("&&&&&&&&&&&&&&&&&&&&&&&77")
								// 		var supplierSocket = global.orderUsersIds[data["supplier_id"]];
								// 		io.to(supplierSocket).emit("track_driver_route", {"latitude": data["latitude"], "longitude" : data["longitude"]});	
								// 	// }
								// }
							});
						});
						var queryDelObj = []
				    	queryDelObj["table_name"] = "nd_booking_req"
				    	queryDelObj["condition"] = " driver_id ="+ data["driver_id"] 
				    	queryDelObj["updateStr"] = " is_deleted=true"
						await customModel.updateQuery(queryDelObj, async function(res){
							// console.log("44444444")
							var queryDelObj = []
					    	queryDelObj["table_name"] = "nd_booking_req"
					    	queryDelObj["condition"] = " driver_id ="+ data["driver_id"] + " and order_id ="+data["order_id"]
					    	queryDelObj["updateStr"] = " is_booked=true, latitude='"+ data["latitude"]+"', longitude='"+data["latitude"] +"', location='"+data["location"]+"'"
							await customModel.updateQuery(queryDelObj, async function(res2){
								// console.log("dddddddddddddd",res2)
								// console.log(55555555)
							});
						});
						var querySelObj = []
				    	querySelObj["select"] = "count(*)"
				    	querySelObj["table_name"] = "nd_order"
				    	querySelObj["condition"] = " ID="+ data["order_id"] +" and booking_status !="+ BOOKING_STATUS_CANCELLED
				    	querySelObj["type"] = "count"
						await customModel.selectQuery(querySelObj, async function(res){
							// console.log("66666666")
							if(res && parseFloat(res)>0){
								var querySelObj = []
						    	querySelObj["select"] = "device_token, id"
						    	querySelObj["table_name"] = "nd_users"
						    	querySelObj["condition"] = " ID="+ data["supplier_id"]
						    	querySelObj["type"] = "single"
								await customModel.selectQuery(querySelObj, async function(res){
									// console.log("7777777777")
									// console.log("~~~~~~~~",data)
									if(res){
										pushCustomData = {}
										pushCustomData["order_id"] = data["order_id"]
										pushCustomData["push_type"] = global.NOTIFICATION_TYPE['booking_confirm']
										requiredFields = [];
										requiredFields["title"] = "Driver Confirmation";
										requiredFields["body"] = "Your booking has been confirmed"
										pushCustomData["title"] = requiredFields["title"]
										pushCustomData["sound"] = 'notification.mp3'
										pushCustomData["body"] = requiredFields["body"]
   										requiredFields["device_token"] = res["device_token"];
   										requiredFields['user_id'] = res["id"];
										requiredFields['isSaved'] = false;
										await customServices.sendPush(pushCustomData, requiredFields, async function(pushRes){
											// console.log("8888888888")
											// console.log("~~~~~~~~",pushRes)
											if(pushRes==true){
												// console.log("7777777")
												cb({"status": true, 'msg':"Booking accepted"});

											} else{
												cb({"status": false, 'msg':"Something went wrong1"});
											}
										});
									}else{
										cb({"status": false, 'msg':"Something went wrong2"});
									}
								});
							}else{
								// console.log("9999999")
								cb({"status": false, 'msg':"Your current booking is cancelled by the supplier"});
							}
						});
					}
				});
			
			// cb({"status": true, 'msg':"Booking accepted"});
			// cb({"status": false, 'msg':"gfgfgfgfgfg"});
		}else{
			io.to(global.orderUsersIds[data.supplier_id]).emit("current_order_status", {"order_id" :data["order_id"], "order_status" : BOOKING_STATUS_PROCESSING, 
				"driver_key":data['driver_id']+"~"+data["vehicle_type"],  "driver_response": false});
			var queryDelObj = []
	    	queryDelObj["table_name"] = "nd_booking_req"
	    	queryDelObj["condition"] = " order_id="+ data["order_id"] + "and driver_id ="+ data["driver_id"] 
	    	queryDelObj["updateStr"] = " is_deleted=true"
			customModel.updateQuery(queryDelObj, async function(res){
				cb({"status": true, 'msg':"Booking declined"});
			});
			
		}
		// console.log("ddddddddddddddddd")
	});
	}
	socket.on("driver_response", async function(data, cb){
		searchRes =  driver_response_check(data, async function(e){
			// console.log(e)
			cb(e)
		});
		// console.log(55555555555555)
		
		
		// 	}else{
		// 		cb({"status": false, 'msg':"Your current booking is cancelled by the supplier"});
		// 	}
		// });

	});
	
/********************************************** Update driver current location *******************************************************/
	socket.on("update_driver_location", function(data){	

		var insertObj = parseInt(data["driver_id"])+",0,0,true"
		customModel.UserObjUpdate(insertObj, data["driver_id"],  function(resUpsert){
			customServices.driverLocationUpdate(data, function(vehicleLocationRes){
				global.vehicle_location = vehicleLocationRes
				// console.log("$$$$$$$$$$$$$$$$$$$$$$$$");
				// errorLogMail("update_driver_location", JSON.stringify(global.vehicle_location)) 
				io.emit("change_driver_status", true);
			})
		});	
		
	    // io.emit("vehicle_location_list", global.vehicle_location);	
	});
/********************************************** Driver available status change *******************************************************/
	socket.on("change_available_status", function (data) {
		// console.log(444)
		
		// errorLogMail("change Driver status", JSON.stringify(data))
		if( data.is_online === true ){
			// console.log(data, "---------")
			var insertObj = parseInt(data.driver_id)+",0,0,true"
			customModel.UserObjUpdate(insertObj, data.driver_id, function(resUpsert){
				if(!in_array(data.driver_id + "~" + data.vehicle_type, global.vehicle_location)){
					customServices.driverLocationUpdate(data, function(vehicleLocationRes){
						io.emit("change_driver_status", true);	
						// console.log(vehicleLocationRes, "***********8888")
						// io.emit("vehicle_locadddtion_list", vehicleLocationRes);
					});
		    	}	else{
		    		io.emit("change_driver_status", true);
		    	}
			});
		} else{

			// console.log("+++++++++++++++")
			if(vehicle_location.hasOwnProperty(data.driver_id + "~" + data.vehicle_type)){
				driver_id = data.driver_id
				delete global.vehicle_location[data.driver_id + "~" + data.vehicle_type]
			}
			io.emit("change_driver_status", true);	
			// io.emit("vehicle_location_list", global.vehicle_location);
		}
		// if(Object.keys(closest_vehicles_with_supplier).length>0){
		// 	for(var supplier_key in closest_vehicles_with_supplier){
		// 		searchingDrivers(closest_vehicles_with_supplier[supplier_key],global.vehicle_location)
		// 	}
			
		// }
	});
 
/*********************************************** Harvsine Formula to get driver list with in 10 km *******************************************/

	socket.on("closest_vehicle_list_generate", async function(data){ 
		// console.log("ddddd", global.vehicle_location)
		// errorLogMail("closest_vehicle_list_generate", JSON.stringify(data))
		searchRes =  searchingDrivers(data, global.vehicle_location)
	});
/*********************************************** Emit After Driver Arrived Pickup location *******************************************/
	
	socket.on("driver_arrived_status", async function(data){
		if(Object.keys(global.orderUsersIds).length>0){
			// errorLogMail("driver_arrived_status", JSON.stringify(data))
			var supplierSocket = global.orderUsersIds[data["supplier_id"]];
			io.to(supplierSocket).emit("get_arrived_status", {"order_id": data["order_id"], "arrived_location": data['arrived_location']});	
			
		}
	});

/*********************************************** Selection of closest vehicle *******************************************/
	
	socket.on("closest_vehicle_selection",  function(data){
		
		var closest_vehicles_temp_google = {}
		// console.log("closest_vehicle_selection");
		async function searchingAndChooseDriver( driversArray ){
		 	
			// errorLogMail(data["order_id"] + '||Socket on started Part1 -- NeedLog', JSON.stringify(driversArray))
			// console.log("old-----------",data.tried_drivers)
		 	// return false;
			await customServices.checkOrderStaus(data["order_id"], async function(resStatus){
				if(resStatus && resStatus["booking_status"] == BOOKING_STATUS_PROCESSING){ 
					if(Object.keys(driversArray).length>0){
						var supplierData = {supplier_id: data.supplier_id, latitude:data.latitude, longitude:data.longitude, socket_id:data.socket_id}
						for (var key in driversArray) {
							await new Promise(next=> {
						        if (driversArray.hasOwnProperty(key)) {
						        	driver_id = key
						        	driveridVehicleType = driver_id.split("~")
						        	vehicle_type = driveridVehicleType[1]
						        	if(vehicle_type != data.vehicle_type){
						        		next();
						        	}
						        	driverData = driversArray[key]
						        	var supplierLatLongObj = { latitude: supplierData["latitude"], longitude: supplierData["longitude"] }
									var driverLatLongObj = { latitude: driverData["latitude"], longitude: driverData["longitude"] }
									var distance = haversine(supplierLatLongObj, driverLatLongObj, { unit: "km"})
									// errorLogMail("distance", JSON.stringify(supplierLatLongObj) + "@@@"+ JSON.stringify(driverLatLongObj)+ "####"+ distance)
									if( MAX_BOOKING_RADIUS>= distance){
										driverData["distance"] = distance
										queryObj = []
										queryObj["select"] = "count(*)"
								    	queryObj["table_name"] = "nd_users_objects"
								    	queryObj["condition"] = " user_id="+ driversArray[key]["driver_id"] + " and is_available = true"  
								    	queryObj["type"] = "count"
										customModel.selectQuery(queryObj, async function(resDriverAvailiblity){
											if(resDriverAvailiblity && parseFloat(resDriverAvailiblity)>0){
												closest_vehicles_temp_google[key] = driverData;
												// console.log("*******************");
												next();
											}else{
												// console.log("&&&&&&&&&&&&&&&&&&&&&")
												next();
											}
											
										})
										
									}else{
										// console.log("###############")
										next();
									}
								}else{
									// console.log("!!!!!!!!!!!!!!!!!!!!")
									next();
								}
							});
						}
					}
				
					// errorLogMail(data["order_id"] + '||Choose cars before searching Part2 -- NeedLog', JSON.stringify(closest_vehicles_temp_google));
				// errorLogMail(data["order_id"] + '||Choose cars before searching Part2 -- NeedLog', "test");
				// console.log("RRRRRRRRRRRR");
				// A function that returns a promise to resolve into the data //fetched from the API or an error
				let getChuckNorrisFact = () => {
					// console.log("TTTTTTTTTTTT");
				  return new Promise(
				    (resolve, reject) => {
						// console.log("YYYYYYYYYYYYYYYY");
					 processData = {};
				 	processData['url'] = REST_URL + "/supplierAppApi/closest_vehicle_selection/";
				 	processData['method'] = 'POST';
					params = {};
					// console.log("BBBBBBBBBBBBBBBB",closest_vehicles_temp_google);
				 	params['drivers_data'] = closest_vehicles_temp_google;
				 	params['request_data'] = data;
				 	params['radius'] = MAX_BOOKING_RADIUS;
				    customServices.httprequests(processData, params, async function(resCheckByGoogle){
				 		// console.log('ooooooooooooooooo',resCheckByGoogle);
					
						// errorLogMail(data["order_id"] + '||Filter driver by api response Part3 -- NeedLog', JSON.stringify(resCheckByGoogle));
				 		if(resCheckByGoogle['status']){
				 			// console.log("_____________________________--")
				 			selectedDriver = sortObjectByDict(resCheckByGoogle['data']);
				 			if(selectedDriver){
								// console.log("UUUUUUUUUUUUUUUUUUU");
					 			// console.log(selectedDriver.driver_id)
					 			var queryObj = [];
						    	queryObj["select"] = "device_token, id, first_name, last_name";
						    	queryObj["table_name"] = "nd_users"
						    	queryObj["condition"] = " ID="+ selectedDriver.driver_id;
						    	// sortedDriver[driver_key]["distance"]
						    	queryObj["type"] = "single";
						    	// queryObj["join"] = " join nd_order on ";
								customModel.selectQuery(queryObj, function(resDriverDetails){
									// console.log("PPPPPPPPPPPPPPPPP");
									// errorLogMail(data["order_id"] + '||Driver details check Part 4 -- NeedLog', JSON.stringify(resDriverDetails));
									if(resDriverDetails){
										// console.log("OOOOOOOOOOOOO");
							 			pushCustomData = {}
										pushCustomData["order_id"] = data.order_id;
										pushCustomData["distance"] = selectedDriver.distance;
										pushCustomData["sound"] = 'notification.mp3'
										pushCustomData["estimated_time"] = selectedDriver.estimated_time ;
										pushCustomData["push_type"] = global.NOTIFICATION_TYPE['new_booking']
										requiredFields = [];
										requiredFields["title"] = "Booking available";
										requiredFields["body"] = "New booking #"+ data.order_uid+" is available for you. Accept your booking before wait time has been crossed";
										requiredFields['user_id'] = selectedDriver.driver_id
										requiredFields['isSaved'] = true
										pushCustomData["title"] = requiredFields["title"];
										pushCustomData["body"] = requiredFields["body"];
										requiredFields["device_token"] = resDriverDetails["device_token"];
										customServices.sendPush(pushCustomData, requiredFields, function(pushRes){
											// console.log(")))))))))))))))))))))))))))))))");
											// console.log("ssssssssssssssssssssssssss",pushRes)
											// errorLogMail(data["order_id"] + '||Push send data Part5 -- NeedLog', JSON.stringify(pushRes))
											if(pushRes == true){
												// console.log("PPPPPPPPPPPPPPPPP");
										    	tableName = "nd_booking_req";
												conditionObj = "driver_id="+ selectedDriver.driver_id + ", order_id="+ data.order_id + 
												", is_deleted=false";
												var updateObj = [];
										    	updateObj["fields"] = "date_created=current_timestamp, estimate_time="+selectedDriver.estimated_time; 
										    	var insertObj = []
										    	insertObj['fields'] = 'order_id, driver_id, is_deleted, estimate_time,date_created, is_booked'
										    	insertObj['values'] = data.order_id +","+ selectedDriver.driver_id+",false,"+ selectedDriver.estimated_time+",current_timestamp, false"
										    	customModel.upsertQueryGeneric(conditionObj, updateObj, insertObj, tableName, async function(resUpsert){
													// console.log("****************************",data['socket_id']);
													// errorLogMail(data["order_id"] + '||Booking Api Successfully called Part6 -- NeedLog', JSON.stringify(processData) + "@@@"+ JSON.stringify(params) + "@@@wait 30 min punch with next array"+ selectedDriver.driver_id+"~"+selectedDriver.vehicle_type)
													io.to(data['socket_id']).emit("closest_vehicles_before_booking", {"driver_key": selectedDriver.driver_id+"~"+selectedDriver.vehicle_type, 
														"order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : selectedDriver.driver_id, "check": "1"});	
												});
												var count = 0;

												interval(async () => {
													// errorLogMail("time to send demo push", "");
												    await sendOptionalPushForbooking(pushCustomData, requiredFields)
												}, 5000, {iterations:2})
												
											} else{
												// console.log("push not send");
												// console.log("!!!!!!!!!!!!4")
												// errorLogMail(data["order_id"] + '||Push not send Part7 -- NeedLog', "Push not send")
												io.to(data['socket_id']).emit("closest_vehicles_before_booking", {"driver_key": selectedDriver.driver_id+"~"+selectedDriver.vehicle_type, "order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : 0});
											}
										});
									}else{
										// console.log("!!!!!!!!!!!!3")
										// console.log("^^^^))))))))))))))", selectedDriver.driver_id)
										io.to(data['socket_id']).emit("closest_vehicles_before_booking", {"check": "2", "driver_key": selectedDriver.driver_id+"~"+selectedDriver.vehicle_type, "order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : 0});
									}
								});
							}else{
								
								// errorLogMail(data["order_id"] + '||Sorted Driver Empty Part 8 -- NeedLog', JSON.stringify(selectedDriver))
								// console.log("!!!!!!!!!!!!1")
				 				io.to(data['socket_id']).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : 0});
				 			}
				 		}else{
							// console.log("!!!!!!!!!!!!2")
				 			// errorLogMail(data["order_id"] + '||Data comming from choose vehicle api Not True Part 9 -- NeedLog', JSON.stringify(resCheckByGoogle))
				 			io.to(data['socket_id']).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : 0});
				 		}
				 		resolve(resCheckByGoogle);
				 	})

				   }
				 );
				};
				getChuckNorrisFact().then(
				   fact => console.log("")
				).catch(
				   error => console.log()
				);
				// console.log("^^^^^^^^^^^^^^^4")
					// console.log("yyyyyyyy")
				} else if(resStatus && resStatus["booking_status"] == BOOKING_STATUS_PLACED){
					// console.log("^^^^^^^^^^^^^^^5")
					io.to(data['socket_id']).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : BOOKING_STATUS_PLACED, "driver_id" : resStatus["driver_id"]});
				} else if(resStatus && resStatus["booking_status"] == BOOKING_STATUS_CANCELLED){
					// console.log("^^^^^^^^^^^^^^^6")
					io.to(data['socket_id']).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : BOOKING_STATUS_CANCELLED, "driver_id" : 0});
				} else if(resStatus && resStatus["booking_status"] == BOOKING_STATUS_COMPLETED){
					// console.log("^^^^^^^^^^^^^^^7")
					io.to(data['socket_id']).emit("closest_vehicles_before_booking", { "driver_key": "", "order_status" : BOOKING_STATUS_COMPLETED, "driver_id" : resStatus["driver_id"]});
				} else{
					
					// errorLogMail(data["order_id"] + '||Booking Api Successfully called Part 10 -- NeedLog', 'else part')
					// console.log("^^^^^^^^^^^^^^^8")
					io.to(data['socket_id']).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : "", "driver_id" : 0});
				}
			});
			
		}
		searchingAndChooseDriver(global.vehicle_location)
	});
	socket.on("disconnect", function () {
      // console.log("Timeout",socket.id )
  	});

	io.emit("supplier_list_for_order", global.orderUsersIds);

});
function sendOptionalPushForbooking(pushCustomData, requiredFields){
	pushCustomData["push_type"] = global.NOTIFICATION_TYPE['optional_booking_req'];
	pushCustomData["sound"] = 'notification.mp3'
	requiredFields['isSaved'] = false

	customServices.sendPush(pushCustomData, requiredFields, function(pushRes){
		
	});
}
function errorLogMail(subject, body){
	fs.appendFile('bookingErrorLog.txt', "\nSub=="+subject+"||"+"body=="+body+"\n", function (err) {
    if (err) 
        return console.log(err);
    return true;
	});
	
}
function sortObject(obj, cancelledDrivers) {
    var arr = [];
    var prop;
    for (prop in obj) {
    	if( cancelledDrivers && in_array(prop, cancelledDrivers)){
    		continue;
    	}
        if (obj.hasOwnProperty(prop)) {
            arr.push({
                "key": prop,
                "value": obj[prop] 
            });
        }
    }
    arr.sort(function(a, b) {
        return a.value.distance - b.value.distance;
    });
    var tmpData = {}
    for(var i in arr){
    	tmpData[arr[i]["key"]] = arr[i]["value"]
    	break;
    }
    return tmpData; // returns array
}
function sortObjectByDict(obj) {
	// console.log("________________", obj)
    var arr1 = [];
    var prop;
    for (prop in obj) {
    	// console.log("************", prop)
        if (obj.hasOwnProperty(prop)) {
            arr1.push({
                "key": prop,
                "value": obj[prop] 
            });
        }
    }
    arr1.sort(function(a, b) {
    	// console.log("************", a)
        return a.value.distance - b.value.distance;
    });
    var tmpData = null;
    for(var i in arr1){
    	tmpData = arr1[i]["value"]
    	break;
    }
    return tmpData;
}
async function searchingDrivers( data, driversArray ){
	// console.log(data )
	// console.log("---------------")
	// console.log("pppp",driversArray)
		closest_vehicles_temp = {}
		if(Object.keys(driversArray).length>0){
			var supplierData = {supplier_id: data.supplier_id, latitude:data.latitude, longitude:data.longitude, socket_id:data.socket_id}
			for (var key in driversArray) {
				await new Promise(next=> {
			        if (driversArray.hasOwnProperty(key)) {
			        	driver_id = key
			        	driveridVehicleType = driver_id.split("~")
			        	vehicle_type = driveridVehicleType[1]
			        	driverData = driversArray[key]
			        	var supplierLatLongObj = { latitude: supplierData["latitude"], longitude: supplierData["longitude"] }
						var driverLatLongObj = { latitude: driverData["latitude"], longitude: driverData["longitude"] }
						var distance = haversine(supplierLatLongObj, driverLatLongObj, { unit: "km"})
						if( MAX_BOOKING_RADIUS>= distance){
							
							driverData["distance"] = distance
							queryObj = []
							queryObj["select"] = "count(*)"
					    	queryObj["table_name"] = "nd_users_objects"
					    	queryObj["condition"] = " user_id="+ driversArray[key]["driver_id"] + " and is_available = true"  
					    	queryObj["type"] = "count"
							customModel.selectQuery(queryObj, function(res){
								if(res && parseFloat(res)>0){
									customServices.closestVehicleLists(supplierData, driversArray[key], MAX_BOOKING_RADIUS,  function(res){
										// console.log("==================", res) 
						            	if(res.status == true){
						            		// console.log("==================", res.status)
											closest_vehicles_temp[key] = res.driver
										}else{
											// console.log(driversArray[key])
										}
										next();
									});
								}else{
									next();
								}
							});
						}else{
							next();
						}
					}else{
						next();
					}
				});
			}
			io.to(data.socket_id).emit("closest_vehicle_lists", closest_vehicles_temp);

		}else{
			io.to(data.socket_id).emit("closest_vehicle_lists", closest_vehicles_temp);
		}
		return true
	}
// http.listen(8002, "0.0.0.0", function() {
// });



//example

http.listen(global.SOCKET_PORT, global.SOCKET_ADDRESS, function() {
});
