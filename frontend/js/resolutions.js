document.addEventListener('DOMContentLoaded', () => {
    const data = [
        { id: 'RES-001', category: 'Shipping Delay', dept: 'Support', time: '45 mins', snippet: 'Customer complained about 3-day delay.', resolution: 'Upgraded shipping to overnight, provided 10% discount coupon.' },
        { id: 'RES-002', category: 'Product Defect', dept: 'Quality', time: '4 hrs', snippet: 'Widget arrived broken.', resolution: 'Initiated immediate replacement. Provided prepaid return label for defective unit.' },
    ];

    document.getElementById('res-container').innerHTML = data.map(item => `
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <span class="bg-slate-100 text-slate-700 px-2 py-1 rounded text-xs font-medium">${item.category}</span>
                </div>
                <div class="text-right text-xs text-slate-500">
                    Dept: ${item.dept} | Avg Time: ${item.time}
                </div>
            </div>
            <div class="mb-4">
                <p class="text-xs text-slate-500 mb-1">Original Issue:</p>
                <p class="text-sm text-slate-700 italic">"${item.snippet}"</p>
            </div>
            <div class="mb-4">
                <p class="text-xs text-slate-500 mb-1">Standard Resolution:</p>
                <p class="text-sm text-slate-800 font-medium">${item.resolution}</p>
            </div>
            <button class="w-full py-2 border border-slate-300 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-50 transition" onclick="showToast('Template copied to clipboard', 'success')">Use as Template</button>
        </div>
    `).join('');
    
    lucide.createIcons();
});
