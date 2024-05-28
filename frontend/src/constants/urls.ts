export const baseURL = "http://localhost:8000";

export const urls = {
  posts: {
    base: (page: number) => `/posts?page=${page}`,
  },
};
