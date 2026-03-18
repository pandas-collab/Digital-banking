class User {
    constructor(data) {
        this.email = data?.email || '';
        this.password = data?.password || '';
    }

    static validate(data) {
        if (!data?.email || !data?.password) {
            throw new Error('Email and password required');
        }
        return true;
    }

    toJSON() {
        return {
            email: this.email
        };
    }
}

module.exports = User;
