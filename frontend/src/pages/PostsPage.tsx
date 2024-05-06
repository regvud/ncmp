import { useEffect } from "react";
import { postService } from "../services/postService";

export const PostPage = () => {
  useEffect(() => {
    postService.getAll().then(({ data }) => console.log(data));
  }, []);

  return <h1>PostPage</h1>;
};
