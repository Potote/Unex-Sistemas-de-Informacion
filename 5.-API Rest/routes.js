var DataArduino = require('./models/dataarduino');

function getDataArduinos(res) {
    DataArduino.find(function (err, dataarduinos) {
        console.log(dataarduinos);
        // if there is an error retrieving, send the error. nothing after res.send(err) will execute
        if (err) {
            res.send(err);
        }

        res.json(dataarduinos); // return all dataarduinos in JSON format
    });
}
;

module.exports = function (app) {

    // api ---------------------------------------------------------------------
    // get all dataarduinos
    app.get('/api/dataarduinos', function (req, res) {
        // use mongoose to get all dataarduinos in the database
        getDataArduinos(res);
    });

    // create dataarduino and send back all dataarduinos after creation
    app.post('/api/dataarduinos', function (req, res) {

        // create a dataarduino, information comes from AJAX request from Angular
        DataArduino.create({
            id_sensor: req.body.id_sensor,
            done: false
        }, function (err, dataarduino) {
            if (err)
                res.send(err);

            // get and return all the dataarduinos after you create another
            getDataArduinos(res);
        });
