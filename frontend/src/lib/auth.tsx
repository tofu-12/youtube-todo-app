"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { usePathname, useRouter } from "next/navigation";

interface AuthContextValue {
  userId: string | null;
  email: string | null;
  login: (userId: string, email: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue>({
  userId: null,
  email: null,
  login: () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [userId, setUserId] = useState<string | null>(null);
  const [email, setEmail] = useState<string | null>(null);
  const [checked, setChecked] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const storedId = localStorage.getItem("user_id");
    const storedEmail = localStorage.getItem("user_email");
    if (storedId && storedEmail) {
      setUserId(storedId);
      setEmail(storedEmail);
    } else if (pathname !== "/auth") {
      router.replace("/auth");
    }
    setChecked(true);
  }, [pathname, router]);

  const login = useCallback(
    (newUserId: string, newEmail: string) => {
      localStorage.setItem("user_id", newUserId);
      localStorage.setItem("user_email", newEmail);
      setUserId(newUserId);
      setEmail(newEmail);
      router.replace("/");
    },
    [router]
  );

  const logout = useCallback(() => {
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_email");
    setUserId(null);
    setEmail(null);
    router.replace("/auth");
  }, [router]);

  if (!checked) {
    return null;
  }

  return (
    <AuthContext.Provider value={{ userId, email, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
