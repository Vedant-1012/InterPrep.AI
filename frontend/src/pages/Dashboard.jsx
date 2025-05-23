// import React, { useState, useEffect } from 'react';
// import { 
//   Box, 
//   Container, 
//   Typography, 
//   Grid, 
//   Card, 
//   CardContent, 
//   Button, 
//   CircularProgress,
//   Chip,
//   Divider,
//   Paper
// } from '@mui/material';
// import { 
//   BarChart, 
//   Bar, 
//   XAxis, 
//   YAxis, 
//   CartesianGrid, 
//   Tooltip, 
//   ResponsiveContainer,
//   PieChart,
//   Pie,
//   Cell
// } from 'recharts';
// import { useNavigate } from 'react-router-dom';
// import { userApi, practiceApi, learningApi } from '../services/api';

// const Dashboard = () => {
//   const [loading, setLoading] = useState(true);
//   const [stats, setStats] = useState(null);
//   const [practiceProgress, setPracticeProgress] = useState(null);
//   const [learningStats, setLearningStats] = useState(null);
//   const [recommendations, setRecommendations] = useState([]);
//   const navigate = useNavigate();

//   useEffect(() => {
//     const fetchDashboardData = async () => {
//       try {
//         setLoading(true);
        
//         // Fetch user stats
//         const userStats = await userApi.getUserStats();
//         setStats(userStats);
        
//         // Fetch practice progress
//         const practiceData = await practiceApi.getPracticeProgress();
//         setPracticeProgress(practiceData);
        
//         // Fetch learning stats
//         const learningData = await learningApi.getLearningStats();
//         setLearningStats(learningData);
        
//         // Fetch recommendations
//         const recommendedTopics = await learningApi.getRecommendations(3);
//         setRecommendations(recommendedTopics);
//       } catch (error) {
//         console.error('Error fetching dashboard data:', error);
//       } finally {
//         setLoading(false);
//       }
//     };
    
//     fetchDashboardData();
//   }, []);

//   // Prepare data for charts
//   const prepareSubmissionData = () => {
//     if (!stats || !stats.submissions) return [];
    
//     return [
//       { name: 'Correct', value: stats.submissions.correct, color: '#4caf50' },
//       { name: 'Incorrect', value: stats.submissions.incorrect, color: '#f44336' },
//       { name: 'Pending', value: stats.submissions.pending, color: '#ff9800' }
//     ];
//   };
  
//   const prepareDifficultyData = () => {
//     if (!practiceProgress || !practiceProgress.difficulties) return [];
    
//     return [
//       { name: 'Easy', correct: practiceProgress.difficulties.easy.correct, incorrect: practiceProgress.difficulties.easy.incorrect },
//       { name: 'Medium', correct: practiceProgress.difficulties.medium.correct, incorrect: practiceProgress.difficulties.medium.incorrect },
//       { name: 'Hard', correct: practiceProgress.difficulties.hard.correct, incorrect: practiceProgress.difficulties.hard.incorrect }
//     ];
//   };
  
//   const COLORS = ['#4caf50', '#f44336', '#ff9800'];

//   if (loading) {
//     return (
//       <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
//         <CircularProgress />
//       </Box>
//     );
//   }

//   return (
//     <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
//       <Typography variant="h4" component="h1" gutterBottom>
//         Dashboard
//       </Typography>
      
//       {/* Welcome Card */}
//       <Paper elevation={2} sx={{ p: 3, mb: 4, borderRadius: 2 }}>
//         <Typography variant="h5" gutterBottom>
//           Welcome back!
//         </Typography>
//         <Typography variant="body1">
//           Continue your interview preparation journey. You've completed {stats?.submissions?.total || 0} practice questions so far.
//         </Typography>
//         <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
//           <Button 
//             variant="contained" 
//             color="primary"
//             onClick={() => navigate('/practice')}
//           >
//             Practice Questions
//           </Button>
//           <Button 
//             variant="outlined" 
//             color="primary"
//             onClick={() => navigate('/learning')}
//           >
//             Learning Resources
//           </Button>
//         </Box>
//       </Paper>
      
