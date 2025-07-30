class SalesChart {
    constructor(canvasId, data) {
        this.canvas = document.getElementById(canvasId);
        this.data = data;
        this.chart = this._createChart();
    }

    _createChart() {
        return new Chart(this.canvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: this.data.dates,
                datasets: [
                    {
                        label: 'Actual Sales',
                        data: this.data.actual,
                        borderColor: '#4bc0c0',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        tension: 0.3,
                        borderWidth: 2
                    },
                    {
                        label: 'Predicted Sales',
                        data: this.data.predicted,
                        borderColor: '#ff6384',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.3,
                        borderWidth: 2,
                        borderDash: [5, 5]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Sales Prediction Performance',
                        font: {
                            size: 16
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: (context) => {
                                let label = context.dataset.label || '';
                                if (label) label += ': ';
                                label += context.parsed.y.toLocaleString();
                                return label;
                            }
                        }
                    },
                    annotation: {
                        annotations: {
                            line1: {
                                type: 'line',
                                yMin: Math.max(...this.data.actual),
                                yMax: Math.max(...this.data.actual),
                                borderColor: 'rgba(75, 75, 75, 0.5)',
                                borderWidth: 1,
                                borderDash: [6, 6],
                                label: {
                                    content: 'Peak Sales',
                                    enabled: true,
                                    position: 'right'
                                }
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: (value) => value.toLocaleString()
                        }
                    },
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    }
}