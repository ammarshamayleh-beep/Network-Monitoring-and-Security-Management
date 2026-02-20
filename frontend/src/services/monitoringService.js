import api from './api';

export const monitoringService = {
    // Get network activity (last 24 hours)
    getNetworkActivity: async () => {
        const response = await api.get('/monitoring/network_activity/');
        return response.data;
    },

    // Get security score trend
    getSecurityScore: async () => {
        const response = await api.get('/monitoring/security_score/');
        return response.data;
    },

    // Get device distribution
    getDeviceDistribution: async () => {
        const response = await api.get('/monitoring/device_distribution/');
        return response.data;
    },
};

export default monitoringService;
