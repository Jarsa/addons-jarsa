$(document).ready(function() {
    odoo.define("payment_conekta_oxxo.payment", function (require) {
        "use strict";

        var ajax = require('web.ajax');
        var $payment = $("#payment_method");

        $payment.on("click", 'button[name="conekta"]', function (ev) {
            
            return false;
        });

        $payment.on("click", 'button[id="conekta_oxxo"]', function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            $('#conekta_oxxo').prop("disabled", true).button('loading');
            var acquirer_id = $(ev.currentTarget).parents('div.oe_sale_acquirer_button').first().data('id');
            if (! acquirer_id) {
                return false;
            }
            ajax.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', {}).then(function(){
                ajax.jsonRpc('/payment/conekta/oxxo/charge', 'call', {}).then(function(response) {
                    if (response === true) {
                        $("#form-oxxo").get(0).submit();
                    } else {
                        $('#conekta_oxxo').prop("disabled", false).button('reset');
                        $('#oxxo-errors').text(response).addClass("alert alert-danger");
                    }
                });
            });
        });
    });
}); 
