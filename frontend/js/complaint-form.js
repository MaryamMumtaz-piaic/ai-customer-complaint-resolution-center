document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('newComplaintForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('submitBtn');
        const origText = btn.innerHTML;
        
        btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Processing...`;
        btn.disabled = true;
        lucide.createIcons();

        try {
            // Simulate API call
            await new Promise(r => setTimeout(r, 1200));
            
            showToast('Complaint logged successfully. Running AI Analysis...', 'success');
            
            // Show AI Panel
            form.style.display = 'none';
            const aiPanel = document.getElementById('aiPanel');
            aiPanel.classList.remove('hidden');
            
            // Re-init icons for AI panel
            lucide.createIcons();
            
        } catch (error) {
            showToast('Failed to submit complaint', 'error');
            btn.innerHTML = origText;
            btn.disabled = false;
        }
    });
});
