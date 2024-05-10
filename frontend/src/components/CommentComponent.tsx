import { useState } from "react";
import { CommentType } from "../types/contentTypes";
import { ReplyMapper } from "./ReplyMapper";

interface CommentComponentProps {
  comment: CommentType;
}

export const CommentComponent = ({ comment }: CommentComponentProps) => {
  const [toggleReplies, setToggleReplise] = useState(false);

  function clickReplies() {
    setToggleReplise((prev) => !prev);
  }

  return (
    <div>
      <h2>{comment.body}</h2>
      <button onClick={clickReplies}>replies</button>
      {toggleReplies && <ReplyMapper replies={comment.replies} />}
    </div>
  );
};
