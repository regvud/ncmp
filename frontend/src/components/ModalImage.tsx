import { useRef, useState } from "react";
import PrismaZoom from "react-prismazoom";
import { baseURL } from "../constants/urls";
import { PostImage } from "../types/contentTypes";

interface ModalImageProps {
  images: PostImage[];
  imagePage: number;
  nextImage: () => void;
  prevImage: () => void;
}

export function ModalImage({
  images,
  imagePage,
  nextImage,
  prevImage,
}: ModalImageProps) {
  const divImageRef = useRef<HTMLImageElement>(null);

  const [togglePopup, setTogglePopup] = useState(false);

  const imageClass = togglePopup
    ? "object-contain w-[80%] h-[80%]"
    : "object-contain w-[60%] h-[70%]";

  const modalWindowClass = togglePopup
    ? "h-screen w-screen bg-black bg-opacity-80 fixed top-1/2 left-1/2 -transform -translate-x-1/2 -translate-y-1/2"
    : "modal-window";

  const imagePath = images[0] ? `${baseURL}${images[imagePage].path}` : "";

  function openImage() {
    setTogglePopup(true);
  }

  function closeImage() {
    setTogglePopup(false);
    divImageRef.current?.blur();
  }

  function handleEscape(e: React.KeyboardEvent<HTMLDivElement>) {
    if (e.key !== "Escape") {
      divImageRef.current?.blur();
      return;
    }
    closeImage();
  }

  return (
    <div
      className={modalWindowClass}
      tabIndex={0}
      onKeyDown={handleEscape}
      ref={divImageRef}
    >
      {togglePopup ? (
        <PrismaZoom>
          <div className="flex justify-center">
            <img className={imageClass} src={imagePath} alt="postImage" />
            <button className="text-white" onClick={closeImage}>
              close
            </button>
            <button onClick={nextImage}>next image</button>
            <button onClick={prevImage}>prev image</button>
          </div>
        </PrismaZoom>
      ) : (
        <img
          className={imageClass}
          onClick={openImage}
          src={imagePath}
          alt="postImage"
        />
      )}
    </div>
  );
}
