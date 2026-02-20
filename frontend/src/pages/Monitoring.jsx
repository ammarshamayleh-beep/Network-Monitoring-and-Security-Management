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
} from '@mui/material';
import {
    PlayArrow as PlayIcon,
    Stop as StopIcon,
    Refresh as RefreshIcon,
} from '@mui/icons-material';
import deviceService from '../services/deviceService';
import monitoringService from '../services/monitoringService';

function Monitoring() {
    const [isMonitoring, setIsMonitoring] = useState(false);
    const [lastUpdate, setLastUpdate] = useState(new Date());

    // Fetch online devices
    const { data: onlineDevices, isLoading, refetch: refetchDevices } = useQuery({
        queryKey: ['online-devices'],
        queryFn: deviceService.getOnlineDevices, // Assuming this endpoint exists or filter getAllDevices
        refetchInterval: isMonitoring ? 5000 : false, // Poll only if monitoring
        enabled: isMonitoring,
    });

    // Fetch network activity (for total traffic simulation or real data)
    const { data: networkActivity, refetch: refetchActivity } = useQuery({
        queryKey: ['network-activity-live'],
        queryFn: monitoringService.getNetworkActivity,
        refetchInterval: isMonitoring ? 5000 : false,
        enabled: isMonitoring,
    });

    const handleToggleMonitoring = () => {
        setIsMonitoring(!isMonitoring);
        if (!isMonitoring) {
            // Trigger immediate refresh when starting
            refetchDevices();
            refetchActivity();
            setLastUpdate(new Date());
        }
    };

    // Derived stats
    const devices = Array.isArray(onlineDevices) ? onlineDevices : (onlineDevices?.results || []);
    // If endpoint not precise, filter local valid unique IPs
    const liveDevicesList = devices.length > 0 ? devices : [];

    // Simulate total traffic based on activity data
    const currentTraffic = networkActivity && networkActivity.length > 0
        ? networkActivity[networkActivity.length - 1].devices * 50 // roughly 50MB per device
        : 0;

    const getTrafficColor = (traffic) => {
        if (traffic > 800) return 'error';
        if (traffic > 300) return 'warning';
        return 'success';
    };

    const getStatusColor = (status) => {
        return (status === 'active' || status === 'online') ? 'success' : 'default';
    };

    return (
        <Box>
            {/* Header */}
            <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                    <Typography variant="h4" fontWeight={700} gutterBottom>
                        Live Monitoring
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Real-time network activity and device monitoring
                    </Typography>
                </Box>
                <Box sx={{ display: 'flex', gap: 2 }}>
                    <Button
                        variant={isMonitoring ? 'outlined' : 'contained'}
                        color={isMonitoring ? 'error' : 'success'}
                        startIcon={isMonitoring ? <StopIcon /> : <PlayIcon />}
                        onClick={handleToggleMonitoring}
                    >
                        {isMonitoring ? 'Stop Monitoring' : 'Start Monitoring'}
                    </Button>
                </Box>
            </Box>

            {/* Status Cards */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Typography variant="body2" color="text.secondary" gutterBottom>
                                Monitoring Status
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                                <Box
                                    sx={{
                                        width: 12,
                                        height: 12,
                                        borderRadius: '50%',
                                        backgroundColor: isMonitoring ? 'success.main' : 'error.main',
                                        animation: isMonitoring ? 'pulse 2s infinite' : 'none',
                                        '@keyframes pulse': {
                                            '0%, 100%': { opacity: 1 },
                                            '50%': { opacity: 0.5 },
                                        },
                                    }}
                                />
                                <Typography variant="h6" fontWeight={600}>
                                    {isMonitoring ? 'Active' : 'Stopped'}
                                </Typography>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Typography variant="body2" color="text.secondary" gutterBottom>
                                Active Connections
                            </Typography>
                            <Typography variant="h4" fontWeight={700} color="primary.main" sx={{ mt: 1 }}>
                                {liveDevicesList.length}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Typography variant="body2" color="text.secondary" gutterBottom>
                                Total Traffic Estimate
                            </Typography>
                            <Typography variant="h4" fontWeight={700} color="info.main" sx={{ mt: 1 }}>
                                {(currentTraffic / 1024).toFixed(2)} GB
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Typography variant="body2" color="text.secondary" gutterBottom>
                                Last Update
                            </Typography>
                            <Typography variant="body1" fontWeight={600} sx={{ mt: 1 }}>
                                {isMonitoring ? new Date().toLocaleTimeString() : 'Paused'}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Live Devices Table */}
            <Card>
                <CardContent>
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                        Live Device Status
                    </Typography>
                    <TableContainer>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>IP Address</TableCell>
                                    <TableCell>Hostname</TableCell>
                                    <TableCell>Status</TableCell>
                                    <TableCell>Last Activity</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {liveDevicesList.length > 0 ? (
                                    liveDevicesList.map((device) => (
                                        <TableRow key={device.id || device.mac} hover>
                                            <TableCell>
                                                <Typography variant="body2" fontWeight={600} color="primary.main">
                                                    {device.ip_address}
                                                </Typography>
                                            </TableCell>
                                            <TableCell>{device.hostname || 'Unknown'}</TableCell>
                                            <TableCell>
                                                <Chip
                                                    label={device.status || 'Active'}
                                                    size="small"
                                                    color={getStatusColor(device.status || 'active')}
                                                    sx={{ textTransform: 'capitalize' }}
                                                />
                                            </TableCell>
                                            <TableCell>
                                                <Typography variant="caption" color="text.secondary">
                                                    {device.last_seen ? new Date(device.last_seen).toLocaleTimeString() : 'Just now'}
                                                </Typography>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                ) : (
                                    <TableRow>
                                        <TableCell colSpan={4} align="center">
                                            {isMonitoring ? "Scanning for active devices..." : "Start monitoring to view live devices."}
                                        </TableCell>
                                    </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </CardContent>
            </Card>
        </Box>
    );
}

export default Monitoring;
