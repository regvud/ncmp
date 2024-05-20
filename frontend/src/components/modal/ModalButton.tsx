interface ModalButtonProps {
  repr: string;
  onClickFunc: () => void;
}

export const ModalButton = ({ repr, onClickFunc }: ModalButtonProps) => {
  return (
    <button className="text-slate-400" onClick={onClickFunc}>
      {repr}
    </button>
  );
};
