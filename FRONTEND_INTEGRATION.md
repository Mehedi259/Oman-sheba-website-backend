# Frontend Integration Guide

## 🔗 Next.js Frontend থেকে Backend Connect করা

### 1. API Base URL Setup

আপনার Next.js frontend-এ একটা `.env.local` file তৈরি করুন:

```bash
# /Users/mehedihasanmridul/website/sheba-website/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 2. API Client Setup

একটা API client utility তৈরি করুন:

```typescript
// lib/api.ts or utils/api.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    credentials: 'include', // Important for session cookies
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}
```

### 3. Example Usage

#### Get Jobs List
```typescript
// app/classifieds/jobs/page.tsx
import { fetchAPI } from '@/lib/api';

export default async function JobsPage() {
  const data = await fetchAPI('/classifieds/jobs/');
  
  return (
    <div>
      <h1>Jobs ({data.count})</h1>
      {data.results.map((job: any) => (
        <div key={job.id}>
          <h2>{job.title}</h2>
          <p>{job.company_name}</p>
          <p>{job.location}</p>
        </div>
      ))}
    </div>
  );
}
```

#### Get Single Job
```typescript
const job = await fetchAPI(`/classifieds/jobs/${id}/`);
```

#### Create Job (with authentication)
```typescript
const newJob = await fetchAPI('/classifieds/jobs/', {
  method: 'POST',
  body: JSON.stringify({
    title: 'Software Engineer',
    company_name: 'Tech Co',
    job_type: 'full_time',
    // ... other fields
  }),
});
```

#### Search & Filter
```typescript
// Search jobs
const jobs = await fetchAPI('/classifieds/jobs/?search=engineer');

// Filter by type and location
const jobs = await fetchAPI('/classifieds/jobs/?job_type=full_time&location=Dhaka');

// Sort by price
const jobs = await fetchAPI('/classifieds/jobs/?ordering=-price');

// Pagination
const jobs = await fetchAPI('/classifieds/jobs/?page=2');
```

### 4. Authentication Example

```typescript
// Login
export async function login(username: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/users/login/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  
  return response.json();
}

// Register
export async function register(data: any) {
  const response = await fetch(`${API_BASE_URL}/users/register/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    throw new Error('Registration failed');
  }
  
  return response.json();
}

// Logout
export async function logout() {
  const response = await fetch(`${API_BASE_URL}/users/logout/`, {
    method: 'POST',
    credentials: 'include',
  });
  
  return response.ok;
}
```

### 5. React Query (Recommended)

আরো ভালো data fetching-এর জন্য React Query use করতে পারেন:

```bash
npm install @tanstack/react-query
```

```typescript
// hooks/useJobs.ts
import { useQuery } from '@tanstack/react-query';
import { fetchAPI } from '@/lib/api';

export function useJobs(filters?: any) {
  return useQuery({
    queryKey: ['jobs', filters],
    queryFn: () => {
      const params = new URLSearchParams(filters);
      return fetchAPI(`/classifieds/jobs/?${params}`);
    },
  });
}

// Usage in component
function JobsList() {
  const { data, isLoading, error } = useJobs({ job_type: 'full_time' });
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading jobs</div>;
  
  return (
    <div>
      {data.results.map((job: any) => (
        <JobCard key={job.id} job={job} />
      ))}
    </div>
  );
}
```

### 6. API Routes (Server-side)

Next.js API routes থেকেও call করতে পারেন:

```typescript
// app/api/jobs/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const response = await fetch('http://localhost:8000/api/classifieds/jobs/', {
    cache: 'no-store', // or 'force-cache' for caching
  });
  
  const data = await response.json();
  return NextResponse.json(data);
}
```

### 7. TypeScript Types

API responses-এর জন্য types define করুন:

```typescript
// types/api.ts

export interface Job {
  id: number;
  title: string;
  description: string;
  company_name: string;
  job_type: 'full_time' | 'part_time' | 'contract' | 'freelance';
  category: string;
  location: string;
  price?: number;
  salary_range?: string;
  experience_required?: string;
  deadline?: string;
  status: 'active' | 'sold' | 'expired' | 'deleted';
  views: number;
  user: number;
  user_name: string;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface Property {
  id: number;
  title: string;
  description: string;
  property_type: 'apartment' | 'house' | 'commercial' | 'land';
  listing_type: 'sale' | 'rent';
  price: number;
  location: string;
  bedrooms?: number;
  bathrooms?: number;
  area_sqft?: number;
  // ... other fields
}

// Similar interfaces for Vehicle, Service, News, etc.
```

### 8. Error Handling

```typescript
export class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new APIError(
        response.status,
        error.detail || error.error || response.statusText
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new Error('Network error: Unable to connect to API');
  }
}
```

### 9. Environment Variables

Different environments-এর জন্য:

```bash
# .env.local (development)
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# .env.production (production)
NEXT_PUBLIC_API_URL=https://api.sheba.com/api
```

### 10. CORS Configuration

Backend already configured আছে `http://localhost:3000` এর জন্য। 

যদি অন্য port use করো, তাহলে backend-এ update করতে হবে:

```python
# sheba_backend/settings.py
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001',  # Add your port
]
```

---

## 🚀 Quick Start

1. Backend running করো: `python manage.py runserver`
2. Frontend-এ `.env.local` file তৈরি করো
3. API client setup করো
4. Start fetching data!

## 📚 Complete API Documentation

বিস্তারিত endpoint documentation-এর জন্য দেখো:
- [API_ENDPOINTS.md](./API_ENDPOINTS.md)
- Swagger UI: http://localhost:8000/swagger/
