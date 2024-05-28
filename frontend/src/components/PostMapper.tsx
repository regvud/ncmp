import { useInfiniteQuery } from "@tanstack/react-query";
import { postService } from "../services/postService";
import { PostCounterType } from "../types/counterContentTypes";
import { PostComponent } from "./PostComponent";

interface PostMapperProps {
  posts: PostCounterType[] | undefined;
}

export const PostMapper = ({ posts }: PostMapperProps) => {
  return (
    <>{posts?.map((post) => <PostComponent post={post} key={post.id} />)}</>
  );
};
