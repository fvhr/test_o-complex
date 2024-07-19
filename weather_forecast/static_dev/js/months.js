function formatDate(dateString) {
        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const date = new Date(dateString);
        return `${date.getDate()} ${months[date.getMonth()]}`;
    }

    // Format all dates on load
    document.addEventListener("DOMContentLoaded", function () {
        const dates = document.querySelectorAll(".date-format");
        dates.forEach(dateElement => {
            const originalDate = dateElement.dataset.date;
            dateElement.textContent = formatDate(originalDate);
        });
    });