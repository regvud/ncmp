import { useState } from "react";
import { PostType } from "../types/contentTypes";
import { CommentMapper } from "./CommentMapper";

interface PostComponentProps {
  post: PostType;
}

export const PostComponent = ({ post }: PostComponentProps) => {
  const [toggleComments, setToggleComments] = useState(false);

  function clickComments() {
    setToggleComments((prev) => !prev);
  }

  return (
    <div className="bg-white border border-black-500">
      <h1>{post.title}</h1>
      <h1>{post.body}</h1>
      <button className="cover-pointer" onClick={clickComments}>
        Comments
      </button>
      {toggleComments && <CommentMapper comments={post.comments} />}
    </div>
  );
};
