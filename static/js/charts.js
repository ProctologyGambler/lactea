const chartEl = document.getElementById('progressChart');
if (chartEl) {
    const labels = JSON.parse(document.getElementById('chart-labels').textContent);
    const values = JSON.parse(document.getElementById('chart-values').textContent);

    // Read skin palette from CSS variables
    const style = getComputedStyle(document.body);
    const barColor = style.getPropertyValue('--chart-bar').trim() || 'rgba(236, 72, 153, 0.7)';
    const barBorder = style.getPropertyValue('--chart-bar-border').trim() || 'rgba(236, 72, 153, 1)';
    const tickColor = style.getPropertyValue('--chart-tick').trim() || '#be185d';
    const gridColor = style.getPropertyValue('--chart-grid').trim() || 'rgba(236, 72, 153, 0.08)';

    new Chart(chartEl, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Minutes pumped',
                data: values,
                backgroundColor: barColor,
                borderColor: barBorder,
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
                    ticks: { color: tickColor },
                    grid: { color: gridColor },
                },
                x: {
                    ticks: {
                        color: tickColor,
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
