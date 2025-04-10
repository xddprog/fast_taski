// AuthWith.ts
import { NavigateFunction } from "react-router-dom";

export function authWithVk(
  event: React.MouseEvent<HTMLButtonElement>,
  navigate: NavigateFunction
) {
  event.preventDefault();
  window.location.assign(
    `${import.meta.env.VITE_VK_API_URL}?client_id=${
      import.meta.env.VITE_VK_APP_ID
    }` +
      `&display=popup` +
      `&redirect_uri=${encodeURIComponent(
        import.meta.env.VITE_REDIRECT_URI + "/auth/callback"
      )}` +
      `&response_type=code` +
      `&v=5.131`
  );
}

export function authWithYandex(
  event: React.MouseEvent<HTMLButtonElement>,
  navigate: NavigateFunction
) {
  event.preventDefault();
  navigate("/auth/callback", { state: { service: "yandex", code: "123" } });
  window.location.assign(
    `${
      import.meta.env.VITE_YANDEX_API_URL
    }/authorize?response_type=token&client_id=${
      import.meta.env.VITE_YANDEX_CLIENT_ID
    }`
  );
}