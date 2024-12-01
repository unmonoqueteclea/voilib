const BASE = import.meta.env.VITE_API_HOST || 'http://localhost'
const PORT = import.meta.env.VITE_API_PORT || '81'
const PREFIX = import.meta.env.VITE_API_PREFIX || ''


const isDefaultPort = (url, port) => {
  const isHttp = url.startsWith('http://') && port === '80';
  const isHttps = url.startsWith('https://') && port === '443';
  return isHttp || isHttps;
};

export const API_URL = isDefaultPort(BASE, PORT) ? BASE + PREFIX : BASE + ':' + PORT + PREFIX;
