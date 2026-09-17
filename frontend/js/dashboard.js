document.addEventListener('DOMContentLoaded', async () => {
    initSkeletons();
    
    try {
        // In real app, fetch from api: const data = await window.api.getDashboard();
        await new Promise(r => setTimeout(r, 800)); // Sim load
        const data = {
            kpis: [
                { title: 'Total Complaints', value: '1,250', trend: '+12%', color: 'blue' },
                { title: 'New Today', value: '45', trend: '+5%', color: 'purple' },
                { title: 'In Progress', value: '320', trend: '-2%', color: 'amber' },
                { title: 'Resolved', value: '850', trend: '+18%', color: 'emerald' },
                { title: 'Escalated', value: '35', trend: '-10%', color: 'rose' },
                { title: 'High Priority', value: '12', trend: '+2%', color: 'orange' }
            ],
            recent: [
                { id: 'C-1001', subject: 'Late Delivery', status: 'In Progress', date: '2 hrs ago' },
                { id: 'C-1002', subject: 'Defective Product', status: 'Escalated', date: '5 hrs ago' },
                { id: 'C-1003', subject: 'Billing Error', status: 'New', date: '1 day ago' },
                { id: 'C-1004', subject: 'Rude Staff', status: 'Resolved', date: '1 day ago' },
                { id: 'C-1005', subject: 'App Crash', status: 'In Progress', date: '2 days ago' }
            ],
            insights: [
                'Spike in "Late Delivery" complaints from NY region detected over last 48h.',
                'Agent Sarah J. resolved 25 tickets this week (15% above average).',
                'Billing issues resolution time dropped by 2.5h after new KB article.'
            ]
        };

        renderKPIs(data.kpis);
        renderRecent(data.recent);
        renderInsights(data.insights);
        initCharts();
        
    } catch (e) {
        showToast('Failed to load dashboard data', 'error');
    }
});

function initSkeletons() {
    const kpiHTML = Array(6).fill(0).map(() => `
        <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
            <div class="skeleton h-4 w-24 mb-2"></div>
            <div class="skeleton h-8 w-16 mb-2"></div>
            <div class="skeleton h-3 w-12"></div>
        </div>
    `).join('');
    document.getElementById('kpi-container').innerHTML = kpiHTML;
    
    document.getElementById('recent-table').innerHTML = Array(5).fill(0).map(() => `
        <tr><td colspan="4" class="px-5 py-4"><div class="skeleton h-4 w-full"></div></td></tr>
    `).join('');
}

function renderKPIs(kpis) {
    const colorMap = {
        blue: 'text-blue-600 bg-blue-100',
        purple: 'text-purple-600 bg-purple-100',
        amber: 'text-amber-600 bg-amber-100',
        emerald: 'text-emerald-600 bg-emerald-100',
        rose: 'text-rose-600 bg-rose-100',
        orange: 'text-orange-600 bg-orange-100'
    };
    
    document.getElementById('kpi-container').innerHTML = kpis.map(k => `
        <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
            <p class="text-sm font-medium text-slate-500 mb-1">${k.title}</p>
            <div class="flex items-end justify-between">
                <h4 class="text-2xl font-bold text-slate-800">${k.value}</h4>
                <span class="text-xs font-medium ${k.trend.startsWith('+') ? 'text-emerald-600' : 'text-rose-600'}">${k.trend}</span>
            </div>
        </div>
    `).join('');
}

function renderRecent(items) {
    const statusColors = {
        'New': 'bg-purple-100 text-purple-700',
        'In Progress': 'bg-blue-100 text-blue-700',
        'Resolved': 'bg-emerald-100 text-emerald-700',
        'Escalated': 'bg-rose-100 text-rose-700'
    };

    document.getElementById('recent-table').innerHTML = items.map(item => `
        <tr class="hover:bg-slate-50 cursor-pointer" onclick="window.location.href='complaint-detail.html?id=${item.id}'">
            <td class="px-5 py-3 font-medium text-indigo-600">${item.id}</td>
            <td class="px-5 py-3 text-slate-800">${item.subject}</td>
            <td class="px-5 py-3">
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${statusColors[item.status]}">${item.status}</span>
            </td>
            <td class="px-5 py-3 text-slate-500">${item.date}</td>
        </tr>
    `).join('');
}

function renderInsights(insights) {
    document.getElementById('ai-insights').innerHTML = insights.map(text => `
        <div class="flex gap-3 bg-indigo-50/50 p-3 rounded-lg border border-indigo-100">
            <div class="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-2 flex-shrink-0"></div>
            <p class="text-sm text-slate-700 leading-relaxed">${text}</p>
        </div>
    `).join('');
}

function initCharts() {
    // Trend Chart
    new Chart(document.getElementById('trendChart'), {
        type: 'line',
        data: {
            labels: ['1', '5', '10', '15', '20', '25', '30'],
            datasets: [{
                label: 'Complaints',
                data: [45, 52, 38, 65, 48, 55, 42],
                borderColor: '#4F46E5',
                backgroundColor: 'rgba(79, 70, 229, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
    });

    // Priority Chart
    new Chart(document.getElementById('priorityChart'), {
        type: 'doughnut',
        data: {
            labels: ['Low', 'Medium', 'High', 'Critical'],
            datasets: [{
                data: [40, 35, 15, 10],
                backgroundColor: ['#94A3B8', '#3B82F6', '#F59E0B', '#E11D48'],
                borderWidth: 0
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'bottom' } } }
    });

    // Dept Chart
    new Chart(document.getElementById('deptChart'), {
        type: 'bar',
        data: {
            labels: ['Support', 'Billing', 'Shipping', 'Product'],
            datasets: [{
                data: [120, 80, 150, 40],
                backgroundColor: '#8B5CF6',
                borderRadius: 4
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
    });

    // Category Chart
    new Chart(document.getElementById('catChart'), {
        type: 'bar',
        data: {
            labels: ['Delivery Delay', 'Quality', 'Refunds', 'Missing Item'],
            datasets: [{
                data: [85, 62, 45, 30],
                backgroundColor: '#10B981',
                borderRadius: 4
            }]
        },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
    });
}
