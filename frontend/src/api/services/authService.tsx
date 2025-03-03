import { AxiosResponse } from "axios";
import { axiosClient } from "../client/axiosClient";
import { LoginUserInterface, RegisterUserInterface } from "../schemas/auth";
import { OAuthServices } from "../../utils/enums";



export default class AuthService {
    public BASE_URL = "/auth";

    public async loginUser(loginData: LoginUserInterface, code: string): Promise<AxiosResponse> {
        return axiosClient.post(`${this.BASE_URL}/login`, loginData, { params: { code: code } });
    }

    public async authWithOAuth(service: OAuthServices): Promise<void> {
        let url: string = ""
        if (service === OAuthServices.YANDEX) {
            url = `${import.meta.env.VITE_YANDEX_API_URL}/authorize?response_type=token&client_id=${import.meta.env.VITE_YANDEX_CLIENT_ID}`;

        } else if (service === OAuthServices.VK) { 
            url = `${import.meta.env.VITE_VK_API_URL}?client_id=${import.meta.env.VITE_VK_APP_ID}`
            + `&display=popup`
            + `&redirect_uri=${encodeURIComponent(import.meta.env.VITE_REDIRECT_URI + '/auth/callback')}`
            + `&response_type=code`
            + `&v=5.131`
        } else if (service === OAuthServices.GITHUB) {
            url = `${import.meta.env.VITE_GITHUB_OAUTH_URL}/authorize?client_id=${import.meta.env.VITE_GITHUB_CLIENT_ID}`
            + `&redirect_uri=${encodeURIComponent(import.meta.env.VITE_BASE_API_URL + '/auth/callback?service=github')}`
        }
        window.location.assign(url)
    }

    public async registerUser(registerData: RegisterUserInterface, code: string): Promise<AxiosResponse> {
        return axiosClient.post(`${this.BASE_URL}/register`, registerData, { params: { code: code } });
    }

    public async authWithGithub(code: string): Promise<AxiosResponse> {
        return axiosClient.post(`${this.BASE_URL}/github`, {}, { params: { code: code } });
    }

    public async authWithVk(code: string): Promise<AxiosResponse> {
        return axiosClient.post(`${this.BASE_URL}/vk`, {}, { params: { code: code } });
    }

    public async authWithYandex(code: string): Promise<AxiosResponse> {
        return axiosClient.post(`${this.BASE_URL}/yandex`, {}, { params: { access_token: code } });
    }

    public async checkUserExist(
        userForm: RegisterUserInterface | LoginUserInterface, isRegister: boolean
    ): Promise<AxiosResponse> {
        return axiosClient.post(
            `${this.BASE_URL}/check-exist`,
            userForm,
            {
                params: { is_register: isRegister }
            });
    }

    public async getCurrentUser(): Promise<AxiosResponse> {
        return axiosClient.get(`${this.BASE_URL}/current_user`);
    }

    public async logoutUser(): Promise<AxiosResponse> {
        return axiosClient.delete(`${this.BASE_URL}/logout`);
    }

    public async refreshToken(): Promise<AxiosResponse> {
        return axiosClient.get(`${this.BASE_URL}/refresh`);
    }
}