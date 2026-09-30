document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            // Income vs Expense Chart
            const ctxOverview = document.getElementById('overviewChart').getContext('2d');
            new Chart(ctxOverview, {
                type: 'bar',
                data: {
                    labels: data.monthly.labels,
                    datasets: [
                        {
                            label: 'Income',
                            data: data.monthly.income,
                            backgroundColor: 'rgba(16, 185, 129, 0.75)',
                            borderRadius: 6
                        },
                        {
                            label: 'Expense',
                            data: data.monthly.expense,
                            backgroundColor: 'rgba(239, 68, 68, 0.75)',
                            borderRadius: 6
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'top' } }
                }
            });

            // Category Distribution Chart
            const ctxCategory = document.getElementById('categoryChart').getContext('2d');
            new Chart(ctxCategory, {
                type: 'doughnut',
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
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom' } }
                }
            });
        });
});