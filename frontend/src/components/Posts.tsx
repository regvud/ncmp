import { useEffect, useState } from "react";
import { postService } from "../services/postService";
import { PostType } from "../types/contentTypes";
import { PostMapper } from "./PostMapper";

export const Posts = () => {
  const [posts, setPosts] = useState<PostType[] | []>([]);

  useEffect(() => {
    postService.getAll().then(({ data }) => setPosts(data));
  }, []);

  return (
    <>
      <PostMapper posts={posts} />
    </>
  );
};
