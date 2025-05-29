import { AxiosResponse } from "axios";
import { useEffect } from "react";
import { NavigateFunction } from "react-router-dom";
import AuthService from "../../api/services/authService";
import { BaseUserInterface } from "../../interfaces/authInterfaces";

export default function useUserAuthCallback(
  navigate: NavigateFunction,
  authService: AuthService,
  setUser: React.Dispatch<React.SetStateAction<BaseUserInterface | null>>
) {
  useEffect(() => {
    const hash = window.location.hash;

    // 🔐 Авторизация через Яндекс (access_token в hash)
    if (hash.includes("access_token")) {
      const hashParams = new URLSearchParams(hash.slice(1));
      const access_token = hashParams.get("access_token");

      if (access_token) {
        // Удаляем хэш из URL, чтобы не мешал React Router'у
        const cleanUrl = `${window.location.origin}${window.location.pathname}`;
        window.history.replaceState(null, "", cleanUrl);

        // Выполняем авторизацию
        authService.authWithYandex(access_token)
          .then((response: AxiosResponse) => {
            console.log("✅ Успешная авторизация через Яндекс");
            setUser(response.data);
            navigate("/profile");
          })
          .catch((err) => {
            console.error("❌ Ошибка авторизации через Яндекс:", err);
            navigate("/register");
          });

        return;
      }
    }

    // 🔓 Авторизация через VK (code в query string)
    const searchParams = new URLSearchParams(window.location.search);
    const code = searchParams.get("code");

    if (code) {
      authService.authWithVk(code)
        .then((response: AxiosResponse) => {
          console.log("✅ Успешная авторизация через VK");
          setUser(response.data);
          navigate("/profile");
        })
        .catch((err) => {
          console.error("❌ Ошибка авторизации через VK:", err);
          navigate("/register");
        });
    } else {
      navigate("/register");
    }

  }, []);
}
