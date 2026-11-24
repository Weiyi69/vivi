"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { AuthField } from "@/components/auth/AuthField";
import { AuthShell } from "@/components/auth/AuthShell";
import { AuthSubmit } from "@/components/auth/AuthSubmit";
import { apiMessage, apiRequest } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setPending(true);
    setMessage("");
    const result = await apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    if (result.status === 200) {
      router.push("/profile");
      return;
    }
    setMessage(apiMessage(result.data, "Login failed"));
    setPending(false);
  }

  return (
    <AuthShell title="Welcome back" description="Sign in to continue to Vivi.">
      <form className="space-y-4" onSubmit={submit}>
        <AuthField label="Email" name="email" type="email" value={email} onChange={setEmail} autoComplete="email" />
        <AuthField label="Password" name="password" type="password" value={password} onChange={setPassword} autoComplete="current-password" />
        {message && <p role="alert" className="text-sm text-secondary">{message}</p>}
        <AuthSubmit pending={pending}>Sign in</AuthSubmit>
      </form>
    </AuthShell>
  );
}
