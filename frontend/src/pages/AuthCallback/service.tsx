import { AxiosResponse } from "axios";
import { axiosClient } from "./api";
import { LoginUserInterface, RegisterUserInterface } from "./interfaces";




export default class AuthService {
    public BASE_URL = "/auth";

    public async loginUser(loginData: LoginUserInterface, code: string): Promise<AxiosResponse> {
        return axiosClient.post(`${this.BASE_URL}/login`, loginData, {params: {code: code}});
    }

    public async registerUser(registerData: RegisterUserInterface, code: string): Promise<AxiosResponse> {
        return axiosClient.post(`${this.BASE_URL}/register`, registerData, {params: {code: code}});
    }
    
    public async authWithVk(code: string): Promise<AxiosResponse> {
        return axiosClient.post(`${this.BASE_URL}/vk`, {}, {params: {code: code}});
    }

    public async authWithYandex(code: string): Promise<AxiosResponse> {
        return axiosClient.post(`${this.BASE_URL}/yandex`, {}, {params: {access_token: code}});
    }

    public async checkUserExist(
        userForm: RegisterUserInterface | LoginUserInterface, isRegister: boolean
    ): Promise<AxiosResponse> {
        return axiosClient.post(
            `${this.BASE_URL}/check-exist`, 
            userForm, 
            {params: {is_register: isRegister}
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