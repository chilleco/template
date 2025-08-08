import axios from 'axios';

const API_BASE = process.env.API_BASE_URL || 'https://api.myapp.com';

// Создаем экземпляр axios с базовыми настройками
export const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
});

// Интерцептор: автоматическое подставление JWT токена в заголовки
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

// Интерцептор: обработка 401 ответа (например, попытка refresh)
apiClient.interceptors.response.use(
  response => response,
  async error => {
    if (error.response && error.response.status === 401) {
      // токен просрочен, пробуем обновить
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        // вызов нашего /auth/token/refresh
        try {
          const res = await axios.post(`${API_BASE}/auth/token/refresh`, {}, {
            headers: {'Authorization': `Bearer ${refreshToken}`}
          });
          localStorage.setItem('access_token', res.data.access_token);
          // повторяем оригинальный запрос
          error.config.headers['Authorization'] = `Bearer ${res.data.access_token}`;
          return axios(error.config);
        } catch (refreshErr) {
          // не удалось refresh – редирект на логин
          window.location.href = '/login';
        }
      } else {
        // нет refresh токена – редирект на логин
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
