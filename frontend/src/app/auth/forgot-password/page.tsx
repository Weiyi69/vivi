"use client";

import { useState } from "react";

import { AuthField } from "@/components/auth/AuthField";
import { AuthShell } from "@/components/auth/AuthShell";
import { AuthSubmit } from "@/components/auth/AuthSubmit";
import { apiMessage, apiRequest } from "@/lib/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setPending(true);
    const result = await apiRequest("/auth/password-reset/request", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
    setMessage(apiMessage(result.data, "Could not process the reset request"));
    setPending(false);
  }

  return (
    <AuthShell title="Forgot password" description="Request a secure password reset message.">
      <form className="space-y-4" onSubmit={submit}>
        <AuthField label="Email" name="email" type="email" value={email} onChange={setEmail} autoComplete="email" />
        {message && <p role="status" className="text-sm text-secondary">{message}</p>}
        <AuthSubmit pending={pending}>Send reset link</AuthSubmit>
      </form>
    </AuthShell>
  );
}