//       <Grid container spacing={4}>
//         {/* Stats Overview */}
//         <Grid item xs={12} md={8}>
//           <Card sx={{ height: '100%' }}>
//             <CardContent>
//               <Typography variant="h6" gutterBottom>
//                 Your Progress
//               </Typography>
//               <Grid container spacing={2}>
//                 <Grid item xs={12} sm={4}>
//                   <Box sx={{ textAlign: 'center', p: 2 }}>
//                     <Typography variant="h3" color="primary">
//                       {stats?.submissions?.total || 0}
//                     </Typography>
//                     <Typography variant="body2" color="textSecondary">
//                       Total Questions Attempted
//                     </Typography>
//                   </Box>
//                 </Grid>
//                 <Grid item xs={12} sm={4}>
//                   <Box sx={{ textAlign: 'center', p: 2 }}>
//                     <Typography variant="h3" color="success.main">
//                       {stats?.submissions?.correct || 0}
//                     </Typography>
//                     <Typography variant="body2" color="textSecondary">
//                       Correct Solutions
//                     </Typography>
//                   </Box>
//                 </Grid>
//                 <Grid item xs={12} sm={4}>
//                   <Box sx={{ textAlign: 'center', p: 2 }}>
//                     <Typography variant="h3" color="secondary">
//                       {stats?.favorites_count || 0}
//                     </Typography>
//                     <Typography variant="body2" color="textSecondary">
//                       Favorite Questions
//                     </Typography>
//                   </Box>
//                 </Grid>
//               </Grid>
              
//               <Divider sx={{ my: 2 }} />
              
//               <Typography variant="subtitle1" gutterBottom>
//                 Submission Results
//               </Typography>
//               <Box sx={{ height: 250 }}>
//                 <ResponsiveContainer width="100%" height="100%">
//                   <PieChart>
//                     <Pie
//                       data={prepareSubmissionData()}
//                       cx="50%"
//                       cy="50%"
//                       labelLine={false}
//                       outerRadius={80}
//                       fill="#8884d8"
//                       dataKey="value"
//                       label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
//                     >
//                       {prepareSubmissionData().map((entry, index) => (
//                         <Cell key={`cell-${index}`} fill={entry.color} />
//                       ))}
//                     </Pie>
//                     <Tooltip />
//                   </PieChart>
//                 </ResponsiveContainer>
//               </Box>
//             </CardContent>
//           </Card>
//         </Grid>
        
//         {/* Recommendations */}
//         <Grid item xs={12} md={4}>
//           <Card sx={{ height: '100%' }}>
//             <CardContent>
//               <Typography variant="h6" gutterBottom>
//                 Recommended Topics
//               </Typography>
//               <Typography variant="body2" color="textSecondary" paragraph>
//                 Based on your progress, we recommend focusing on these topics:
//               </Typography>
              
//               {recommendations.length > 0 ? (
//                 <Box sx={{ mt: 2 }}>
//                   {recommendations.map((topic) => (
//                     <Paper 
//                       key={topic.id} 
//                       elevation={1} 
//                       sx={{ 
//                         p: 2, 
//                         mb: 2, 
//                         cursor: 'pointer',
//                         '&:hover': { bgcolor: 'action.hover' }
//                       }}
//                       onClick={() => navigate(`/learning/${topic.id}`)}
//                     >
//                       <Typography variant="subtitle1">{topic.name}</Typography>
//                       <Typography variant="body2" color="textSecondary" noWrap>
//                         {topic.description}
//                       </Typography>
//                       <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
//                         <Box
//                           sx={{
//                             width: '100%',
//                             mr: 1,
//                             bgcolor: 'grey.300',
//                             borderRadius: 5,
//                             height: 8
//                           }}
//                         >
//                           <Box
//                             sx={{
//                               width: `${topic.progress_percentage}%`,
//                               bgcolor: 'primary.main',
//                               borderRadius: 5,
//                               height: 8
//                             }}
//                           />
//                         </Box>
//                         <Typography variant="body2" color="textSecondary">
//                           {Math.round(topic.progress_percentage)}%
//                         </Typography>
//                       </Box>
//                     </Paper>
//                   ))}
                  
