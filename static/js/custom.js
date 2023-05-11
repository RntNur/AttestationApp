document.addEventListener('DOMContentLoaded', function () {
    let alerts = document.querySelectorAll('.alert');
    for (let i = 0; i < alerts.length; i++) {
        (function (alert) {
            setTimeout(function () {
                alert.style.opacity = 0;
                setTimeout(function () {
                    alert.remove();
                }, 1000);
            }, 3000);
        })(alerts[i]);
    }
});