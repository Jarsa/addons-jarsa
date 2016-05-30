odoo.define('website_sale.tour', function (require) {
'use strict';

var Tour = require('web.Tour');

Tour.register({
    id:   'shop_buy_prod_conekta',
    name: "Try to buy products",
    path: '/shop',
    mode: 'test',
    steps: [
        {
            title:  "search ipod",
            element: 'form:has(input[name="search"]) a.a-submit',
            onload: function() {
                $('input[name="search"]').val("ipod");
            }
        },
        {
            title:     "select ipod",
            element:   '.oe_product_cart a:contains("iPod")',
        },
        {
            title:     "select ipod 32GB",
            waitFor:   '#product_detail',
            element:   'label:contains(32 GB) input',
        },
        {
            title:     "click on add to cart",
            waitFor:   'label:contains(32 GB) input:propChecked',
            element:   '#product_detail form[action^="/shop/cart/update"] .btn',
        },
        {
            title:     "add one more iPod",
            waitFor:   '.my_cart_quantity:contains(2)',
            element:   '#cart_products tr:contains("32 GB") a.js_add_cart_json:eq(1)',
        },
        {
            title:     "set one iPod",
            waitNot:   '#cart_products tr:contains("Apple In-Ear Headphones")',
            element:   '#cart_products input.js_quantity',
            sampleText: '1',
        },
        {
            title:     "go to checkout",
            waitFor:   '#cart_products input.js_quantity:propValue(1)',
            element:   'a[href="/shop/checkout"]',
        },
        {
            title:     "test with input error",
            element:   'form[action="/shop/confirm_order"] .btn:contains("Confirm")',
            onload: function (tour) {
                $("input[name='phone']").val("");
            },
        },
        {
            title:     "test without input error",
            waitFor:   'form[action="/shop/confirm_order"] .has-error',
            element:   'form[action="/shop/confirm_order"] .btn:contains("Confirm")',
            onload: function (tour) {
                if ($("input[name='name']").val() === "")
                    $("input[name='name']").val("website_sale-test-shoptest");
                if ($("input[name='email']").val() === "")
                    $("input[name='email']").val("website_sale_test_shoptest@websitesaletest.odoo.com");
                $("input[name='phone']").val("123");
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
            element:   '.oe_sale_acquirer_button .btn[type="submit"]:visible',
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

