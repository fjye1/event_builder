// ─── Helper Functions (no DOM access here) ───────────────────────────────────

function populateSelect(selectEl, items, placeholder) {
    selectEl.innerHTML = `<option value="0">${placeholder}</option>`;
    items.forEach(item => {
        const opt = document.createElement("option");
        opt.value = item.id;
        opt.textContent = item.name;
        selectEl.appendChild(opt);
    });
}

function makeTagSelect(selectId, containerId, inputId, placeholder) {
    const select    = document.getElementById(selectId);
    const container = document.getElementById(containerId);
    const input     = document.getElementById(inputId);
    let options     = [];

    function render() {
        const selected = Array.from(select.selectedOptions).map(o => ({
            id: o.value, name: o.text
        }));
        container.innerHTML = "";
        selected.forEach(item => {
            const tag = document.createElement("span");
            tag.className = "tag";
            tag.innerHTML = `${item.name} <button type="button" data-id="${item.id}">×</button>`;
            tag.querySelector("button").addEventListener("click", () => {
                select.querySelector(`option[value="${item.id}"]`).selected = false;
                render();
                if (selectId === "product") refreshExtras();
            });
            container.appendChild(tag);
        });
        container.appendChild(input);
        input.placeholder = selected.length ? "" : placeholder;
    }

    function setOptions(newOptions) {
        options = newOptions;
        select.innerHTML = "";
        options.forEach(item => {
            const opt = document.createElement("option");
            opt.value = item.id;
            opt.text  = item.name;
            select.appendChild(opt);
        });
        render();
    }

    input.addEventListener("input", () => {
        const q = input.value.toLowerCase();
        document.getElementById(inputId + "_suggestions")?.remove();
        if (!q) return;
        const alreadySelected = Array.from(select.selectedOptions).map(s => s.value);
        const matches = options.filter(o =>
            o.name.toLowerCase().includes(q) && !alreadySelected.includes(String(o.id))
        );
        if (!matches.length) return;
        const list = document.createElement("ul");
        list.id = inputId + "_suggestions";
        list.className = "tag-suggestions";
        matches.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item.name;
            li.addEventListener("mousedown", (e) => {
                e.preventDefault();
                select.querySelector(`option[value="${item.id}"]`).selected = true;
                input.value = "";
                list.remove();
                render();
                if (selectId === "product") refreshExtras();
            });
            list.appendChild(li);
        });
        input.style.position = "relative";
        input.insertAdjacentElement("afterend", list);
    });

    input.addEventListener("blur", () => {
        setTimeout(() => document.getElementById(inputId + "_suggestions")?.remove(), 150);
    });

    return { setOptions, render };
}

// ─── Everything that touches the DOM ─────────────────────────────────────────

document.addEventListener("DOMContentLoaded", async () => {
    console.log("✅ event.js loaded");
    console.log("Flatpickr available:", typeof flatpickr !== "undefined");

    // ─── Simple Selects ──────────────────────────────────────────────────────
    const companySelect = document.getElementById("company_id");
    const clientSelect  = document.getElementById("client_id");
    const venueSelect   = document.getElementById("venue_id");

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

    // ─── Tag Widgets ─────────────────────────────────────────────────────────
    const staffWidget   = makeTagSelect("staff",   "staff-tags",   "staff-input",   "Search staff...");
    const productWidget = makeTagSelect("product", "product-tags", "product-input", "Search products...");
    const extraWidget   = makeTagSelect("extra",   "extra-tags",   "extra-input",   "Search extras...");

    async function refreshExtras() {
        const selected = Array.from(document.getElementById("product").selectedOptions)
                             .map(o => o.value);
        if (!selected.length) {
            extraWidget.setOptions([]);
            return;
        }
        const params = selected.map(id => `product_id=${id}`).join("&");
        const res    = await fetch(`/api/extras?${params}`);
        extraWidget.setOptions(await res.json());
    }

    // ─── Load Staff & Products ────────────────────────────────────────────────
    const [staffRes, productRes] = await Promise.all([
        fetch("/api/staff"),
        fetch("/api/products")
    ]);
    staffWidget.setOptions(await staffRes.json());
    productWidget.setOptions(await productRes.json());

    // ─── Flatpickr ────────────────────────────────────────────────────────────
    flatpickr("#date", {
        dateFormat: "Y-m-d",
        defaultDate: null,
        allowInput: true,
    });

    flatpickr(".timepicker", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        defaultDate: null,
        time_24hr: true,
        minuteIncrement: 15,
        allowInput: true,
    });
});