import { useEffect } from "react";
import { NavigateFunction } from "react-router-dom";
import { AxiosResponse } from "axios";
import { BaseUserInterface } from "./interfaces";
import AuthService from "./service";

export default function useUserAuthCallback(
    searchParam: URLSearchParams, 
    navigate: NavigateFunction, 
    authService: AuthService, 
    setUser: React.Dispatch<React.SetStateAction<BaseUserInterface | null>> 
) {
    useEffect(() => {
        const code = searchParam.get("code");
        const service = searchParam.get("service");

        if (service === "yandex") {
            const hashParams = new URLSearchParams(window.location.hash.slice(1))
            const access_token =  hashParams.get("access_token")
            
            if (access_token) {
                authService.authWithYandex(access_token).then((response: AxiosResponse) => {
                    setUser(response.data)
                })
            }
        } else if (code) {
            authService.authWithVk(code).then((response: AxiosResponse) => {
                setUser(response.data)
            })
        } else {
            // navigate("/register")
        }
        // navigate("/")
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])
}