const express = require('express');
const app = express();

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Basic test endpoint
app.get('/test', (req, res) => {
    res.json({ test: true, message: 'Integration tests ready' });
});

module.exports = app;
