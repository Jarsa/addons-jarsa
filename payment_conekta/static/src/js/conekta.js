$(document).ready(function() {
    odoo.define("payment_conekta.payment", function (require) {
        "use strict";

        var ajax = require('web.ajax');
        var $payment = $("#payment_method");
        var $conekta_input = $("img[title='Conekta']").parent().children('input');

        $("input[name='acquirer']").on("change", function (ev) {
            if ($conekta_input.is(":focus")) {
                $('#payment_method div').first().removeClass("col-lg-5").addClass("col-lg-3");
                $("#card-form").parent().parent().parent().removeClass("col-lg-3 col-sm-3").addClass("col-lg-5 col-sm-6");
                $("#card-form").parent().parent().removeClass("pull-right").addClass("pull-left");
                $("#card-wrapper").show();
            } else {
                $('#payment_method div').first().removeClass("col-lg-3").addClass("col-lg-5");
                $("#card-form").parent().parent().parent().removeClass("col-lg-5 col-sm-6").addClass("col-lg-3 col-sm-3");
                $("#card-wrapper").hide();
            }
        });

        $payment.on("click", 'button[name="conekta"]', function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            var $form = $(ev.currentTarget).parents('form');
            $form.find("button").prop("disabled", true).button('loading');
            var acquirer_id = $(ev.currentTarget).parents('div.oe_sale_acquirer_button').first().data('id');
            if (! acquirer_id) {
                return false;
            }
            Conekta.token.create($form, conektaSuccessResponseHandler, conektaErrorResponseHandler);
            ajax.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', {});
            return false;
        });

        var conektaSuccessResponseHandler = function(token) {
            var $form = $("#card-form");
            $form.append($("<input type='hidden' name='token_id'>").val(token.id));
            ajax.jsonRpc('/payment/conekta/charge', 'call', {'token': token.id}).then(function(response) {
                if (response === true) {
                    $form.get(0).submit();
                } else {
                    $form.find(".card-errors").text(response).addClass("alert alert-danger");
                    $form.find("button").prop("disabled", false).button('reset');
                }
            });
        };

        var conektaErrorResponseHandler = function(response) {
            var $form = $("#card-form");
            $form.find(".card-errors").text(response.message);
            $form.find("button").prop("disabled", false);
        };

        $('#card-form').card({
            container: '.card-wrapper',
            width: 200,

            formSelectors: {
                numberInput: '#conekta-card-number',
                expiryInput: '#exp_month, #exp_year',
                cvcInput: '#cvc',
                nameInput: '#cardholder_name'
            },
        });

        $('#conekta-card-number').on('keyup', function(){
            var card_number = this;
            var validation = Conekta.card.validateNumber(card_number.value);
            if (validation === true) {
                $("#card-number-div").removeClass("has-error").addClass("has-success");
                $("#card-form").find("button").prop("disabled", false);
            } else {
                $("#card-number-div").removeClass("has-success").addClass("has-error");
                $("#card-form").find("button").prop("disabled", true);
            }
        });

        $('#cvc').on('keyup', function(){
            var cvc = this;
            var validation = Conekta.card.validateCVC(cvc.value);
            if (validation === true) {
                $("#cvc-div").removeClass("has-error").addClass("has-success");
                $("#card-form").find("button").prop("disabled", false);
            } else {
                $("#cvc-div").removeClass("has-success").addClass("has-error");
                $("#card-form").find("button").prop("disabled", true);
            }
        });

        $('.expiration').on('keyup', function(){
            var exp_month = $("#exp_month");
            var exp_year = $("#exp_year");
            var validation = Conekta.card.validateExpirationDate(exp_month.val(), exp_year.val());
            if (validation === true) {
                $("#expiration-div").removeClass("has-error").addClass("has-success");
                $("#card-form").find("button").prop("disabled", false);
            } else {
                $("#expiration-div").removeClass("has-success").addClass("has-error");
                $("#card-form").find("button").prop("disabled", true);
            }
        });

    });
}); 
