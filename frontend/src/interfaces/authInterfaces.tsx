export interface LoginUserInterface {
  email: string;
  password: string;
}

export interface RegisterUserInterface extends LoginUserInterface {
  username: string;
  password_repeat?: string;
}

export interface BaseUserInterface {
  id: number;
  username: string;
}
