export interface FormProps {
  title: string;
  formType?: string;
  login: string;
  pass?: string;
  passRep?: string;
  handleLogin?: (e: React.FormEvent<HTMLFormElement>) => void;
  handleRegistre?: (e: React.FormEvent<HTMLFormElement>) => void;
  handlePass?: (value: string) => void;
  handlePassRep?: (value: string) => void;
  handleEmail: (value: string) => void;
}
