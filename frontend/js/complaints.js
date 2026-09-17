document.addEventListener('DOMContentLoaded', async () => {
    renderSkeletons();
    
    try {
        await new Promise(r => setTimeout(r, 600)); // Simulate API delay
        const mockComplaints = [
            { id: 'C-1001', customer: 'John Doe', subject: 'Late Delivery', category: 'Shipping', priority: 'High', status: 'In Progress', agent: 'Sarah Jenkins', created: '2023-10-25 10:30' },
            { id: 'C-1002', customer: 'Jane Smith', subject: 'Defective Product', category: 'Product Quality', priority: 'Critical', status: 'Escalated', agent: 'Mike Ross', created: '2023-10-24 14:15' },
            { id: 'C-1003', customer: 'Bob Wilson', subject: 'Billing Error', category: 'Finance', priority: 'Medium', status: 'New', agent: 'Unassigned', created: '2023-10-25 09:00' },
            { id: 'C-1004', customer: 'Alice Brown', subject: 'Rude Staff', category: 'Customer Service', priority: 'High', status: 'Resolved', agent: 'Sarah Jenkins', created: '2023-10-23 11:20' },
            { id: 'C-1005', customer: 'Charlie Davis', subject: 'App Crash', category: 'Technical', priority: 'Low', status: 'In Progress', agent: 'IT Dept', created: '2023-10-25 15:45' }
        ];
        
        renderTable(mockComplaints);
    } catch (e) {
        showToast('Failed to load complaints', 'error');
    }
});

function renderSkeletons() {
    document.getElementById('complaints-tbody').innerHTML = Array(5).fill(0).map(() => `
        <tr><td colspan="9" class="px-6 py-4"><div class="skeleton h-4 w-full"></div></td></tr>
    `).join('');
}

function renderTable(data) {
    const priorityColors = {
        'Low': 'bg-slate-100 text-slate-700',
        'Medium': 'bg-blue-100 text-blue-700',
        'High': 'bg-amber-100 text-amber-700',
        'Critical': 'bg-rose-100 text-rose-700'
    };
    
    const statusColors = {
        'New': 'bg-purple-100 text-purple-700',
        'In Progress': 'bg-blue-100 text-blue-700',
        'Resolved': 'bg-emerald-100 text-emerald-700',
        'Escalated': 'bg-rose-100 text-rose-700'
    };

    if (data.length === 0) {
        document.getElementById('complaints-tbody').innerHTML = `
            <tr><td colspan="9" class="px-6 py-12 text-center text-slate-500">
                <i data-lucide="inbox" class="w-12 h-12 mx-auto mb-3 text-slate-300"></i>
                <p>No complaints found matching your filters.</p>
            </td></tr>
        `;
        lucide.createIcons();
        return;
    }

    document.getElementById('complaints-tbody').innerHTML = data.map(item => `
        <tr class="hover:bg-slate-50 group">
            <td class="px-6 py-4 font-medium text-indigo-600 cursor-pointer" onclick="window.location.href='complaint-detail.html?id=${item.id}'">${item.id}</td>
            <td class="px-6 py-4 text-slate-800">${item.customer}</td>
            <td class="px-6 py-4 text-slate-800 font-medium max-w-[200px] truncate" title="${item.subject}">${item.subject}</td>
            <td class="px-6 py-4 text-slate-600">${item.category}</td>
            <td class="px-6 py-4"><span class="inline-flex px-2 py-1 rounded text-xs font-medium ${priorityColors[item.priority]}">${item.priority}</span></td>
            <td class="px-6 py-4"><span class="inline-flex px-2 py-1 rounded text-xs font-medium ${statusColors[item.status]}">${item.status}</span></td>
            <td class="px-6 py-4 text-slate-600">${item.agent}</td>
            <td class="px-6 py-4 text-slate-500 text-xs">${item.created}</td>
            <td class="px-6 py-4 text-right">
                <button class="text-indigo-600 hover:text-indigo-900 mx-1" onclick="window.location.href='complaint-detail.html?id=${item.id}'">View</button>
            </td>
        </tr>
    `).join('');
}
