"use client";

import { useState } from "react";

import { AuthField } from "@/components/auth/AuthField";
import { AuthShell } from "@/components/auth/AuthShell";
import { AuthSubmit } from "@/components/auth/AuthSubmit";
import { apiMessage, apiRequest } from "@/lib/api";

export default function RegisterPage() {
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setPending(true);
    setMessage("");
    if (password !== confirmation) {
      setMessage("Passwords do not match");
      setPending(false);
      return;
    }
    const result = await apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        display_name: displayName,
        email,
        password,
        password_confirmation: confirmation,
      }),
    });
    setMessage(apiMessage(result.data, "Registration could not be completed"));
    setPending(false);
  }

  return (
    <AuthShell title="Create your account" description="Start organizing your studies with Vivi.">
      <form className="space-y-4" onSubmit={submit}>
        <AuthField label="Display name" name="display-name" value={displayName} onChange={setDisplayName} autoComplete="name" />
        <AuthField label="Email" name="email" type="email" value={email} onChange={setEmail} autoComplete="email" />
        <AuthField label="Password" name="password" type="password" value={password} onChange={setPassword} autoComplete="new-password" />
        <AuthField label="Confirm password" name="confirmation" type="password" value={confirmation} onChange={setConfirmation} autoComplete="new-password" />
        {message && <p role="alert" className="text-sm text-secondary">{message}</p>}
        <AuthSubmit pending={pending}>Create account</AuthSubmit>
      </form>
    </AuthShell>
  );
}
