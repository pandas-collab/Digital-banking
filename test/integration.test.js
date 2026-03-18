const app = require('../index');
const request = require('supertest');

describe('Integration Tests', () => {
    test('Health check returns 200', async () => {
        const response = await request(app).get('/health');
        expect(response.statusCode).toBe(200);
        expect(response.body.status).toBe('ok');
    });

    test('Test endpoint returns correct structure', async () => {
        const response = await request(app).get('/test');
        expect(response.statusCode).toBe(200);
        expect(response.body.test).toBe(true);
    });
});
