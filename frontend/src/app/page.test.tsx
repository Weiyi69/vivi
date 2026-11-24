import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Home from "./page";

describe("Home", () => {
  it("renders the Vivi foundation shell", () => {
    render(<Home />);
    expect(screen.getByText("Vivi")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Your study workspace starts here." }),
    ).toBeInTheDocument();
  });
});
