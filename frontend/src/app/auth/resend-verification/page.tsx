"use client";

import { useState } from "react";

import { AuthField } from "@/components/auth/AuthField";
import { AuthShell } from "@/components/auth/AuthShell";
import { AuthSubmit } from "@/components/auth/AuthSubmit";
import { apiMessage, apiRequest } from "@/lib/api";

export default function ResendVerificationPage() {
  const [email, setEmail] = useState("");
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setPending(true);
    const result = await apiRequest("/auth/resend-verification", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
    setMessage(apiMessage(result.data, "Could not resend verification"));
    setPending(false);
  }

  return (
    <AuthShell title="Resend verification" description="Request another account verification message.">
      <form className="space-y-4" onSubmit={submit}>
        <AuthField label="Email" name="email" type="email" value={email} onChange={setEmail} autoComplete="email" />
        {message && <p role="status" className="text-sm text-secondary">{message}</p>}
        <AuthSubmit pending={pending}>Send verification</AuthSubmit>
      </form>
    </AuthShell>
  );
}
