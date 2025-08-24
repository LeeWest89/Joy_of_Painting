// components/SearchBar.tsx
'use client';

import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import debounce from 'lodash/debounce';
import episodeData from '../../episodeData.json';

// Define the type for the raw JSON data
interface RawPainting {
  [key: string]: string;
}

// Define the processed painting type with boolean feature flags
interface Painting {
  id: string;
  painting_title: string;
  season: string;
  episode: string;
  painting_index: string;
  img_src: string;
  youtube_src: string;
  num_colors: string;
  colors: string;
  color_hex: string;
  EPISODE: string;
  TITLE: string;
  Episode_TITLE: string;
  Month: string;
  Day: string;
  Year: string;
  Black_Gesso: boolean;
  Bright_Red: boolean;
  Burnt_Umber: boolean;
  Cadmium_Yellow: boolean;
  Dark_Sienna: boolean;
  Indian_Red: boolean;
  Indian_Yellow: boolean;
  Liquid_Black: boolean;
  Liquid_Clear: boolean;
  Midnight_Black: boolean;
  Phthalo_Blue: boolean;
  Phthalo_Green: boolean;
  Prussian_Blue: boolean;
  Sap_Green: boolean;
  Titanium_White: boolean;
  Van_Dyke_Brown: boolean;
  Yellow_Ochre: boolean;
  Alizarin_Crimson: boolean;
  APPLE_FRAME: boolean;
  AURORA_BOREALIS: boolean;
  BARN: boolean;
  BEACH: boolean;
  BOAT: boolean;
  BRIDGE: boolean;
  BUILDING: boolean;
  BUSHES: boolean;
  CABIN: boolean;
  CACTUS: boolean;
  CIRCLE_FRAME: boolean;
  CIRRUS: boolean;
  CLIFF: boolean;
  CLOUDS: boolean;
  CONIFER: boolean;
  CUMULUS: boolean;
  DECIDUOUS: boolean;
  DIANE_ANDRE: boolean;
  DOCK: boolean;
  DOUBLE_OVAL_FRAME: boolean;
  FARM: boolean;
  FENCE: boolean;
  FIRE: boolean;
  FLORIDA_FRAME: boolean;
  FLOWERS: boolean;
  FOG: boolean;
  FRAMED: boolean;
  GRASS: boolean;
  GUEST: boolean;
  HALF_CIRCLE_FRAME: boolean;
  HALF_OVAL_FRAME: boolean;
  HILLS: boolean;
  LAKE: boolean;
  LAKES: boolean;
  LIGHTHOUSE: boolean;
  MILL: boolean;
  MOON: boolean;
  MOUNTAIN: boolean;
  MOUNTAINS: boolean;
  NIGHT: boolean;
  OCEAN: boolean;
  OVAL_FRAME: boolean;
  PALM_TREES: boolean;
  PATH: boolean;
  PERSON: boolean;
  PORTRAIT: boolean;
  RECTANGLE_3D_FRAME: boolean;
  RECTANGULAR_FRAME: boolean;
  RIVER: boolean;
  ROCKS: boolean;
  SEASHELL_FRAME: boolean;
  SNOW: boolean;
  SNOWY_MOUNTAIN: boolean;
  SPLIT_FRAME: boolean;
  STEVE_ROSS: boolean;
  STRUCTURE: boolean;
  SUN: boolean;
  TOMB_FRAME: boolean;
  TREE: boolean;
  TREES: boolean;
  TRIPLE_FRAME: boolean;
  WATERFALL: boolean;
  WAVES: boolean;
  WINDMILL: boolean;
  WINDOW_FRAME: boolean;
  WINTER: boolean;
  WOOD_FRAMED: boolean;
  [key: string]: string | boolean;
}

