import { ReplyType, UserLikeType, CommentType, PostType } from "./contentTypes";

export type ReplyCounterType = ReplyType & {
  likes_count: number;
  users_liked: number[];
};

export type CommentCounterType = CommentType & {
  replies_count: number;
  likes_count: number;
  users_liked: number[];
  replies: ReplyCounterType[] | [];
};

export type PostCounterType = PostType & {
  comments_count: number;
  likes_count: number;
  users_liked: UserLikeType[];
  comments: CommentCounterType[] | [];
};
