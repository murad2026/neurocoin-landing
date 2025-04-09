import React from 'react';
import clsx from 'clsx';

export const Button = ({ children, className = '', ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) => {
  return (
    <button
      {...props}
      className={clsx(
        'bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-2xl transition duration-300',
        className
      )}
    >
      {children}
    </button>
  );
};
