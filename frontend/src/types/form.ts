export interface FormProps {
  title: string;
  formType?: string;
  login: string;
  pass?: string;
  passRep?: string;
  handleLogin?: () => void;
  handleRegistre?: () => void;
  handlePass?: (value: string) => void;
  handlePassRep?: (value: string) => void;
  handleEmail: (value: string) => void;
}
