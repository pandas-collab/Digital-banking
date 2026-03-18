import request from 'supertest';
import app from '../index';

describe('Agent Integration Tests', () => {
    it('should return health status', async () => {
        const res = await request(app).get('/health');
        expect(res.status).toBe(200);
        expect(res.body.status).toBe('ok');
    });

    it('should echo posted data', async () => {
        const testData = { test: 'value' };
        const res = await request(app)
            .post('/api/echo')
            .send({ data: testData });
        expect(res.status).toBe(200);
        expect(res.body.echo).toEqual(testData);
    });
});
