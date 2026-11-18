document.addEventListener("DOMContentLoaded", function () {

    // SIDEBAR TOGGLE

    const menuToggle = document.getElementById("menuToggle");

    const sidebar = document.getElementById("sidebar");

    if (menuToggle && sidebar) {

        menuToggle.addEventListener("click", function () {

            sidebar.classList.toggle("active");

        });

    }


    // SALES ANALYTICS CHART

    const salesCanvas = document.getElementById("salesChart");

    if (salesCanvas) {

        new Chart(salesCanvas, {

            type: "line",

            data: {

                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],

                datasets: [{

                    label: "Sales Revenue",

                    data: [12000, 19000, 15000, 25000, 22000, 35000],

                    borderWidth: 3,

                    tension: 0.4,

                    fill: true

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: true,

                plugins: {

                    legend: {

                        display: true

                    }

                }

            }

        });

    }


    // PRODUCT DISTRIBUTION CHART

    const productCanvas = document.getElementById("productChart");

    const productData = window.dashboardData || {};

    if (productCanvas) {

        new Chart(productCanvas, {

            type: "doughnut",

            data: {

                labels: productData.productLabels || [],

                datasets: [{

                    label: "Stock",

                    data: productData.productCounts || [],

                    borderWidth: 1

                }]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        position: "bottom"

                    }

                }

            }

        });

    }


    // AUTO DISMISS ALERTS

    setTimeout(function () {

        document.querySelectorAll(".alert").forEach(function (alert) {

            const instance = bootstrap.Alert.getOrCreateInstance(alert);

            instance.close();

        });

    }, 4000);


});