"use client";

import { useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";

import { AuthField } from "@/components/auth/AuthField";
import { AuthShell } from "@/components/auth/AuthShell";
import { AuthSubmit } from "@/components/auth/AuthSubmit";
import { apiMessage, apiRequest } from "@/lib/api";

function ResetPasswordForm() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") ?? "";
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setPending(true);
    if (password !== confirmation) {
      setMessage("Passwords do not match");
      setPending(false);
      return;
    }

    const result = await apiRequest("/auth/password-reset/confirm", {
      method: "POST",
      body: JSON.stringify({
        token,
        password,
        password_confirmation: confirmation,
      }),
    });
    setMessage(apiMessage(result.data, "Password reset failed"));
    setPending(false);
  }

  return (
    <AuthShell title="Reset password" description="Choose a new password for your account.">
      <form className="space-y-4" onSubmit={submit}>
        {!token && <p role="alert" className="text-sm text-secondary">The reset link is missing or invalid.</p>}
        <AuthField label="New password" name="password" type="password" value={password} onChange={setPassword} autoComplete="new-password" />
        <AuthField label="Confirm password" name="confirmation" type="password" value={confirmation} onChange={setConfirmation} autoComplete="new-password" />
        {message && <p role="alert" className="text-sm text-secondary">{message}</p>}
        <AuthSubmit pending={pending}>Reset password</AuthSubmit>
      </form>
    </AuthShell>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<p className="p-8 text-secondary">Loading reset form...</p>}>
      <ResetPasswordForm />
    </Suspense>
  );
}
