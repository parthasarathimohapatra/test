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
		    method: processData["method"],
		    json: true,   // <--Very important!!!
		    body: params
		}, function (error, response, body){
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
		// console.log(driverDetails+"___________"+supplierDatails	)
		var distance = require("google-distance");
		distance.apiKey = "AIzaSyDOZCiwPSXUm58TOjViGXwbsfKYkP6t0jw";
		distance.get(
			  {
			    origin: supplierDatails["latitude"] + ", "+ supplierDatails["longitude"],
			    destination: driverDetails["latitude"] + ", "+ driverDetails["longitude"],
			  },
			  function(err, data) {
			    if (err){
			    	cb({"status":err})
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
				cb(res)
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
		    data: {
		        obj
		    },
		    notification: {
		        title: reqObj["title"],
		        body: reqObj["body"]
		    }
		};

		//callback style
		fcm.send(message, function(err, response){
		    if (err) {
		    	// console.log(44444444444)
		        cb(false)
		    } else {

		        cb(true)
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