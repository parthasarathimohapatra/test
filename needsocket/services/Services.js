const haversine = require("haversine")
var FCM = require("fcm-node")
var serverKey = "AAAA-BZrTDk:APA91bFB7jw8hCehQbp6hRPFgSLLefUGMo45wsIZpEK3B5DWwB_W_0iJSZcQ25ZJ4tFbDvRJOXf6etVSCa9JMfRsrNWyVa7IZ2iOkh66HeBq356dDD6EGucn2NibweousjFKfVzhUOkV";
var fcm = new FCM(serverKey)
var customModel = require("../model/Model.js")

var Services = {
	/********************************************* AJAX Call ***********************************************/
	httprequests(processData, params, cb) {
		var request = require("request");
		request({
		    url: processData["url"],
		    method: 'post',
		    json: true,   // <--Very important!!!
		    body: params
		}, function (error, response, body){
			// console.log("44444444444", processData["url"])
		    cb(body)
		});
	},
	/********************************************* Add driver location details ***********************************************/
	driverLocationUpdate(driverData, cb){
		tmpArray ={}
		tmpArray["socket_id"] = driverData.socket_id;
		tmpArray["latitude"] = driverData.latitude;
		tmpArray["longitude"] = driverData.longitude;
		tmpArray["vehicle_type"] = driverData.vehicle_type;
		tmpArray["vehicle_image"] = driverData.vehicle_image;
		tmpArray["vehicle_type_name"] = driverData.vehicle_type_name;
		tmpArray["driver_id"] = driverData.driver_id;
		driverId = driverData.driver_id;
		global.vehicle_location[driverId +"~"+ driverData.vehicle_type] = tmpArray;
		cb(global.vehicle_location);
	},
	/********************************************* Closest vehicles list Harvesine ***********************************************/
	closestVehicleListsHarvesine(supplierDatails, driverDetails, radius ){
		// console.log(supplierDatails["latitude"])

		var supplierLatLongObj = { latitude: supplierDatails["latitude"], longitude: supplierDatails["longitude"] }
		var driverLatLongObj = { latitude: driverDetails["latitude"], longitude: driverDetails["longitude"] }
		// 714504.18 (in meters)
		var distance = haversine(supplierLatLongObj, driverLatLongObj, { unit: "km"})
		if( radius>= distance){
			return driverDetails
		}
		else{
			return false
		}
	},

	closestVehicleLists(supplierDatails, driverDetails, radius,  cb){
		// console.log("tttttttttttttttttttttttttttttttttttt", driverDetails	)
		var distance = require("google-distance");
		distance.apiKey = "AIzaSyDOZCiwPSXUm58TOjViGXwbsfKYkP6t0jw";
		distance.get(
			  {
			    origin: supplierDatails["latitude"] + ", "+ supplierDatails["longitude"],
			    destination: driverDetails["latitude"] + ", "+ driverDetails["longitude"],
			  },
			  function(err, data) {
			    if (err){
			    	cb({"status":false})
			    }else{
			    	var calDistance =  (parseFloat(data["distanceValue"])/1000).toFixed(1);
			    	if( radius >= calDistance){
			    		driverDetails["distance"] = calDistance
			    		driverDetails["estimated_time"] = data["durationValue"]
			    		// driverDetails["destination"] = data["destination"]
						cb({"status":true, "driver": driverDetails })
					}
					else{
						cb({"status":false})
					}
			    }

			    
		});
	
	
		// console.log(supplierDatails["latitude"])

		// var supplierLatLongObj = { latitude: supplierDatails["latitude"], longitude: supplierDatails["longitude"] }
		// var driverLatLongObj = { latitude: driverDetails["latitude"], longitude: driverDetails["longitude"] }
		// // 714504.18 (in meters)
		// var distance = haversine(supplierLatLongObj, driverLatLongObj, { unit: "km"})
		// if( radius>= distance){
		// 	cb({"status":true, "distance": distance })
		// }
		// else{
		// 	cb({"status":false, "distance": distance })
		// }
	},
	checkOrderStaus(order_id, cb){
		queryObj = []
		queryObj["select"] = "id, booking_status, driver_id"
    	queryObj["table_name"] = "nd_order"
    	queryObj["condition"] = " ID="+ order_id   
    	queryObj["type"] = "single"
		customModel.selectQuery(queryObj, function(res){
			if(!res){
				cb(false)
			} else{
				var queryDelObj = []
		    	queryDelObj["table_name"] = "nd_booking_req"
		    	queryDelObj["condition"] = " order_id ="+ order_id 
		    	queryDelObj["updateStr"] = " is_deleted=true"
				customModel.updateQuery(queryDelObj, async function(resUp){
					cb(res)
				});
				
			}
		});
	},
	/********************************************* Closest vehicles list filter with vehicle type ***********************************************/
	
	isEmptyObject(obj, cb){

	    var name;
	    for(var name in obj) {

	        if (obj.hasOwnProperty(name)) {
	            cb(false)
	        }
	    }
	    cb(true)
	},
	sendPush(obj, reqObj, cb){
		var message = {
		    to: reqObj["device_token"], // required fill with device token or topics
		    collapse_key: "green" ,
		    data: obj,
		    notification: {
		        title: reqObj["title"],
		        body: reqObj["body"],
		        sound:'notification.mp3'
		    }
		};

		//callback style
		fcm.send(message, function(err, response){
		    if (err) {
		    	// console.log(44444444444)
		        cb(false)
		    } else {
		    	if(reqObj['isSaved'] == true){
			    	var fieldVal = "'"+reqObj['title']+ "', '"+reqObj['body']+ "', '"+obj.toString()+ "'," + reqObj['user_id']+ ", true, false ";
			    	var fields = "title ,body, extra_data, user_id, is_status, is_deleted";
			    	var insertObj = {'fields':fields, 'fieldVal':fieldVal}
					customModel.insertQuery(insertObj, 'nd_notifications',  function(insertedRes){
						// console.log(insertedRes)
						cb(true)
					});	
				}else{
					cb(true)
				}
		        
		    }
		});
	}, 
	sendCurrentDriverLocation(supplierDatails, driverDetails, cb){
		this.closestVehicleLists(supplierDatails, driverDetails, MAX_BOOKING_RADIUS, function(res){
			// console.log("^^^^^^^^^^^^", res);
			if(res['status']){
				cb(res)
			}else{
				cb(false)
			}
		});
	},
	currentDateTime(city, offset, cb){
	    d = new Date();
	    utc = d.getTime() + (d.getTimezoneOffset() * 60000);
	    nd = new Date(utc + (3600000*offset));
	    return "The local time in " + city + " is " + nd.toLocaleString();

	},	
};
module.exports = Services;