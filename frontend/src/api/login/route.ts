interface LoginData {
  username: string | null;
  email: string;
  password: string;
}

interface LoginResponse {
  success: boolean;
  message?: string;
}

export async function loginUser(
  username: string | null,
  email: string,
  password: string
): Promise<LoginResponse> {
  const LoginData: LoginData = {
    username,
    email,
    password,
  };

  try {
    const response = await fetch("https://fasttaski.ru/api/v1/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(LoginData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || "Ошибка при регистрации");
    }

    return await response.json();
  } catch (error) {
    // Явно указываем, что error — это unknown, и обрабатываем его
    if (error instanceof Error) {
      throw new Error(error.message || "Неизвестная ошибка");
    }
    // Если это не Error, бросаем общую ошибку
    throw new Error("Неизвестная ошибка");
  }
}
