import api from './api';

export const deviceService = {
    // Get all devices
    getAllDevices: async (params = {}) => {
        const response = await api.get('/devices/', { params });
        return response.data;
    },

    // Get device by ID
    getDeviceById: async (id) => {
        const response = await api.get(`/devices/${id}/`);
        return response.data;
    },

    // Get active devices only
    getOnlineDevices: async () => {
        const response = await api.get('/devices/active/');
        return response.data;
    },

    // Get device statistics
    getStatistics: async () => {
        const response = await api.get('/devices/statistics/');
        return response.data;
    },

    // Sync devices from desktop app
    syncDevices: async (devices) => {
        const response = await api.post('/devices/sync/', { devices });
        return response.data;
    },

    // Block device
    blockDevice: async (id) => {
        const response = await api.post(`/devices/${id}/block/`);
        return response.data;
    },

    // Mark device as trusted
    markTrusted: async (id) => {
        const response = await api.post(`/devices/${id}/mark_trusted/`);
        return response.data;
    },
};

export default deviceService;
