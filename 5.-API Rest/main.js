angular.module('dataarduinoController', [])

        // inject the DataArduino service factory into our controller
        .controller('mainController', ['$scope','$http','DataArduinos', function($scope, $http, DataArduinos) {
                $scope.formData = {};
                $scope.loading = true;

                // GET =====================================================================
                // when landing on the page, get all dataarduinos and show them
                // use the service to get all the dataarduinos
                DataArduinos.get()
                        .success(function(data) {
                                console.log(data);
                                $scope.dataarduinos = data;
                                $scope.loading = false;
                        });

                // CREATE ==================================================================
                // when submitting the add form, send the text to the node API
                $scope.createDataArduino = function() {

                        // validate the formData to make sure that something is there
                        // if form is empty, nothing will happen
                        if ($scope.formData. id_sensor != undefined) {
                                $scope.loading = true;

                                // call the create function from our service (returns a promise object)
                                DataArduinos.create($scope.formData)

                                        // if successful creation, call our get function to get all the new dataarduinos
                                        .success(function(data) {
                                                $scope.loading = false;
                                                $scope.formData = {}; // clear the form so our user is ready to enter another
                                                $scope.dataarduinos = data; // assign our new list of dataarduinos
                                        });
                        }
                };

                // DELETE ==================================================================
                // delete a dataarduino after checking it
                $scope.deleteDataArduino = function(id) {
                        $scope.loading = true;

                        DataArduinos.delete(id)
                                // if successful creation, call our get function to get all the new dataarduinos
                                .success(function(data) {
                                        $scope.loading = false;
                                        $scope.dataarduinos = data; // assign our new list of dataarduinos
                                });
                };
        }]);


