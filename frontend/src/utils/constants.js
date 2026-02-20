// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// API Endpoints
export const API_ENDPOINTS = {
    // Auth
    LOGIN: '/auth/login/',
    LOGOUT: '/auth/logout/',

    // Devices
    DEVICES: '/devices/',
    DEVICE_DETAIL: (id) => `/devices/${id}/`,
    DEVICES_ACTIVE: '/devices/active/',
    DEVICES_STATISTICS: '/devices/statistics/',
    DEVICES_SYNC: '/devices/sync/',
    DEVICE_BLOCK: (id) => `/devices/${id}/block/`,
    DEVICE_TRUST: (id) => `/devices/${id}/mark_trusted/`,

    // Security (when implemented)
    SECURITY_ALERTS: '/security/alerts/',
    SECURITY_SCORE: '/security/score/',

    // Monitoring (when implemented)
    MONITORING_LIVE: '/monitoring/live/',
    MONITORING_STATS: '/monitoring/stats/',
};

// Refresh Intervals (in milliseconds)
export const REFRESH_INTERVALS = {
    DASHBOARD: 30000, // 30 seconds
    DEVICES: 15000, // 15 seconds
    MONITORING: 5000, // 5 seconds
    SECURITY: 60000, // 1 minute
};

// Chart Colors
export const CHART_COLORS = {
    PRIMARY: '#00d4ff',
    SECONDARY: '#7c4dff',
    SUCCESS: '#00e676',
    WARNING: '#ffa726',
    ERROR: '#ff5252',
    INFO: '#00d4ff',
};

// Device Types
export const DEVICE_TYPES = {
    COMPUTER: 'computer',
    PHONE: 'phone',
    TABLET: 'tablet',
    IOT: 'iot',
    ROUTER: 'router',
    OTHER: 'other',
};

// Status Types
export const STATUS_TYPES = {
    ACTIVE: 'active',
    ONLINE: 'online',
    OFFLINE: 'offline',
    IDLE: 'idle',
    UNKNOWN: 'unknown',
};

// Severity Levels
export const SEVERITY_LEVELS = {
    CRITICAL: 'critical',
    HIGH: 'high',
    MEDIUM: 'medium',
    LOW: 'low',
    INFO: 'info',
};

// Local Storage Keys
export const STORAGE_KEYS = {
    AUTH_TOKEN: 'authToken',
    USER_PREFERENCES: 'userPreferences',
    APP_SETTINGS: 'appSettings',
};
