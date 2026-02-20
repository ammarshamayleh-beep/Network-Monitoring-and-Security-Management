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
    AreaChart,
    Area,
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
} from 'recharts';
import StatCard from '../components/cards/StatCard';
import deviceService from '../services/deviceService';
import monitoringService from '../services/monitoringService';

function Dashboard() {
    const navigate = useNavigate();

    // Fetch statistics
    const { data: stats, isLoading: isLoadingStats, refetch: refetchStats } = useQuery({
        queryKey: ['device-statistics'],
        queryFn: deviceService.getStatistics,
        refetchInterval: 5000,
    });

    // Fetch network activity
    const { data: activityData, isLoading: isLoadingActivity, refetch: refetchActivity } = useQuery({
        queryKey: ['network-activity'],
        queryFn: monitoringService.getNetworkActivity,
        refetchInterval: 5000,
        initialData: [],
    });

    // Fetch device distribution
    const { data: deviceTypeData, isLoading: isLoadingTypes, refetch: refetchTypes } = useQuery({
        queryKey: ['device-distribution'],
        queryFn: monitoringService.getDeviceDistribution,
        refetchInterval: 5000,
        initialData: [],
    });

    // Fetch security score trend
    const { data: securityData, isLoading: isLoadingSecurity, refetch: refetchSecurity } = useQuery({
        queryKey: ['security-score'],
        queryFn: monitoringService.getSecurityScore,
        refetchInterval: 5000,
        initialData: [],
    });

    // Fetch recent devices (active ones for "Recent Activity")
    const { data: recentDevices, isLoading: isLoadingRecent, refetch: refetchRecent } = useQuery({
        queryKey: ['recent-devices'],
        queryFn: () => deviceService.getAllDevices({ limit: 5 }), // Assuming backend supports limit or we slice
        select: (data) => {
            // Sort by last_seen descending and take top 5
            return Array.isArray(data) ? [...data].sort((a, b) => new Date(b.last_seen) - new Date(a.last_seen)).slice(0, 4) : [];
        },
        refetchInterval: 5000,
    });

    const handleRefresh = () => {
        refetchStats();
        refetchActivity();
        refetchTypes();
        refetchSecurity();
        refetchRecent();
    };

    const isLoading = isLoadingStats || isLoadingActivity || isLoadingTypes || isLoadingSecurity || isLoadingRecent;

    if (isLoading && !stats) { // Show loading only on first load if no data
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
                <CircularProgress />
            </Box>
        );
    }

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
                    startIcon={<RefreshIcon />}
                    onClick={handleRefresh}
                    sx={{ borderRadius: 2 }}
                >
                    Refresh Data
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
                        trend="up"
                        trendValue="+3"
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Active Now"
                        value={statistics.active_devices}
                        icon={ActiveIcon}
                        color="success"
                        trend="up"
                        trendValue="+2"
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Security Score"
                        value={`${Math.round(statistics.average_security_score || 0)}/100`}
                        icon={SecurityIcon}
                        color="info"
                        trend="up"
                        trendValue="+5"
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Active Alerts"
                        value={statistics.total_alerts}
                        icon={AlertIcon}
                        color="warning"
                        trend="down"
                        trendValue="-1"
                    />
                </Grid>
            </Grid>

            {/* Charts Row 1 */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                {/* Network Activity Chart */}
                <Grid item xs={12} md={8}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Network Activity (24 Hours)
                            </Typography>
                            <ResponsiveContainer width="100%" height={300}>
                                <LineChart data={activityData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#1a2548" />
                                    <XAxis dataKey="time" stroke="#b0bec5" />
                                    <YAxis stroke="#b0bec5" />
                                    <Tooltip
                                        contentStyle={{
                                            backgroundColor: '#141b3d',
                                            border: '1px solid #1a2548',
                                            borderRadius: 8,
                                        }}
                                    />
                                    <Legend />
                                    <Line
                                        type="monotone"
                                        dataKey="devices"
                                        stroke="#00d4ff"
                                        strokeWidth={3}
                                        dot={{ fill: '#00d4ff', r: 5 }}
                                        activeDot={{ r: 7 }}
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Device Type Distribution */}
                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Device Types
                            </Typography>
                            <ResponsiveContainer width="100%" height={300}>
                                <PieChart>
                                    <Pie
                                        data={deviceTypeData}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={60}
                                        outerRadius={100}
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        {deviceTypeData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.color} />
                                        ))}
                                    </Pie>
                                    <Tooltip
                                        contentStyle={{
                                            backgroundColor: '#141b3d',
                                            border: '1px solid #1a2548',
                                            borderRadius: 8,
                                        }}
                                    />
                                    <Legend />
                                </PieChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Charts Row 2 */}
            <Grid container spacing={3}>
                {/* Security Score Trend */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Security Score Trend
                            </Typography>
                            <ResponsiveContainer width="100%" height={250}>
                                <AreaChart data={securityData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#1a2548" />
                                    <XAxis dataKey="date" stroke="#b0bec5" />
                                    <YAxis stroke="#b0bec5" />
                                    <Tooltip
                                        contentStyle={{
                                            backgroundColor: '#141b3d',
                                            border: '1px solid #1a2548',
                                            borderRadius: 8,
                                        }}
                                    />
                                    <Area
                                        type="monotone"
                                        dataKey="score"
                                        stroke="#00e676"
                                        fill="#00e67640"
                                        strokeWidth={2}
                                    />
                                </AreaChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Recent Activity */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                                <Typography variant="h6" fontWeight={600}>
                                    Recent Activity
                                </Typography>
                                <Button size="small" onClick={() => navigate('/devices')}>
                                    View All
                                </Button>
                            </Box>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                                {(recentDevices || []).length > 0 ? (
                                    recentDevices.map((device) => (
                                        <Box
                                            key={device.id || device.mac_address}
                                            sx={{
                                                p: 2,
                                                borderRadius: 2,
                                                backgroundColor: 'background.card',
                                                border: '1px solid',
                                                borderColor: 'divider',
                                            }}
                                        >
                                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                                                <Typography variant="body2" fontWeight={600}>
                                                    {device.hostname || 'Unknown Device'}
                                                </Typography>
                                                <Typography variant="caption" color="text.secondary">
                                                    {new Date(device.last_seen).toLocaleTimeString()}
                                                </Typography>
                                            </Box>
                                            <Typography variant="caption" color="text.secondary">
                                                {device.ip_address} - {device.vendor || 'Unknown Vendor'}
                                            </Typography>
                                        </Box>
                                    ))
                                ) : (
                                    <Typography variant="body2" color="text.secondary" textAlign="center" sx={{ py: 4 }}>
                                        No recent activity detected
                                    </Typography>
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
