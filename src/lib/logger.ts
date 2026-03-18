interface LogEntry {
  timestamp: string;
  level: 'info' | 'warn' | 'error';
  message: string;
  data?: any;
}

const isBrowser = typeof window !== 'undefined';

export const logger = {
  log: (level: LogEntry['level'], message: string, data?: any) => {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      data
    };

    if (isBrowser && (process.env.NODE_ENV === 'development' || window.debugMode)) {
      console[level](`[${entry.timestamp}] ${level.toUpperCase()}: ${message}`, data || '');
    }
  },

  info: (message: string, data?: any) => {
    logger.log('info', message, data);
  },

  warn: (message: string, data?: any) => {
    logger.log('warn', message, data);
  },

  error: (message: string, data?: any) => {
    logger.log('error', message, data);
  }
};

export default logger;
