import { ReplyType } from "../types/contentTypes";

interface ReplyComponentProps {
  reply: ReplyType;
}

export const ReplyComponent = ({ reply }: ReplyComponentProps) => {
  return (
    <div>
      <h1>{reply.body}</h1>
    </div>
  );
};
