// app/page.tsx
import SearchBar from '@/components/searchBar';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Joy of Painting Search</h1>
      <SearchBar />
    </div>
  );
}