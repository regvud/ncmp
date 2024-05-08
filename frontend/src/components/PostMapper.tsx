import { PostType } from "../types/contentTypes";
import { PostComponent } from "./PostComponent";

interface PostMapperProps {
  posts: PostType[];
}

export const PostMapper = ({ posts }: PostMapperProps) => {
  return (
    <>
      {posts.map((post) => (
        <PostComponent post={post} key={post.id} />
      ))}
    </>
  );
};
