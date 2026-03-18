const UserService = require('../src/services/UserService');
const User = require('../src/models/User');

describe('UserService', () => {
    test('should create user successfully', async () => {
        const userData = { email: 'test@example.com', password: 'secret' };
        const user = await UserService.createUser(userData);
        expect(user).toBeInstanceOf(User);
    });

    test('should reject invalid user data', async () => {
        await expect(UserService.createUser({})).rejects.toThrow('User creation failed');
    });
});
