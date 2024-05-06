import { urls } from "../constants/urls";
import { PostType } from "../types/contentTypes";
import { apiService } from "./apiService";

export const postService = {
  getAll: () => apiService.get<PostType[]>(urls.posts.base),
};
