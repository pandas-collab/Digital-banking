const User = require('../src/models/User');

describe('User Model', () => {
    test('should create user with valid data', () => {
        const user = new User({ email: 'test@example.com', password: 'secret' });
        expect(user.email).toBe('test@example.com');
    });

    test('should throw error for invalid data', () => {
        expect(() => User.validate({})).toThrow('Email and password required');
    });

    test('should exclude password from JSON', () => {
        const user = new User({ email: 'test@example.com', password: 'secret' });
        const json = user.toJSON();
        expect(json.password).toBeUndefined();
    });
});
