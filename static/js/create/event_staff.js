document.addEventListener("DOMContentLoaded", function () {
    const eventSelect = document.getElementById("event_id"); // if you have it
    const productSelect = document.getElementById("event_product_id");

    function loadEventProducts() {
        const eventId = eventSelect ? eventSelect.value : null;

        if (!eventId) {
            productSelect.innerHTML = "";
            return;
        }

        fetch(`/api/event_products?event_id=${eventId}`)
            .then(response => response.json())
            .then(data => {
                productSelect.innerHTML = "";

                // Optional general assignment
                const generalOption = document.createElement("option");
                generalOption.value = "";
                generalOption.textContent = "— General Event —";
                productSelect.appendChild(generalOption);

                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = item.label;
                    productSelect.appendChild(option);
                });
            });
    }

    // Run on change
    if (eventSelect) {
        eventSelect.addEventListener("change", loadEventProducts);
    }

    // Run on page load
    loadEventProducts();
});
