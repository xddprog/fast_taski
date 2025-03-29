import axios, { CreateAxiosDefaults } from "axios";

const baseQueryInstance: CreateAxiosDefaults = {
    baseURL: import.meta.env.VITE_BASE_API_URL,
    withCredentials: true,
    headers: {
        ["Content-Type"]: "application/json"
    }
}


export const axiosClient = axios.create(baseQueryInstance);


axiosClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
  
      if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== "/auth/refresh") {
          originalRequest._retry = true;
  
          try {
            await axiosClient.post("/auth/refresh");
            return axiosClient(originalRequest);
          } catch (error) {
              return Promise.reject(error);
          }
      }
          return Promise.reject(error);
      }
  );
  