// List of feature flags to convert to booleans
const featureFlags = [
  'Black_Gesso',
  'Bright_Red',
  'Burnt_Umber',
  'Cadmium_Yellow',
  'Dark_Sienna',
  'Indian_Red',
  'Indian_Yellow',
  'Liquid_Black',
  'Liquid_Clear',
  'Midnight_Black',
  'Phthalo_Blue',
  'Phthalo_Green',
  'Prussian_Blue',
  'Sap_Green',
  'Titanium_White',
  'Van_Dyke_Brown',
  'Yellow_Ochre',
  'Alizarin_Crimson',
  'APPLE_FRAME',
  'AURORA_BOREALIS',
  'BARN',
  'BEACH',
  'BOAT',
  'BRIDGE',
  'BUILDING',
  'BUSHES',
  'CABIN',
  'CACTUS',
  'CIRCLE_FRAME',
  'CIRRUS',
  'CLIFF',
  'CLOUDS',
  'CONIFER',
  'CUMULUS',
  'DECIDUOUS',
  'DIANE_ANDRE',
  'DOCK',
  'DOUBLE_OVAL_FRAME',
  'FARM',
  'FENCE',
  'FIRE',
  'FLORIDA_FRAME',
  'FLOWERS',
  'FOG',
  'FRAMED',
  'GRASS',
  'GUEST',
  'HALF_CIRCLE_FRAME',
  'HALF_OVAL_FRAME',
  'HILLS',
  'LAKE',
  'LAKES',
  'LIGHTHOUSE',
  'MILL',
  'MOON',
  'MOUNTAIN',
  'MOUNTAINS',
  'NIGHT',
  'OCEAN',
  'OVAL_FRAME',
  'PALM_TREES',
  'PATH',
  'PERSON',
  'PORTRAIT',
  'RECTANGLE_3D_FRAME',
  'RECTANGULAR_FRAME',
  'RIVER',
  'ROCKS',
  'SEASHELL_FRAME',
  'SNOW',
  'SNOWY_MOUNTAIN',
  'SPLIT_FRAME',
  'STEVE_ROSS',
  'STRUCTURE',
  'SUN',
  'TOMB_FRAME',
  'TREE',
  'TREES',
  'TRIPLE_FRAME',
  'WATERFALL',
  'WAVES',
  'WINDMILL',
  'WINDOW_FRAME',
  'WINTER',
  'WOOD_FRAMED',
];

// Transform raw JSON data to convert "0"/"1" to booleans for feature flags
const paintings: Painting[] = (episodeData as RawPainting[]).map((item) => {
  const transformed: Painting = { ...item } as any;
  featureFlags.forEach((key) => {
    transformed[key] = item[key] === '1';
  });
  return transformed;
});

const SearchBar: React.FC = () => {
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<Painting[]>([]);
  const router = useRouter();

  // Debounced search function
  const handleSearch = useCallback(
    debounce((searchTerm: string) => {
      if (searchTerm.trim() === '') {
        setResults([]);
        return;
      }

      const lowerCaseQuery = searchTerm.toLowerCase();
      const filteredResults = paintings.filter((painting) => {
        // Check if query matches
        const matchesStringField = Object.entries(painting).some(([key, value]) => {
          if (typeof value === 'string') {
            return value.toLowerCase().includes(lowerCaseQuery);
          }
          return false;
        });

        // Check if query matches a feature flag
        const matchesFeature = featureFlags.some(
          (key) =>
            painting[key] === true && key.toLowerCase().includes(lowerCaseQuery)
        );

        return matchesStringField || matchesFeature;
      });
      setResults(filteredResults);
    }, 300),
    []
  );

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    handleSearch(value);
  };

  // Handle result click
  const handleResultClick = (id: string) => {
    router.push(`/painting/${id}`);
    setQuery('');
    setResults([]);
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query)}`);
      setQuery('');
      setResults([]);
    }
  };

  return (
    <div className="relative w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="relative">
        <input
          type="text"
          value={query}
          onChange={handleChange}
          placeholder="Search paintings, seasons, episodes, colors, features..."
          className="w-full px-4 py-2 text-gray-700 bg-white border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </button>
      </form>

      {results.length > 0 && (
        <ul className="absolute z-10 w-full mt-1 bg-white border rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {results.map((painting) => (
            <li
              key={painting.id}
              onClick={() => handleResultClick(painting.id)}
              className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
            >
              <div className="font-semibold">{painting.painting_title}</div>
              <div className="text-sm text-gray-600">
                Season {painting.season}, Episode {painting.episode}
              </div>
              <div className="text-sm text-gray-500">
                Features:{' '}
                {featureFlags
                  .filter((key) => painting[key] === true)
                  .map((key) => key.charAt(0) + key.slice(1).toLowerCase())
                  .join(', ')}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchBar;