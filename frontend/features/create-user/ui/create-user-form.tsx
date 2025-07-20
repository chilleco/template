"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { CreateUserForm, createUserFormSchema } from "../model";
import { createUser } from "../api";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/shared/ui/button";
import { toast } from "sonner";
import { SuccessToast } from "./success-toast";

export function CreateUserFormCard() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const { register, handleSubmit, formState } = useForm<CreateUserForm>({
    resolver: zodResolver(createUserFormSchema),
  });

  async function onSubmit(data: CreateUserForm) {
    setLoading(true);
    try {
      await createUser(data);
      toast.custom(<SuccessToast email={data.email} />, { duration: 5000 });
      router.push("/dashboard/users");
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card className="w-full max-w-lg">
      <CardHeader>
        <CardTitle>Create user</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="grid gap-4">
          <div className="grid gap-1">
            <Label htmlFor="name">Name</Label>
            <Input id="name" {...register("name")} />
            {formState.errors.name && (
              <p className="text-destructive text-sm">
                {formState.errors.name.message}
              </p>
            )}
          </div>

          <div className="grid gap-1">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" {...register("email")} />
            {formState.errors.email && (
              <p className="text-destructive text-sm">
                {formState.errors.email.message}
              </p>
            )}
          </div>

          <div className="grid gap-1">
            <Label htmlFor="password">Password</Label>
            <Input id="password" type="password" {...register("password")} />
            {formState.errors.password && (
              <p className="text-destructive text-sm">
                {formState.errors.password.message}
              </p>
            )}
          </div>

          <Button type="submit" loading={loading}>
            {loading ? "Creating…" : "Create"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
