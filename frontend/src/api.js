const BASE = import.meta.env.VITE_API_HOST || 'http://localhost'
const PORT = import.meta.env.VITE_API_PORT || '81'
const PREFIX = import.meta.env.VITE_API_PREFIX || ''
export const API_URL =  BASE + ':' + PORT + PREFIX
