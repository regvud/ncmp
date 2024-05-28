import { CommentCounterType } from "../types/counterContentTypes";
import { CommentComponent } from "./CommentComponent";

interface CommentMapperProps {
  comments: CommentCounterType[];
}

export const CommentMapper = ({ comments }: CommentMapperProps) => {
  return (
    <>
      {comments.map((comment) => (
        <CommentComponent comment={comment} key={comment.id} />
      ))}
    </>
  );
};
