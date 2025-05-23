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
  Tabs,
  Tab,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Divider,
  Paper,
  Chip
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { questionsApi, practiceApi } from '../services/api';

const Practice = () => {
  const [loading, setLoading] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [questions, setQuestions] = useState([]);
  const [practiceSession, setPracticeSession] = useState([]);
  const [filters, setFilters] = useState({
    topic: '',
    difficulty: '',
    company: ''
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [generating, setGenerating] = useState(false);
  
  const navigate = useNavigate();

  // Fetch initial questions
  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      const data = await questionsApi.getQuestions({ limit: 10 });
      setQuestions(data);
    } catch (error) {
      console.error('Error fetching questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPracticeSession = async () => {
    try {
      setLoading(true);
      const data = await practiceApi.getPracticeSession(filters);
      setPracticeSession(data);
    } catch (error) {
      console.error('Error fetching practice session:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
    
    // Load practice session when switching to that tab
    if (newValue === 1 && practiceSession.length === 0) {
      fetchPracticeSession();
    }
  };

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = async () => {
    try {
      setLoading(true);
      const data = await questionsApi.getQuestions({
        ...filters,
        query: searchQuery,
        limit: 10
      });
      setQuestions(data);
    } catch (error) {
      console.error('Error searching questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateQuestion = async () => {
    try {
      setGenerating(true);
      const newQuestion = await questionsApi.generateQuestion(filters);
      
      // Add to questions list
      setQuestions(prev => [newQuestion, ...prev]);
      
      // Navigate to the new question
      navigate(`/practice/${newQuestion.id}`);
    } catch (error) {
      console.error('Error generating question:', error);
    } finally {
      setGenerating(false);
    }
  };

  const handleStartPractice = () => {
    fetchPracticeSession();
  };

  const handleQuestionClick = (questionId) => {
    navigate(`/practice/${questionId}`);
  };

  const handleToggleFavorite = async (questionId, isFavorite, event) => {
    event.stopPropagation();
    try {
      if (isFavorite) {
        await questionsApi.removeFromFavorites(questionId);
      } else {
        await questionsApi.addToFavorites(questionId);
      }
      
      // Update questions list
      setQuestions(prev => 
        prev.map(q => 
          q.id === questionId ? { ...q, is_favorite: !isFavorite } : q
        )
      );
      
      // Update practice session list if needed
      if (practiceSession.length > 0) {
        setPracticeSession(prev => 
          prev.map(q => 
            q.id === questionId ? { ...q, is_favorite: !isFavorite } : q
          )
        );
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  // Topic options
  const topics = [
    { value: 'arrays', label: 'Arrays & Strings' },
    { value: 'linked_lists', label: 'Linked Lists' },
    { value: 'stacks_queues', label: 'Stacks & Queues' },
    { value: 'trees_graphs', label: 'Trees & Graphs' },
    { value: 'recursion', label: 'Recursion' },
    { value: 'dynamic_programming', label: 'Dynamic Programming' },
    { value: 'sorting_searching', label: 'Sorting & Searching' },
    { value: 'bit_manipulation', label: 'Bit Manipulation' }
  ];

  // Difficulty options
  const difficulties = [
    { value: 'easy', label: 'Easy' },
    { value: 'medium', label: 'Medium' },
    { value: 'hard', label: 'Hard' }
  ];

  // Company options
  const companies = [
    { value: 'google', label: 'Google' },
    { value: 'amazon', label: 'Amazon' },
    { value: 'microsoft', label: 'Microsoft' },
    { value: 'facebook', label: 'Facebook' },
    { value: 'apple', label: 'Apple' },
    { value: 'netflix', label: 'Netflix' }
  ];

  const renderQuestionCard = (question) => (
    <Paper 
      elevation={2} 
      sx={{ 
        p: 3, 
        mb: 2, 
        borderRadius: 2,
        cursor: 'pointer',
        '&:hover': { bgcolor: 'action.hover' }
      }}
      onClick={() => handleQuestionClick(question.id)}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Typography variant="h6" gutterBottom>
          {question.title}
        </Typography>
        <Box>
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
          <Chip 
            label={question.topic} 
            size="small"
            color="primary"
            variant="outlined"
          />
        </Box>
      </Box>
      
      <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
        {question.content.split('\n')[0].substring(0, 150)}...
      </Typography>
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Button 
          variant="outlined" 
          size="small"
          onClick={(e) => handleToggleFavorite(question.id, question.is_favorite, e)}
          color={question.is_favorite ? 'secondary' : 'primary'}
        >
          {question.is_favorite ? 'Unfavorite' : 'Favorite'}
        </Button>
        
        {question.company && (
          <Chip 
            label={question.company} 
            size="small"
            variant="outlined"
          />
        )}
      </Box>
    </Paper>
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Practice Questions
      </Typography>
      
      <Tabs 
        value={tabValue} 
        onChange={handleTabChange} 
        sx={{ mb: 4 }}
        variant="fullWidth"
      >
        <Tab label="Browse Questions" />
        <Tab label="Practice Session" />
        <Tab label="Generate Question" />
      </Tabs>
      
      {/* Browse Questions Tab */}
      {tabValue === 0 && (
        <>
          <Paper elevation={1} sx={{ p: 3, mb: 4 }}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="topic-label">Topic</InputLabel>
                  <Select
                    labelId="topic-label"
                    name="topic"
                    value={filters.topic}
                    label="Topic"
                    onChange={handleFilterChange}
                  >
                    <MenuItem value="">Any</MenuItem>
                    {topics.map(topic => (
                      <MenuItem key={topic.value} value={topic.value}>
                        {topic.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="difficulty-label">Difficulty</InputLabel>
                  <Select
                    labelId="difficulty-label"
                    name="difficulty"
                    value={filters.difficulty}
                    label="Difficulty"
                    onChange={handleFilterChange}
                  >
                    <MenuItem value="">Any</MenuItem>
                    {difficulties.map(difficulty => (
                      <MenuItem key={difficulty.value} value={difficulty.value}>
                        {difficulty.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="company-label">Company</InputLabel>
                  <Select
                    labelId="company-label"
                    name="company"
                    value={filters.company}
                    label="Company"
                    onChange={handleFilterChange}
                  >
                    <MenuItem value="">Any</MenuItem>
                    {companies.map(company => (
                      <MenuItem key={company.value} value={company.value}>
                        {company.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={3}>
                <Button 
                  variant="contained" 
                  fullWidth
                  onClick={handleSearch}
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Search'}
                </Button>
              </Grid>
            </Grid>
          </Paper>
          
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          ) : (
            <>
              {questions.length > 0 ? (
                questions.map(question => renderQuestionCard(question))
              ) : (
                <Typography variant="body1" sx={{ textAlign: 'center', py: 4 }}>
                  No questions found. Try adjusting your filters.
                </Typography>
              )}
            </>
          )}
        </>
      )}
      
      {/* Practice Session Tab */}
      {tabValue === 1 && (
        <>
          <Paper elevation={1} sx={{ p: 3, mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Personalized Practice Session
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              Create a customized practice session based on your preferences. We'll select questions tailored to your needs.
            </Typography>
            
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="session-topic-label">Topic</InputLabel>
                  <Select
                    labelId="session-topic-label"
                    name="topic"
                    value={filters.topic}
                    label="Topic"
                    onChange={handleFilterChange}
                  >
                    <MenuItem value="">Any</MenuItem>
                    {topics.map(topic => (
                      <MenuItem key={topic.value} value={topic.value}>
                        {topic.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="session-difficulty-label">Difficulty</InputLabel>
                  <Select
                    labelId="session-difficulty-label"
                    name="difficulty"
                    value={filters.difficulty}
                    label="Difficulty"
                    onChange={handleFilterChange}
                  >
                    <MenuItem value="">Any</MenuItem>
                    {difficulties.map(difficulty => (
                      <MenuItem key={difficulty.value} value={difficulty.value}>
                        {difficulty.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="session-company-label">Company</InputLabel>
                  <Select
                    labelId="session-company-label"
                    name="company"
                    value={filters.company}
                    label="Company"
                    onChange={handleFilterChange}
                  >
                    <MenuItem value="">Any</MenuItem>
                    {companies.map(company => (
                      <MenuItem key={company.value} value={company.value}>
                        {company.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={3}>
                <Button 
                  variant="contained" 
                  fullWidth
                  onClick={handleStartPractice}
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Start Practice'}
                </Button>
              </Grid>
            </Grid>
          </Paper>
          
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          ) : (
            <>
              {practiceSession.length > 0 ? (
                <>
                  <Typography variant="h6" gutterBottom>
                    Your Practice Session ({practiceSession.length} questions)
                  </Typography>
                  {practiceSession.map(question => renderQuestionCard(question))}
                </>
              ) : (
                <Typography variant="body1" sx={{ textAlign: 'center', py: 4 }}>
                  No practice session started yet. Configure your preferences and click "Start Practice".
                </Typography>
              )}
            </>
          )}
        </>
      )}
      
      {/* Generate Question Tab */}
      {tabValue === 2 && (
        <>
          <Paper elevation={1} sx={{ p: 3, mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Generate Custom Question
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              Use AI to generate a custom interview question based on your preferences.
            </Typography>
            
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={4}>
                <FormControl fullWidth size="small">
                  <InputLabel id="gen-topic-label">Topic</InputLabel>
                  <Select
                    labelId="gen-topic-label"
                    name="topic"
                    value={filters.topic}
                    label="Topic"
                    onChange={handleFilterChange}
                    required
                  >
                    <MenuItem value="">Select Topic</MenuItem>
                    {topics.map(topic => (
                      <MenuItem key={topic.value} value={topic.value}>
                        {topic.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={4}>
                <FormControl fullWidth size="small">
                  <InputLabel id="gen-difficulty-label">Difficulty</InputLabel>
                  <Select
                    labelId="gen-difficulty-label"
                    name="difficulty"
                    value={filters.difficulty}
                    label="Difficulty"
                    onChange={handleFilterChange}
                    required
                  >
                    <MenuItem value="">Select Difficulty</MenuItem>
                    {difficulties.map(difficulty => (
                      <MenuItem key={difficulty.value} value={difficulty.value}>
                        {difficulty.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={4}>
                <FormControl fullWidth size="small">
                  <InputLabel id="gen-company-label">Company (Optional)</InputLabel>
                  <Select
                    labelId="gen-company-label"
                    name="company"
                    value={filters.company}
                    label="Company (Optional)"
                    onChange={handleFilterChange}
                  >
                    <MenuItem value="">Any</MenuItem>
                    {companies.map(company => (
                      <MenuItem key={company.value} value={company.value}>
                        {company.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            
            <Button 
              variant="contained" 
              fullWidth
              sx={{ mt: 3 }}
              onClick={handleGenerateQuestion}
              disabled={generating || !filters.topic || !filters.difficulty}
            >
              {generating ? (
                <>
                  <CircularProgress size={24} sx={{ mr: 1 }} />
                  Generating Question...
                </>
              ) : (
                'Generate Question'
              )}
            </Button>
            
            <Typography variant="body2" color="textSecondary" sx={{ mt: 2, textAlign: 'center' }}>
              Note: Question generation may take up to 30 seconds.
            </Typography>
          </Paper>
          
          <Typography variant="body1" sx={{ textAlign: 'center', py: 2 }}>
            Generated questions will appear in your question list and can be favorited for later practice.
          </Typography>
        </>
      )}
    </Container>
  );
};

export default Practice;
