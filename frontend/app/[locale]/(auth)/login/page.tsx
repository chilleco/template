import { LoginForm } from '@/features/auth/components/login-form';

export default function LoginPage() {
  return (
    <section className="mx-auto flex min-h-[60vh] w-full max-w-4xl items-center justify-center px-6 py-12">
      <LoginForm />
    </section>
  );
}
