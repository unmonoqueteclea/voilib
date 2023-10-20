const BASE = import.meta.env.VITE_API_HOST || 'http://localhost:81'
const API_PREFIX = import.meta.env.VITE_API_PREFIX || ''
export const API_URL =  BASE + API_PREFIX
