// add to cart
$(document).on('click', '.cart-button', function (e) {
    let button = this
    let svg = button.children[0]
    var removeCartUrl = '/static/svg/remove_shopping_cart_24px.svg'

    $.ajax({
        type: "POST",
        url: button.attributes['data-url'].value,
        data: {
            'csrfmiddlewaretoken': button.parentElement.children[0].value
        },
        success: function (response) {
            console.log(response);
            svg.src = removeCartUrl;
            if (button.attributes['data-page'].value == 'list'){
                button.parentElement.parentElement.parentElement.parentElement.children[2].children[1].style.display = "";
            }
            button.classList.remove('cart-button');
            button.classList.add('cart-button-remove');
        },
        error: function () {
            console.log('an error occured');
        }
    });
})


// remove from cart
$(document).on('click', '.cart-button-remove', function(e) {
    let button = this;
    let svg = this.children[0];
    let addCartUrl = '/static/svg/add_shopping_cart_24px.svg';

    $.ajax({
        type: "POST",
        url: button.attributes['data-url-remove'].value,
        data: {
            'csrfmiddlewaretoken': button.parentElement.children[0].value
        },
        success: function (response) {
            console.log(response);
            svg.src = addCartUrl;
            if (button.attributes['data-page'].value == 'list'){
                button.parentElement.parentElement.parentElement.parentElement.children[2].children[1].style.display = "none";
            } else if (button.attributes['data-page'].value == 'cart') {
                button.parentElement.parentElement.style.display = 'none';
            }
            button.classList.remove('cart-button-remove');
            button.classList.add('cart-button');
        }
    });
})