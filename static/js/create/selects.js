document.addEventListener("DOMContentLoaded", function () {
    const companySelect = document.getElementById("company_id");
    const clientSelect  = document.getElementById("client_id");
    const venueSelect   = document.getElementById("venue_id");

    function populateSelect(selectEl, items, placeholder) {
        selectEl.innerHTML = `<option value="0">${placeholder}</option>`;
        items.forEach(item => {
            const opt = document.createElement("option");
            opt.value = item.id;
            opt.textContent = item.name;
            selectEl.appendChild(opt);
        });
    }

    companySelect.addEventListener("change", async () => {
        const companyId = companySelect.value;
        populateSelect(clientSelect, [], "— Select Client —");
        populateSelect(venueSelect,  [], "— None —");
        if (companyId == 0) return;
        const res = await fetch(`/api/clients?company_id=${companyId}`);
        populateSelect(clientSelect, await res.json(), "— Select Client —");
    });

    clientSelect.addEventListener("change", async () => {
        const clientId = clientSelect.value;
        populateSelect(venueSelect, [], "— None —");
        if (clientId == 0) return;
        const res = await fetch(`/api/venues?client_id=${clientId}`);
        populateSelect(venueSelect, await res.json(), "— None —");
    });
});