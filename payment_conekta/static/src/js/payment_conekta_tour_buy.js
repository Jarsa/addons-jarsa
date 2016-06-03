odoo.define('payment_conekta.tour', function (require) {
'use strict';

var Tour = require('web.Tour');

Tour.register({
    id:   'shop_buy_prod_conekta',
    name: "Try to buy products",
    path: '/shop',
    mode: 'test',
    steps: [
        {
            title:     "select ipod",
            element:   '.oe_product_cart a:contains("iPod")',
        },
        {
            title:     "click on add to cart",
            element:   '#product_detail form[action^="/shop/cart/update"] .btn',
        },
        {
            title:     "go to checkout",
            element:   'a[href="/shop/checkout"]',
        },
        {
            title:     "test without input error",
            element:   'form[action="/shop/confirm_order"] .btn:contains("Confirm")',
            onload: function (tour) {
                if ($("input[name='name']").val() === "")
                    $("input[name='name']").val("website_sale-test-shoptest");
                if ($("input[name='email']").val() === "")
                    $("input[name='email']").val("website_sale_test_shoptest@websitesaletest.odoo.com");
                $("input[name='phone']").val("123123123");
                $("input[name='street2']").val("123");
                $("input[name='city']").val("123");
                $("input[name='zip']").val("123");
                $("select[name='country_id']").val("21");
            },
        },
        {
            title:     "select payment",
            element:   '#payment_method label:has(img[title="Conekta"]) input',
        },
        {
            title:     "Pay Now",
            waitFor:   '#payment_method label:has(input:checked):has(img[title="Conekta"])',
            element:   '.oe_sale_acquirer_button .btn[name="conekta"]:visible',
            onload: function(tour){
                $('input[data-conekta="card[name]"]').val('payment_conekta-test');
                $('input[data-conekta="card[number]"]').val('4242424242424242');
                $('input[data-conekta="card[cvc]"]').val('123');
                $('input[data-conekta="card[exp_month]"]').val('10');
                $('input[data-conekta="card[exp_year]"]').val('2019');
            },
        },
        {
            title:     "finish",
            waitFor:   '.oe_website_sale:contains("Thank you for your order")',
        }
    ]
});

});

