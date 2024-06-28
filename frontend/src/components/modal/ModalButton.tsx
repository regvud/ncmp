interface ModalButtonProps {
  SVG: React.FunctionComponent<
    React.SVGProps<SVGSVGElement> & {
      title?: string | undefined;
    }
  >;
  onClickFunc: () => void;
  rotate180?: boolean;
}

export const ModalButton = ({
  SVG,
  onClickFunc,
  rotate180,
}: ModalButtonProps) => {
  return (
    <button onClick={onClickFunc}>
      {rotate180 ? (
        <SVG className="rotate-180" width="50px" height="50px" />
      ) : (
        <SVG width="50px" height="50px" />
      )}
    </button>
  );
};
