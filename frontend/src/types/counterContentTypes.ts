import { PostImage, ReplyType, UserLikeType } from "./contentTypes";

export type CommentCounterType = {
  body: string;
  id: number;
  post_id: number;
  user_id: number;
  replies_count: number;
  likes_count: number;
  users_liked: number[];
  replies: ReplyType[] | [];
  created_at: string | null;
  updated_at: string | null;
};

export type PostCounterType = {
  id: number;
  user_id: number;
  title: string;
  body: string;
  comments_count: number;
  likes_count: number;
  users_liked: UserLikeType[];
  images: PostImage[] | [];
  comments: CommentCounterType[] | [];
  created_at: string | null;
  updated_at: string | null;
};
