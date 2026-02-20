import { useLocation } from 'react-router-dom';
import {
    AppBar,
    Toolbar,
    Typography,
    IconButton,
    Box,
    Chip,
    useTheme,
} from '@mui/material';
import {
    Menu as MenuIcon,
    Notifications as NotificationsIcon,
    AccountCircle as AccountCircleIcon,
} from '@mui/icons-material';

const pageNames = {
    '/dashboard': 'Dashboard',
    '/devices': 'Network Devices',
    '/security': 'Security Analysis',
    '/monitoring': 'Live Monitoring',
    '/reports': 'Reports',
    '/settings': 'Settings',
};

function Navbar({ onMenuClick, isMobile }) {
    const location = useLocation();
    const theme = useTheme();
    const currentPage = pageNames[location.pathname] || 'Dashboard';

    return (
        <AppBar
            position="sticky"
            elevation={0}
            sx={{
                backgroundColor: 'background.paper',
                borderBottom: '1px solid',
                borderColor: 'divider',
            }}
        >
            <Toolbar>
                {/* Mobile menu button */}
                {isMobile && (
                    <IconButton
                        edge="start"
                        onClick={onMenuClick}
                        sx={{ mr: 2, color: 'text.primary' }}
                    >
                        <MenuIcon />
                    </IconButton>
                )}

                {/* Page Title */}
                <Typography
                    variant="h6"
                    sx={{
                        flexGrow: 1,
                        fontWeight: 600,
                        color: 'text.primary',
                    }}
                >
                    {currentPage}
                </Typography>

                {/* Backend Status */}
                <Chip
                    label="Backend Connected"
                    size="small"
                    sx={{
                        backgroundColor: 'success.main',
                        color: 'white',
                        fontWeight: 600,
                        mr: 2,
                        '& .MuiChip-icon': {
                            color: 'white',
                        },
                    }}
                    icon={
                        <Box
                            sx={{
                                width: 8,
                                height: 8,
                                borderRadius: '50%',
                                backgroundColor: 'white',
                                animation: 'pulse 2s infinite',
                                '@keyframes pulse': {
                                    '0%, 100%': { opacity: 1 },
                                    '50%': { opacity: 0.5 },
                                },
                            }}
                        />
                    }
                />

                {/* Notifications */}
                <IconButton sx={{ color: 'text.primary' }}>
                    <NotificationsIcon />
                </IconButton>

                {/* User Profile */}
                <IconButton sx={{ color: 'text.primary' }}>
                    <AccountCircleIcon />
                </IconButton>
            </Toolbar>
        </AppBar>
    );
}

export default Navbar;
