import { useState } from "react";
import { CommentCounterType } from "../types/counterContentTypes";
import { ReplyMapper } from "./ReplyMapper";

interface CommentComponentProps {
  comment: CommentCounterType;
}

export const CommentComponent = ({ comment }: CommentComponentProps) => {
  const [toggleReplies, setToggleReplise] = useState(false);

  function clickReplies() {
    setToggleReplise((prev) => !prev);
  }

  return (
    <div className="border border-orange-500">
      <h2>{comment.body}</h2>
      <h2>liked: {comment.users_liked}</h2>
      <h2>replies: {comment.replies_count}</h2>
      <button onClick={clickReplies}>replies</button>
      {toggleReplies && <ReplyMapper replies={comment.replies} />}
    </div>
  );
};
