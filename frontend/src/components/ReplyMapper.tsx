import { ReplyType } from "../types/contentTypes";
import { ReplyComponent } from "./ReplyComponent";

interface ReplyMapperProps {
  replies: ReplyType[];
}
export const ReplyMapper = ({ replies }: ReplyMapperProps) => {
  return (
    <>
      {replies.map((reply) => (
        <ReplyComponent reply={reply} key={reply.id} />
      ))}
    </>
  );
};
