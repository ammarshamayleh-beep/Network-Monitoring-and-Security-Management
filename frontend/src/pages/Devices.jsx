import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TablePagination,
    TextField,
    InputAdornment,
    Chip,
    IconButton,
    Button,
    CircularProgress,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
} from '@mui/material';
import {
    Search as SearchIcon,
    Refresh as RefreshIcon,
    Info as InfoIcon,
    Block as BlockIcon,
    CheckCircle as TrustedIcon,
} from '@mui/icons-material';
import deviceService from '../services/deviceService';

function Devices() {
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedDevice, setSelectedDevice] = useState(null);
    const [detailsOpen, setDetailsOpen] = useState(false);

    // Fetch devices from API
    const { data, isLoading, refetch } = useQuery({
        queryKey: ['devices'],
        queryFn: deviceService.getAllDevices,
        refetchInterval: 15000, // Refresh every 15 seconds
    });

    const devices = data?.results || [];

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const handleViewDetails = (device) => {
        setSelectedDevice(device);
        setDetailsOpen(true);
    };

    const handleCloseDetails = () => {
        setDetailsOpen(false);
        setSelectedDevice(null);
    };

    // Filter devices based on search
    const filteredDevices = devices.filter((device) =>
        device.ip_address?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        device.hostname?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        device.mac_address?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const getStatusColor = (status) => {
        switch (status?.toLowerCase()) {
            case 'active':
            case 'online':
                return 'success';
            case 'offline':
                return 'error';
            default:
                return 'default';
        }
    };

    if (isLoading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box>
            {/* Header */}
            <Box sx={{ mb: 4 }}>
                <Typography variant="h4" fontWeight={700} gutterBottom>
                    Network Devices
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    All devices detected on your network
                </Typography>
            </Box>

            {/* Controls */}
            <Card sx={{ mb: 3 }}>
                <CardContent>
                    <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                        <TextField
                            placeholder="Search by IP, hostname, or MAC..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            sx={{ flexGrow: 1 }}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <SearchIcon />
                                    </InputAdornment>
                                ),
                            }}
                        />
                        <Button
                            variant="contained"
                            startIcon={<RefreshIcon />}
                            onClick={() => refetch()}
                        >
                            Refresh
                        </Button>
                    </Box>
                </CardContent>
            </Card>

            {/* Devices Table */}
            <Card>
                <TableContainer>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>IP Address</TableCell>
                                <TableCell>Hostname</TableCell>
                                <TableCell>MAC Address</TableCell>
                                <TableCell>Vendor</TableCell>
                                <TableCell>Type</TableCell>
                                <TableCell>Status</TableCell>
                                <TableCell>Last Seen</TableCell>
                                <TableCell align="center">Actions</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {filteredDevices
                                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                                .map((device) => (
                                    <TableRow
                                        key={device.id}
                                        hover
                                        sx={{ cursor: 'pointer' }}
                                        onClick={() => handleViewDetails(device)}
                                    >
                                        <TableCell>
                                            <Typography variant="body2" fontWeight={600} color="primary.main">
                                                {device.ip_address}
                                            </Typography>
                                        </TableCell>
                                        <TableCell>{device.hostname || 'Unknown'}</TableCell>
                                        <TableCell>
                                            <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                                                {device.mac_address || 'N/A'}
                                            </Typography>
                                        </TableCell>
                                        <TableCell>{device.vendor || 'Unknown'}</TableCell>
                                        <TableCell>
                                            <Chip
                                                label={device.device_type || 'Unknown'}
                                                size="small"
                                                color="info"
                                                variant="outlined"
                                            />
                                        </TableCell>
                                        <TableCell>
                                            <Chip
                                                label={device.status || 'Unknown'}
                                                size="small"
                                                color={getStatusColor(device.status)}
                                            />
                                        </TableCell>
                                        <TableCell>
                                            <Typography variant="caption" color="text.secondary">
                                                {device.last_seen
                                                    ? new Date(device.last_seen).toLocaleString()
                                                    : 'Never'}
                                            </Typography>
                                        </TableCell>
                                        <TableCell align="center" onClick={(e) => e.stopPropagation()}>
                                            <IconButton size="small" onClick={() => handleViewDetails(device)}>
                                                <InfoIcon fontSize="small" />
                                            </IconButton>
                                        </TableCell>
                                    </TableRow>
                                ))}
                        </TableBody>
                    </Table>
                </TableContainer>
                <TablePagination
                    component="div"
                    count={filteredDevices.length}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onPageChange={handleChangePage}
                    onRowsPerPageChange={handleChangeRowsPerPage}
                    rowsPerPageOptions={[5, 10, 25, 50]}
                />
            </Card>

            {/* Device Details Dialog */}
            <Dialog open={detailsOpen} onClose={handleCloseDetails} maxWidth="sm" fullWidth>
                <DialogTitle>
                    <Typography variant="h6" fontWeight={600}>
                        Device Details
                    </Typography>
                </DialogTitle>
                <DialogContent dividers>
                    {selectedDevice && (
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                            <Box>
                                <Typography variant="caption" color="text.secondary">
                                    IP Address
                                </Typography>
                                <Typography variant="body1" fontWeight={600}>
                                    {selectedDevice.ip_address}
                                </Typography>
                            </Box>
                            <Box>
                                <Typography variant="caption" color="text.secondary">
                                    MAC Address
                                </Typography>
                                <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                                    {selectedDevice.mac_address || 'N/A'}
                                </Typography>
                            </Box>
                            <Box>
                                <Typography variant="caption" color="text.secondary">
                                    Hostname
                                </Typography>
                                <Typography variant="body1">
                                    {selectedDevice.hostname || 'Unknown'}
                                </Typography>
                            </Box>
                            <Box>
                                <Typography variant="caption" color="text.secondary">
                                    Vendor
                                </Typography>
                                <Typography variant="body1">
                                    {selectedDevice.vendor || 'Unknown'}
                                </Typography>
                            </Box>
                            <Box>
                                <Typography variant="caption" color="text.secondary">
                                    Device Type
                                </Typography>
                                <Typography variant="body1">
                                    {selectedDevice.device_type || 'Unknown'}
                                </Typography>
                            </Box>
                            <Box>
                                <Typography variant="caption" color="text.secondary">
                                    Status
                                </Typography>
                                <Chip
                                    label={selectedDevice.status || 'Unknown'}
                                    size="small"
                                    color={getStatusColor(selectedDevice.status)}
                                    sx={{ mt: 0.5 }}
                                />
                            </Box>
                            <Box>
                                <Typography variant="caption" color="text.secondary">
                                    First Seen
                                </Typography>
                                <Typography variant="body2">
                                    {selectedDevice.first_seen
                                        ? new Date(selectedDevice.first_seen).toLocaleString()
                                        : 'Unknown'}
                                </Typography>
                            </Box>
                            <Box>
                                <Typography variant="caption" color="text.secondary">
                                    Last Seen
                                </Typography>
                                <Typography variant="body2">
                                    {selectedDevice.last_seen
                                        ? new Date(selectedDevice.last_seen).toLocaleString()
                                        : 'Unknown'}
                                </Typography>
                            </Box>
                        </Box>
                    )}
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDetails}>Close</Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
}

export default Devices;
