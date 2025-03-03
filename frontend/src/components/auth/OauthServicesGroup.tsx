import { Button, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import AuthService from '../../api/services/authService';
import { OAuthServices } from '../../utils/enums';


interface ComponentProps {
    isRegisterForm: boolean
}


export default function OauthServicesGroup ({isRegisterForm}: ComponentProps): JSX.Element {
    const navigate = useNavigate();
    const authServices: { name: OAuthServices, icon: string}[] = [
        { name: OAuthServices.YANDEX, icon: '/public/social/yandex.png', },
        { name: OAuthServices.VK, icon: '/public/social/vk.png'},
        { name: OAuthServices.GITHUB, icon: '/public/social/github.png'},
        { name: OAuthServices.TELEGRAM, icon: '/public/social/telegram.png' },
    ];
    const authService = new AuthService();

    function authWithOAuth(service: OAuthServices) {
        authService.authWithOAuth(service)
    }

    return (
        <ButtonsContiner>
            <StyledButton type="primary" htmlType="submit">
                {!isRegisterForm ? "Войти": "Зарегистрироваться"}
            </StyledButton>
            
            <ButtonsGrid>
            {authServices.map((service) => (
                <StyledButton key={service.name} onClick={() => authWithOAuth(service.name)}>
                    <StyledLinkButtonImage src={service.icon} />
                </StyledButton>
            ))}
            </ButtonsGrid>
            <LinksContainer>
                <LinksContinerItem>
                    <Typography.Paragraph style={{margin: 0}}>Забыли пароль?</Typography.Paragraph>
                    {isRegisterForm ? <a>Восстановить</a>: null}
                </LinksContinerItem>
                <LinksContinerItem>
                    <Typography.Paragraph>
                        {!isRegisterForm ? "Нет аккаунта?": "Есть аккаунт?"}
                        </Typography.Paragraph>
                    <a onClick={() => navigate(isRegisterForm ? "/login": "/register")}>
                        {isRegisterForm ? "Войти": "Зарегистрироваться"}
                    </a>
                </LinksContinerItem>
            </LinksContainer>
        </ButtonsContiner>
    )
}


const ButtonsContiner = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px
`;

const ButtonsGrid = styled.div`
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    width: 100%;
`;

const LinksContainer = styled.div`
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    align-items: center;
    width: 100%;
`;


const StyledButton = styled(Button)`
    box-shadow: none;
    width: 100%;
    height: 40px;
`;

const StyledLinkButtonImage = styled.img`
    width: 20px;
    height: 20px;
`;

const LinksContinerItem = styled.div`
    display: flex;
    gap: 5px;
`;