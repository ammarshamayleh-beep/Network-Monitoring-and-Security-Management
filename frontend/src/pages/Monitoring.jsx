import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Grid,
    Chip,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Button,
    CircularProgress,
    LinearProgress,
} from '@mui/material';
import {
    PlayArrow as PlayIcon,
    Stop as StopIcon,
    Refresh as RefreshIcon,
    Speed as SpeedIcon,
    Devices as DevicesIcon,
    History as HistoryIcon,
} from '@mui/icons-material';
import deviceService from '../services/deviceService';
import monitoringService from '../services/monitoringService';

function Monitoring() {
    const [isMonitoring, setIsMonitoring] = useState(false);
    const [lastUpdate, setLastUpdate] = useState(new Date());

    // Fetch online devices
    const {
        data: onlineDevices,
        isLoading: devicesLoading,
        isFetching: isFetchingDevices,
        refetch: refetchDevices
    } = useQuery({
        queryKey: ['online-devices'],
        queryFn: deviceService.getOnlineDevices,
        refetchInterval: isMonitoring ? 3000 : false,
        enabled: true,
    });

    // Fetch network activity
    const {
        data: networkActivity,
        isLoading: activityLoading,
        isFetching: isFetchingActivity,
        refetch: refetchActivity
    } = useQuery({
        queryKey: ['network-activity-live'],
        queryFn: monitoringService.getNetworkActivity,
        refetchInterval: isMonitoring ? 3000 : false,
        enabled: true,
    });

    const handleToggleMonitoring = () => {
        setIsMonitoring(!isMonitoring);
        if (!isMonitoring) {
            refetchDevices();
            refetchActivity();
        }
    };

    const handleManualRefresh = async () => {
        await Promise.all([refetchDevices(), refetchActivity()]);
        setLastUpdate(new Date());
    };

    useEffect(() => {
        if (onlineDevices || networkActivity) {
            setLastUpdate(new Date());
        }
    }, [onlineDevices, networkActivity]);

    // Derived stats
    const liveDevicesList = Array.isArray(onlineDevices) ? onlineDevices : (onlineDevices?.results || []);

    // Last traffic point
    const latestStat = networkActivity && networkActivity.length > 0
        ? networkActivity[networkActivity.length - 1]
        : null;

    const currentTraffic = latestStat ? (latestStat.devices * 50) : 0;

    const getStatusColor = (status) => {
        const s = String(status).toLowerCase();
        return (s === 'active' || s === 'online') ? 'success' : 'default';
    };

    const isRefreshing = isFetchingDevices || isFetchingActivity;

    return (
        <Box>
            {/* Top Progress Bar when loading */}
            {isRefreshing && <LinearProgress sx={{ mb: 2, borderRadius: 1, height: 4 }} />}
            {!isRefreshing && <Box sx={{ mb: 2, height: 4 }} />}

            {/* Header */}
            <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                    <Typography variant="h4" fontWeight={700} gutterBottom>
                        Live Monitoring
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                        Real-time inspection of your network ecosystem
                    </Typography>
                </Box>
                <Box sx={{ display: 'flex', gap: 2 }}>
                    <Button
                        variant="outlined"
                        onClick={handleManualRefresh}
                        startIcon={isRefreshing ? <CircularProgress size={16} color="inherit" /> : <RefreshIcon />}
                        disabled={isRefreshing}
                        sx={{ minWidth: 160 }}
                    >
                        {isRefreshing ? 'Refreshing...' : 'Manual Refresh'}
                    </Button>
                    <Button
                        variant={isMonitoring ? 'outlined' : 'contained'}
                        color={isMonitoring ? 'error' : 'success'}
                        startIcon={isMonitoring ? <StopIcon /> : <PlayIcon />}
                        onClick={handleToggleMonitoring}
                        sx={{ minWidth: 180 }}
                    >
                        {isMonitoring ? 'Stop Real-time' : 'Start Real-time'}
                    </Button>
                </Box>
            </Box>

            {/* Status Cards */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid item xs={12} sm={6} md={3}>
                    <Card sx={{ height: '100%', borderLeft: 6, borderColor: isMonitoring ? 'success.main' : 'error.main', transition: 'all 0.3s' }}>
                        <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                <Typography variant="overline" color="text.secondary">System Status</Typography>
                                <HistoryIcon fontSize="small" color="disabled" />
                            </Box>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                                <Box
                                    sx={{
                                        width: 10,
                                        height: 10,
                                        borderRadius: '50%',
                                        backgroundColor: isMonitoring ? 'success.main' : 'error.main',
                                        boxShadow: isMonitoring ? '0 0 10px #00e676' : 'none',
                                        animation: isMonitoring ? 'pulse 1.5s infinite' : 'none',
                                        '@keyframes pulse': {
                                            '0%': { transform: 'scale(1)', opacity: 1 },
                                            '50%': { transform: 'scale(1.5)', opacity: 0.5 },
                                            '100%': { transform: 'scale(1)', opacity: 1 },
                                        },
                                    }}
                                />
                                <Typography variant="h5" fontWeight={700}>
                                    {isMonitoring ? 'LIVE' : 'IDLE'}
                                </Typography>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <Card sx={{ height: '100%', borderLeft: 6, borderColor: 'primary.main' }}>
                        <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                <Typography variant="overline" color="text.secondary">Active Devices</Typography>
                                <DevicesIcon fontSize="small" color="disabled" />
                            </Box>
                            <Typography variant="h4" fontWeight={800} color="primary.main">
                                {devicesLoading ? <CircularProgress size={24} /> : liveDevicesList.length}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <Card sx={{ height: '100%', borderLeft: 6, borderColor: 'info.main' }}>
                        <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                <Typography variant="overline" color="text.secondary">Current Traffic</Typography>
                                <SpeedIcon fontSize="small" color="disabled" />
                            </Box>
                            <Typography variant="h4" fontWeight={800} color="info.main">
                                {activityLoading ? (
                                    <CircularProgress size={24} />
                                ) : (
                                    `${(currentTraffic / 1024).toFixed(2)} GB`
                                )}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <Card sx={{ height: '100%', borderLeft: 6, borderColor: 'warning.main' }}>
                        <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                <Typography variant="overline" color="text.secondary">Last Sync</Typography>
                                <RefreshIcon fontSize="small" color="disabled" />
                            </Box>
                            <Typography variant="body1" fontWeight={700}>
                                {lastUpdate.toLocaleTimeString()}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                                {isMonitoring ? 'Polling every 3s' : 'Static view'}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Live Devices Table */}
            <Card sx={{ borderRadius: 2, overflow: 'hidden' }}>
                <Box sx={{ p: 2, backgroundColor: 'rgba(255,255,255,0.03)', borderBottom: '1px solid divider', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="h6" fontWeight={700}>
                        Active Discovery Feed
                    </Typography>
                    {isRefreshing && <CircularProgress size={20} />}
                </Box>
                <TableContainer>
                    <Table>
                        <TableHead>
                            <TableRow sx={{ backgroundColor: 'rgba(255,255,255,0.02)' }}>
                                <TableCell sx={{ fontWeight: 700 }}>ENDPOINT</TableCell>
                                <TableCell sx={{ fontWeight: 700 }}>IDENTITY / HOSTNAME</TableCell>
                                <TableCell sx={{ fontWeight: 700 }}>VULNERABILITY STATUS</TableCell>
                                <TableCell sx={{ fontWeight: 700 }}>LAST SEEN</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {devicesLoading && liveDevicesList.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={4} align="center" sx={{ py: 10 }}>
                                        <CircularProgress size={40} />
                                        <Typography sx={{ mt: 2 }} color="text.secondary">Connecting to Discovery Service...</Typography>
                                    </TableCell>
                                </TableRow>
                            ) : liveDevicesList.length > 0 ? (
                                liveDevicesList.map((device) => (
                                    <TableRow key={device.id || device.mac_address} hover>
                                        <TableCell>
                                            <Typography variant="body2" fontWeight={800} color="primary.main">
                                                {device.ip_address}
                                            </Typography>
                                            <Typography variant="caption" color="text.secondary">
                                                MAC: {device.mac_address}
                                            </Typography>
                                        </TableCell>
                                        <TableCell>
                                            <Typography variant="body2">{device.hostname || 'Unknown Node'}</Typography>
                                            <Typography variant="caption" color="text.secondary">{device.vendor || 'Generic Device'}</Typography>
                                        </TableCell>
                                        <TableCell>
                                            <Chip
                                                label={String(device.status || 'Active').toUpperCase()}
                                                size="small"
                                                color={getStatusColor(device.status || 'active')}
                                                sx={{ fontWeight: 600, px: 1 }}
                                            />
                                        </TableCell>
                                        <TableCell>
                                            <Typography variant="body2">
                                                {device.last_seen ? new Date(device.last_seen).toLocaleTimeString() : 'Just now'}
                                            </Typography>
                                        </TableCell>
                                    </TableRow>
                                ))
                            ) : (
                                <TableRow>
                                    <TableCell colSpan={4} align="center" sx={{ py: 8 }}>
                                        <Box sx={{ opacity: 0.5 }}>
                                            <DevicesIcon sx={{ fontSize: 48, mb: 1 }} />
                                            <Typography variant="h6">No active devices detected</Typography>
                                            <Typography variant="body2">
                                                Ensure the Desktop Application is running, connected, and has performed a Scan.
                                            </Typography>
                                            <Button
                                                variant="contained"
                                                sx={{ mt: 2 }}
                                                onClick={() => refetchDevices()}
                                                disabled={isRefreshing}
                                            >
                                                {isRefreshing ? 'Retrying...' : 'Retry Discovery'}
                                            </Button>
                                        </Box>
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Card>
        </Box>
    );
}

export default Monitoring;
