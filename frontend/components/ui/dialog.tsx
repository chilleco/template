export function Dialog({ children }: any) {
  return <div>{children}</div>;
}

export function DialogTrigger({ children }: any) {
  return <div>{children}</div>;
}

export function DialogContent({ children }: any) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg max-w-md w-full mx-4">
        {children}
      </div>
    </div>
  );
} 