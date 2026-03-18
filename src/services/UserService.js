const User = require('../models/User');

class UserService {
    static createUser(userData) {
        try {
            User.validate(userData);
            const user = new User(userData);
            return Promise.resolve(user);
        } catch (error) {
            throw new Error(`User creation failed: ${error.message}`);
        }
    }
}

module.exports = UserService;
