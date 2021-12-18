vehicle_location = {}
orderUsersIds = {}
BOOKING_STATUS_PROCESSING = 1
BOOKING_STATUS_PLACED = 2
BOOKING_STATUS_CANCELLED = 3
BOOKING_STATUS_COMPLETED = 4
MAX_BOOKING_RADIUS = 20
ON_GOING_DRIVERS = {}
NOTIFICATION_TYPE = {"booking_confirm":"BOOKING_CONFIRMED_FROM_DRIVER", "cross_overhead":"CROSSED_THRESHOLD", "new_booking":"NEW_BOOKING_AVAILABLE", 
"arrived_first_drop":"ARRIVED_AT_FIRST_LOCATION", "arrived_second_drop":"ARRIVED_AT_SECOND_LOCATION", "arrived_at_pickup":"ARRIVED_AT_PICKUP_LOCATION",
 "force_drop":"DROP_FORCEFULLY", "optional_booking_req":"OPTIONAL_BOOKING_REQUEST"}

// module.exports = constants;