import { forwardRef } from "react";
import type { InputHTMLAttributes } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AlertCircle } from "lucide-react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  icon?: React.ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className = "", label, error, icon, id, ...props }, ref) => {
    const inputId = id || label.toLowerCase().replace(/\s+/g, '-');
    
    return (
      <div className={`w-full ${className}`}>
        <label htmlFor={inputId} className="block text-sm font-medium text-slate-700 dark:text-neutral-300 mb-1.5 ml-1 transition-colors">
          {label}
        </label>
        <div className="relative group">
          {icon && (
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400 dark:text-neutral-500 group-focus-within:text-indigo-600 dark:group-focus-within:text-indigo-500 transition-colors">
              {icon}
            </div>
          )}
          <input
            id={inputId}
            ref={ref}
            className={`
              w-full rounded-xl bg-white dark:bg-neutral-900/50 backdrop-blur-sm border 
              ${error ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-slate-200 dark:border-white/10 focus:ring-indigo-600 dark:focus:ring-indigo-500 focus:border-indigo-600 dark:focus:border-indigo-500'}
              ${icon ? 'pl-11' : 'pl-4'}
              pr-4 py-3 text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-600
              shadow-sm transition-all outline-none focus:ring-2 focus:ring-opacity-50
              hover:bg-slate-50 dark:hover:bg-neutral-800/50
            `}
            {...props}
          />
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="absolute -bottom-6 left-1 flex items-center text-xs text-red-600 dark:text-red-500"
              >
                <AlertCircle className="w-3.5 h-3.5 mr-1" />
                <span>{error}</span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    );
  }
);

Input.displayName = "Input";
