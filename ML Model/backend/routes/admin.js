const express = require('express');
const Quiz = require('../models/Quiz');
const axios = require('axios');

const router = express.Router();

// Fetch all quizzes
router.get('/quizzes', async (req, res) => {
  try {
    const quizzes = await Quiz.find({});
    res.status(200).json(quizzes);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch quizzes' });
  }
});

// Analyze a specific quiz
router.get('/analyze/:quizId', async (req, res) => {
  const { quizId } = req.params;

  try {
    const quiz = await Quiz.findById(quizId);
    if (!quiz) return res.status(404).json({ error: 'Quiz not found' });

    // Prepare data for ML model
    const quizData = quiz.responses.map((r, i) => `${i + 1}. ${r.question} - ${r.answer}`).join('\n');

    // Call the ML model API
    const response = await axios.post('http://localhost:5000/analyze', { data: quizData });

    res.status(200).json({ result: response.data.result });
  } catch (error) {
    console.error('Error analyzing quiz:', error.message);
    res.status(500).json({ error: 'Failed to analyze quiz' });
  }
});

module.exports = router;
