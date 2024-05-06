// {
//   "title": "new post",
//     "body": "post body",
//       "images": [],
//         "id": 6,
//           "user_id": 10,
//             "comments": [
//               {
//                 "body": "unsend me later",
//                 "id": 21,
//                 "post_id": 6,
//                 "user_id": 14,
//                 "replies": [
//                   {
//                     "body": "reply to unsend wtf",
//                     "id": 16,
//                     "to_user": 14,
//                     "user_id": 10,
//                     "created_at": "2024-05-06T16:39:19.487539+03:00",
//                     "updated_at": null
//                   },
//                 }
//                 },
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

export type PostType = {
  id: number;
  user_id: number;
  title: string;
  body: string;
  images: string[];
  comments: CommentType[] | [];
  created_at: string | null;
  updated_at: string | null;
};
