"use client";

import { useEffect, useState } from "react";

import { AuthField } from "@/components/auth/AuthField";
import { AuthShell } from "@/components/auth/AuthShell";
import { AuthSubmit } from "@/components/auth/AuthSubmit";
import { apiMessage, apiRequest } from "@/lib/api";

export default function ProfilePage() {
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    void apiRequest("/auth/me").then((result) => {
      if (result.status === 200) {
        setDisplayName(String(result.data.display_name ?? ""));
        setEmail(String(result.data.email ?? ""));
      } else {
        setMessage(apiMessage(result.data, "Please sign in"));
      }
    });
  }, []);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setPending(true);
    const result = await apiRequest("/auth/me", {
      method: "PATCH",
      body: JSON.stringify({ display_name: displayName }),
    });
    setMessage(apiMessage(result.data, "Profile could not be updated"));
    setPending(false);
  }

  return (
    <AuthShell title="Profile" description="Manage your Vivi account details.">
      <form className="space-y-4" onSubmit={submit}>
        <div>
          <p className="text-sm text-secondary">Email</p>
          <p className="mt-1 text-primary">{email || "Not available"}</p>
        </div>
        <AuthField label="Display name" name="display-name" value={displayName} onChange={setDisplayName} autoComplete="name" />
        {message && <p role="status" className="text-sm text-secondary">{message}</p>}
        <AuthSubmit pending={pending}>Save profile</AuthSubmit>
      </form>
    </AuthShell>
  );
}
