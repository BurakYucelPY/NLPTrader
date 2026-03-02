// Merkezi API yapılandırması
// Deploy ortamında VITE_API_URL environment variable'ı ile değiştirilebilir
export const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
