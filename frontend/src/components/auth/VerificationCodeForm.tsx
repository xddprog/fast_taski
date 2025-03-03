import { Button, Form, Input, Typography } from "antd";
import { AxiosError } from "axios";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { LoginUserInterface, RegisterUserInterface } from '../../api/schemas/auth';
import { BaseUserInterface } from "../../api/schemas/user";
import AuthService from "../../api/services/authService";
import { BaseContainer } from "../styled/Container";
import { BaseResponse } from "../../api/schemas/response";


interface ComponentProps {
    setUser: React.Dispatch<React.SetStateAction<BaseUserInterface | null>>,
    userForm: RegisterUserInterface | LoginUserInterface,
    handleError: (error: AxiosError<BaseResponse>) => void
}


export default function VerificationCodeForm({ setUser, userForm, handleError }: ComponentProps) {
    const [form] = Form.useForm();
    const authService = new AuthService();
    const navigate = useNavigate()

    async function verifyUser() {
        const values = await form.validateFields()
        const code = Object.values(values).join('')

        if ('username' in userForm) {
            authService.registerUser(
                userForm as RegisterUserInterface, code
            ).then(res => {
                setUser(res.data)
                navigate("/")
            }).catch(
                (error) => handleError(error)
            );
        } else {
            authService.loginUser(
                userForm as LoginUserInterface, code
            ).then(res => {
                setUser(res.data)
                navigate("/")
            }).catch(
                (error) => handleError(error)
            );
        }
    }

    return (
        <Container>
            <TextsContainer>
                <Typography.Title style={{ margin: 0 }}>Верификация</Typography.Title>
                <Typography.Paragraph>Пожалуйста, проверьте вашу почту</Typography.Paragraph>
            </TextsContainer>
            <StyledForm form={form}>
                <StyledFormItem name="first">
                    <StyledInput maxLength={1} />
                </StyledFormItem>
                <StyledFormItem name="second">
                    <StyledInput maxLength={1} />
                </StyledFormItem>
                <StyledFormItem name="third">
                    <StyledInput maxLength={1} />
                </StyledFormItem>
                <StyledFormItem name="fourth">
                    <StyledInput maxLength={1} />
                </StyledFormItem>
                <StyledFormItem name="fifth">
                    <StyledInput maxLength={1} />
                </StyledFormItem>
                <StyledFormItem name="sixth">
                    <StyledInput maxLength={1} />
                </StyledFormItem>
            </StyledForm>
            <StyledButton type="primary" onClick={verifyUser}>Подтвердить</StyledButton>
        </Container>
    )
}


const StyledInput = styled(Input)`
    width: 45px;
    height: 45px;
    text-align: center;
    font-size: 24px;
    font-weight: 300;
    color: #8762bf;
`;

const StyledFormItem = styled(Form.Item)`
    margin: 0;
`;

const Container = styled(BaseContainer)`
    width: 300px;
    background: #171818;
    border-radius: 10px;
    padding: 40px 20px;
`;

const TextsContainer = styled(Container)`
    width: 100%;
    padding: 0;
`

const StyledForm = styled(Form)`
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin-top: 10px;
    gap: 5px;
`

const StyledButton = styled(Button)`
    margin-top: 24px;
    box-shadow: none;
    width: 100%;
    height: 40px;
`;