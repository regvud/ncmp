import { useState } from "react";
import { PostCounterType } from "../types/counterContentTypes";
import { CommentMapper } from "./CommentMapper";
import { ModalButton } from "./modal/ModalButton";
import { ModalImage } from "./modal/ModalImage";
import { UserLikeMapper } from "./UserLikeComponent";
import { ReactComponent as ArrowRight } from "../assets/buttons/arrowRight.svg";

interface PostComponentProps {
  post: PostCounterType;
}

export const PostComponent = ({ post }: PostComponentProps) => {
  const [toggleComments, setToggleComments] = useState(false);
  const [imagePage, setImagePage] = useState(0);

  console.log(post.images.length);
  const imagesLength = post?.images?.length;

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
    <div className="flex flex-col items-center border border-sky-500 rounded w-[60%]">
      <h1 className="text-slate-400"> {post.title}</h1>
      {imagesLength > 0 && (
        <div className="flex justify-around border py-[10px]">
          <>
            {imagesLength > 1 && (
              <ModalButton
                SVG={ArrowRight}
                onClickFunc={prevImage}
                rotate180={true}
              />
            )}
          </>
          <ModalImage
            images={post.images}
            imagePage={imagePage}
            nextImage={nextImage}
            prevImage={prevImage}
          />
          <>
            {imagesLength > 1 && (
              <ModalButton SVG={ArrowRight} onClickFunc={nextImage} />
            )}
          </>
        </div>
      )}
      <div>
        <div className="flex justify-around">
          <span> likes: {post.likes_count}</span>
          <UserLikeMapper userLikes={post.users_liked} />
        </div>
        <p>{post.body}</p>
        <button onClick={clickComments}>Comments: {post.comments_count}</button>
        {toggleComments && <CommentMapper comments={post.comments} />}
      </div>
    </div>
  );
};
