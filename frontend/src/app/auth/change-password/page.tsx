"use client";

import { useState } from "react";

import { AuthField } from "@/components/auth/AuthField";
import { AuthShell } from "@/components/auth/AuthShell";
import { AuthSubmit } from "@/components/auth/AuthSubmit";
import { apiMessage, apiRequest } from "@/lib/api";

export default function ChangePasswordPage() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setPending(true);
    if (newPassword !== confirmation) {
      setMessage("Passwords do not match");
      setPending(false);
      return;
    }
    const result = await apiRequest("/auth/change-password", {
      method: "POST",
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword,
        new_password_confirmation: confirmation,
      }),
    });
    setMessage(apiMessage(result.data, "Password could not be changed"));
    setPending(false);
  }

  return (
    <AuthShell title="Change password" description="Update your password and revoke existing sessions.">
      <form className="space-y-4" onSubmit={submit}>
        <AuthField label="Current password" name="current-password" type="password" value={currentPassword} onChange={setCurrentPassword} autoComplete="current-password" />
        <AuthField label="New password" name="new-password" type="password" value={newPassword} onChange={setNewPassword} autoComplete="new-password" />
        <AuthField label="Confirm password" name="confirmation" type="password" value={confirmation} onChange={setConfirmation} autoComplete="new-password" />
        {message && <p role="status" className="text-sm text-secondary">{message}</p>}
        <AuthSubmit pending={pending}>Change password</AuthSubmit>
      </form>
    </AuthShell>
  );
}
