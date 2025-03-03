import { Button, Typography } from "antd";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { BaseUserInterface } from "../../api/schemas/user";
import AuthService from "../../api/services/authService";
import { BaseContainer } from "../../components/styled/Container";


interface ComponentProps {
    user: BaseUserInterface | null,
}

export default function MainPage({ user }: ComponentProps): JSX.Element {
    const [appUser, setAppUser] = useState<BaseUserInterface | null>(null)
    const authService = new AuthService();
    const navigate = useNavigate();

    useEffect(() => {
        if (user) {
            setAppUser(user)
        } else {
            authService.getCurrentUser().then((res) => {
                setAppUser(res.data)
            }).catch(() => {
                navigate("/login")
            })
        }
    }, [])

    function logout() {
        authService.logoutUser().then(() => {
            navigate("/login")
        })
    }

    return (
        <Container>
            <Typography.Title level={2}>Добро пожаловать, {appUser?.username}</Typography.Title>
            <StyledButton type="primary" onClick={logout}>Выйти</StyledButton>
        </Container>
    );
}


const Container = styled(BaseContainer)`
    flex-direction: column;
`

const StyledButton = styled(Button)`
    box-shadow: none;
    width: 200px;
    height: 40px;
`;
