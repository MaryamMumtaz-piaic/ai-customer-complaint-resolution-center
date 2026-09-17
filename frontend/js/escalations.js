document.addEventListener('DOMContentLoaded', () => {
    const data = [
        { id: 'C-1002', subject: 'Defective Product', priority: 'Critical', escalatedTo: 'Manager Team', deadline: 'Today 17:00' },
        { id: 'C-0985', subject: 'Legal Threat', priority: 'Critical', escalatedTo: 'Legal Dept', deadline: 'Overdue (Yesterday)' },
        { id: 'C-1044', subject: 'Repeated Billing Issue', priority: 'High', escalatedTo: 'Finance Head', deadline: 'Tomorrow 12:00' }
    ];

    document.getElementById('esc-tbody').innerHTML = data.map(item => `
        <tr class="hover:bg-slate-50 ${item.deadline.includes('Overdue') ? 'bg-rose-50/30' : ''}">
            <td class="px-6 py-4 font-medium text-indigo-600"><a href="complaint-detail.html?id=${item.id}">${item.id}</a></td>
            <td class="px-6 py-4 text-slate-800 font-medium">${item.subject}</td>
            <td class="px-6 py-4"><span class="text-rose-600 bg-rose-100 px-2 py-1 rounded text-xs font-medium">${item.priority}</span></td>
            <td class="px-6 py-4 text-slate-600">${item.escalatedTo}</td>
            <td class="px-6 py-4 font-medium ${item.deadline.includes('Overdue') ? 'text-rose-600' : 'text-slate-600'}">${item.deadline}</td>
            <td class="px-6 py-4 text-right">
                <button class="px-3 py-1 bg-indigo-600 text-white rounded text-xs font-medium hover:bg-indigo-700">Resolve</button>
            </td>
        </tr>
    `).join('');
    
    lucide.createIcons();
});