//                   <Button 
//                     variant="outlined" 
//                     fullWidth 
//                     sx={{ mt: 2 }}
//                     onClick={() => navigate('/learning')}
//                   >
//                     View All Topics
//                   </Button>
//                 </Box>
//               ) : (
//                 <Typography variant="body1" sx={{ mt: 2 }}>
//                   No recommendations available yet. Start practicing to get personalized recommendations.
//                 </Typography>
//               )}
//             </CardContent>
//           </Card>
//         </Grid>
        
//         {/* Performance by Difficulty */}
//         <Grid item xs={12} md={6}>
//           <Card>
//             <CardContent>
//               <Typography variant="h6" gutterBottom>
//                 Performance by Difficulty
//               </Typography>
//               <Box sx={{ height: 300 }}>
//                 <ResponsiveContainer width="100%" height="100%">
//                   <BarChart
//                     data={prepareDifficultyData()}
//                     margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
//                   >
//                     <CartesianGrid strokeDasharray="3 3" />
//                     <XAxis dataKey="name" />
//                     <YAxis />
//                     <Tooltip />
//                     <Bar dataKey="correct" stackId="a" fill="#4caf50" name="Correct" />
//                     <Bar dataKey="incorrect" stackId="a" fill="#f44336" name="Incorrect" />
//                   </BarChart>
//                 </ResponsiveContainer>
//               </Box>
//             </CardContent>
//           </Card>
//         </Grid>
        
//         {/* Learning Progress */}
//         <Grid item xs={12} md={6}>
//           <Card>
//             <CardContent>
//               <Typography variant="h6" gutterBottom>
//                 Learning Progress
//               </Typography>
//               {learningStats ? (
//                 <>
//                   <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
//                     <Box sx={{ position: 'relative', display: 'inline-flex', mr: 2 }}>
//                       <CircularProgress 
//                         variant="determinate" 
//                         value={learningStats.overall_progress} 
//                         size={80} 
//                         thickness={4}
//                         sx={{ color: 'primary.main' }}
//                       />
//                       <Box
//                         sx={{
//                           top: 0,
//                           left: 0,
//                           bottom: 0,
//                           right: 0,
//                           position: 'absolute',
//                           display: 'flex',
//                           alignItems: 'center',
//                           justifyContent: 'center',
//                         }}
//                       >
//                         <Typography variant="body2" component="div" color="text.secondary">
//                           {`${Math.round(learningStats.overall_progress)}%`}
//                         </Typography>
//                       </Box>
//                     </Box>
//                     <Box>
//                       <Typography variant="body1">
//                         Overall Learning Progress
//                       </Typography>
//                       <Typography variant="body2" color="textSecondary">
//                         {learningStats.completed_content} of {learningStats.total_content} topics completed
//                       </Typography>
//                     </Box>
//                   </Box>
                  
//                   <Typography variant="subtitle2" gutterBottom>
//                     Progress by Category
//                   </Typography>
                  
//                   {learningStats.category_progress.map((category) => (
//                     <Box key={category.id} sx={{ mb: 2 }}>
//                       <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
//                         <Typography variant="body2">{category.name}</Typography>
//                         <Typography variant="body2">{Math.round(category.percentage)}%</Typography>
//                       </Box>
//                       <Box
//                         sx={{
//                           width: '100%',
//                           bgcolor: 'grey.300',
//                           borderRadius: 5,
//                           height: 8
//                         }}
//                       >
//                         <Box
//                           sx={{
//                             width: `${category.percentage}%`,
//                             bgcolor: 'primary.main',
//                             borderRadius: 5,
//                             height: 8
//                           }}
//                         />
//                       </Box>
//                     </Box>
//                   ))}
//                 </>
//               ) : (
//                 <Typography variant="body1">
//                   No learning progress data available yet. Start exploring the learning resources.
//                 </Typography>
//               )}
              
//               <Button 
//                 variant="outlined" 
//                 fullWidth 
//                 sx={{ mt: 2 }}
//                 onClick={() => navigate('/learning')}
//               >
//                 Continue Learning
//               </Button>
//             </CardContent>
//           </Card>
//         </Grid>
//       </Grid>
//     </Container>
//   );
// };

