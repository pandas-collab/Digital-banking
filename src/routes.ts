import { Router } from 'express';

export const routes = Router();

routes.get('/', (req, res) => {
    res.json({ message: 'Agent integration API' });
});

routes.post('/echo', (req, res) => {
    const { data } = req.body;
    if (!data) {
        return res.status(400).json({ error: 'data field required' });
    }
    res.json({ echo: data });
});
