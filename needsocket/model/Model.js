var pg = require('pg');
var envConst = require("../constants/env.js");
var HOST = '192.168.0.65';
var DATABASE = 'need_deliver';
var USERNAME = 'postgres'
var PASSWORD = 'navsoftpsql'
var port = 5432;
if(global.ENVIORNMENT == "Production"){
	// console.log(333333333)
	var HOST = 'needdeliver.cn2vrmdn89gz.us-east-1.rds.amazonaws.com';
	var DATABASE = 'needdeliver';
	var USERNAME = 'needdeliver'
	var PASSWORD = 'Needdeliver!234$'
	var port = 5432;
} else if(global.ENVIORNMENT == "Stagging"){
	var HOST = '192.168.0.65';
	var DATABASE = 'need_deliver';
	var USERNAME = 'postgres'
	var PASSWORD = 'navsoftpsql'
	var port = 5432;
} 
var config = {
  user: USERNAME, //env var: PGUSER
  database: DATABASE, //env var: PGDATABASE
  password: PASSWORD, //env var: PGPASSWORD
  host: HOST, // Server hosting the postgres database
  port: port, //env var: PGPORT
  max: 10000000, // max number of clients in the pool
  idleTimeoutMillis: 30000, // how long a client is allowed to remain idle before being closed
};
var pool = new pg.Pool(config);
var Model = {
	/********************************************* AJAX Call ***********************************************/
	selectQuery(queryObj, cb) {
		pool.connect(function(err, client, done) {
			if(err) {
				return console.error('error fetching client from pool', err);
			}
			var select = queryObj["select"] ? queryObj["select"] : "*";
			var condition = queryObj["condition"] ? queryObj["condition"] : "";
			// console.log("select "+select+" from "+queryObj["table_name"]+ " where "+ condition)
			client.query("select "+select+" from "+queryObj["table_name"]+ " where "+ condition , function(err, result) {
			// client.query("select * from nd_users", function(err, result) {
			//call `done()` to release the client back to the pool
				done();

				if(err) {
				  	cb(false);
				} else{
					if(result.rows.length>0){ 
						if(queryObj["type"] === "single"){
							cb(result.rows[0]);
						} else if(queryObj["type"] === "multiple"){ 
							cb(result.rows);
							
						} else{
							// console.log(result)
							cb(result.rows[0]["count"]);
						}
					}else{
						cb(false);
					}
					
				}

			});
		});
			
	},
	upsertQuery(queryObj, user_id, is_status, cb){
		var selectQueryObj = []
    	selectQueryObj["select"] = "count(*)"
    	selectQueryObj["table_name"] = "nd_users_objects"
    	selectQueryObj["condition"] = " user_id="+ user_id
    	selectQueryObj["type"] = "count"
		Model.selectQuery(selectQueryObj, async function(res){
			if(res && parseFloat(res)>0){
				pool.connect(function(err, client, done) {
					if(err) {
						return console.error('error fetching client from pool', err);
					}

					client.query("update nd_users_objects set is_available="+is_status+" where user_id="+ user_id , function(err, result) {

						done();

						if(err) {
						  	cb(false);
						} else{
							cb(result)
							
						}

					});
				});
			}else{
				var insertObj = queryObj['insertObj']	
				pool.connect(function(err, client, done) {
					if(err) {
						return console.error('error fetching client from pool', err);
					}
					client.query('insert into  nd_users_objects("user_id", "over_all_rating", "no_of_reviews", "is_available") values ('+insertObj+")", function(err, result) {

						done();
						// console.log(err)
						if(err) {
						  	cb(false);
						} else{
							cb(result)
							
						}

					});
				});
			}
			
		});
		
	},
	insertQuery(queryObj, table_name, cb){
		var selectQueryObj = []
    	// console.log("&&&&&&&&&&&&&&&&&&&&&&&&&&&&", queryObj['fieldVal'])
		var fieldVal = queryObj['fieldVal']	
		var fields = queryObj['fields']
		pool.connect(function(err, client, done) {
			if(err) {
				return console.error('error fetching client from pool', err);
			}

			client.query('insert into  '+table_name+' ('+fields+') values ('+fieldVal+")", function(err, result) {

				done();
				// console.log("********************************",err)
				if(err) {
				  	cb(false);
				} else{
					cb(result)
					
				}

			});
		});
			
			
		
	},
	UserObjUpdate(insertObj, user_id, cb){
		var selectQueryObj = [];
    	selectQueryObj["select"] = "count(*)";
    	selectQueryObj["table_name"] = "nd_users_objects";
    	selectQueryObj["condition"] = "user_id="+ user_id;
    	selectQueryObj["type"] = "count";
		Model.selectQuery(selectQueryObj, async function(res){
			if(res == 0){
				pool.connect(function(err, client, done) {
					if(err) {
						return console.error('error fetching client from pool', err);
					}
					client.query('insert into  nd_users_objects("user_id", "over_all_rating", "no_of_reviews", "is_available") values ('+insertObj+")", function(err, result) {

						done();
						console.log(err)
						if(err) {
						  	cb(false);
						} else{
							cb(result)
							
						}

					});
				});
			}else{
				cb(false);
			}
			
		});
	},
	upsertQueryGeneric(conditionObj, updateObj, insertObj, tableName, cb){
		var selectQueryObj = [];
    	conditionObj["select"] = "count(*)";
    	selectQueryObj["table_name"] = tableName;
    	selectQueryObj["condition"] = conditionObj;
    	selectQueryObj["type"] = "count";
    	// console.log(updateObj)
    	// console.log("(((()))))))))))", selectQueryObj)
		Model.selectQuery(selectQueryObj, async function(res){
			// console.log("++++++++++", res)
			if(res && parseFloat(res)>0){
				pool.connect(function(err, client, done) {
					if(err) {
						return console.error('error fetching client from pool', err);
					}
					var updateQueryObj = []
					updateQueryObj = updateObj;
					updateQueryObj['fields'] = updateObj['fields'];
					updateQueryObj['conditions'] = conditionObj;
					// console.log("update "+ tableName +" set "+ updateQueryObj['fields'] +" where "+ updateQueryObj['conditions'])
					client.query("update "+ tableName +" set "+ updateQueryObj['fields'] +" where "+ updateQueryObj['conditions'] , function(error, result) {
						
						done();

						if(error) {
						  	cb(false);
						} else{
							cb(result);
							
						}

					});
				});
			}else{
				var insertQueryObj =[];
				insertQueryObj['fields'] = insertObj['fields'];
				insertQueryObj['values'] = insertObj['values'];
				pool.connect(function(err, client, done) {
					if(err) {
						return console.error('error fetching client from pool', err);
					}
					client.query('insert into  '+ tableName +'('+insertQueryObj['fields']+') values ('+insertQueryObj['values']+")", function(err, result) {

						done();
						// console.log(err)
						if(err) {
						  	cb(false);
						} else{
							cb(result)
							
						}

					});
				});
			}
			
		});
		
	},
	updateQuery(queryObj, cb){
		pool.connect(function(err, client, done) {
			if(err) {
				return console.error('error fetching client from pool', err);
			}
			// var select = queryObj["select"] ? '+'+queryObj["select"] +'"' : "*";
			var condition = queryObj["condition"] ? queryObj["condition"] : "";
			var updateStr = queryObj["updateStr"] ? queryObj["updateStr"] : "";
			// console.log("update "+queryObj["table_name"] +" set "+updateStr+ " where "+ condition)
			client.query("update "+queryObj["table_name"] +" set "+updateStr+ " where "+ condition , function(err, result) {
			// client.query("select * from nd_users", function(err, result) {
			//call `done()` to release the client back to the pool
				done();

				if(err) {
				  	cb(false);
				} else{
					cb(result)
					
				}

			});
		});
	},
	

};
module.exports = Model;