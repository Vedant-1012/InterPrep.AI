import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Grid, 
  Paper, 
  Button, 
  CircularProgress,
  Divider,
  Breadcrumbs,
  Link,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip
} from '@mui/material';
import { useParams, useNavigate, Link as RouterLink } from 'react-router-dom';
import { learningApi, practiceApi } from '../services/api';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CodeIcon from '@mui/icons-material/Code';
import MenuBookIcon from '@mui/icons-material/MenuBook';

const LearningTopic = () => {
  const { topicId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [topic, setTopic] = useState(null);
  const [relatedQuestions, setRelatedQuestions] = useState([]);
  
  useEffect(() => {
    const fetchTopicData = async () => {
      try {
        setLoading(true);
        
        // Fetch topic content with progress
        const topicData = await learningApi.getTopicWithProgress(topicId);
        setTopic(topicData);
        
        // Fetch related practice questions
        const practiceData = await practiceApi.getPracticeSession({
          topic: topicData.name.toLowerCase().replace(/\s+/g, '_'),
          limit: 3
        });
        setRelatedQuestions(practiceData);
      } catch (error) {
        console.error('Error fetching topic data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchTopicData();
  }, [topicId]);

  const handleMarkCompleted = async (contentId, isCompleted) => {
    try {
      await learningApi.updateProgress({
        content_id: contentId,
        completed: !isCompleted
      });
      
      // Update local state
      setTopic(prev => ({
        ...prev,
        content: prev.content.map(item => 
          item.id === contentId ? { ...item, completed: !isCompleted } : item
        )
      }));
    } catch (error) {
      console.error('Error updating progress:', error);
    }
  };

  const renderContentItem = (contentItem) => {
    switch (contentItem.content_type) {
      case 'text':
        return (
          <Typography variant="body1" component="div" sx={{ whiteSpace: 'pre-line' }}>
            {contentItem.content}
          </Typography>
        );
      case 'code':
        return (
          <Paper 
            variant="outlined" 
            sx={{ 
              p: 2, 
              bgcolor: 'grey.900', 
              color: 'grey.100',
              fontFamily: 'monospace',
              overflowX: 'auto'
            }}
          >
            <pre style={{ margin: 0 }}>{contentItem.content}</pre>
          </Paper>
        );
      case 'example':
        const example = JSON.parse(contentItem.content);
        return (
          <Paper variant="outlined" sx={{ p: 2, bgcolor: 'grey.50' }}>
            <Typography variant="subtitle1" gutterBottom>
              Example: {example.title}
            </Typography>
            <Typography variant="body2" component="div" sx={{ whiteSpace: 'pre-line' }}>
              {example.description}
            </Typography>
            {example.code && (
              <Paper 
                variant="outlined" 
                sx={{ 
                  p: 2, 
                  mt: 2,
                  bgcolor: 'grey.900', 
                  color: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto'
                }}
              >
                <pre style={{ margin: 0 }}>{example.code}</pre>
              </Paper>
            )}
          </Paper>
        );
      default:
        return (
          <Typography variant="body1">
            {contentItem.content}
          </Typography>
        );
    }
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
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Button 
          startIcon={<ArrowBackIcon />} 
          onClick={() => navigate('/learning')}
          sx={{ mr: 2 }}
        >
          Back to Learning
        </Button>
        <Breadcrumbs aria-label="breadcrumb">
          <Link component={RouterLink} to="/learning" underline="hover" color="inherit">
            Learning
          </Link>
          <Typography color="text.primary">{topic?.name}</Typography>
        </Breadcrumbs>
      </Box>
      
      <Paper elevation={2} sx={{ p: 3, mb: 4, borderRadius: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <MenuBookIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
          <Typography variant="h4" component="h1">
            {topic?.name}
          </Typography>
        </Box>
        <Typography variant="body1" paragraph>
          {topic?.description}
        </Typography>
      </Paper>
      
      <Grid container spacing={4}>
        {/* Main Content */}
        <Grid item xs={12} md={8}>
          <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
            {topic?.content.map((contentItem, index) => (
              <Box key={contentItem.id} sx={{ mb: 4 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    {contentItem.title}
                  </Typography>
                  <Button
                    variant="outlined"
                    size="small"
                    color={contentItem.completed ? "success" : "primary"}
                    startIcon={contentItem.completed ? <CheckCircleIcon /> : null}
                    onClick={() => handleMarkCompleted(contentItem.id, contentItem.completed)}
                  >
                    {contentItem.completed ? "Completed" : "Mark as Completed"}
                  </Button>
                </Box>
                
                {renderContentItem(contentItem)}
                
                {index < topic.content.length - 1 && (
                  <Divider sx={{ my: 3 }} />
                )}
              </Box>
            ))}
          </Paper>
        </Grid>
        
        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          {/* Progress Card */}
          <Paper elevation={2} sx={{ p: 3, mb: 4, borderRadius: 2 }}>
            <Typography variant="h6" gutterBottom>
              Your Progress
            </Typography>
            
            {topic?.content && (
              <>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ position: 'relative', display: 'inline-flex', mr: 2 }}>
                    <CircularProgress 
                      variant="determinate" 
                      value={(topic.content.filter(item => item.completed).length / topic.content.length) * 100} 
                      size={60} 
                      thickness={4}
                      sx={{ color: 'primary.main' }}
                    />
                    <Box
                      sx={{
                        top: 0,
                        left: 0,
                        bottom: 0,
                        right: 0,
                        position: 'absolute',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      <Typography variant="body2" component="div" color="text.secondary">
                        {`${Math.round((topic.content.filter(item => item.completed).length / topic.content.length) * 100)}%`}
                      </Typography>
                    </Box>
                  </Box>
                  <Box>
                    <Typography variant="body2" color="textSecondary">
                      {topic.content.filter(item => item.completed).length} of {topic.content.length} sections completed
                    </Typography>
                  </Box>
                </Box>
                
                <List dense>
                  {topic.content.map((item) => (
                    <ListItem key={item.id}>
                      <ListItemIcon sx={{ minWidth: 36 }}>
                        {item.completed ? 
                          <CheckCircleIcon color="success" fontSize="small" /> : 
                          <CheckCircleIcon color="disabled" fontSize="small" />
                        }
                      </ListItemIcon>
                      <ListItemText 
                        primary={item.title} 
                        primaryTypographyProps={{ 
                          variant: 'body2',
                          color: item.completed ? 'textPrimary' : 'textSecondary'
                        }}
                      />
                    </ListItem>
                  ))}
                </List>
              </>
            )}
          </Paper>
          
          {/* Related Practice Questions */}
          <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
            <Typography variant="h6" gutterBottom>
              Related Practice Questions
            </Typography>
            
            {relatedQuestions.length > 0 ? (
              <>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Apply what you've learned with these practice questions:
                </Typography>
                
                {relatedQuestions.map(question => (
                  <Card key={question.id} variant="outlined" sx={{ mb: 2 }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <CodeIcon sx={{ mr: 1, color: 'primary.main' }} />
                        <Typography variant="subtitle1">
                          {question.title}
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', mb: 1 }}>
                        <Chip 
                          label={question.difficulty} 
                          size="small"
                          color={
                            question.difficulty === 'easy' ? 'success' : 
                            question.difficulty === 'medium' ? 'warning' : 
                            'error'
                          }
                          sx={{ mr: 1 }}
                        />
                      </Box>
                      <Button 
                        variant="outlined" 
                        size="small" 
                        fullWidth
                        onClick={() => navigate(`/practice/${question.id}`)}
                      >
                        Practice Now
                      </Button>
                    </CardContent>
                  </Card>
                ))}
                
                <Button 
                  variant="contained" 
                  fullWidth
                  onClick={() => navigate('/practice')}
                  sx={{ mt: 1 }}
                >
                  More Practice Questions
                </Button>
              </>
            ) : (
              <Typography variant="body2" color="textSecondary">
                No related practice questions available.
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default LearningTopic;
