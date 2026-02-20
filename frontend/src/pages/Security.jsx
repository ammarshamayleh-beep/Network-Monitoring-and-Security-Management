import { useQuery } from '@tanstack/react-query';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Grid,
    LinearProgress,
    Chip,
    List,
    ListItem,
    ListItemText,
    ListItemIcon,
    CircularProgress,
    Button,
} from '@mui/material';
import {
    CheckCircle as CheckIcon,
    Warning as WarningIcon,
    Error as ErrorIcon,
    Info as InfoIcon,
    Refresh as RefreshIcon,
} from '@mui/icons-material';
import {
    RadialBarChart,
    RadialBar,
    Legend,
    ResponsiveContainer,
    Tooltip,
} from 'recharts';
import monitoringService from '../services/monitoringService';
import alertService from '../services/alertService';

const recommendations = [
    'Close unnecessary open ports (3389, 445)',
    'Enable Windows Firewall on all devices',
    'Update antivirus definitions',
    'Review and update device access permissions',
    'Enable network encryption (WPA3)',
];

// Map severity to color and icon
const getSeverityConfig = (severity) => {
    switch (severity?.toLowerCase()) {
        case 'critical':
        case 'high':
            return { color: 'error', icon: ErrorIcon };
        case 'medium':
            return { color: 'warning', icon: WarningIcon };
        case 'low':
            return { color: 'info', icon: InfoIcon };
        default:
            return { color: 'success', icon: CheckIcon };
    }
};

