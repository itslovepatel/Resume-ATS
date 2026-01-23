'use client';

import { motion } from 'framer-motion';
import { ArrowRight, CheckCircle2, Shield, Zap } from 'lucide-react';

export default function Hero() {
  return (
    <section className="relative pt-32 pb-20 overflow-hidden bg-gradient-hero">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-40">
        <div className="absolute top-20 left-10 w-72 h-72 bg-brand-200 rounded-full mix-blend-multiply filter blur-3xl animate-pulse-slow" />
        <div className="absolute top-40 right-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl animate-pulse-slow delay-1000" />
        <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-3xl animate-pulse-slow delay-2000" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-2 bg-brand-50 rounded-full border border-brand-100 mb-8"
          >
            <Zap className="w-4 h-4 text-brand-600" />
            <span className="text-sm font-medium text-brand-700">
              AI-Powered Resume Analysis
            </span>
          </motion.div>

          {/* Main Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-4xl sm:text-5xl lg:text-6xl font-extrabold font-display text-gray-900 mb-6 leading-tight"
          >
            See Your Resume Through
            <br />
            <span className="text-gradient">an ATS Lens</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto mb-10"
          >
            Upload your resume and get an ATS score, skills analysis, and
            recruiter-level insights in seconds. No signup required.
          </motion.p>

          {/* CTA Button */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <a
              href="#upload"
              className="btn-primary text-lg px-8 py-4 inline-flex items-center gap-2 group"
            >
              Analyze Your Resume
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </a>
            <p className="mt-4 text-sm text-gray-500">
              Supports PDF & DOCX • Max 5MB
            </p>
          </motion.div>

          {/* Trust Indicators */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="flex flex-wrap items-center justify-center gap-6 mt-12"
          >
            <div className="flex items-center gap-2 text-gray-600">
              <CheckCircle2 className="w-5 h-5 text-success-500" />
              <span className="text-sm font-medium">Blazingly Fast ⚡</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600">
              <Shield className="w-5 h-5 text-success-500" />
              <span className="text-sm font-medium">Zero Data Stored 🔒</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600">
              <Zap className="w-5 h-5 text-success-500" />
              <span className="text-sm font-medium">100% Open Source</span>
            </div>
          </motion.div>

          {/* Privacy Badge - Humorous */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="mt-8 inline-flex items-center gap-2 px-4 py-2 bg-green-50 rounded-full border border-green-200"
          >
            <Shield className="w-4 h-4 text-green-600" />
            <span className="text-sm text-green-700 font-medium">
              Your data? We literally can&apos;t afford the storage to keep it 😅
            </span>
          </motion.div>
        </div>

        {/* Preview Image Placeholder */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="mt-16 relative"
        >
          <div className="relative mx-auto max-w-4xl">
            <div className="absolute inset-0 bg-gradient-to-r from-brand-500/20 to-purple-500/20 rounded-3xl blur-2xl" />
            <div className="relative bg-white rounded-2xl shadow-2xl border border-gray-200 p-8">
              <div className="flex items-center gap-2 mb-6">
                <div className="w-3 h-3 rounded-full bg-red-400" />
                <div className="w-3 h-3 rounded-full bg-yellow-400" />
                <div className="w-3 h-3 rounded-full bg-green-400" />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="col-span-1 space-y-4">
                  <div className="h-32 bg-gradient-to-br from-brand-500 to-brand-600 rounded-xl flex items-center justify-center">
                    <span className="text-4xl font-bold text-white">85</span>
                  </div>
                  <div className="h-4 bg-gray-100 rounded-full" />
                  <div className="h-4 bg-gray-100 rounded-full w-2/3" />
                </div>
                <div className="col-span-2 space-y-4">
                  <div className="h-6 bg-gray-100 rounded-full w-1/2" />
                  <div className="h-4 bg-gray-100 rounded-full" />
                  <div className="h-4 bg-gray-100 rounded-full w-5/6" />
                  <div className="h-4 bg-gray-100 rounded-full w-4/6" />
                  <div className="flex gap-2 mt-4">
                    <div className="h-8 w-20 bg-brand-100 rounded-full" />
                    <div className="h-8 w-24 bg-brand-100 rounded-full" />
                    <div className="h-8 w-16 bg-brand-100 rounded-full" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
