(function ($) {

    var GoogleMapsAPI = {

        __apiUrl: 'https://maps.googleapis.com/maps/api/geocode/json',

        __defaultData: {
            sensor: 'true_or_false'
        },

        _escapeVariable: function (string) {
            if (typeof string === 'string') {
                string = string.replace(/[\s]/, '+');
                return string;
            } else {
                return false;
            }
        },

        _getFullData: function (data) {
            return $.extend({}, GoogleMapsAPI.__defaultData, data);
        },

        _request: function (method, data, complete, success, error) {
            method = (method.toUpperCase() === 'GET' || method.toUpperCase() === 'POST') ? method.toUpperCase() : 'GET';
            data = typeof data !== 'undefined' ? data : {};
            complete = typeof complete === 'function' ? complete : function (jqXHR, textStatus) {};
            success = typeof success === 'function' ? success : function (data, textStatus, jqXHR) {};
            error = typeof error === 'function' ? error : function (jqXHR, textStatus, errorThrown) {};

            $.ajax({
                method: method,
                url: GoogleMapsAPI.__apiUrl,
                data: GoogleMapsAPI._getFullData(data),
                async: true,
                complete: complete,
                success: success,
                error: error
            });

            return true;
        },

        getZipcodeFromAddress: function (address) {
            return GoogleMapsAPI._request(
                'GET',
                { address: GoogleMapsAPI._escapeVariable(address) },
                function (jqXHR, textStatus) {},
                function (data, textStatus, jqXHR) {
                    var zipcode = null;
                    if (data.status === 'OK' && typeof data.results !== 'undefined') {
                        for (var result = 0; result < data.results.length; result++) {
                            for (var component = 0; component < data.results[result].address_components.length; component++) {
                                if ($.inArray('postal_code', data.results[result].address_components[component].types) > -1) {
                                    zipcode = data.results[result].address_components[component].long_name;
                                    break;
                                }
                            }
                            if (zipcode !== null) {
                                break;
                            }
                        }
                        if (zipcode !== null) {
                            ZipCodeObserver.notify(zipcode);
                        } else {
                            console.log('No zip code found for given address.');
                        }
                    } else {
                        console.log('Geocode API status failed.');
                    }
                },
                function (jqXHR, textStatus, errorThrown) {
                    console.warn('Ajax request to Google Geocode API failed: ' + textStatus + ' - ' + errorThrown);
                }
            );
        }

    };

    var ZipCodeObserver = {

        __observers: [],

        observe: function (observer) {
            if (typeof observer === 'function') {
                ZipCodeObserver.__observers.push(observer);
                return true;
            } else {
                return false;
            }
        },

        notify: function (zipcode) {
            for (var observer in ZipCodeObserver.__observers) {
                return ZipCodeObserver.__observers[observer](zipcode);
            }

            return true;
        }

    };

    $(document).ready(function () {

        var addressField = $('[data-autofill=address]');
        var cityField = $('[data-autofill=city]');
        var stateField = $('[data-autofill=state]');
        var zipCodeField = $('[data-autofill=zipcode]');

        if (
            addressField.length > 0 &&
            cityField.length > 0 &&
            stateField.length > 0 &&
            zipCodeField.length > 0
        ) {
            $(addressField).add($(cityField)).add($(stateField)).on('change', function (e) {
                if (
                    $(addressField).val() &&
                    $(cityField).val() &&
                    $(stateField).val()
                ) {
                    GoogleMapsAPI.getZipcodeFromAddress($(addressField).val() + ' ' + $(cityField).val() + ', ' + $(stateField).val());
                }
            });

            ZipCodeObserver.observe(function (zipcode) {
                $(zipCodeField).val(zipcode);
            });
        } else {
            console.warn('Autofill is missing a required field.');
        }

    });

})(jQuery);
