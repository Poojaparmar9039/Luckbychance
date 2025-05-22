

    $('#country-dropdown').change(function () {
        var countryID = $(this).val();
        $('#state-dropdown').html('<option value="">Select State</option>');
        $('#city-dropdown').html('<option value="">Select City</option>');
        if (countryID) {
            $.ajax({
                url: '{% url "get_states" %}',
                data: {'country_id': countryID},
                success: function (data) {
                    $.each(data.states, function (i, state) {
                        $('#state-dropdown').append('<option value="' + state.id + '">' + state.name + '</option>');
                    });
                }
            });
        }
    });

    $('#state-dropdown').change(function () {
        var stateID = $(this).val();
        $('#city-dropdown').html('<option value="">Select City</option>');
        if (stateID) {
            $.ajax({
                url: '{% url "get_cities" %}',
                data: {'state_id': stateID},
                success: function (data) {
                    $.each(data.cities, function (i, city) {
                        $('#city-dropdown').append('<option value="' + city.id + '">' + city.name + '</option>');
                    });
                }
            });
        }
    });

