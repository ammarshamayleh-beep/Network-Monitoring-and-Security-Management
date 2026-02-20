import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import AppLayout from './components/layout/AppLayout.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Devices from './pages/Devices.jsx';
import Security from './pages/Security.jsx';
import Monitoring from './pages/Monitoring.jsx';
import Reports from './pages/Reports.jsx';
import Settings from './pages/Settings.jsx';

console.log('Smart Guardian Frontend: App component loading...');

function App() {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="devices" element={<Devices />} />
          <Route path="security" element={<Security />} />
          <Route path="monitoring" element={<Monitoring />} />
          <Route path="reports" element={<Reports />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </Box>
  );
}

export default App;
