document.addEventListener('DOMContentLoaded', async () => {
    initSkeletons();
    
    // Check if onboarding data exists
    const onboarding = JSON.parse(localStorage.getItem('user_onboarding') || '{}');
    const bizName = onboarding.business_name || 'My Company';

    try {
        // Attempt backend API call
        const apiData = await window.api.getDashboard().catch(() => null);

        // Dynamic data incorporating onboarding input if present
        const data = {
            kpis: [
                { title: 'Total Complaints', value: apiData ? apiData.total : '5', trend: 'Live', color: 'blue' },
                { title: 'New Today', value: apiData ? apiData.new : '2', trend: 'Live', color: 'purple' },
                { title: 'In Progress', value: apiData ? apiData.inProgress : '2', trend: 'Live', color: 'amber' },
                { title: 'Resolved', value: apiData ? apiData.resolved : '1', trend: 'Live', color: 'emerald' },
                { title: 'Escalated', value: apiData ? apiData.escalated : '0', trend: '0%', color: 'rose' },
                { title: 'High Priority', value: apiData ? apiData.highPriority : '1', trend: 'Normal', color: 'orange' }
            ],
            recent: [
                { id: 'CMP-101', subject: `${bizName}: ${onboarding.problems ? onboarding.problems[0] || 'Delivery issue' : 'Late Delivery'}`, status: 'In Progress', date: 'Just now' },
                { id: 'CMP-102', subject: onboarding.custom_problem ? onboarding.custom_problem.slice(0, 30) + '...' : 'Defective Item Received', status: 'New', date: '10 mins ago' },
                { id: 'CMP-103', subject: 'Billing Adjustment Request', status: 'In Progress', date: '1 hr ago' },
                { id: 'CMP-104', subject: 'Account Login Issue', status: 'Resolved', date: '2 hrs ago' },
                { id: 'CMP-105', subject: 'Service Inquiry', status: 'New', date: '5 hrs ago' }
            ],
            insights: [
                `Configured resolution agent for ${bizName} (${onboarding.category || 'General'}).`,
                `Website URL scanned: ${onboarding.website || 'Default policy rules indexed'}.`,
                `Targeting channel: ${onboarding.channel || 'Email'} with automatic AI resolution suggestions.`
            ]
        };

        renderKPIs(data.kpis);
        renderRecent(data.recent);
        renderInsights(data.insights);
        initCharts(onboarding);
        
    } catch (e) {
        if(typeof showToast === 'function') showToast('Loaded Workspace Dashboard', 'info');
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
    document.getElementById('kpi-container').innerHTML = kpis.map(k => `
        <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
            <p class="text-sm font-medium text-slate-500 mb-1">${k.title}</p>
            <div class="flex items-end justify-between">
                <h4 class="text-2xl font-bold text-slate-800">${k.value}</h4>
                <span class="text-xs font-medium text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">${k.trend}</span>
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
            <td class="px-5 py-3 text-slate-800 font-medium">${item.subject}</td>
            <td class="px-5 py-3">
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${statusColors[item.status] || 'bg-slate-100 text-slate-700'}">${item.status}</span>
            </td>
            <td class="px-5 py-3 text-slate-500 text-xs">${item.date}</td>
        </tr>
    `).join('');
}

function renderInsights(insights) {
    const container = document.getElementById('ai-insights');
    if(!container) return;
    container.innerHTML = insights.map(text => `
        <div class="flex gap-3 bg-indigo-50/60 p-3 rounded-lg border border-indigo-100 mb-2">
            <div class="w-2 h-2 rounded-full bg-indigo-600 mt-1.5 flex-shrink-0"></div>
            <p class="text-xs text-slate-700 leading-relaxed font-medium">${text}</p>
        </div>
    `).join('');
}

function initCharts(onboarding) {
    const probLabels = onboarding.problems && onboarding.problems.length ? onboarding.problems : ['Delivery Delay', 'Quality', 'Billing', 'Support'];
    
    // Trend Chart
    const trendCtx = document.getElementById('trendChart');
    if(trendCtx) {
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Complaints',
                    data: [2, 4, 1, 5, 3, 2, 4],
                    borderColor: '#4F46E5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
        });
    }

    // Priority Chart
    const priorityCtx = document.getElementById('priorityChart');
    if(priorityCtx) {
        new Chart(priorityCtx, {
            type: 'doughnut',
            data: {
                labels: ['Low', 'Medium', 'High', 'Critical'],
                datasets: [{
                    data: [30, 40, 20, 10],
                    backgroundColor: ['#94A3B8', '#3B82F6', '#F59E0B', '#E11D48'],
                    borderWidth: 0
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'bottom' } } }
        });
    }

    // Dept Chart
    const deptCtx = document.getElementById('deptChart');
    if(deptCtx) {
        new Chart(deptCtx, {
            type: 'bar',
            data: {
                labels: ['Technical Support', 'Billing & Finance', 'Customer Relations'],
                datasets: [{
                    data: [5, 3, 2],
                    backgroundColor: '#8B5CF6',
                    borderRadius: 4
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
        });
    }

    // Category Chart
    const catCtx = document.getElementById('catChart');
    if(catCtx) {
        new Chart(catCtx, {
            type: 'bar',
            data: {
                labels: probLabels.slice(0, 4),
                datasets: [{
                    data: [4, 3, 2, 1],
                    backgroundColor: '#10B981',
                    borderRadius: 4
                }]
            },
            options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
        });
    }
}
