const API_BASE = 'http://localhost:8000/api';

// Mock data fallback
const mockData = {
    dashboard: {
        total: 1250, new: 45, inProgress: 320, resolved: 850, escalated: 35, highPriority: 12
    },
    complaints: [
        { id: 'C-1001', customer: 'John Doe', subject: 'Late Delivery', category: 'Shipping', priority: 'High', status: 'In Progress', agent: 'Sarah Jenkins', created: '2023-10-25T10:30:00Z' },
        { id: 'C-1002', customer: 'Jane Smith', subject: 'Defective Product', category: 'Product Quality', priority: 'Critical', status: 'Escalated', agent: 'Mike Ross', created: '2023-10-24T14:15:00Z' },
    ]
};

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const apiFetch = async (endpoint, options = {}) => {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.warn(`API call failed for ${endpoint}, using mock data if available.`, error);
        await delay(500); // Simulate network latency
        
        // Return mock data based on endpoint
        if (endpoint.includes('/dashboard')) return mockData.dashboard;
        if (endpoint.includes('/complaints')) return mockData.complaints;
        
        throw error;
    }
};

window.api = {
    getDashboard: () => apiFetch('/analytics/dashboard'),
    getComplaints: (filters) => apiFetch('/complaints', { method: 'POST', body: JSON.stringify(filters) }),
    getComplaint: (id) => apiFetch(`/complaints/${id}`),
    createComplaint: (data) => apiFetch('/complaints', { method: 'POST', body: JSON.stringify(data) }),
    // ... add other endpoints as needed
};
