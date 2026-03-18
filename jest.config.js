module.exports = {
    testEnvironment: 'node',
    roots: ['<rootDir>/src', '<rootDir>/tests'],
    testMatch: ['**/__tests__/**/*.js', '**/?(*.)+(spec|test).js'],
    collectCoverageFrom: [
        'src/**/*.js',
        '!src/index.js'
    ],
    transform: {
        '^.+\\.js$': 'babel-jest'
    }
};
