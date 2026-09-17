// Global app state and utilities

// Toast Notification System
const createToastContainer = () => {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    return container;
};

window.showToast = (message, type = 'info') => {
    const container = createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    // Select icon based on type
    let icon = 'info';
    if(type === 'success') icon = 'check-circle';
    if(type === 'error') icon = 'x-circle';
    if(type === 'warning') icon = 'alert-triangle';

    toast.innerHTML = `
        <i data-lucide="${icon}" class="w-5 h-5 flex-shrink-0 ${type === 'success' ? 'text-emerald-500' : type === 'error' ? 'text-rose-500' : type === 'warning' ? 'text-amber-500' : 'text-blue-500'}"></i>
        <div class="text-sm font-medium text-slate-800">${message}</div>
    `;
    
    container.appendChild(toast);
    if(window.lucide) lucide.createIcons({ root: toast });
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
};

// Auth check
const checkAuth = () => {
    if(window.location.pathname.endsWith('index.html') || window.location.pathname === '/') return;
    const user = localStorage.getItem('user');
    if (!user) {
        window.location.href = 'index.html';
    }
};

// Initialize common UI elements
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    if(window.lucide) lucide.createIcons();
    
    // Sidebar active state
    const currentPath = window.location.pathname.split('/').pop();
    document.querySelectorAll('.sidebar-nav-item').forEach(item => {
        if(item.getAttribute('href') === currentPath) {
            item.classList.add('bg-indigo-50', 'text-indigo-600');
            item.classList.remove('text-slate-600', 'hover:bg-slate-50');
        }
    });

    // User profile in sidebar
    const user = JSON.parse(localStorage.getItem('user'));
    const userProfileEl = document.getElementById('sidebar-user-profile');
    if(user && userProfileEl) {
        userProfileEl.innerHTML = `
            <div class="flex items-center gap-3 w-full">
                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold">
                    ${user.email.charAt(0).toUpperCase()}
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-slate-900 truncate">${user.email}</p>
                    <p class="text-xs text-slate-500 truncate">Agent</p>
                </div>
            </div>
        `;
    }
});

// Logout
window.logout = () => {
    localStorage.removeItem('user');
    window.location.href = 'index.html';
};
