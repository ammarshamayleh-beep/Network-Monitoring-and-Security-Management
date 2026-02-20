import api from './api';

export const alertService = {
    // Get all alerts
    getAllAlerts: async (params = {}) => {
        const response = await api.get('/alerts/', { params });
        return response.data;
    },

    // Get alert by ID
    getAlertById: async (id) => {
        const response = await api.get(`/alerts/${id}/`);
        return response.data;
    },

    // Create new alert (mostly for internal use or simulation)
    createAlert: async (data) => {
        const response = await api.post('/alerts/', data);
        return response.data;
    },

    // Mark alert as resolved
    resolveAlert: async (id) => {
        const response = await api.patch(`/alerts/${id}/`, { resolved: true });
        return response.data;
    },

    // Get alerts stats (simulated for now if not endpoint exists)
    getStats: async () => {
        // We can either add an endpoint or calculate on frontend
        const response = await api.get('/alerts/');
        const alerts = response.data.results || response.data; // Handle pagination if present

        return {
            total: alerts.length,
            high: alerts.filter(a => a.severity === 'high').length,
            medium: alerts.filter(a => a.severity === 'medium').length,
            low: alerts.filter(a => a.severity === 'low').length,
            critical: alerts.filter(a => a.severity === 'critical').length,
        };
    }
};

export default alertService;
