const express = require('express');
const fs = require('fs');
const path = require('path');
const Quiz = require('../models/Quiz');
const router = express.Router();

// Route to handle quiz submission
router.post('/', async (req, res) => {
    try {
        const { name, responses } = req.body;

        if (!name || !responses || !Array.isArray(responses) || responses.length === 0) {
            return res.status(400).json({ error: 'Invalid input data' });
        }

        // Save quiz data to MongoDB
        const quiz = new Quiz({ name, responses });
        await quiz.save();

        // Prepare input text file for ML model
        const inputText = responses.map(r => `${r.question} - ${r.answer}`).join('\n');
        const inputDir = path.join(__dirname, '../../ml_model/input');
        const inputFile = path.join(inputDir, 'input.txt');

        if (!fs.existsSync(inputDir)) {
            fs.mkdirSync(inputDir, { recursive: true });
        }

        fs.writeFileSync(inputFile, inputText);

        // Call ML model (assuming Flask app is running on port 5000)
        const axios = require('axios');
        const mlApiUrl = 'http://localhost:5000/analyze_quiz';
        const response = await axios.post(mlApiUrl, { responses });

        return res.status(200).json({ message: 'Quiz submitted successfully', result: response.data });

    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'An error occurred while processing the quiz' });
    }
});

module.exports = router;
