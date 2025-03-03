import { AxiosError } from "axios";
import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { RegisterUserInterface } from "../../api/schemas/auth";
import { BaseUserInterface } from "../../api/schemas/user";
import VerificationCodeForm from "../../components/auth/VerificationCodeForm";
import { BaseContainer } from "../../components/styled/Container";
import { BaseResponse } from "../../api/schemas/response";


interface ComponentProps {
    setUser: React.Dispatch<React.SetStateAction<BaseUserInterface | null>>,
    handleError: (error: AxiosError<BaseResponse>) => void
}

export default function VerificationPage({ setUser, handleError }: ComponentProps) {
    const location = useLocation();
    const navigate = useNavigate()

    useEffect(() => {
        if (!location.state?.redirected) {
            navigate("/register")
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])


    return (
        <BaseContainer>
            <VerificationCodeForm
                setUser={setUser}
                userForm={location.state?.userForm as RegisterUserInterface}
                handleError={handleError}
            />
        </BaseContainer>
    );
}
