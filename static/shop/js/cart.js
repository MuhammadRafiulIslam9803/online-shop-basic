function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }
        }
    }

    return cookieValue;
}


document.addEventListener("click", async function (event) {

    const button = event.target.closest(
        "[data-cart-action]"
    );

    if (!button) {
        return;
    }

    event.preventDefault();

    const url = button.dataset.url;
    const itemId = button.dataset.itemId;

    const csrfToken = getCookie("csrftoken");

    if (!csrfToken) {
        console.error("CSRF token not found!");
        return;
    }

    button.disabled = true;

    try {

        const response = await fetch(url, {

            method: "POST",

            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json"
            }

        });

        const data = await response.json();

        console.log("Cart response:", data);


        if (!data.success) {
            return;
        }


        // Remove item
        if (data.deleted) {

            const cartItem = document.getElementById(
                `cart-item-${itemId}`
            );

            if (cartItem) {
                cartItem.remove();
            }

            updateTotal(data.total);

            updateNavbarCount(data.cart_count);

            updateItemsCount();

            return;
        }


        // Quantity
        const quantity = document.getElementById(
            `quantity-${itemId}`
        );

        if (quantity) {
            quantity.textContent = data.quantity;
        }


        // Subtotal
        const subtotal = document.getElementById(
            `subtotal-${itemId}`
        );

        if (subtotal) {
            subtotal.textContent = `৳${data.subtotal}`;
        }


        // Total
        updateTotal(data.total);


        // Navbar
        updateNavbarCount(data.cart_count);

    }

    catch (error) {

        console.error(
            "Cart AJAX error:",
            error
        );

    }

    finally {

        button.disabled = false;

    }

});


function updateTotal(total) {

    const element = document.getElementById(
        "cart-total"
    );

    if (element) {
        element.textContent = `৳${total}`;
    }

}


function updateNavbarCount(count) {

    const element = document.getElementById(
        "navbar-cart-count"
    );

    if (element) {
        element.textContent = count;
    }

}


function updateItemsCount() {

    const element = document.getElementById(
        "cart-items-count"
    );

    if (!element) {
        return;
    }

    const items = document.querySelectorAll(
        '[id^="cart-item-"]'
    );

    element.textContent = items.length;

}