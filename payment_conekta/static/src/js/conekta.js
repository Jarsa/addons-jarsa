$(function () {
  $("#card-form").submit(function(event) {
    var $form = $(this);
    $form.find("button").prop("disabled", true);
    Conekta.token.create($form, conektaSuccessResponseHandler, conektaErrorResponseHandler);
    return false;
  });
});

var conektaSuccessResponseHandler = function(token) {
    var $form = $("#card-form");
    $form.append($("<input name='token_id'>").val(token.id));
    $form.get(0).submit();
};

var conektaErrorResponseHandler = function(response) {
  var $form = $("#card-form");
  $form.find(".card-errors").text(response.message);
  $form.find("button").prop("disabled", false);
};

function getCardInfo() {
    var card_number = document.getElementById("conekta-card-number");
    var validation = Conekta.card.validateNumber(card_number.value)
    if (validation == true) {
        $("#card-number-div").removeClass("has-error").addClass("has-success");
    } else {
        $("#card-number-div").removeClass("has-success").addClass("has-error");
    }
    var brand = Conekta.card.getBrand(card_number.value);
    if (brand == "visa") {
        $("#visa").show();
        $("#mastercard").hide();
        $("#amex").hide();
        $("#all-cards").hide();
    } else if (brand == "mastercard") {
        $("#visa").hide();
        $("#mastercard").show();
        $("#amex").hide();
        $("#all-cards").hide();
    } else if (brand == "amex") {
        $("#visa").hide();
        $("#mastercard").hide();
        $("#amex").show();
        $("#all-cards").hide();
    } else {
        $("#visa").hide();
        $("#mastercard").hide();
        $("#amex").hide();
        $("#all-cards").show();
    }
}

function validateCVC() {
    var cvc = document.getElementById("cvc");
    var validation = Conekta.card.validateCVC(cvc.value);
    if (validation == true) {
        $("#cvc-div").removeClass("has-error").addClass("has-success");
    } else {
        $("#cvc-div").removeClass("has-success").addClass("has-error");
    }
}

function validateExpiration() {
    var exp_month = document.getElementById("exp_month");
    var exp_year = document.getElementById("exp_year");
    var validation = Conekta.card.validateExpirationDate(exp_month.value, exp_year.value)
    if (validation == true) {
        $("#expiration-div").removeClass("has-error").addClass("has-success");
    } else {
        $("#expiration-div").removeClass("has-success").addClass("has-error");
    }
}