import { FC } from 'react';

type Props = {
  message: React.ReactNode;
  onClose: () => void;
  extraBtn?: { label: string; onClick: () => void };
};

const Modal: FC<Props> = ({ message, onClose, extraBtn }) => (
  <div
    style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0,0,0,0.4)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
    }}
    onClick={onClose}
  >
    <div
      style={{
        background: '#fff',
        padding: 24,
        borderRadius: 8,
        minWidth: 260,
        textAlign: 'center',
      }}
      onClick={(e) => e.stopPropagation()}
    >
      <p style={{ whiteSpace: 'pre-wrap' }}>{message}</p>
      {extraBtn && (
        <button onClick={extraBtn.onClick} style={{ marginRight: 8 }}>
          {extraBtn.label}
        </button>
      )}
      <button onClick={onClose}>OK</button>
    </div>
  </div>
);

export default Modal;
