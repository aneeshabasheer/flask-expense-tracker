document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            // Monthly Trend Line Chart
            const ctxTrend = document.getElementById('trendChart').getContext('2d');
            new Chart(ctxTrend, {
                type: 'line',
                data: {
                    labels: data.monthly.labels,
                    datasets: [
                        {
                            label: 'Income ($)',
                            data: data.monthly.income,
                            borderColor: '#10b981',
                            fill: false,
                            tension: 0.3
                        },
                        {
                            label: 'Expenses ($)',
                            data: data.monthly.expense,
                            borderColor: '#ef4444',
                            fill: false,
                            tension: 0.3
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

            // Expense Breakdown Pie Chart
            const ctxPie = document.getElementById('expensePieChart').getContext('2d');
            new Chart(ctxPie, {
                type: 'pie',
                data: {
                    labels: data.categories.labels,
                    datasets: [{
                        data: data.categories.data,
                        backgroundColor: [
                            '#f59e0b', '#3b82f6', '#ec4899', '#8b5cf6',
                            '#10b981', '#06b6d4', '#6366f1', '#64748b'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        });
});