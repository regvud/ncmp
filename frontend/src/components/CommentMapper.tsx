import { CommentType } from "../types/contentTypes";
import { CommentComponent } from "./CommentComponent";

interface CommentMapperProps {
  comments: CommentType[];
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
