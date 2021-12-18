var app = require("express")();
var http = require("http").Server(app);
var io = require("socket.io")(http, {"pingInterval": 3000, "pingTimeout": 4000});
var diff = require("deep-diff").diff;
var pg = require("pg");
var in_array = require("in_array");
var customServices = require("./services/Services.js");
var customModel = require("./model/Model.js");
var constants = require("./constants/Constants.js");
var restApiBaseUrl = "http://192.168.0.164:8000";
var suplierApiUrl = restApiBaseUrl + "/supplierAppApi/";
var moment = require("moment-timezone");
var now = moment();
var formatted = moment.tz(now,"Asia/Kolkata");
var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database(":memory:");
const haversine = require("haversine");
var distance = require("google-distance");
distance.apiKey = "AIzaSyDOZCiwPSXUm58TOjViGXwbsfKYkP6t0jw";
require("events").EventEmitter.defaultMaxListeners = 0; 
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
	
	console.log(socket.id)
/*********************** This event is fired borderStyle: "solid" "dotted" "dashed"  Supplier when he press on the confirm booking( at the time of searching driver api) ************************************/
	socket.on("set_customer_id_before_booking", function(data){
			global.orderUsersIds[data.user_id] = socket.id
			// io.emit("supplier_list_for_order", global.orderUsersIds);
	});
/*********************** This event is fired by Driver when he reject or accept any booking ************************************/	
	socket.on("driver_response", async function(data){
		console.log(data)
		if(data.response_type === true){

			var queryObj = []
			var n = new Date()
	    	// queryObj["select"] = "device_token, id"
	    	queryObj["table_name"] = "nd_order"
	    	queryObj["condition"] = " id="+ data["order_id"]
	    	queryObj["updateStr"] = "driver_id="+data["driver_id"]+ ", booking_time=current_timestamp, booking_status=2"
			await customModel.updateQuery(queryObj,async  function(res){
				var upsertQueryObj = []
		    	upsertQueryObj["insertObj"] = parseInt(data["driver_id"])+",0,0,false"
				await customModel.upsertQuery(upsertQueryObj, data["driver_id"], false, async function(resUpsert){

					io.to(global.orderUsersIds[data.supplier_id]).emit("current_order_status", {order_id :data["order_id"], "order_status" : BOOKING_STATUS_PLACED, "driver_response": true});
				});
			});
			var queryDelObj = []
	    	queryDelObj["table_name"] = "nd_booking_req"
	    	queryDelObj["condition"] = " driver_id ="+ data["driver_id"] 
	    	queryDelObj["updateStr"] = " is_deleted=true"
			customModel.updateQuery(queryDelObj, async function(res){
				
			});
			var querySelObj = []
	    	querySelObj["select"] = "device_token, id"
	    	querySelObj["table_name"] = "nd_users"
	    	querySelObj["condition"] = " ID="+ data["supplier_id"]
	    	querySelObj["type"] = "single"
			customModel.selectQuery(querySelObj, function(res){
				if(res){
					pushCustomData = []
					pushCustomData["order_id"] = data["order_id"]
					requiredFields = [];
					requiredFields["title"] = "Your booking has been confirmed";
					requiredFields["body"] = "";
					requiredFields["device_token"] = res["device_token"];
					customServices.sendPush(pushCustomData, requiredFields, function(pushRes){
						
						if(pushRes==true){
							console.log("send")

						}else{
							console.log("Not send")
						}
					});
				}else{

				}
			});

		}else{
			io.to(global.orderUsersIds[data.supplier_id]).emit("current_order_status", {order_id :data["order_id"], "order_status" : BOOKING_STATUS_PROCESSING, "driver_response": false});
			var queryDelObj = []
	    	queryDelObj["table_name"] = "nd_booking_req"
	    	queryDelObj["condition"] = " order_id="+ data["order_id"] + "and driver_id ="+ data["driver_id"] 
	    	queryDelObj["updateStr"] = " is_deleted=true"
			customModel.updateQuery(queryDelObj, async function(res){
				
			});
		}
	});
	
