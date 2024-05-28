export type Paginated<T> = {
  items: T[];
  pages: number;
  page: number;
  size: number;
};
