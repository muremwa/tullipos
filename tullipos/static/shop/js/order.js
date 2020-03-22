// deducts removed shoe's price from total cart price
function updateCartPrice (price) {
    const cartPrice = document.getElementById('cart-total');
    const newPrice = cartPrice.innerText - price;
    cartPrice.innerText = newPrice;

    if (newPrice == 0) {
        cartPrice.parentElement.style.display = 'none';
        document.getElementById('no-items-inc').style.display = 'block';
        document.getElementById('top-cart-line').style.display = 'none';
    };
}