'use client';

import { useQuery } from '@tanstack/react-query';

import { endpoints } from '@/config/api';
import { apiClient } from '@/lib/api-client';
import { postSchema } from '@/lib/schemas/post';

export function usePosts() {
  return useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const response = await apiClient.get(endpoints.posts);
      return postSchema.array().parse(response.data);
    }
  });
}
