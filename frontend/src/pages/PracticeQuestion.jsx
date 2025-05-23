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
  Chip,
  IconButton,
  Tooltip
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { questionsApi, submissionsApi, practiceApi } from '../services/api';
import { Editor } from '@monaco-editor/react';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import RefreshIcon from '@mui/icons-material/Refresh';

const PracticeQuestion = () => {
  const { questionId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('javascript');
  const [evaluating, setEvaluating] = useState(false);
  const [evaluation, setEvaluation] = useState(null);
  const [generating, setGenerating] = useState(false);
  
  // Load question data
  useEffect(() => {
    const fetchQuestion = async () => {
      try {
        setLoading(true);
        const data = await questionsApi.getQuestion(questionId);
        setQuestion(data);
        
        // Set initial code template based on question
        if (data.code_template) {
          setCode(data.code_template);
        } else {
          // Default template if none provided
          setCode(`// Write your solution for "${data.title}" here\n\n`);
        }
      } catch (error) {
        console.error('Error fetching question:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchQuestion();
  }, [questionId]);

  const handleCodeChange = (value) => {
    setCode(value);
  };

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      setEvaluating(true);
      setEvaluation(null);
      
      // Submit solution for evaluation
      const result = await practiceApi.evaluateSolution({
        question_id: questionId,
        code,
        language
      });
      
      // Record activity
      await practiceApi.recordActivity({
        question_id: questionId,
        completed: result.passed
      });
      
      setEvaluation(result);
    } catch (error) {
      console.error('Error evaluating solution:', error);
    } finally {
      setEvaluating(false);
    }
  };

  const handleToggleFavorite = async () => {
    try {
      if (question.is_favorite) {
        await questionsApi.removeFromFavorites(questionId);
      } else {
        await questionsApi.addToFavorites(questionId);
      }
      
      // Update question state
      setQuestion(prev => ({
        ...prev,
        is_favorite: !prev.is_favorite
      }));
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  const handleGenerateSimilar = async () => {
    try {
      setGenerating(true);
      const newQuestion = await questionsApi.generateSimilarQuestion(questionId);
      
      // Navigate to the new question
      navigate(`/practice/${newQuestion.id}`);
    } catch (error) {
      console.error('Error generating similar question:', error);
    } finally {
      setGenerating(false);
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
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <IconButton onClick={() => navigate('/practice')} sx={{ mr: 1 }}>
          <ArrowBackIcon />
        </IconButton>
        <Typography variant="h4" component="h1" sx={{ flexGrow: 1 }}>
          Practice Question
        </Typography>
        <Box>
          <Tooltip title={question?.is_favorite ? "Remove from favorites" : "Add to favorites"}>
            <IconButton 
              onClick={handleToggleFavorite}
              color={question?.is_favorite ? "secondary" : "default"}
            >
              {question?.is_favorite ? <FavoriteIcon /> : <FavoriteBorderIcon />}
            </IconButton>
          </Tooltip>
          <Button 
            variant="outlined" 
            startIcon={<RefreshIcon />}
            onClick={handleGenerateSimilar}
            disabled={generating}
            sx={{ ml: 1 }}
          >
            {generating ? 'Generating...' : 'Similar Question'}
          </Button>
        </Box>
      </Box>
      
      <Grid container spacing={2}>
        {/* Question Panel */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3, height: '100%', borderRadius: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5" gutterBottom>
                {question?.title}
              </Typography>
              <Box>
                <Chip 
                  label={question?.difficulty} 
                  size="small"
                  color={
                    question?.difficulty === 'easy' ? 'success' : 
                    question?.difficulty === 'medium' ? 'warning' : 
                    'error'
                  }
                  sx={{ mr: 1 }}
                />
                <Chip 
                  label={question?.topic} 
                  size="small"
                  color="primary"
                  variant="outlined"
                />
              </Box>
            </Box>
            
            <Divider sx={{ mb: 2 }} />
            
            <Box sx={{ 
              mb: 3, 
              maxHeight: 'calc(100vh - 350px)', 
              overflowY: 'auto',
              pr: 1
            }}>
              <Typography variant="body1" component="div" sx={{ whiteSpace: 'pre-line' }}>
                {question?.content}
              </Typography>
              
              {question?.examples && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Examples:
                  </Typography>
                  {question.examples.map((example, index) => (
                    <Paper 
                      key={index} 
                      variant="outlined" 
                      sx={{ p: 2, mb: 2, bgcolor: 'grey.50' }}
                    >
                      <Typography variant="body2" component="div" sx={{ whiteSpace: 'pre-line' }}>
                        <strong>Input:</strong> {example.input}
                      </Typography>
                      <Typography variant="body2" component="div" sx={{ whiteSpace: 'pre-line' }}>
                        <strong>Output:</strong> {example.output}
                      </Typography>
                      {example.explanation && (
                        <Typography variant="body2" component="div" sx={{ whiteSpace: 'pre-line', mt: 1 }}>
                          <strong>Explanation:</strong> {example.explanation}
                        </Typography>
                      )}
                    </Paper>
                  ))}
                </Box>
              )}
              
              {question?.constraints && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Constraints:
                  </Typography>
                  <Typography variant="body2" component="div" sx={{ whiteSpace: 'pre-line' }}>
                    {question.constraints}
                  </Typography>
                </Box>
              )}
            </Box>
          </Paper>
        </Grid>
        
        {/* Code Editor Panel */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3, height: '100%', borderRadius: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5" gutterBottom>
                Your Solution
              </Typography>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button 
                  variant="contained" 
                  color="primary"
                  onClick={handleSubmit}
                  disabled={evaluating}
                >
                  {evaluating ? 'Evaluating...' : 'Submit Solution'}
                </Button>
              </Box>
            </Box>
            
            <Divider sx={{ mb: 2 }} />
            
            <Box sx={{ height: 'calc(100vh - 350px)' }}>
              <Editor
                height="100%"
                language={language}
                value={code}
                onChange={handleCodeChange}
                theme="vs-dark"
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  wordWrap: 'on',
                  automaticLayout: true,
                }}
              />
            </Box>
            
            {evaluation && (
              <Paper 
                elevation={1} 
                sx={{ 
                  mt: 2, 
                  p: 2, 
                  bgcolor: evaluation.passed ? 'success.light' : 'error.light',
                  color: evaluation.passed ? 'success.contrastText' : 'error.contrastText'
                }}
              >
                <Typography variant="h6" gutterBottom>
                  {evaluation.passed ? 'Solution Accepted!' : 'Solution Failed'}
                </Typography>
                <Typography variant="body2" component="div" sx={{ whiteSpace: 'pre-line' }}>
                  {evaluation.feedback}
                </Typography>
                
                {evaluation.test_results && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Test Results:
                    </Typography>
                    {evaluation.test_results.map((test, index) => (
                      <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Box 
                          sx={{ 
                            width: 16, 
                            height: 16, 
                            borderRadius: '50%', 
                            bgcolor: test.passed ? 'success.main' : 'error.main',
                            mr: 1
                          }} 
                        />
                        <Typography variant="body2">
                          Test {index + 1}: {test.passed ? 'Passed' : 'Failed'} 
                          {test.message && ` - ${test.message}`}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                )}
              </Paper>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default PracticeQuestion;
