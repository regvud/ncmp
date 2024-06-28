import { ReplyCounterType } from "../types/counterContentTypes";

interface ReplyComponentProps {
  reply: ReplyCounterType;
}

export const ReplyComponent = ({ reply }: ReplyComponentProps) => {
  return (
    <div>
      <h1>{reply.body}</h1>
      <h1>likes: {reply.likes_count}</h1>
    </div>
  );
};
