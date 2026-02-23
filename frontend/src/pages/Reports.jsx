import { useState, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Grid,
    TextField,
    MenuItem,
    Button,
    Divider,
    Chip,
    LinearProgress,
    Alert,
    CircularProgress,
    List,
    ListItem,
    ListItemText,
} from '@mui/material';
import PdfIcon from '@mui/icons-material/PictureAsPdf';
import CsvIcon from '@mui/icons-material/TableChart';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';
import monitoringService from '../services/monitoringService';
import deviceService from '../services/deviceService';
import alertService from '../services/alertService';

function Reports() {
    const [reportType, setReportType] = useState('security');
    const [dateRange, setDateRange] = useState('week');
    const [isGenerating, setIsGenerating] = useState(false);
    const reportRef = useRef(null);

    // Fetch data for preview
    const { data: devices, isLoading: devicesLoading } = useQuery({
        queryKey: ['all-devices'],
        queryFn: deviceService.getAllDevices,
    });
    const { data: securityScore } = useQuery({
        queryKey: ['security-score-trend'],
        queryFn: monitoringService.getSecurityScore,
    });
    const { data: alerts } = useQuery({
        queryKey: ['alerts'],
        queryFn: () => alertService.getAllAlerts(),
    });

    const handleGenerate = () => {
        setIsGenerating(true);
        setTimeout(() => {
            setIsGenerating(false);
            // In a real app, this might trigger a specific backend generation
        }, 800);
    };

    const handleExportPDF = async () => {
        if (!reportRef.current) return;

        setIsGenerating(true);
        try {
            const canvas = await html2canvas(reportRef.current, {
                scale: 2,
                backgroundColor: '#0a1929',
                logging: false,
                useCORS: true
            });

            const imgData = canvas.toDataURL('image/png');
            const pdf = new jsPDF({
                orientation: 'portrait',
                unit: 'mm',
                format: 'a4'
            });

            const imgProps = pdf.getImageProperties(imgData);
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

            pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
            pdf.save(`smart-guardian-${reportType}-report.pdf`);
        } catch (error) {
            console.error('PDF export failed:', error);
            alert('Failed to export PDF.');
        } finally {
            setIsGenerating(false);
        }
    };

    const handleExportCSV = () => {
        setIsGenerating(true);
        try {
            let csvContent = "data:text/csv;charset=utf-8,";
            let fileName = `smart-guardian-${reportType}.csv`;

            if (reportType === 'devices' || reportType === 'comprehensive' || reportType === 'network') {
                const deviceList = devices?.results || devices || [];
                csvContent += "ID,Name,IP Address,MAC Address,Status,First Seen\n";
                deviceList.forEach(dev => {
                    csvContent += `${dev.id},"${dev.name}","${dev.ip_address}","${dev.mac_address}","${dev.status}","${dev.first_seen}"\n`;
                });
            } else {
                const alertList = alerts?.results || alerts || [];
                csvContent += "ID,Severity,Message,Timestamp\n";
                alertList.forEach(alt => {
                    csvContent += `${alt.id},"${alt.severity}","${alt.message}","${alt.timestamp}"\n`;
                });
            }

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", fileName);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } finally {
            setIsGenerating(false);
        }
    };

    // Derived data
    const deviceList = devices?.results || devices || [];
    const totalDevices = deviceList.length;
    const activeDevices = deviceList.filter(d => d.status === 'active' || d.status === 'online').length;

    const currentScoreData = securityScore && securityScore.length > 0
        ? securityScore[securityScore.length - 1]
        : { score: 85 };
    const currentScore = currentScoreData.score;

    const alertList = alerts?.results || alerts || [];
    const criticalAlerts = alertList.filter((a) => a.severity === 'critical').length;
    const warnings = alertList.filter((a) => a.severity === 'medium' || a.severity === 'high').length;

    // Helper to render dynamic content based on report type
    const renderPreviewContent = () => {
        switch (reportType) {
            case 'devices':
                return (
                    <>
                        <Typography variant="h6" gutterBottom fontWeight={600}>
                            1. DEVICE INVENTORY LIST
                        </Typography>
                        <Box sx={{ mb: 4 }}>
                            <List dense>
                                {deviceList.slice(0, 10).map((dev, i) => (
                                    <ListItem key={i} sx={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                        <ListItemText
                                            primary={`${dev.name || 'Unknown Device'} (${dev.ip_address})`}
                                            secondary={`MAC: ${dev.mac_address} | Status: ${dev.status}`}
                                            primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                                            secondaryTypographyProps={{ variant: 'caption' }}
                                        />
                                    </ListItem>
                                ))}
                            </List>
                            {totalDevices > 10 && (
                                <Typography variant="caption" color="text.secondary" sx={{ fontStyle: 'italic', ml: 2 }}>
                                    + {totalDevices - 10} more devices in full export
                                </Typography>
                            )}
                        </Box>
                        <Typography variant="h6" gutterBottom fontWeight={600}>
                            2. NETWORK SUMMARY
                        </Typography>
                        <Typography variant="body2" sx={{ ml: 2 }}>• Total Detected Devices: {totalDevices}</Typography>
                        <Typography variant="body2" sx={{ ml: 2 }}>• Active/Online Now: {activeDevices}</Typography>
                    </>
                );

            case 'network':
                return (
                    <>
                        <Typography variant="h6" gutterBottom fontWeight={600}>
                            1. NETWORK CONNECTIVITY STATUS
                        </Typography>
                        <Box sx={{ ml: 2, mb: 3 }}>
                            <Typography variant="body2">• Gateway Status: Online</Typography>
                            <Typography variant="body2">• Network Range: 192.168.1.0/24</Typography>
                            <Typography variant="body2">• Average Latency: 12ms</Typography>
                        </Box>
                        <Typography variant="h6" gutterBottom fontWeight={600}>
                            2. RECENT NETWORK EVENTS
                        </Typography>
                        <Box sx={{ ml: 2 }}>
                            {alertList.length > 0 ? (
                                alertList.slice(0, 5).map((a, i) => (
                                    <Typography key={i} variant="body2" gutterBottom>
                                        [{new Date(a.timestamp).toLocaleTimeString()}] {a.message}
                                    </Typography>
                                ))
                            ) : (
                                <Typography variant="body2">No major network events detected.</Typography>
                            )}
                        </Box>
                    </>
                );

            case 'comprehensive':
                return (
                    <>
                        <Typography variant="h6" gutterBottom fontWeight={600}>
                            1. SYSTEM OVERVIEW
                        </Typography>
                        <Box sx={{ ml: 2, mb: 3 }}>
                            <Typography variant="body2">• Security Score: {currentScore}/100</Typography>
                            <Typography variant="body2">• Device Count: {totalDevices}</Typography>
                            <Typography variant="body2">• Active Threats: {criticalAlerts}</Typography>
                        </Box>
                        <Typography variant="h6" gutterBottom fontWeight={600}>
                            2. TOP IDENTIFIED DEVICES
                        </Typography>
                        <Box sx={{ ml: 2, mb: 3 }}>
                            {deviceList.slice(0, 3).map((d, i) => (
                                <Typography key={i} variant="body2">• {d.name} ({d.ip_address})</Typography>
                            ))}
                        </Box>
                        <Typography variant="h6" gutterBottom fontWeight={600}>
                            3. SECURITY SUMMARY
                        </Typography>
                        <Box sx={{ ml: 2 }}>
                            <Typography variant="body2">• Critical Vulnerabilities: {criticalAlerts}</Typography>
                            <Typography variant="body2">• Medium/High Warnings: {warnings}</Typography>
                        </Box>
                    </>
                );

            case 'security':
            default:
                return (
                    <>
                        <Typography variant="h6" gutterBottom fontWeight={600}>
                            1. SECURITY RISK ANALYSIS
                        </Typography>
                        <Box sx={{ ml: 2, mb: 3 }}>
                            <Typography variant="body2" gutterBottom>
                                • Security Score: {currentScore}/100
                            </Typography>
                            <LinearProgress
                                variant="determinate"
                                value={currentScore}
                                color={currentScore > 70 ? 'success' : 'error'}
                                sx={{ height: 6, width: '200px', my: 1, borderRadius: 3 }}
                            />
                            <Typography variant="body2" gutterBottom>
                                • Status: {currentScore > 70 ? 'Secured' : 'Critically Vulnerable'}
                            </Typography>
                        </Box>

                        <Typography variant="h6" gutterBottom fontWeight={600}>
                            2. DETECTED THREATS & VULNERABILITIES
                        </Typography>
                        <Box sx={{ ml: 2, mb: 3 }}>
                            {criticalAlerts > 0 ? (
                                alertList.filter(a => a.severity === 'critical').slice(0, 4).map((a, i) => (
                                    <Typography key={i} variant="body2" color="error.main" gutterBottom>
                                        [CRITICAL] {a.message}
                                    </Typography>
                                ))
                            ) : (
                                <Alert severity="success" sx={{ py: 0 }}>No critical security threats detected.</Alert>
                            )}
                        </Box>

                        <Typography variant="h6" gutterBottom fontWeight={600}>
                            3. MITIGATION RECOMMENDATIONS
                        </Typography>
                        <Box sx={{ pl: 2 }}>
                            <Typography variant="body2">• Deploy latest security patches to all workstations.</Typography>
                            <Typography variant="body2">• Block port 3389/22 from external access.</Typography>
                            <Typography variant="body2">• Revise password policy for IoT devices.</Typography>
                        </Box>
                    </>
                );
        }
    };

    return (
        <Box>
            <Box sx={{ mb: 4 }}>
                <Typography variant="h4" fontWeight={700} gutterBottom>
                    Reports
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    Build and export customized security reports
                </Typography>
            </Box>

            <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Customization
                            </Typography>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, mt: 3 }}>
                                <TextField
                                    select
                                    label="Selection"
                                    value={reportType}
                                    onChange={(e) => setReportType(e.target.value)}
                                    fullWidth
                                >
                                    <MenuItem value="security">Security Analysis</MenuItem>
                                    <MenuItem value="devices">Device Inventory</MenuItem>
                                    <MenuItem value="network">Network Activity</MenuItem>
                                    <MenuItem value="comprehensive">Comprehensive Report</MenuItem>
                                </TextField>

                                <TextField
                                    select
                                    label="Range"
                                    value={dateRange}
                                    onChange={(e) => setDateRange(e.target.value)}
                                    fullWidth
                                >
                                    <MenuItem value="today">Today</MenuItem>
                                    <MenuItem value="week">Past Week</MenuItem>
                                    <MenuItem value="month">Past Month</MenuItem>
                                </TextField>

                                <Divider />

                                <Button
                                    variant="contained"
                                    size="large"
                                    onClick={handleGenerate}
                                    fullWidth
                                    disabled={isGenerating}
                                >
                                    Refresh Data
                                </Button>

                                <Box sx={{ display: 'flex', gap: 1 }}>
                                    <Button
                                        variant="outlined"
                                        startIcon={isGenerating ? <CircularProgress size={20} /> : <PdfIcon />}
                                        onClick={handleExportPDF}
                                        fullWidth
                                        disabled={isGenerating}
                                    >
                                        PDF
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        startIcon={isGenerating ? <CircularProgress size={20} /> : <CsvIcon />}
                                        onClick={handleExportCSV}
                                        fullWidth
                                        disabled={isGenerating}
                                    >
                                        CSV
                                    </Button>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={8}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Live Preview
                            </Typography>

                            <Box
                                ref={reportRef}
                                sx={{
                                    mt: 2,
                                    p: 4,
                                    backgroundColor: 'background.default',
                                    borderRadius: 2,
                                    minHeight: 500,
                                    border: '1px solid',
                                    borderColor: 'divider',
                                    color: 'text.primary',
                                    position: 'relative'
                                }}
                            >
                                {isGenerating && (
                                    <Box sx={{
                                        position: 'absolute',
                                        top: 0, left: 0, right: 0, bottom: 0,
                                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                                        backgroundColor: 'rgba(0,0,0,0.6)', zIndex: 10,
                                        borderRadius: 2
                                    }}>
                                        <CircularProgress />
                                    </Box>
                                )}

                                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                                    <Typography variant="h5" fontWeight={800} color="primary">
                                        SMART GUARDIAN
                                    </Typography>
                                    <Chip label="INTERNAL SECURE" size="small" color="primary" variant="outlined" />
                                </Box>

                                <Typography variant="h4" fontWeight={400} sx={{ mb: 0.5 }}>
                                    {reportType === 'security'
                                        ? 'Security Audit'
                                        : reportType === 'devices'
                                            ? 'Inventory Report'
                                            : reportType === 'network'
                                                ? 'Traffic Analysis'
                                                : 'Comprehensive Audit'}
                                </Typography>

                                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 3 }}>
                                    ID: SG-{Math.floor(Math.random() * 900000)} | {new Date().toLocaleString()}
                                </Typography>

                                <Divider sx={{ my: 3, borderStyle: 'dashed' }} />

                                {renderPreviewContent()}

                                <Box sx={{ mt: 'auto', pt: 6, textAlign: 'center' }}>
                                    <Typography variant="caption" color="text.secondary" sx={{ opacity: 0.5 }}>
                                        Generated by Smart Network Guardian Professional v2.0
                                        <br />
                                        © {new Date().getFullYear()} CyberSecurity Workspace
                                    </Typography>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
}

export default Reports;
