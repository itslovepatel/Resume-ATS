'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Upload,
  FileText,
  X,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react';

interface UploadSectionProps {
  onAnalyze: (file: File) => void;
  error: string | null;
}

export default function UploadSection({ onAnalyze, error }: UploadSectionProps) {
  const [file, setFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    setValidationError(null);

    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0];
      if (rejection.errors[0]?.code === 'file-too-large') {
        setValidationError('File size exceeds 5MB limit');
      } else if (rejection.errors[0]?.code === 'file-invalid-type') {
        setValidationError('Invalid file type. Please upload PDF or DOCX');
      } else {
        setValidationError('Invalid file');
      }
      return;
    }

    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxSize: 5 * 1024 * 1024, // 5MB
    multiple: false,
  });

  const handleRemoveFile = () => {
    setFile(null);
    setValidationError(null);
  };

  const handleAnalyze = () => {
    if (file) {
      onAnalyze(file);
    }
  };

  const displayError = error || validationError;

  return (
    <section id="upload" className="py-20 bg-white">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-10"
        >
          <h2 className="section-title text-3xl sm:text-4xl">
            Upload Your Resume
          </h2>
          <p className="section-subtitle">
            Drop your resume file and let our AI analyze it for ATS compatibility
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          {/* Error Display */}
          <AnimatePresence>
            {displayError && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-6"
              >
                <div className="flex items-center gap-3 p-4 bg-danger-50 border border-danger-100 rounded-xl text-danger-600">
                  <AlertCircle className="w-5 h-5 flex-shrink-0" />
                  <span className="text-sm font-medium">{displayError}</span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Dropzone */}
          <div
            {...getRootProps()}
            className={`relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-300
              ${
                isDragActive
                  ? 'border-brand-500 bg-brand-50'
                  : file
                  ? 'border-success-500 bg-success-50'
                  : 'border-gray-300 hover:border-brand-400 hover:bg-gray-50'
              }
            `}
          >
            <input {...getInputProps()} />

            <AnimatePresence mode="wait">
              {file ? (
                <motion.div
                  key="file"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="flex flex-col items-center"
                >
                  <div className="w-16 h-16 bg-success-100 rounded-2xl flex items-center justify-center mb-4">
                    <CheckCircle2 className="w-8 h-8 text-success-600" />
                  </div>
                  <div className="flex items-center gap-3 mb-2">
                    <FileText className="w-5 h-5 text-gray-500" />
                    <span className="font-medium text-gray-900">{file.name}</span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleRemoveFile();
                      }}
                      className="p-1 hover:bg-gray-200 rounded-full transition-colors"
                    >
                      <X className="w-4 h-4 text-gray-500" />
                    </button>
                  </div>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </motion.div>
              ) : (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="flex flex-col items-center"
                >
                  <div
                    className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-4 transition-colors ${
                      isDragActive ? 'bg-brand-100' : 'bg-gray-100'
                    }`}
                  >
                    <Upload
                      className={`w-8 h-8 transition-colors ${
                        isDragActive ? 'text-brand-600' : 'text-gray-400'
                      }`}
                    />
                  </div>
                  <p className="text-lg font-semibold text-gray-900 mb-2">
                    {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume'}
                  </p>
                  <p className="text-gray-500 mb-4">or click to browse</p>
                  <div className="flex items-center gap-2 text-sm text-gray-400">
                    <span className="px-3 py-1 bg-gray-100 rounded-full">PDF</span>
                    <span className="px-3 py-1 bg-gray-100 rounded-full">DOCX</span>
                    <span className="text-gray-300">•</span>
                    <span>Max 5MB</span>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Analyze Button */}
          <AnimatePresence>
            {file && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="mt-6 text-center"
              >
                <button onClick={handleAnalyze} className="btn-primary text-lg px-10 py-4">
                  Analyze Resume
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </section>
  );
}
