/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_BASE_API_URL: string;
    readonly VITE_GITHUB_OAUTH_URL: string
    readonly VITE_GITHUB_CLIENT_ID: string
    readonly VITE_VK_API_URL: string
    readonly VITE_VK_APP_ID: string
    readonly VITE_VK_SECRET: string
    readonly VITE_REDIRECT_URI: string
    readonly VITE_YANDEX_API_URL: string
    readonly VITE_YANDEX_CLIENT_ID: string
}
  
interface ImportMeta {
    readonly env: ImportMetaEnv;
}
  