function Security() {
    // Fetch security score
    const { data: scoreData, isLoading: isLoadingScore, refetch: refetchScore } = useQuery({
        queryKey: ['security-score-trend'],
        queryFn: monitoringService.getSecurityScore,
    });

    // Fetch alerts
    const { data: alertsData, isLoading: isLoadingAlerts, refetch: refetchAlerts } = useQuery({
        queryKey: ['alerts'],
        queryFn: () => alertService.getAllAlerts(),
    });

    const handleRefresh = () => {
        refetchScore();
        refetchAlerts();
    };

    const isLoading = isLoadingScore || isLoadingAlerts;

    // Process data
    const currentScore = scoreData && scoreData.length > 0 ? scoreData[scoreData.length - 1].score : 85;
    const securityScoreChartData = [{ name: 'Score', value: currentScore, fill: currentScore > 70 ? '#00e676' : '#ff1744' }];

    const alerts = Array.isArray(alertsData) ? alertsData : (alertsData?.results || []);

    // Derive vulnerabilities stat from alerts for now
    const vulnerabilities = [
        { name: 'Critical Issues', count: alerts.filter(a => a.severity === 'critical').length, severity: 'critical', color: 'error' },
        { name: 'High Risks', count: alerts.filter(a => a.severity === 'high').length, severity: 'high', color: 'error' },
        { name: 'Medium Risks', count: alerts.filter(a => a.severity === 'medium').length, severity: 'medium', color: 'warning' },
        { name: 'Low Risks', count: alerts.filter(a => a.severity === 'low').length, severity: 'low', color: 'info' },
    ];

    if (isLoading && !scoreData && !alertsData) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box>
            {/* Header */}
            <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                    <Typography variant="h4" fontWeight={700} gutterBottom>
                        Security Analysis
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Comprehensive security assessment of your network
                    </Typography>
                </Box>
                <Button
                    variant="contained"
                    startIcon={<RefreshIcon />}
                    onClick={handleRefresh}
                    sx={{ borderRadius: 2 }}
                >
                    Refresh Analysis
                </Button>
            </Box>

            {/* Overview Row */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                {/* Security Score */}
                <Grid item xs={12} md={5}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Overall Security Score
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: 300 }}>
                                <Box sx={{ textAlign: 'center' }}>
                                    <ResponsiveContainer width={250} height={250}>
                                        <RadialBarChart
                                            cx="50%"
                                            cy="50%"
                                            innerRadius="80%"
                                            outerRadius="100%"
                                            data={securityScoreChartData}
                                            startAngle={180}
                                            endAngle={0}
                                        >
                                            <RadialBar
                                                minAngle={15}
                                                background
                                                clockWise
                                                dataKey="value"
                                                cornerRadius={10}
                                            />
                                            <Tooltip />
                                        </RadialBarChart>
                                    </ResponsiveContainer>
                                    <Typography variant="h2" fontWeight={700} color={currentScore > 70 ? "success.main" : "error.main"} sx={{ mt: -10 }}>
                                        {currentScore}
                                    </Typography>
                                    <Typography variant="h6" color="text.secondary">
                                        / 100
                                    </Typography>
                                    <Chip
                                        label={currentScore > 90 ? "Excellent" : currentScore > 70 ? "Good" : "At Risk"}
                                        color={currentScore > 70 ? "success" : "error"}
                                        sx={{ mt: 2, fontWeight: 600 }}
                                    />
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Vulnerabilities */}
                <Grid item xs={12} md={7}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Risk Assessment
                            </Typography>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 3 }}>
                                {vulnerabilities.map((vuln, index) => (
                                    <Box key={index}>
                                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                                <Typography variant="body2" fontWeight={600}>
                                                    {vuln.name}
                                                </Typography>
                                                <Chip label={vuln.count} size="small" color={vuln.color} />
                                            </Box>
                                            <Chip
                                                label={vuln.severity}
                                                size="small"
                                                color={vuln.color}
                                                variant="outlined"
                                                sx={{ textTransform: 'uppercase' }}
                                            />
                                        </Box>
                                        <LinearProgress
                                            variant="determinate"
                                            value={Math.min((vuln.count / 10) * 100, 100)} // Normalize to 10 max for bar
                                            color={vuln.color}
                                            sx={{ height: 8, borderRadius: 4 }}
                                        />
                                    </Box>
                                ))}
                                {alerts.length === 0 && (
                                    <Typography variant="body2" color="text.secondary" textAlign="center" sx={{ mt: 2 }}>
                                        No vulnerabilities detected. Good job!
                                    </Typography>
                                )}
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Alerts and Recommendations */}
            <Grid container spacing={3}>
                {/* Security Alerts Timeline */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Recent Security Alerts
                            </Typography>
                            <List sx={{ maxHeight: 400, overflow: 'auto' }}>
                                {alerts.length > 0 ? (
                                    alerts.slice(0, 10).map((alert, index) => { // Show top 10
                                        const { color, icon: IconComponent } = getSeverityConfig(alert.severity);
                                        return (
                                            <ListItem
                                                key={alert.id || index}
                                                sx={{
                                                    borderRadius: 2,
                                                    mb: 1,
                                                    backgroundColor: 'background.card',
                                                    border: '1px solid',
                                                    borderColor: 'divider',
                                                }}
                                            >
                                                <ListItemIcon>
                                                    <IconComponent color={color} />
                                                </ListItemIcon>
                                                <ListItemText
                                                    primary={alert.alert_type || 'Security Alert'} // Use alert_type from model
                                                    secondary={
                                                        <>
                                                            <Typography component="span" variant="body2" color="text.primary">
                                                                {alert.description}
                                                            </Typography>
                                                            <br />
                                                            <Typography component="span" variant="caption" color="text.secondary">
                                                                {new Date(alert.timestamp).toLocaleString()}
                                                            </Typography>
                                                        </>
                                                    }
                                                    primaryTypographyProps={{ fontWeight: 500 }}
                                                />
                                            </ListItem>
                                        );
                                    })
                                ) : (
                                    <Typography variant="body2" color="text.secondary" sx={{ p: 2, textAlign: 'center' }}>
                                        No recent alerts.
                                    </Typography>
                                )}
                            </List>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Recommendations */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Security Recommendations
                            </Typography>
                            <List>
                                {recommendations.map((rec, index) => (
                                    <ListItem
                                        key={index}
                                        sx={{
                                            borderRadius: 2,
                                            mb: 1,
                                            backgroundColor: 'background.card',
                                            border: '1px solid',
                                            borderColor: 'divider',
                                        }}
                                    >
                                        <ListItemIcon>
                                            <CheckIcon color="success" />
                                        </ListItemIcon>
                                        <ListItemText
                                            primary={rec}
                                            primaryTypographyProps={{ variant: 'body2' }}
                                        />
                                    </ListItem>
                                ))}
                            </List>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
}

export default Security;
