const line = document.getElementById("line");
const pie = document.getElementById("pie");
let myChart1, myChart2, data_expense, labels_expense, label_title_expense;

const renderExpenseChart = (data, labels, type, title) => {
    const ctx = document.getElementById("myChart").getContext("2d");

    // Destroy existing charts if they exist
    if (myChart1) {
        myChart1.destroy();
    }
    if (myChart2) {
        myChart2.destroy();
    }

    // Create a new chart instance
    if (type === "line") {
        myChart1 = new Chart(ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: "This month's expenses",
                    data: data,
                    backgroundColor: [
                        "rgba(255, 99, 132, 0.2)",
                        "rgba(54, 162, 235, 0.2)",
                        "rgba(255, 206, 86, 0.2)",
                        "rgba(75, 192, 192, 0.2)",
                        "rgba(153, 102, 255, 0.2)",
                        "rgba(255, 159, 64, 0.2)"
                    ],
                    borderColor: [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)",
                        "rgba(75, 192, 192, 1)",
                        "rgba(153, 102, 255, 1)",
                        "rgba(255, 159, 64, 1)"
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                title: {
                    display: true,
                    text: title
                }
            }
        });
    } else if (type === "pie") {
        myChart2 = new Chart(ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: "This month's expenses",
                    data: data,
                    backgroundColor: [
                        "rgba(255, 99, 132, 0.2)",
                        "rgba(54, 162, 235, 0.2)",
                        "rgba(255, 206, 86, 0.2)",
                        "rgba(75, 192, 192, 0.2)",
                        "rgba(153, 102, 255, 0.2)",
                        "rgba(255, 159, 64, 0.2)"
                    ],
                    borderColor: [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)",
                        "rgba(75, 192, 192, 1)",
                        "rgba(153, 102, 255, 1)",
                        "rgba(255, 159, 64, 1)"
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                title: {
                    display: true,
                    text: title
                }
            }
        });
    }
};

const getChartData = (chartType) => {
    fetch("/expense-category-summary/")
        .then(response => response.json())
        .then(data => {
            const expenseCategoryData = data.expense_category_data;
            label_title_expense = data.label_title;
            const [expenseLabels, expenseData] = [Object.keys(expenseCategoryData), Object.values(expenseCategoryData)];
            renderExpenseChart(expenseData, expenseLabels, chartType, label_title_expense);
        });
};

document.addEventListener("DOMContentLoaded", () => {
    // Load pie chart by default
    getChartData("pie");

    // Add event listeners for switching between chart types
    line.addEventListener("click", () => {
        getChartData("line");
    });

    pie.addEventListener("click", () => {
        getChartData("pie");
    });
});
