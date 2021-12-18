
var Modeld = {
	checkDriverAvailablity : function(cb){
		setTimeout(async function(){
			await cb( 1111);
		},1000)
	}
}
module.exports = Modeld;