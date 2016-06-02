var mongoose = require('mongoose');

module.exports = mongoose.model('DataArduino', {
    id_sensor: {
        type: String,
        default: ''
    },
    temperature: {
            type: String,
            default: ''
        },
    humidity: {
            type: String,
            default: ''
        },
    date: {
            type: String,
            default: ''
        },
    hour: {
            type: String,
            default: ''
        },
        coord: {
        latitude: String,
        longitude: String
    }
});