// export default Dashboard;



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
  Chip,
  Divider,
  Paper
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { userApi, practiceApi, learningApi } from '../services/api';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [practiceProgress, setPracticeProgress] = useState(null);
  const [learningStats, setLearningStats] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);

        // 🔍 Debugging user stats
        console.log("📊 Fetching user stats...");
        const userStats = await userApi.getUserStats();
        console.log("✅ User stats response:", userStats);
        setStats(userStats);

        // 🔍 Debugging practice progress
        console.log("📈 Fetching practice progress...");
        const practiceData = await practiceApi.getPracticeProgress();
        console.log("✅ Practice progress:", practiceData);
        setPracticeProgress(practiceData);

        // 🔍 Debugging learning stats
        console.log("📘 Fetching learning stats...");
        const learningData = await learningApi.getLearningStats();
        console.log("✅ Learning stats:", learningData);
        setLearningStats(learningData);

        // 🔍 Debugging recommendations
        console.log("✨ Fetching recommendations...");
        const recommendedTopics = await learningApi.getRecommendations(3);
        console.log("✅ Recommended topics:", recommendedTopics);
        setRecommendations(recommendedTopics);

      } catch (error) {
        console.error('❌ Error fetching dashboard data:', error);
        console.error('📄 Error details:', error.response?.data);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const prepareSubmissionData = () => {
    if (!stats || !stats.submissions) return [];
    return [
      { name: 'Correct', value: stats.submissions.correct, color: '#4caf50' },
      { name: 'Incorrect', value: stats.submissions.incorrect, color: '#f44336' },
      { name: 'Pending', value: stats.submissions.pending, color: '#ff9800' }
    ];
  };

  const prepareDifficultyData = () => {
    if (!practiceProgress || !practiceProgress.difficulties) return [];
    return [
      { name: 'Easy', correct: practiceProgress.difficulties.easy.correct, incorrect: practiceProgress.difficulties.easy.incorrect },
      { name: 'Medium', correct: practiceProgress.difficulties.medium.correct, incorrect: practiceProgress.difficulties.medium.incorrect },
      { name: 'Hard', correct: practiceProgress.difficulties.hard.correct, incorrect: practiceProgress.difficulties.hard.incorrect }
    ];
  };

  const COLORS = ['#4caf50', '#f44336', '#ff9800'];

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
        Dashboard
      </Typography>

      <Paper elevation={2} sx={{ p: 3, mb: 4, borderRadius: 2 }}>
        <Typography variant="h5" gutterBottom>
          Welcome back!
        </Typography>
        <Typography variant="body1">
          Continue your interview preparation journey. You've completed {stats?.submissions?.total || 0} practice questions so far.
        </Typography>
        <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
          <Button variant="contained" color="primary" onClick={() => navigate('/practice')}>Practice Questions</Button>
          <Button variant="outlined" color="primary" onClick={() => navigate('/learning')}>Learning Resources</Button>
        </Box>
      </Paper>

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Your Progress</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <Box sx={{ textAlign: 'center', p: 2 }}>
                    <Typography variant="h3" color="primary">{stats?.submissions?.total || 0}</Typography>
                    <Typography variant="body2" color="textSecondary">Total Questions Attempted</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box sx={{ textAlign: 'center', p: 2 }}>
                    <Typography variant="h3" color="success.main">{stats?.submissions?.correct || 0}</Typography>
                    <Typography variant="body2" color="textSecondary">Correct Solutions</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box sx={{ textAlign: 'center', p: 2 }}>
                    <Typography variant="h3" color="secondary">{stats?.favorites_count || 0}</Typography>
                    <Typography variant="body2" color="textSecondary">Favorite Questions</Typography>
                  </Box>
                </Grid>
              </Grid>

              <Divider sx={{ my: 2 }} />

              <Typography variant="subtitle1" gutterBottom>Submission Results</Typography>
              <Box sx={{ height: 250 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={prepareSubmissionData()}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {prepareSubmissionData().map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* ... rest of the component unchanged (Recommendations, Performance, Learning Progress) */}
        {/* You can copy those from your original if not debugging that section yet */}
      </Grid>
    </Container>
  );
};

export default Dashboard;