/********************************************** Update driver current location *******************************************************/
	socket.on("update_driver_location", function(data){	

		var insertObj = parseInt(data["driver_id"])+",0,0,true"
		customModel.UserObjUpdate(insertObj, data["driver_id"],  function(resUpsert){
			console.log(resUpsert)
			customServices.driverLocationUpdate(data, function(vehicleLocationRes){
				global.vehicle_location = vehicleLocationRes

			})
		});	
		
	    // io.emit("vehicle_location_list", global.vehicle_location);	
	});
/********************************************** Driver available status change *******************************************************/
	socket.on("change_available_status", function (data) {
		io.emit("change_driver_status", true);	

		if( data.is_online === true ){
			// console.log(data, "---------")
			var insertObj = parseInt(data.driver_id)+",0,0,true"
			customModel.UserObjUpdate(insertObj, data.driver_id, function(resUpsert){
				if(!in_array(data.driver_id + "~" + data.vehicle_type, global.vehicle_location)){
					customServices.driverLocationUpdate(data, function(vehicleLocationRes){
						console.log(vehicleLocationRes, "***********8888")
						// io.emit("vehicle_locadddtion_list", vehicleLocationRes);
					});
		    	}	
			});
		} else{
			console.log("+++++++++++++++")
			if(vehicle_location.hasOwnProperty(data.driver_id + "~" + data.vehicle_type)){
				driver_id = data.driver_id
				delete global.vehicle_location[data.driver_id + "~" + data.vehicle_type]
			}
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

		searchRes =  searchingDrivers(data, global.vehicle_location)
	});

/*********************************************** Selection of closest vehicle *******************************************/
	
	socket.on("closest_vehicle_selection", async function(data){
		
		var closest_vehicles_temp_google = {}
		async function searchingAndChooseDriver( driversArray ){
			customServices.checkOrderStaus(data["order_id"], async function(resStatus){
				if(resStatus && resStatus["booking_status"] == BOOKING_STATUS_PROCESSING){ 
					if(Object.keys(driversArray).length>0){
					    if(data.tried_drivers.length !=0){
						    var key_val = data.tried_drivers[data.tried_drivers.length - 1];
						    var userObj = key_val.split("~");
						    var queryObj = []
					    	queryObj["select"] = "device_token, id"
					    	queryObj["table_name"] = "nd_users"
					    	queryObj["condition"] = " ID="+ userObj[0]
					    	queryObj["type"] = "single"
							customModel.selectQuery(queryObj, async function(res){
								if(res){
									pushCustomData = []
									pushCustomData["supplier_id"] = data.supplier_id,
									pushCustomData["order_id"] = data.order_id,
									pushCustomData["page_name"] = "driver_response_page"
									requiredFields = []
									requiredFields["title"] = "Your booking #"+ data.order_uid+" has been cancelled"
									requiredFields["body"] = "You have crossed normal wait time"
									requiredFields["device_token"] = res["device_token"]
									customServices.sendPush(pushCustomData, requiredFields, function(pushRes){
									});
								}
							});
						}
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
										if( MAX_BOOKING_RADIUS>= distance){
											driverData["distance"] = distance
											queryObj = []
											queryObj["select"] = "count(*)"
									    	queryObj["table_name"] = "nd_users_objects"
									    	queryObj["condition"] = " user_id="+ driversArray[key]["driver_id"] + "and is_available = true"  
									    	queryObj["type"] = "count"
											customModel.selectQuery(queryObj, function(res){
												if(res && parseFloat(res)>0){
													customServices.closestVehicleLists(supplierData, driversArray[key], MAX_BOOKING_RADIUS,  function(res){
										            	if(res.status === true){
															closest_vehicles_temp_google[key] = res.driver
														}
														next();
													});
												}else{
													next();
												}
											});
										}
									}
								});
							}
							if(Object.keys(driversArray).length>0){
								
								sortedDriver = sortObject(closest_vehicles_temp_google, data.tried_drivers)
								if(Object.keys(sortedDriver).length >0){
								    for(var driver_key in sortedDriver){
								    	var queryObj = [];
								    	queryObj["select"] = "device_token, id, first_name, last_name";
								    	queryObj["table_name"] = "nd_users"
								    	queryObj["condition"] = " ID="+ sortedDriver[driver_key]["driver_id"];
								    	queryObj["type"] = "single";
								    	// queryObj["join"] = " join nd_order on ";

										customModel.selectQuery(queryObj, function(res){
											// console.log(res)
											if(res){
												pushCustomData = []
												pushCustomData["order_id"] = data.order_id;
												pushCustomData["distance"] = sortedDriver[driver_key]["distance"];
												pushCustomData["estimated_time"] = sortedDriver[driver_key]["estimated_time"];
												requiredFields = [];
												requiredFields["title"] = "New booking #"+ data.order_uid+" is available";
												requiredFields["body"] = "";
												requiredFields["device_token"] = res["device_token"];
												customServices.sendPush(pushCustomData, requiredFields, function(pushRes){
														console.log(res["device_token"])
													if(pushRes==true){

												    	tableName = "nd_booking_req";
														conditionObj = "driver_id="+ sortedDriver[driver_key]["driver_id"] + ", order_id="+ data.order_id + 
														", is_deleted=false";
														var updateObj = [];
												    	updateObj["fields"] = "date_created=current_timestamp, estimate_time="+sortedDriver[driver_key]["estimated_time"]; 
												    	var insertObj = []
												    	insertObj['fields'] = 'order_id, driver_id, is_deleted, estimate_time,date_created'
												    	insertObj['values'] = data.order_id +","+ sortedDriver[driver_key]["driver_id"]+",false,"+ sortedDriver[driver_key]["estimated_time"]+",current_timestamp"
												    	customModel.upsertQueryGeneric(conditionObj, updateObj, insertObj, tableName, function(resUpsert){
												    		// console.log(resUpsert)
														});
														io.to(data.socket_id).emit("closest_vehicles_before_booking", {"driver_key": driver_key, 
															"order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : sortedDriver[driver_key]["driver_id"]});	

													}else{
														io.to(data.socket_id).emit("closest_vehicles_before_booking", {"driver_key": driver_key, "order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : 0});

													}
												});
											}else{
												io.to(data.socket_id).emit("closest_vehicles_before_booking", {"driver_key": driver_key, "order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : 0});
											}
										});
										break;
									}
								}else{
									io.to(data.socket_id).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : 0});
								}
							}else{
								io.to(data.socket_id).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : 0});
							}
							
						}else{
							io.to(data.socket_id).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : 0});
						}
					} else{
						io.to(data.socket_id).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : BOOKING_STATUS_PROCESSING, "driver_id" : 0});
					}
				}else if(resStatus && resStatus["booking_status"] == BOOKING_STATUS_PLACED){
					io.to(data.socket_id).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : BOOKING_STATUS_PLACED, "driver_id" : resStatus["driver_id"]});
				} else if(resStatus && resStatus["booking_status"] == BOOKING_STATUS_CANCELLED){
					io.to(data.socket_id).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : BOOKING_STATUS_CANCELLED, "driver_id" : resStatus["driver_id"]});
				} else if(resStatus && resStatus["booking_status"] == BOOKING_STATUS_COMPLETED){
					io.to(data.socket_id).emit("closest_vehicles_before_booking", { "driver_key": "", "order_status" : BOOKING_STATUS_COMPLETED, "driver_id" : resStatus["driver_id"]});
				} else{
					io.to(data.socket_id).emit("closest_vehicles_before_booking", {"driver_key": "", "order_status" : "", "driver_id" : 0});
				}
			});
		}
		searchingAndChooseDriver(global.vehicle_location)
	});
	socket.on("disconnect", function () {
      console.log("Timeout",socket.id )
  	});

	io.emit("supplier_list_for_order", global.orderUsersIds);
});
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
async function searchingDrivers( data, driversArray ){
	// console.log(data )
	// console.log("---------------")
	// console.log(driversArray)
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
http.listen(8002, "192.168.0.164", function() {
});
