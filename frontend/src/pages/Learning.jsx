import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  Button, 
  CircularProgress,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Collapse,
  Breadcrumbs,
  Link
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { learningApi } from '../services/api';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import SchoolIcon from '@mui/icons-material/School';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';

const Learning = () => {
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState([]);
  const [learningPath, setLearningPath] = useState([]);
  const [expandedCategories, setExpandedCategories] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLearningData = async () => {
      try {
        setLoading(true);
        
        // Fetch personalized learning path
        const pathData = await learningApi.getLearningPath();
        setLearningPath(pathData);
        
        // Initialize expanded state for categories
        const expanded = {};
        pathData.forEach(category => {
          expanded[category.id] = false;
        });
        setExpandedCategories(expanded);
      } catch (error) {
        console.error('Error fetching learning data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchLearningData();
  }, []);

  const handleCategoryToggle = (categoryId) => {
    setExpandedCategories(prev => ({
      ...prev,
      [categoryId]: !prev[categoryId]
    }));
  };

  const handleTopicClick = (topicId) => {
    navigate(`/learning/${topicId}`);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Learning Resources
      </Typography>
      
      <Paper elevation={2} sx={{ p: 3, mb: 4, borderRadius: 2 }}>
        <Typography variant="h5" gutterBottom>
          Your Learning Journey
        </Typography>
        <Typography variant="body1" paragraph>
          Structured learning resources based on "Cracking the Coding Interview" to help you master technical interview concepts.
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Track your progress through each topic and build a solid foundation for your interviews.
        </Typography>
      </Paper>
      
      <Grid container spacing={4}>
        {/* Learning Path Navigation */}
        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ borderRadius: 2 }}>
            <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'white', borderRadius: '8px 8px 0 0' }}>
              <Typography variant="h6">
                Learning Path
              </Typography>
            </Box>
            <List component="nav" sx={{ p: 0 }}>
              {learningPath.map(category => (
                <React.Fragment key={category.id}>
                  <ListItemButton onClick={() => handleCategoryToggle(category.id)}>
                    <ListItemIcon>
                      <MenuBookIcon />
                    </ListItemIcon>
                    <ListItemText primary={category.name} />
                    {expandedCategories[category.id] ? <ExpandLess /> : <ExpandMore />}
                  </ListItemButton>
                  <Collapse in={expandedCategories[category.id]} timeout="auto" unmountOnExit>
                    <List component="div" disablePadding>
                      {category.topics.map(topic => {
                        const progressPercentage = topic.progress_percentage || 0;
                        const isCompleted = progressPercentage === 100;
                        
                        return (
                          <ListItemButton 
                            key={topic.id} 
                            sx={{ pl: 4 }}
                            onClick={() => handleTopicClick(topic.id)}
                          >
                            <ListItemIcon>
                              {isCompleted ? 
                                <CheckCircleIcon color="success" /> : 
                                <RadioButtonUncheckedIcon color={progressPercentage > 0 ? "primary" : "disabled"} />
                              }
                            </ListItemIcon>
                            <ListItemText 
                              primary={topic.name} 
                              secondary={`${Math.round(progressPercentage)}% complete`}
                            />
                          </ListItemButton>
                        );
                      })}
                    </List>
                  </Collapse>
                  <Divider />
                </React.Fragment>
              ))}
            </List>
          </Paper>
          
          {/* Learning Stats */}
          <Paper elevation={2} sx={{ mt: 3, p: 3, borderRadius: 2 }}>
            <Typography variant="h6" gutterBottom>
              Your Progress
            </Typography>
            
            {learningPath.map(category => {
              // Calculate category progress
              const totalTopics = category.topics.length;
              const completedTopics = category.topics.filter(t => t.progress_percentage === 100).length;
              const inProgressTopics = category.topics.filter(t => t.progress_percentage > 0 && t.progress_percentage < 100).length;
              
              return (
                <Box key={category.id} sx={{ mb: 2 }}>
                  <Typography variant="subtitle2">{category.name}</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <Box sx={{ flexGrow: 1, mr: 1 }}>
                      <Box
                        sx={{
                          height: 8,
                          borderRadius: 5,
                          bgcolor: 'grey.300',
                          position: 'relative'
                        }}
                      >
                        <Box
                          sx={{
                            position: 'absolute',
                            left: 0,
                            top: 0,
                            height: '100%',
                            borderRadius: 5,
                            bgcolor: 'primary.main',
                            width: `${(completedTopics / totalTopics) * 100}%`
                          }}
                        />
                        <Box
                          sx={{
                            position: 'absolute',
                            left: `${(completedTopics / totalTopics) * 100}%`,
                            top: 0,
                            height: '100%',
                            borderRadius: 5,
                            bgcolor: 'info.main',
                            width: `${(inProgressTopics / totalTopics) * 100}%`
                          }}
                        />
                      </Box>
                    </Box>
                    <Typography variant="body2" color="textSecondary">
                      {completedTopics}/{totalTopics}
                    </Typography>
                  </Box>
                </Box>
              );
            })}
          </Paper>
        </Grid>
        
        {/* Learning Overview */}
        <Grid item xs={12} md={8}>
          <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
              <SchoolIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
              <Typography variant="h5">
                Interview Preparation Guide
              </Typography>
            </Box>
            
            <Typography variant="body1" paragraph>
              Welcome to your structured learning path based on "Cracking the Coding Interview." This comprehensive guide will help you master the key concepts and techniques needed to excel in technical interviews.
            </Typography>
            
            <Typography variant="body1" paragraph>
              Each topic includes:
            </Typography>
            
            <Box component="ul" sx={{ pl: 4 }}>
              <Box component="li" sx={{ mb: 1 }}>
                <Typography variant="body1">
                  <strong>Concept explanations</strong> - Clear, concise explanations of fundamental concepts
                </Typography>
              </Box>
              <Box component="li" sx={{ mb: 1 }}>
                <Typography variant="body1">
                  <strong>Example problems</strong> - Illustrative examples with step-by-step solutions
                </Typography>
              </Box>
              <Box component="li" sx={{ mb: 1 }}>
                <Typography variant="body1">
                  <strong>Common patterns</strong> - Recurring patterns and techniques to recognize
                </Typography>
              </Box>
              <Box component="li">
                <Typography variant="body1">
                  <strong>Practice questions</strong> - Links to relevant practice questions
                </Typography>
              </Box>
            </Box>
            
            <Divider sx={{ my: 3 }} />
            
            <Typography variant="h6" gutterBottom>
              Getting Started
            </Typography>
            
            <Typography variant="body1" paragraph>
              We recommend following these steps:
            </Typography>
            
            <Box sx={{ mb: 3 }}>
              <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  1. Start with the fundamentals
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Begin with data structures like Arrays, Strings, and Linked Lists to build a solid foundation.
                </Typography>
              </Paper>
              
              <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  2. Progress to algorithms
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Move on to sorting, searching, and recursion to understand algorithmic thinking.
                </Typography>
              </Paper>
              
              <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  3. Tackle advanced topics
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Once comfortable, explore dynamic programming, graphs, and system design.
                </Typography>
              </Paper>
              
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  4. Practice regularly
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Apply what you've learned by solving practice questions in the Practice section.
                </Typography>
              </Paper>
            </Box>
            
            <Button 
              variant="contained" 
              color="primary"
              onClick={() => {
                // Find first topic in first category
                if (learningPath.length > 0 && learningPath[0].topics.length > 0) {
                  handleTopicClick(learningPath[0].topics[0].id);
                }
              }}
              disabled={learningPath.length === 0 || learningPath[0]?.topics.length === 0}
            >
              Start Learning
            </Button>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Learning;
