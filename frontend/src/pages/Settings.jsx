import { useState } from 'react';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Grid,
    TextField,
    Button,
    Switch,
    FormControlLabel,
    Divider,
    Alert,
} from '@mui/material';
import {
    Save as SaveIcon,
    Refresh as RefreshIcon,
} from '@mui/icons-material';

function Settings() {
    const [settings, setSettings] = useState({
        backendUrl: 'http://localhost:8000/api',
        scanInterval: '15',
        alertNewDevices: true,
        alertSecurity: true,
        autoSync: true,
        darkMode: true,
    });

    const [saved, setSaved] = useState(false);

    const handleChange = (field) => (event) => {
        setSettings({
            ...settings,
            [field]: event.target.type === 'checkbox' ? event.target.checked : event.target.value,
        });
        setSaved(false);
    };

    const handleSave = () => {
        // Save settings to localStorage or API
        localStorage.setItem('appSettings', JSON.stringify(settings));
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
    };

    const handleReset = () => {
        setSettings({
            backendUrl: 'http://localhost:8000/api',
            scanInterval: '15',
            alertNewDevices: true,
            alertSecurity: true,
            autoSync: true,
            darkMode: true,
        });
    };

    return (
        <Box>
            {/* Header */}
            <Box sx={{ mb: 4 }}>
                <Typography variant="h4" fontWeight={700} gutterBottom>
                    Settings
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    Configure your Smart Network Guardian application
                </Typography>
            </Box>

            {saved && (
                <Alert severity="success" sx={{ mb: 3 }}>
                    Settings saved successfully!
                </Alert>
            )}

            <Grid container spacing={3}>
                {/* Backend Settings */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Backend Configuration
                            </Typography>

                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, mt: 3 }}>
                                <TextField
                                    label="Backend API URL"
                                    value={settings.backendUrl}
                                    onChange={handleChange('backendUrl')}
                                    fullWidth
                                    helperText="URL of your Django backend server"
                                />

                                <TextField
                                    label="Auto Scan Interval (minutes)"
                                    type="number"
                                    value={settings.scanInterval}
                                    onChange={handleChange('scanInterval')}
                                    fullWidth
                                    helperText="How often to automatically scan the network"
                                />

                                <FormControlLabel
                                    control={
                                        <Switch
                                            checked={settings.autoSync}
                                            onChange={handleChange('autoSync')}
                                        />
                                    }
                                    label="Auto-sync with backend"
                                />
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Alert Settings */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Alert Preferences
                            </Typography>

                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 3 }}>
                                <FormControlLabel
                                    control={
                                        <Switch
                                            checked={settings.alertNewDevices}
                                            onChange={handleChange('alertNewDevices')}
                                        />
                                    }
                                    label="Alert on new device detected"
                                />

                                <FormControlLabel
                                    control={
                                        <Switch
                                            checked={settings.alertSecurity}
                                            onChange={handleChange('alertSecurity')}
                                        />
                                    }
                                    label="Alert on security threats"
                                />

                                <Divider sx={{ my: 1 }} />

                                <Typography variant="subtitle2" color="text.secondary">
                                    Email Notifications (Coming Soon)
                                </Typography>
                                <TextField
                                    label="Email Address"
                                    type="email"
                                    placeholder="your@email.com"
                                    fullWidth
                                    disabled
                                />
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Appearance Settings */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Appearance
                            </Typography>

                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 3 }}>
                                <FormControlLabel
                                    control={
                                        <Switch
                                            checked={settings.darkMode}
                                            onChange={handleChange('darkMode')}
                                        />
                                    }
                                    label="Dark Mode (Currently Active)"
                                />
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                {/* About */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                About
                            </Typography>

                            <Box sx={{ mt: 3 }}>
                                <Typography variant="body2" gutterBottom>
                                    <strong>Version:</strong> 2.0 Professional
                                </Typography>
                                <Typography variant="body2" gutterBottom>
                                    <strong>Developer:</strong> Smart Network Guardian Team
                                </Typography>
                                <Typography variant="body2" gutterBottom>
                                    <strong>License:</strong> MIT License
                                </Typography>
                                <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                                    © 2024 Smart Network Guardian. All rights reserved.
                                </Typography>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Action Buttons */}
            <Box sx={{ display: 'flex', gap: 2, mt: 4, justifyContent: 'flex-end' }}>
                <Button
                    variant="outlined"
                    startIcon={<RefreshIcon />}
                    onClick={handleReset}
                >
                    Reset to Defaults
                </Button>
                <Button
                    variant="contained"
                    startIcon={<SaveIcon />}
                    onClick={handleSave}
                >
                    Save Settings
                </Button>
            </Box>
        </Box>
    );
}

export default Settings;
