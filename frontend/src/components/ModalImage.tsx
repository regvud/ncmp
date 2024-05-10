import { useEffect, useRef } from "react";
import "./ModalImage.css";

interface ModalImageProps {
  imagePath: string;
  toggler: React.Dispatch<React.SetStateAction<boolean>>;
}

export function ModalImage({ imagePath, toggler }: ModalImageProps) {
  const imageRef = useRef<HTMLImageElement>(null);

  function cleanPrevModal() {
    const prevModal = document.getElementById("modal-window");

    if (prevModal) {
      prevModal.remove();
    }
  }

  useEffect(() => {
    imageRef.current?.focus();
    cleanPrevModal();
  }, []);

  return (
    <div id="modal-window">
      <img
        className="object-contain w-[90%] h-[90%] fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
        src={imagePath}
        alt="postImage"
        ref={imageRef}
        onClick={() => toggler(false)}
        onKeyDown={(e: React.KeyboardEvent<HTMLImageElement>) => {
          if (e.key === "Escape") {
            toggler(false);
          }
        }}
        tabIndex={0} // Make the image focusable
      />
    </div>
  );
}
