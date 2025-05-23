import React from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Paper, 
  Button, 
  Link
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import SentimentDissatisfiedIcon from '@mui/icons-material/SentimentDissatisfied';

const NotFound = () => {
  return (
    <Container maxWidth="md" sx={{ mt: 8, mb: 4 }}>
      <Paper elevation={2} sx={{ p: 4, borderRadius: 2, textAlign: 'center' }}>
        <SentimentDissatisfiedIcon sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
        
        <Typography variant="h3" component="h1" gutterBottom>
          404 - Page Not Found
        </Typography>
        
        <Typography variant="h6" color="textSecondary" paragraph>
          Oops! The page you're looking for doesn't exist.
        </Typography>
        
        <Typography variant="body1" paragraph>
          The page might have been moved, deleted, or never existed in the first place.
        </Typography>
        
        <Box sx={{ mt: 4 }}>
          <Button 
            variant="contained" 
            color="primary" 
            component={RouterLink} 
            to="/"
            size="large"
            sx={{ mr: 2 }}
          >
            Go to Home
          </Button>
          
          <Button 
            variant="outlined" 
            component={RouterLink} 
            to="/dashboard"
            size="large"
          >
            Go to Dashboard
          </Button>
        </Box>
        
        <Box sx={{ mt: 4 }}>
          <Typography variant="body2" color="textSecondary">
            If you believe this is an error, please{' '}
            <Link component={RouterLink} to="/contact">
              contact support
            </Link>.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default NotFound;
