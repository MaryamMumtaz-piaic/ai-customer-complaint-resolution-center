document.addEventListener('DOMContentLoaded', () => {
    const data = [
        { name: 'Shipping_Policy_v2.pdf', type: 'PDF', chunks: 142, status: 'Ready', date: '2023-10-20' },
        { name: 'Refund_Guidelines.docx', type: 'DOCX', chunks: 85, status: 'Ready', date: '2023-10-18' },
        { name: 'Q3_Product_Specs.pdf', type: 'PDF', chunks: 312, status: 'Processing', date: '2023-10-25' },
        { name: 'Old_Returns.txt', type: 'TXT', chunks: 45, status: 'Archived', date: '2022-01-15' }
    ];

    const getStatusHtml = (status) => {
        if(status === 'Ready') return `<span class="bg-emerald-100 text-emerald-700 px-2 py-1 rounded text-xs font-medium"><i data-lucide="check" class="w-3 h-3 inline mr-1"></i>Ready</span>`;
        if(status === 'Processing') return `<span class="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-medium"><i data-lucide="loader-2" class="w-3 h-3 inline mr-1 animate-spin"></i>Processing</span>`;
        if(status === 'Archived') return `<span class="bg-amber-100 text-amber-700 px-2 py-1 rounded text-xs font-medium">Archived</span>`;
    };

    const getTypeIcon = (type) => {
        if(type === 'PDF') return 'file-text';
        if(type === 'DOCX') return 'file';
        return 'file-minus';
    };

    document.getElementById('kb-tbody').innerHTML = data.map(item => `
        <tr class="hover:bg-slate-50">
            <td class="px-6 py-4 font-medium text-slate-800 flex items-center gap-2"><i data-lucide="${getTypeIcon(item.type)}" class="w-4 h-4 text-slate-400"></i>${item.name}</td>
            <td class="px-6 py-4 text-slate-600">${item.type}</td>
            <td class="px-6 py-4 text-slate-600">${item.chunks}</td>
            <td class="px-6 py-4">${getStatusHtml(item.status)}</td>
            <td class="px-6 py-4 text-slate-500">${item.date}</td>
            <td class="px-6 py-4 text-right">
                <button class="text-slate-400 hover:text-rose-600 mx-1" title="Delete"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
            </td>
        </tr>
    `).join('');
    
    lucide.createIcons();

    // Dropzone mock
    document.getElementById('dropzone').addEventListener('click', () => {
        showToast('File explorer opened (mock)', 'info');
    });
});
