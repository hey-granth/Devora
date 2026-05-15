import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';

export default function RootPage() {
  const cookieStore = cookies();
  const hasRefreshToken = cookieStore.has('refresh_token');

  if (hasRefreshToken) {
    redirect('/dashboard');
  }

  redirect('/login');
}
