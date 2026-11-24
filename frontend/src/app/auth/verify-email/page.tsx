"use client";

import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";

import { AuthShell } from "@/components/auth/AuthShell";
import { apiMessage, apiRequest } from "@/lib/api";

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const [message, setMessage] = useState("Verifying...");

  useEffect(() => {
    if (!token) {
      void Promise.resolve().then(() =>
        setMessage("The verification link is missing or invalid."),
      );
      return;
    }
    void apiRequest("/auth/verify-email", {
      method: "POST",
      body: JSON.stringify({ token }),
    }).then((result) => setMessage(apiMessage(result.data, "Verification failed")));
  }, [token]);

  return (
    <AuthShell title="Email verification" description="Confirming your Vivi account.">
      <p role="status" className="text-sm text-secondary">{message}</p>
    </AuthShell>
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={<p className="p-8 text-secondary">Verifying...</p>}>
      <VerifyEmailContent />
    </Suspense>
  );
}
