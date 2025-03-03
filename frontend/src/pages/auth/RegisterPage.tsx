import RegisterForm from "../../components/auth/RegisterForm"
import { AxiosError } from "axios"
import { BaseContainer } from "../../components/styled/Container"
import { BaseResponse } from "../../api/schemas/response"


interface ComponentProps {
    handleError: (error: AxiosError<BaseResponse>) => void
}


export default function RegisterPage({ handleError }: ComponentProps) {
    return (
        <BaseContainer>
            <RegisterForm handleError={handleError}/>
        </BaseContainer>
    )
}
    
