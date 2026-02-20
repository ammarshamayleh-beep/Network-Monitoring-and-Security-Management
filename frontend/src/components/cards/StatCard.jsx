import { Card, CardContent, Box, Typography, useTheme } from '@mui/material';
import { TrendingUp, TrendingDown } from '@mui/icons-material';

function StatCard({ title, value, icon: Icon, trend, trendValue, color = 'primary' }) {
    const theme = useTheme();
    const isPositive = trend === 'up';

    return (
        <Card
            sx={{
                height: '100%',
                background: `linear-gradient(135deg, ${theme.palette[color].main}15 0%, ${theme.palette[color].main}05 100%)`,
                border: `1px solid ${theme.palette[color].main}30`,
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: `0 8px 24px ${theme.palette[color].main}40`,
                },
            }}
        >
            <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box sx={{ flexGrow: 1 }}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                            {title}
                        </Typography>
                        <Typography variant="h3" fontWeight={700} color={`${color}.main`} sx={{ mb: 1 }}>
                            {value}
                        </Typography>

                        {trendValue && (
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                {isPositive ? (
                                    <TrendingUp sx={{ fontSize: 16, color: 'success.main' }} />
                                ) : (
                                    <TrendingDown sx={{ fontSize: 16, color: 'error.main' }} />
                                )}
                                <Typography
                                    variant="caption"
                                    color={isPositive ? 'success.main' : 'error.main'}
                                    fontWeight={600}
                                >
                                    {trendValue}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                    vs last scan
                                </Typography>
                            </Box>
                        )}
                    </Box>

                    {Icon && (
                        <Box
                            sx={{
                                width: 56,
                                height: 56,
                                borderRadius: 2,
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                backgroundColor: `${color}.main`,
                                color: `${color}.contrastText`,
                            }}
                        >
                            <Icon sx={{ fontSize: 32 }} />
                        </Box>
                    )}
                </Box>
            </CardContent>
        </Card>
    );
}

export default StatCard;
