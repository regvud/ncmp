import { useEffect, useRef, useState } from "react";
import PrismaZoom from "react-prismazoom";
import { baseURL } from "../../constants/urls";
import { PostImage } from "../../types/contentTypes";
import { ModalButton } from "./ModalButton";
import { ReactComponent as ArrowRight } from "../../assets/buttons/arrowRight.svg";

interface ModalImageProps {
  images: PostImage[];
  imagePage: number;
  nextImage?: () => void;
  prevImage?: () => void;
}

export function ModalImage({
  images,
  imagePage,
  nextImage,
  prevImage,
}: ModalImageProps) {
  const divImageRef = useRef<HTMLImageElement>(null);
  const [togglePopup, setTogglePopup] = useState(false);

  const imageClass = "object-contain w-[100%] min-h-[600px] rounded";

  const modalWindowClass = togglePopup
    ? "bg-black bg-opacity-80 fixed top-1/2 left-1/2 -transform -translate-x-1/2 -translate-y-1/2"
    : "max-w-[80%] max-h-[50%]";

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

  useEffect(() => {
    if (togglePopup) document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "scroll";
    };
  }, [togglePopup]);

  return (
    <div
      className={modalWindowClass}
      tabIndex={0}
      onKeyDown={handleEscape}
      ref={divImageRef}
    >
      {togglePopup ? (
        <div className="flex justify-around items-center h-screen w-screen">
          {images.length > 1 && prevImage && (
            <ModalButton
              SVG={ArrowRight}
              onClickFunc={prevImage}
              rotate180={true}
            />
          )}
          <div className="flex flex-col justify-around items-center w-[80%]">
            <button className="text-white" onClick={closeImage}>
              ☒
            </button>
            <PrismaZoom>
              <img className={imageClass} src={imagePath} alt="postImage" />
            </PrismaZoom>
          </div>
          {images.length > 1 && nextImage && (
            <ModalButton SVG={ArrowRight} onClickFunc={nextImage} />
          )}
        </div>
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
