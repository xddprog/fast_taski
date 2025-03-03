import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { Form, Input, Typography } from "antd";
import { useForm } from "antd/es/form/Form";
import { AxiosError } from "axios";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { RegisterUserInterface } from "../../api/schemas/auth";
import AuthService from "../../api/services/authService";
import OauthServicesGroup from "./OauthServicesGroup";
import { BaseContainer } from "../styled/Container";
import { BaseResponse } from "../../api/schemas/response";


interface ComponentProps {
    handleError: (error: AxiosError<BaseResponse>) => void
}


export default function RegisterForm({ handleError }: ComponentProps) {
    const [form] = useForm<RegisterUserInterface>();
    const navigate = useNavigate();
    const authService = new AuthService();

    async function onFinish() {
        const userForm = await form.validateFields();
        await authService.checkUserExist(userForm, true).then(() => {
            navigate(
                "/verification",
                { state: { redirected: true, userForm: userForm } }
            )
        }).catch(
            (error) => handleError(error)
        );
    }

    return (
        <FormContainer>
            <Typography.Title level={1}>Регистрация</Typography.Title>
            <StyledForm
                name="normal_login"
                initialValues={{
                    remember: true,
                }}
                onFinish={onFinish}
                form={form}
            >
                <Form.Item
                    name="username"
                    hasFeedback
                    rules={[
                        {
                            required: true,
                            message: "Пожалуйста, введите свой никнейм!",
                        },
                    ]}
                >
                    <Input prefix={<MailOutlined />} placeholder="Username" size="large" />
                </Form.Item>
                <Form.Item
                    name="email"
                    hasFeedback
                    rules={[
                        {
                            required: true,
                            message: "Пожалуйста, введите свою почту!",
                            type: "email",
                        },
                    ]}
                >
                    <Input prefix={<MailOutlined />} type="email" placeholder="Почта" size="large" />
                </Form.Item>
                <Form.Item
                    name="password"
                    hasFeedback
                    rules={[
                        {
                            required: true,
                            message: "Пожалуйста, введите свой пароль!",
                        },
                    ]}
                >
                    <Input prefix={<LockOutlined />} type="password" placeholder="Пароль" size="large" />
                </Form.Item>
                <OauthServicesGroup isRegisterForm={true} />
            </StyledForm>
        </FormContainer>
    );
}

const StyledForm = styled(Form<RegisterUserInterface>)`
    width: 100%;
    margin-bottom: 10px;
`;


const FormContainer = styled(BaseContainer)`
    flex-direction: column;
    max-width: 300px;
    width: 100%;
`;

