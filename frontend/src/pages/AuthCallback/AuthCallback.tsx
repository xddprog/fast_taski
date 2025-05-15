import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import AuthService from "../../api/services/authService";
import { BaseUserInterface } from "../../interfaces/authInterfaces";
import useUserAuthCallback from "./hook";

const AuthCallback: React.FC = () => {
  const navigate = useNavigate();
  const [searchParam] = useSearchParams();
  const authService = new AuthService();
  const [user, setUser] = useState<BaseUserInterface | null>(null);

  useUserAuthCallback(searchParam, navigate, authService, setUser);

  useSearchParams();
  return (
    <>
      <div>Авторизация...</div>
      {user && <div>Пользователь: {user.username}</div>}
    </>
  );
};

export default AuthCallback;
