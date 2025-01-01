// import axios from 'axios';

// const api = axios.create({
//   baseURL: 'http://127.0.0.1:8000/api', // Replace with your Django server URL
//   headers: {
//     'Content-Type': 'application/json',
//   }
// });

// // Add token to request if authenticated
// api.interceptors.request.use(config => {
//   const token = localStorage.getItem('access_token');
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`;
//   }
//   return config;
// }, error => {
//   return Promise.reject(error);
// });

// export default api;
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',  // Django backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add Authorization header for authenticated requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  
  // Check if the endpoint does not require authentication (e.g., register or login)
  const isPublicEndpoint = config.url.includes('/register/') || config.url.includes('/login/');

  // Add Authorization header for protected routes only
  if (token && !isPublicEndpoint) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  return config;
}, error => {
  return Promise.reject(error);
});

export default api;
