import { useState } from "react";
import { PostCounterType } from "../types/counterContentTypes";
import { CommentMapper } from "./CommentMapper";
import { ModalImage } from "./modal/ModalImage";

interface PostComponentProps {
  post: PostCounterType;
}

export const PostComponent = ({ post }: PostComponentProps) => {
  const [toggleComments, setToggleComments] = useState(false);
  const [imagePage, setImagePage] = useState(0);

  const imagesLength = post.images.length;

  function clickComments() {
    setToggleComments((prev) => !prev);
  }

  function checkIfLastPage() {
    if (imagePage === imagesLength - 1) {
      setImagePage(0);
      return 1;
    }
    return 0;
  }

  function checkIfFirstPage() {
    if (imagePage === 0) {
      setImagePage(imagesLength - 1);
      return 1;
    }
    return 0;
  }

  function nextImage() {
    const isLastPage = checkIfLastPage();
    if (!isLastPage) {
      setImagePage(imagePage + 1);
    }
  }

  function prevImage() {
    const isFirstPage = checkIfFirstPage();
    if (!isFirstPage) {
      setImagePage(imagePage - 1);
    }
  }

  return (
    <div className="border border-sky-500">
      <h1 className="text-slate-400">{post.title}</h1>
      <h2>{post.body}</h2>
      <h2>user liked: {post.users_liked}</h2>
      <h2>comments: {post.comments_count}</h2>
      {imagesLength > 0 && (
        <div className="flex justify-between w-[50%] h-[50%]">
          {imagesLength > 1 && <button onClick={prevImage}>prev image</button>}
          <ModalImage
            images={post.images}
            imagePage={imagePage}
            nextImage={nextImage}
            prevImage={prevImage}
          />
          {imagesLength > 1 && <button onClick={nextImage}>next image</button>}
        </div>
      )}
      <button onClick={clickComments}>Comments</button>
      {toggleComments && <CommentMapper comments={post.comments} />}
    </div>
  );
};
