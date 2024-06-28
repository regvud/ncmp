import { ReplyType } from "../types/contentTypes";
import { ReplyCounterType } from "../types/counterContentTypes";
import { ReplyComponent } from "./ReplyComponent";

interface ReplyMapperProps {
  replies: ReplyCounterType[];
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
