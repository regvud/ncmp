import { CommentType } from "../types/contentTypes";

interface CommentComponentProps {
  comment: CommentType;
}

export const CommentComponent = ({ comment }: CommentComponentProps) => {
  return (
    <div>
      <h2>{comment.body}</h2>
    </div>
  );
};
