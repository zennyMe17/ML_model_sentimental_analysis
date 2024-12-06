const mongoose = require('mongoose');

const responseSchema = new mongoose.Schema({
  question: String,
  answer: String,
});

const quizSchema = new mongoose.Schema({
  name: { type: String, required: true },
  responses: [responseSchema],
}, { timestamps: true });

module.exports = mongoose.model('Quiz', quizSchema);
