const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.post('/api/users', async (req, res) => {
    try {
        const { UserService } = require('./services/UserService');
        const user = await UserService.createUser(req.body);
        res.json({ success: true, user: user.toJSON() });
    } catch (error) {
        console.error('User creation failed:', error);
        res.status(400).json({ error: error.message });
    }
});

app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

if (process.env.NODE_ENV !== 'test') {
    app.listen(PORT, () => {
        console.log(`Server running on port ${PORT}`);
    });
}

module.exports = app;
