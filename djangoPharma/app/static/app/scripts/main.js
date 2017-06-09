$(document).ready(function () {

    var url = 'http://localhost:8000';

    // add to cart
    $('#addToCart').on('click', function () {
        var quantity = $('#quantity').val();
        var drug_id = $('#drugId').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        // hide the messages
        hideAlertResultMessages();
        var data = {
            quantity: quantity,
            drug_id: drug_id
        };
        $.ajax({
            type: "POST",
            url: url + '/add_to_cart',
            data: data, beforeSend: function (xmlHTTPRequest) {
                xmlHTTPRequest.setRequestHeader('X-CSRFToken', token)
            },
            success: function () {
                $('#cart-alert-success').removeClass('hidden')
            },
            error: function (xhr, textStatus, errorThrown) {
                $('#cart-alert-fail').removeClass('hidden')
            }
        });
    });

    $('#updateCart').on('click', function () {
        debugger;
        var quantity = $('#quantity').val();
        // TODO here we will have many
        var drug_id = $('.drug').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        // hide the messages
        hideAlertResultMessages();
        var data = {
            quantity: quantity,
            drug_id: drug_id
        };
        $.ajax({
            type: "POST",
            url: url + '/update_cart',
            data: data, beforeSend: function (xmlHTTPRequest) {
                xmlHTTPRequest.setRequestHeader('X-CSRFToken', token)
            },
            success: function () {
                $('#cart-alert-success').removeClass('hidden')
            },
            error: function (xhr, textStatus, errorThrown) {
                $('#cart-alert-fail').removeClass('hidden')
            }
        });
    });

     $('#removeFromCart').on('click', function () {
        debugger;
        // TODO here we will have many
        var drug_id = $('.drug').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        // hide the messages
        hideAlertResultMessages();
        var data = {
            drug_id: drug_id
        };
        $.ajax({
            type: "POST",
            url: url + '/remove_from_cart',
            data: data, beforeSend: function (xmlHTTPRequest) {
                xmlHTTPRequest.setRequestHeader('X-CSRFToken', token)
            },
            success: function () {
                $('#cart-alert-success').removeClass('hidden')
            },
            error: function (xhr, textStatus, errorThrown) {
                $('#cart-alert-fail').removeClass('hidden')
            }
        });
    });

    function hideAlertResultMessages() {
        $('#cart-alert-success').addClass('hidden');
        $('#cart-alert-fail').addClass('hidden');
    }

});
