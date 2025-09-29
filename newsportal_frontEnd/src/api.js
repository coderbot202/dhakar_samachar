// newsportal_frontEnd/src/api.js

import axios from 'axios';

const api = axios.create({
  // Use 127.0.0.1 to match Django's preferred loopback address
  baseURL: 'http://127.0.0.1:8000/api/',
});

export default api;