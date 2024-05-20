import { useState } from "react";
import { PostType } from "../types/contentTypes";
import { CommentMapper } from "./CommentMapper";
import { ModalImage } from "./modal/ModalImage";

interface PostComponentProps {
  post: PostType;
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
    <div>
      <h1 className="text-slate-400">{post.title}</h1>
      <h2>{post.body}</h2>
      {imagesLength > 0 && (
        <div>
          <ModalImage
            images={post.images}
            imagePage={imagePage}
            nextImage={nextImage}
            prevImage={prevImage}
          />
          {imagesLength > 1 && <button onClick={nextImage}>next image</button>}
          {imagesLength > 1 && <button onClick={prevImage}>prev image</button>}
        </div>
      )}
      <button onClick={clickComments}>Comments</button>
      {toggleComments && <CommentMapper comments={post.comments} />}
    </div>
  );
};
