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

function getCardBrand() {
    var card_number = document.getElementById("conekta-card-number");
    var brand = Conekta.card.getBrand(card_number.value);
    console.log(brand)
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