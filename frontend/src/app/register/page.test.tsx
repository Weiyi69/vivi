import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import RegisterPage from "./page";

describe("RegisterPage", () => {
  it("renders accessible registration fields", () => {
    render(<RegisterPage />);
    expect(screen.getByRole("heading", { name: "Create your account" })).toBeInTheDocument();
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });
});
