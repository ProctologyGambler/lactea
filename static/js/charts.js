const chartEl = document.getElementById('progressChart');
if (chartEl) {
    const labels = JSON.parse(document.getElementById('chart-labels').textContent);
    const values = JSON.parse(document.getElementById('chart-values').textContent);

    new Chart(chartEl, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Minutes pumped',
                data: values,
                backgroundColor: 'rgba(236, 72, 153, 0.7)',
                borderColor: 'rgba(236, 72, 153, 1)',
                borderWidth: 1,
                borderRadius: 4,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.parsed.y} min`,
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#be185d' },
                    grid: { color: 'rgba(236, 72, 153, 0.08)' },
                },
                x: {
                    ticks: {
                        color: '#be185d',
                        maxRotation: 0,
                        autoSkip: true,
                        autoSkipPadding: 12,
                    },
                    grid: { display: false },
                },
            },
        },
    });
}
