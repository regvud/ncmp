import { PostImage, ReplyType } from "./contentTypes";

export type CommentCounterType = {
  body: string;
  id: number;
  post_id: number;
  user_id: number;
  replies_count: number;
  users_liked: number;
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
  users_liked: number;
  images: PostImage[] | [];
  comments: CommentCounterType[] | [];
  created_at: string | null;
  updated_at: string | null;
};
