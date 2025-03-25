interface RegisterData {
  username: string;
  email: string;
  password: string;
}

interface RegisterResponse {
  success: boolean;
  message?: string;
}

export async function registerUser(
  username: string,
  email: string,
  password: string
): Promise<RegisterResponse> {
  const registerData: RegisterData = {
    username,
    email,
    password,
  };

  try {
    console.log(JSON.stringify(registerData));
    const response = await fetch("https://fasttaski.ru/api/v1/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(registerData),
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
