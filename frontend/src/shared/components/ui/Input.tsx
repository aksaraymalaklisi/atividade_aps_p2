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
        <label htmlFor={inputId} className="block text-sm font-medium text-slate-700 mb-1.5 ml-1">
          {label}
        </label>
        <div className="relative group">
          {icon && (
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400 group-focus-within:text-indigo-500 transition-colors">
              {icon}
            </div>
          )}
          <input
            id={inputId}
            ref={ref}
            className={`
              w-full rounded-xl bg-white/50 backdrop-blur-sm border 
              ${error ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-slate-200 focus:ring-indigo-500 focus:border-indigo-500'}
              ${icon ? 'pl-11' : 'pl-4'}
              pr-4 py-3 text-slate-900 placeholder:text-slate-400
              shadow-sm transition-all outline-none focus:ring-2 focus:ring-opacity-50
              hover:bg-white/80
            `}
            {...props}
          />
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="absolute -bottom-6 left-1 flex items-center text-xs text-red-500"
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
