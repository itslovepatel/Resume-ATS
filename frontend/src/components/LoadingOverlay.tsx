'use client';

import { motion } from 'framer-motion';
import { FileText, Loader2 } from 'lucide-react';

export default function LoadingOverlay() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center"
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-white rounded-3xl p-12 shadow-2xl max-w-md w-full mx-4 text-center"
      >
        {/* Animated Icon */}
        <div className="relative w-24 h-24 mx-auto mb-8">
          {/* Outer spinning ring */}
          <div className="absolute inset-0 border-4 border-brand-200 rounded-full" />
          <div className="absolute inset-0 border-4 border-transparent border-t-brand-600 rounded-full animate-spin" />
          
          {/* Center icon */}
          <div className="absolute inset-4 bg-brand-50 rounded-full flex items-center justify-center">
            <FileText className="w-8 h-8 text-brand-600" />
          </div>
        </div>

        {/* Loading text */}
        <h3 className="text-xl font-bold text-gray-900 mb-3">
          Analyzing Your Resume
        </h3>
        
        <p className="text-gray-600 mb-6">
          Our AI is parsing your resume and calculating your ATS score...
        </p>

        {/* Progress steps */}
        <div className="space-y-3">
          <LoadingStep text="Extracting text content" delay={0} />
          <LoadingStep text="Identifying skills & keywords" delay={1} />
          <LoadingStep text="Analyzing experience" delay={2} />
          <LoadingStep text="Calculating ATS score" delay={3} />
        </div>
      </motion.div>
    </motion.div>
  );
}

function LoadingStep({ text, delay }: { text: string; delay: number }) {
  return (
    <motion.div
      initial={{ opacity: 0.4 }}
      animate={{ opacity: [0.4, 1, 0.4] }}
      transition={{
        duration: 2,
        repeat: Infinity,
        delay: delay * 0.5,
      }}
      className="flex items-center gap-3 text-sm text-gray-600"
    >
      <Loader2 className="w-4 h-4 animate-spin text-brand-600" />
      <span>{text}</span>
    </motion.div>
  );
}
