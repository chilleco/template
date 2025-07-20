"use client";

import * as React from "react";
import { Button as ShadButton, type ButtonProps } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

export interface AppButtonProps extends ButtonProps {
  loading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, AppButtonProps>(
  ({ loading, children, ...rest }, ref) => (
    <ShadButton ref={ref} disabled={loading || rest.disabled} {...rest}>
      {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {children}
    </ShadButton>
  ),
);
Button.displayName = "AppButton";
