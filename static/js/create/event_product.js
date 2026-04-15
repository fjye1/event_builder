
document.addEventListener("DOMContentLoaded", function () {
    const productSelect = document.getElementById("product_id");
    const extrasSelect = document.getElementById("extras");

    function updateExtras() {
        const productId = productSelect.value;

        if (!productId) {
            extrasSelect.innerHTML = "";
            return;
        }

        fetch(`/api/extras?product_id=${productId}`)
            .then(response => response.json())
            .then(data => {
                extrasSelect.innerHTML = "";

                data.forEach(extra => {
                    const option = document.createElement("option");
                    option.value = extra.id;
                    option.textContent = extra.name;
                    extrasSelect.appendChild(option);
                });
            });
    }

    // Trigger on change
    productSelect.addEventListener("change", updateExtras);

    // Trigger once on load
    updateExtras();
});
