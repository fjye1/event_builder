document.addEventListener("DOMContentLoaded", function () {
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