document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    new Chart(document.getElementById('volumeChart'), {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Volume',
                data: [350, 420, 280, 390],
                borderColor: '#4F46E5',
                tension: 0.3,
                fill: false
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    new Chart(document.getElementById('distChart'), {
        type: 'doughnut',
        data: {
            labels: ['Shipping', 'Quality', 'Billing', 'Service'],
            datasets: [{
                data: [45, 25, 20, 10],
                backgroundColor: ['#4F46E5', '#10B981', '#F59E0B', '#E11D48']
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    new Chart(document.getElementById('channelChart'), {
        type: 'pie',
        data: {
            labels: ['Email', 'Phone', 'Web'],
            datasets: [{
                data: [60, 25, 15],
                backgroundColor: ['#3B82F6', '#8B5CF6', '#14B8A6']
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
});
