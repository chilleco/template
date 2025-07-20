import { CheckCircle } from "lucide-react";

export function SuccessToast({ email }: { email: string }) {
  return (
    <div className="flex items-center gap-2">
      <CheckCircle className="h-5 w-5 text-green-600" />
      <span>User {email} created!</span>
    </div>
  );
}
