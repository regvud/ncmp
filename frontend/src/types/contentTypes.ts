export type UserLikeType = {
  userId: number;
  avatar: string;
};

export type ReplyType = {
  body: string;
  id: number;
  to_user: number;
  user_id: number;
  created_at: string | null;
  updated_at: string | null;
};

export type CommentType = {
  body: string;
  id: number;
  post_id: number;
  user_id: number;
  replies: ReplyType[] | [];
  created_at: string | null;
  updated_at: string | null;
};

export type PostImage = {
  id: number;
  post_id: number;
  path: string;
};

export type PostType = {
  id: number;
  user_id: number;
  title: string;
  body: string;
  images: PostImage[] | [];
  comments: CommentType[] | [];
  created_at: string | null;
  updated_at: string | null;
};
