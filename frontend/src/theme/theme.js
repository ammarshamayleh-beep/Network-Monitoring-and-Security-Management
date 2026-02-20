import { createTheme } from '@mui/material/styles';

// Professional Dark Theme - Inspired by Cisco Meraki & Modern Dashboards
const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#00d4ff', // Cyan - for primary actions and highlights
            light: '#4de4ff',
            dark: '#00a3cc',
            contrastText: '#0a0e27',
        },
        secondary: {
            main: '#7c4dff', // Purple accent
            light: '#b47cff',
            dark: '#5523cc',
            contrastText: '#ffffff',
        },
        background: {
            default: '#0a0e27', // Deep midnight blue
            paper: '#141b3d', // Slightly lighter for cards
            card: '#1a2548', // For elevated components
        },
        text: {
            primary: '#e8eaf6',
            secondary: '#b0bec5',
            disabled: '#546e7a',
        },
        success: {
            main: '#00e676', // Bright green for success states
            light: '#69f0ae',
            dark: '#00c853',
        },
        warning: {
            main: '#ffa726', // Orange for warnings
            light: '#ffb74d',
            dark: '#f57c00',
        },
        error: {
            main: '#ff5252', // Red for errors and critical alerts
            light: '#ff867f',
            dark: '#c50e29',
        },
        info: {
            main: '#00d4ff',
            light: '#4de4ff',
            dark: '#00a3cc',
        },
        divider: 'rgba(255, 255, 255, 0.08)',
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Segoe UI", "Arial", sans-serif',
        h1: {
            fontSize: '2.5rem',
            fontWeight: 700,
            letterSpacing: '-0.02em',
        },
        h2: {
            fontSize: '2rem',
            fontWeight: 600,
            letterSpacing: '-0.01em',
        },
        h3: {
            fontSize: '1.75rem',
            fontWeight: 600,
        },
        h4: {
            fontSize: '1.5rem',
            fontWeight: 600,
        },
        h5: {
            fontSize: '1.25rem',
            fontWeight: 600,
        },
        h6: {
            fontSize: '1rem',
            fontWeight: 600,
        },
        subtitle1: {
            fontSize: '1rem',
            fontWeight: 500,
            lineHeight: 1.75,
        },
        subtitle2: {
            fontSize: '0.875rem',
            fontWeight: 500,
            lineHeight: 1.57,
        },
        body1: {
            fontSize: '1rem',
            lineHeight: 1.5,
        },
        body2: {
            fontSize: '0.875rem',
            lineHeight: 1.43,
        },
        button: {
            fontWeight: 600,
            textTransform: 'none', // Don't uppercase buttons
            letterSpacing: '0.02em',
        },
    },
    shape: {
        borderRadius: 12, // Rounded corners for modern look
    },
    shadows: [
        'none',
        '0px 2px 4px rgba(0, 0, 0, 0.2)',
        '0px 4px 8px rgba(0, 0, 0, 0.25)',
        '0px 8px 16px rgba(0, 0, 0, 0.3)',
        '0px 12px 24px rgba(0, 0, 0, 0.35)',
        '0px 16px 32px rgba(0, 0, 0, 0.4)',
        '0px 20px 40px rgba(0, 0, 0, 0.45)',
        '0px 24px 48px rgba(0, 0, 0, 0.5)',
        // ... rest can be default
        ...Array(17).fill('0px 24px 48px rgba(0, 0, 0, 0.5)'),
    ],
    components: {
        MuiCssBaseline: {
            styleOverrides: {
                body: {
                    scrollbarWidth: 'thin',
                    '&::-webkit-scrollbar': {
                        width: '8px',
                        height: '8px',
                    },
                    '&::-webkit-scrollbar-track': {
                        background: '#0a0e27',
                    },
                    '&::-webkit-scrollbar-thumb': {
                        background: '#1a2548',
                        borderRadius: '4px',
                        '&:hover': {
                            background: '#2a3558',
                        },
                    },
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 8,
                    padding: '10px 24px',
                    fontWeight: 600,
                },
                contained: {
                    boxShadow: '0px 4px 12px rgba(0, 212, 255, 0.3)',
                    '&:hover': {
                        boxShadow: '0px 6px 16px rgba(0, 212, 255, 0.4)',
                    },
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    backgroundImage: 'none',
                    borderRadius: 16,
                    border: '1px solid rgba(255, 255, 255, 0.05)',
                    boxShadow: '0px 4px 16px rgba(0, 0, 0, 0.3)',
                },
            },
        },
        MuiPaper: {
            styleOverrides: {
                root: {
                    backgroundImage: 'none',
                },
            },
        },
        MuiTableCell: {
            styleOverrides: {
                root: {
                    borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
                },
                head: {
                    fontWeight: 600,
                    backgroundColor: '#1a2548',
                },
            },
        },
        MuiChip: {
            styleOverrides: {
                root: {
                    fontWeight: 500,
                },
            },
        },
    },
});

export default theme;
