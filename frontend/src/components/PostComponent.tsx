import { useState } from "react";
import { baseURL } from "../constants/urls";
import { PostType } from "../types/contentTypes";
import { CommentMapper } from "./CommentMapper";
import { ModalImage } from "./ModalImage";

interface PostComponentProps {
  post: PostType;
}

export const PostComponent = ({ post }: PostComponentProps) => {
  const [toggleComments, setToggleComments] = useState(false);
  const [imagePage, setImagePage] = useState(0);

  const imagesLength = post.images.length;

  const imagePath = post.images[0]
    ? `${baseURL}${post.images[imagePage].path}`
    : "";

  function clickComments() {
    setToggleComments((prev) => !prev);
  }

  function scrollImage() {
    if (imagePage === imagesLength - 1) {
      setImagePage(0);
      return;
    }

    setImagePage(imagePage + 1);
  }

  return (
    <div>
      <h1 className="text-slate-400">{post.title}</h1>
      <h2>{post.body}</h2>
      {imagesLength > 0 && (
        <div>
          <ModalImage imagePath={imagePath} />
          {imagesLength > 1 && (
            <button onClick={scrollImage}>next image</button>
          )}
        </div>
      )}
      <button onClick={clickComments}>Comments</button>
      {toggleComments && <CommentMapper comments={post.comments} />}
    </div>
  );
};
