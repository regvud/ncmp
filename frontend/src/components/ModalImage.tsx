import { useRef, useState } from "react";
import PrismaZoom from "react-prismazoom";

interface ModalImageProps {
  imagePath: string;
}

export function ModalImage({ imagePath }: ModalImageProps) {
  const imageRef = useRef<HTMLImageElement>(null);

  const [togglePopup, setTogglePopup] = useState(false);
  const divTabIndex = useRef<number | undefined>(0);

  const imageClass = togglePopup
    ? "object-contain w-[80%] h-[80%]"
    : "object-contain w-[60%] h-[70%]";

  const modalWindowClass = togglePopup
    ? "h-screen w-screen bg-black bg-opacity-80 fixed top-1/2 left-1/2 -transform -translate-x-1/2 -translate-y-1/2 focus:outline-none"
    : "modal-window";

  function openImage() {
    setTogglePopup(true);
    divTabIndex.current = 0;
  }

  function closeImage() {
    setTogglePopup(false);
    divTabIndex.current = undefined;
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLDivElement>) {
    if (event.key === "Escape") {
      closeImage();
    }
  }

  return (
    <div
      className={modalWindowClass}
      onKeyDown={handleKeyDown}
      tabIndex={divTabIndex.current}
    >
      {togglePopup ? (
        <PrismaZoom>
          <div className="flex justify-center items-center">
            <img
              className={imageClass}
              src={imagePath}
              alt="postImage"
              ref={imageRef}
            />
            <button className="text-white" onClick={closeImage}>
              close
            </button>
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
