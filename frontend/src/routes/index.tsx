import { HashRouter as Router, Route } from 'react-router-dom';
import Dashboard from '../screens/dashboard';

export const ScreenPaths = {
  DASHBOARD: '/',
};

const Routes: React.FC = () => {
  return (
    <Router>
      <Route path={ScreenPaths.DASHBOARD} component={Dashboard} />
    </Router>
  );
};

export default Routes;
