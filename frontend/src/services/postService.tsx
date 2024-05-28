import { urls } from "../constants/urls";
import { Paginated } from "../types/axiosTypes";
import { PostCounterType } from "../types/counterContentTypes";
import { apiService } from "./apiService";

export const postService = {
  getAll: (page: number) =>
    apiService.get<Paginated<PostCounterType>>(urls.posts.base(page)),
};
