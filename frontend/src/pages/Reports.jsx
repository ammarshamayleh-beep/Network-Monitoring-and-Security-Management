import { useQuery } from '@tanstack/react-query';
import monitoringService from '../services/monitoringService';
import deviceService from '../services/deviceService';
import alertService from '../services/alertService';

function Reports() {
    const [reportType, setReportType] = useState('security');
    const [dateRange, setDateRange] = useState('week');

    // Fetch data for preview
    const { data: devices } = useQuery({ queryKey: ['all-devices'], queryFn: deviceService.getAllDevices });
    const { data: stats } = useQuery({ queryKey: ['device-statistics'], queryFn: deviceService.getStatistics }); // Use stats endpoint if available or derive
    const { data: securityScore } = useQuery({ queryKey: ['security-score-trend'], queryFn: monitoringService.getSecurityScore });
    const { data: alerts } = useQuery({ queryKey: ['alerts'], queryFn: () => alertService.getAllAlerts() });

    const handleGenerate = () => {
        console.log('Generating report:', { reportType, dateRange });
        // In real implementation, this would call the API
        alert("Report generation started! (Simulation)");
    };

    // Derived data for preview
    const totalDevices = devices?.count || devices?.length || 0;
    const activeDevices = devices?.results?.filter(d => d.status === 'active' || d.status === 'online').length || 0;
    const currentScore = securityScore && securityScore.length > 0 ? securityScore[securityScore.length - 1].score : 85;
    const alertList = alerts?.results || alerts || [];
    const criticalAlerts = alertList.filter(a => a.severity === 'critical').length;
    const warnings = alertList.filter(a => a.severity === 'medium' || a.severity === 'high').length;

    return (
        <Box>
            {/* ... Header & Config ... */}
            <Box sx={{ mb: 4 }}>
                <Typography variant="h4" fontWeight={700} gutterBottom>
                    Reports
                </Typography>
                {/* ... */}
            </Box>

            <Grid container spacing={3}>
                {/* Report Configuration */}
                <Grid item xs={12} md={4}>
                    {/* ... kept same ... */}
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Report Configuration
                            </Typography>

                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, mt: 3 }}>
                                <TextField
                                    select
                                    label="Report Type"
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
                                    label="Date Range"
                                    value={dateRange}
                                    onChange={(e) => setDateRange(e.target.value)}
                                    fullWidth
                                >
                                    <MenuItem value="today">Today</MenuItem>
                                    <MenuItem value="week">Last 7 Days</MenuItem>
                                    <MenuItem value="month">Last 30 Days</MenuItem>
                                    <MenuItem value="custom">Custom Range</MenuItem>
                                </TextField>

                                <Divider />

                                <Button
                                    variant="contained"
                                    size="large"
                                    onClick={handleGenerate}
                                    fullWidth
                                >
                                    Generate Report
                                </Button>

                                <Box sx={{ display: 'flex', gap: 1 }}>
                                    <Button variant="outlined" startIcon={<PdfIcon />} fullWidth>
                                        Export PDF
                                    </Button>
                                    <Button variant="outlined" startIcon={<CsvIcon />} fullWidth>
                                        Export CSV
                                    </Button>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Report Preview */}
                <Grid item xs={12} md={8}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Report Preview
                            </Typography>

                            <Box
                                sx={{
                                    mt: 3,
                                    p: 3,
                                    backgroundColor: 'background.default',
                                    borderRadius: 2,
                                    minHeight: 400,
                                }}
                            >
                                <Typography variant="h5" gutterBottom>
                                    SMART NETWORK GUARDIAN
                                </Typography>
                                <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                                    {reportType === 'security' ? 'Security Analysis Report' : 'network Report'}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                    Generated on: {new Date().toLocaleDateString()}
                                </Typography>

                                <Divider sx={{ my: 3 }} />

                                <Typography variant="h6" gutterBottom>
                                    1. NETWORK OVERVIEW
                                </Typography>
                                <Box sx={{ pl: 2, mb: 3 }}>
                                    <Typography variant="body2" gutterBottom>
                                        • Total Devices: {totalDevices}
                                    </Typography>
                                    <Typography variant="body2" gutterBottom>
                                        • Active Devices: {activeDevices}
                                    </Typography>
                                    <Typography variant="body2" gutterBottom>
                                        • Network Type: WiFi (192.168.1.0/24)
                                    </Typography>
                                </Box>

                                <Typography variant="h6" gutterBottom>
                                    2. SECURITY STATUS
                                </Typography>
                                <Box sx={{ pl: 2, mb: 3 }}>
                                    <Typography variant="body2" gutterBottom>
                                        • Security Score: {currentScore}/100 ({currentScore > 70 ? 'Good' : 'Risk'})
                                    </Typography>
                                    <Typography variant="body2" gutterBottom>
                                        • Critical Alerts: {criticalAlerts}
                                    </Typography>
                                    <Typography variant="body2" gutterBottom>
                                        • Warnings: {warnings}
                                    </Typography>
                                </Box>

                                <Typography variant="h6" gutterBottom>
                                    3. DETECTED ISSUES
                                </Typography>
                                <Box sx={{ pl: 2, mb: 3 }}>
                                    <Typography variant="body2" gutterBottom>
                                        [!] Port 3389 (RDP) is open on 2 devices
                                    </Typography>
                                    <Typography variant="body2" gutterBottom>
                                        [!] Firewall not detected on 3 devices
                                    </Typography>
                                    <Typography variant="body2" gutterBottom>
                                        [!] Weak WiFi encryption detected
                                    </Typography>
                                </Box>

                                <Typography variant="h6" gutterBottom>
                                    4. RECOMMENDATIONS
                                </Typography>
                                <Box sx={{ pl: 2 }}>
                                    <Typography variant="body2" gutterBottom>
                                        • Close unnecessary open ports
                                    </Typography>
                                    <Typography variant="body2" gutterBottom>
                                        • Enable firewall on all devices
                                    </Typography>
                                    <Typography variant="body2" gutterBottom>
                                        • Upgrade to WPA3 encryption
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
