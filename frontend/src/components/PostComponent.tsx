import { useEffect, useState } from "react";
import { baseURL } from "../constants/urls";
import { PostType } from "../types/contentTypes";
import { CommentMapper } from "./CommentMapper";
import { ModalImage } from "./ModalImage";

interface PostComponentProps {
  post: PostType;
}

export const PostComponent = ({ post }: PostComponentProps) => {
  const [toggleComments, setToggleComments] = useState(false);
  const [togglePopup, setTogglePopup] = useState(false);
  const [imagePage, setImagePage] = useState(0);

  const imagesLength = post.images.length;

  const imagePath = post.images[0]
    ? `${baseURL}${post.images[imagePage].path}`
    : "";

  useEffect(() => {
    if (togglePopup) {
      document.body.style.overflow = "hidden";
      return;
    }

    document.body.style.overflow = "scroll";
  }, [togglePopup]);

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

  function imageClick() {
    setTogglePopup((prev) => !prev);
  }

  return (
    <div className="bg-white border border-black-500">
      <h1 className="text-slate-400">{post.title}</h1>
      <h2>{post.body}</h2>
      {imagesLength > 0 && (
        <div>
          <img
            className="object-contain w-[60%] h-[50%] cursor-pointer"
            src={imagePath}
            alt="postImage"
            onClick={imageClick}
          />
          {togglePopup && (
            <ModalImage imagePath={imagePath} toggler={setTogglePopup} />
          )}

          {imagesLength > 1 && (
            <button onClick={scrollImage}>next image</button>
          )}
        </div>
      )}
      <button className="cover-pointer" onClick={clickComments}>
        Comments
      </button>
      {toggleComments && <CommentMapper comments={post.comments} />}
    </div>
  );
};
