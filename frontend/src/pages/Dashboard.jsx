import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
    Grid,
    Card,
    CardContent,
    Typography,
    Box,
    CircularProgress,
    Button,
} from '@mui/material';
import {
    Devices as DevicesIcon,
    CheckCircle as ActiveIcon,
    Warning as AlertIcon,
    Security as SecurityIcon,
    Refresh as RefreshIcon,
} from '@mui/icons-material';
import {
    LineChart,
    Line,
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    AreaChart,
    Area,
} from 'recharts';
import StatCard from '../components/cards/StatCard';
import deviceService from '../services/deviceService';
import monitoringService from '../services/monitoringService';

function Dashboard() {
    const navigate = useNavigate();

    // Fetch statistics
    const {
        data: stats,
        isLoading: isLoadingStats,
        isFetching: isFetchingStats,
        refetch: refetchStats
    } = useQuery({
        queryKey: ['device-statistics'],
        queryFn: deviceService.getStatistics,
        refetchInterval: 5000,
    });

    // Fetch network activity
    const {
        data: activityData,
        isLoading: isLoadingActivity,
        isFetching: isFetchingActivity,
        refetch: refetchActivity
    } = useQuery({
        queryKey: ['network-activity'],
        queryFn: monitoringService.getNetworkActivity,
        refetchInterval: 5000,
        initialData: [],
    });

    // Fetch device distribution
    const { data: deviceTypeData, refetch: refetchTypes } = useQuery({
        queryKey: ['device-distribution'],
        queryFn: monitoringService.getDeviceDistribution,
        refetchInterval: 5000,
        initialData: [],
    });

    // Fetch security score trend
    const { data: securityData, refetch: refetchSecurity } = useQuery({
        queryKey: ['security-score'],
        queryFn: monitoringService.getSecurityScore,
        refetchInterval: 5000,
        initialData: [],
    });

    // Fetch recent devices
    const { data: recentDevices, refetch: refetchRecent } = useQuery({
        queryKey: ['recent-devices'],
        queryFn: () => deviceService.getAllDevices({ limit: 5 }),
        select: (data) => {
            return Array.isArray(data) ? [...data].sort((a, b) => new Date(b.last_seen) - new Date(a.last_seen)).slice(0, 4) : [];
        },
        refetchInterval: 5000,
    });

    const isRefreshing = isFetchingStats || isFetchingActivity;

    const handleRefresh = async () => {
        await Promise.all([
            refetchStats(),
            refetchActivity(),
            refetchTypes(),
            refetchSecurity(),
            refetchRecent()
        ]);
    };

    const statistics = stats || {
        total_devices: 0,
        active_devices: 0,
        total_alerts: 0,
        average_security_score: 0,
    };

    return (
        <Box>
            {/* Header */}
            <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                    <Typography variant="h4" fontWeight={700} gutterBottom>
                        Network Overview
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Real-time monitoring of your network infrastructure
                    </Typography>
                </Box>
                <Button
                    variant="contained"
                    startIcon={isRefreshing ? <CircularProgress size={16} color="inherit" /> : <RefreshIcon />}
                    onClick={handleRefresh}
                    disabled={isRefreshing}
                    sx={{ borderRadius: 2, minWidth: 150 }}
                >
                    {isRefreshing ? 'Updating...' : 'Refresh Data'}
                </Button>
            </Box>

            {/* Stat Cards */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Total Devices"
                        value={statistics.total_devices}
                        icon={DevicesIcon}
                        color="primary"
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Active Now"
                        value={statistics.active_devices}
                        icon={ActiveIcon}
                        color="success"
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Security Score"
                        value={`${Math.round(statistics.average_security_score || 0)}/100`}
                        icon={SecurityIcon}
                        color="info"
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Active Alerts"
                        value={statistics.total_alerts}
                        icon={AlertIcon}
                        color="warning"
                    />
                </Grid>
            </Grid>

            {/* Charts Section */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid item xs={12} md={8}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Network Activity (Nodes)
                            </Typography>
                            <ResponsiveContainer width="100%" height={300}>
                                <LineChart data={activityData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                    <XAxis dataKey="time" stroke="rgba(255,255,255,0.5)" />
                                    <YAxis stroke="rgba(255,255,255,0.5)" />
                                    <Tooltip contentStyle={{ backgroundColor: '#1a1a2e', border: 'none', borderRadius: 8 }} />
                                    <Line type="monotone" dataKey="devices" stroke="#00d4ff" strokeWidth={3} dot={{ r: 4 }} />
                                </LineChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Device Distribution
                            </Typography>
                            <ResponsiveContainer width="100%" height={300}>
                                <PieChart>
                                    <Pie
                                        data={deviceTypeData}
                                        innerRadius={60}
                                        outerRadius={80}
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        {deviceTypeData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.color} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                    <Legend />
                                </PieChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Recent Activity Section */}
            <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Security Trend
                            </Typography>
                            <ResponsiveContainer width="100%" height={250}>
                                <AreaChart data={securityData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                    <XAxis dataKey="date" stroke="rgba(255,255,255,0.5)" />
                                    <YAxis stroke="rgba(255,255,255,0.5)" />
                                    <Tooltip />
                                    <Area type="monotone" dataKey="score" stroke="#00e676" fill="rgba(0, 230, 118, 0.2)" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                                <Typography variant="h6" fontWeight={600}>Recent Nodes</Typography>
                                <Button size="small" onClick={() => navigate('/devices')}>View All</Button>
                            </Box>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                                {recentDevices && recentDevices.length > 0 ? (
                                    recentDevices.map((device) => (
                                        <Box key={device.id || device.mac_address} sx={{ p: 1.5, borderRadius: 2, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)' }}>
                                            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                                                <Typography variant="body2" fontWeight={600}>{device.hostname || 'Unknown'}</Typography>
                                                <Typography variant="caption" color="text.secondary">{new Date(device.last_seen).toLocaleTimeString()}</Typography>
                                            </Box>
                                            <Typography variant="caption" color="primary.main">{device.ip_address}</Typography>
                                        </Box>
                                    ))
                                ) : (
                                    <Typography variant="body2" color="text.secondary" textAlign="center" py={4}>No active nodes detected</Typography>
                                )}
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
}

export default Dashboard;
