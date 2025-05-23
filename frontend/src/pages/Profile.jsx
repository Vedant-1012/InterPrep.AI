import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Grid, 
  Paper, 
  Button, 
  CircularProgress,
  Avatar,
  TextField,
  Divider,
  Tabs,
  Tab,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { userApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';
import DeleteIcon from '@mui/icons-material/Delete';
import FavoriteIcon from '@mui/icons-material/Favorite';

const Profile = () => {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [favorites, setFavorites] = useState([]);
  const [history, setHistory] = useState([]);
  const [tabValue, setTabValue] = useState(0);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    bio: ''
  });
  
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        setLoading(true);
        
        // Fetch user profile
        const profileData = await userApi.getCurrentUser();
        setProfile(profileData);
        
        // Initialize form data
        setFormData({
          username: profileData.username,
          email: profileData.email,
          bio: profileData.bio || ''
        });
        
        // Fetch favorites
        const favoritesData = await userApi.getUserFavorites();
        setFavorites(favoritesData);
        
        // Fetch practice history
        const historyData = await userApi.getUserHistory();
        setHistory(historyData);
      } catch (error) {
        console.error('Error fetching user data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchUserData();
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleEditToggle = () => {
    if (editing) {
      // Cancel editing, reset form
      setFormData({
        username: profile.username,
        email: profile.email,
        bio: profile.bio || ''
      });
    }
    setEditing(!editing);
  };

  const handleProfileUpdate = async () => {
    try {
      setLoading(true);
      
      // Update profile
      const updatedProfile = await userApi.updateProfile(formData);
      setProfile(updatedProfile);
      
      // Exit edit mode
      setEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleQuestionClick = (questionId) => {
    navigate(`/practice/${questionId}`);
  };

  if (loading && !profile) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Profile
      </Typography>
      
      <Grid container spacing={4}>
        {/* Profile Information */}
        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
              <Avatar 
                sx={{ 
                  width: 100, 
                  height: 100, 
                  bgcolor: 'primary.main',
                  fontSize: '2.5rem',
                  mb: 2
                }}
              >
                {profile?.username?.charAt(0).toUpperCase() || 'U'}
              </Avatar>
              
              {!editing ? (
                <>
                  <Typography variant="h5" gutterBottom>
                    {profile?.username}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {profile?.email}
                  </Typography>
                  {profile?.bio && (
                    <Typography variant="body1" sx={{ mt: 2, textAlign: 'center' }}>
                      {profile.bio}
                    </Typography>
                  )}
                </>
              ) : (
                <Box sx={{ width: '100%' }}>
                  <TextField
                    margin="normal"
                    fullWidth
                    label="Username"
                    name="username"
                    value={formData.username}
                    onChange={handleInputChange}
                  />
                  <TextField
                    margin="normal"
                    fullWidth
                    label="Email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleInputChange}
                  />
                  <TextField
                    margin="normal"
                    fullWidth
                    label="Bio"
                    name="bio"
                    multiline
                    rows={3}
                    value={formData.bio}
                    onChange={handleInputChange}
                  />
                </Box>
              )}
            </Box>
            
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
              {!editing ? (
                <Button 
                  variant="outlined" 
                  startIcon={<EditIcon />}
                  onClick={handleEditToggle}
                >
                  Edit Profile
                </Button>
              ) : (
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button 
                    variant="outlined" 
                    color="error"
                    startIcon={<CancelIcon />}
                    onClick={handleEditToggle}
                  >
                    Cancel
                  </Button>
                  <Button 
                    variant="contained" 
                    startIcon={<SaveIcon />}
                    onClick={handleProfileUpdate}
                    disabled={loading}
                  >
                    Save
                  </Button>
                </Box>
              )}
            </Box>
            
            <Divider sx={{ my: 3 }} />
            
            <Typography variant="h6" gutterBottom>
              Account Statistics
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="h4" color="primary">
                    {profile?.stats?.questions_attempted || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Questions Attempted
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={6}>
                <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="h4" color="success.main">
                    {profile?.stats?.correct_solutions || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Correct Solutions
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
            
            <Button 
              variant="outlined" 
              color="error"
              fullWidth
              sx={{ mt: 3 }}
              onClick={handleLogout}
            >
              Logout
            </Button>
          </Paper>
        </Grid>
        
        {/* Tabs for Favorites and History */}
        <Grid item xs={12} md={8}>
          <Paper elevation={2} sx={{ borderRadius: 2 }}>
            <Tabs 
              value={tabValue} 
              onChange={handleTabChange}
              variant="fullWidth"
              sx={{ borderBottom: 1, borderColor: 'divider' }}
            >
              <Tab label="Favorite Questions" />
              <Tab label="Practice History" />
            </Tabs>
            
            <Box sx={{ p: 3 }}>
              {/* Favorites Tab */}
              {tabValue === 0 && (
                <>
                  {favorites.length > 0 ? (
                    <List>
                      {favorites.map((question) => (
                        <Paper 
                          key={question.id} 
                          variant="outlined" 
                          sx={{ 
                            mb: 2, 
                            p: 2,
                            cursor: 'pointer',
                            '&:hover': { bgcolor: 'action.hover' }
                          }}
                          onClick={() => handleQuestionClick(question.id)}
                        >
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                            <Box>
                              <Typography variant="subtitle1">
                                {question.title}
                              </Typography>
                              <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                                {question.content.split('\n')[0].substring(0, 100)}...
                              </Typography>
                              <Box sx={{ display: 'flex', gap: 1 }}>
                                <Chip 
                                  label={question.difficulty} 
                                  size="small"
                                  color={
                                    question.difficulty === 'easy' ? 'success' : 
                                    question.difficulty === 'medium' ? 'warning' : 
                                    'error'
                                  }
                                />
                                <Chip 
                                  label={question.topic} 
                                  size="small"
                                  color="primary"
                                  variant="outlined"
                                />
                                {question.company && (
                                  <Chip 
                                    label={question.company} 
                                    size="small"
                                    variant="outlined"
                                  />
                                )}
                              </Box>
                            </Box>
                            <IconButton 
                              color="secondary"
                              onClick={(e) => {
                                e.stopPropagation();
                                // Remove from favorites logic
                              }}
                            >
                              <FavoriteIcon />
                            </IconButton>
                          </Box>
                        </Paper>
                      ))}
                    </List>
                  ) : (
                    <Box sx={{ textAlign: 'center', py: 4 }}>
                      <Typography variant="body1" paragraph>
                        You haven't favorited any questions yet.
                      </Typography>
                      <Button 
                        variant="contained" 
                        onClick={() => navigate('/practice')}
                      >
                        Browse Questions
                      </Button>
                    </Box>
                  )}
                </>
              )}
              
              {/* History Tab */}
              {tabValue === 1 && (
                <>
                  {history.length > 0 ? (
                    <List>
                      {history.map((item) => (
                        <Paper 
                          key={item.id} 
                          variant="outlined" 
                          sx={{ 
                            mb: 2, 
                            p: 2,
                            cursor: 'pointer',
                            '&:hover': { bgcolor: 'action.hover' }
                          }}
                          onClick={() => handleQuestionClick(item.question_id)}
                        >
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                            <Box>
                              <Typography variant="subtitle1">
                                {item.question_title}
                              </Typography>
                              <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
                                <Chip 
                                  label={item.status} 
                                  size="small"
                                  color={item.status === 'correct' ? 'success' : 'error'}
                                />
                                <Chip 
                                  label={item.difficulty} 
                                  size="small"
                                  color={
                                    item.difficulty === 'easy' ? 'success' : 
                                    item.difficulty === 'medium' ? 'warning' : 
                                    'error'
                                  }
                                  variant="outlined"
                                />
                              </Box>
                              <Typography variant="body2" color="textSecondary">
                                Attempted: {new Date(item.created_at).toLocaleDateString()}
                              </Typography>
                            </Box>
                            <Button 
                              variant="outlined" 
                              size="small"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleQuestionClick(item.question_id);
                              }}
                            >
                              Try Again
                            </Button>
                          </Box>
                        </Paper>
                      ))}
                    </List>
                  ) : (
                    <Box sx={{ textAlign: 'center', py: 4 }}>
                      <Typography variant="body1" paragraph>
                        You haven't attempted any questions yet.
                      </Typography>
                      <Button 
                        variant="contained" 
                        onClick={() => navigate('/practice')}
                      >
                        Start Practicing
                      </Button>
                    </Box>
                  )}
                </>
              )}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Profile;
