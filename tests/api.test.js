const request = require('supertest');
const app = require('../src/index');

describe('API Endpoints', () => {
    test('POST /api/users should create user', async () => {
        const response = await request(app)
            .post('/api/users')
            .send({ email: 'test@example.com', password: 'secret' });

        expect(response.status).toBe(200);
        expect(response.body.success).toBe(true);
    });

    test('GET /health should return status', async () => {
        const response = await request(app).get('/health');
        expect(response.status).toBe(200);
        expect(response.body.status).toBe('ok');
    });
});
