'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAuth } from '@/hooks/use-auth';

const schema = z.object({
  identifier: z.string().min(3),
  password: z.string().min(8)
});

type FormValues = z.infer<typeof schema>;

export function LoginForm() {
  const { login } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  const onSubmit = handleSubmit(async data => {
    await login.mutateAsync(data);
  });

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Sign in</CardTitle>
        <CardDescription>Authenticate with email, username, or phone — magic links and WebAuthn fit in the same flow.</CardDescription>
      </CardHeader>
      <form className="space-y-6" onSubmit={onSubmit}>
        <div className="space-y-2">
          <Label htmlFor="identifier">Email / Username / Phone</Label>
          <Input id="identifier" autoComplete="username" {...register('identifier')} />
          {errors.identifier ? <p className="text-sm text-red-500">{errors.identifier.message}</p> : null}
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input id="password" type="password" autoComplete="current-password" {...register('password')} />
          {errors.password ? <p className="text-sm text-red-500">{errors.password.message}</p> : null}
        </div>
        <Button type="submit" className="w-full" disabled={isSubmitting || login.isPending}>
          Continue
        </Button>
      </form>
    </Card>
  );
}
