import LoginForm from "../../components/auth/LoginForm";
import { AxiosError } from "axios";
import { BaseContainer } from "../../components/styled/Container";
import { BaseResponse } from "../../api/schemas/response";


interface ComponentProps {
    handleError: (error: AxiosError<BaseResponse>) => void
}


export default function LoginPage({ handleError }: ComponentProps) {
    return (
        <BaseContainer>
            <LoginForm handleError={handleError}/>
        </BaseContainer>
    );
}
