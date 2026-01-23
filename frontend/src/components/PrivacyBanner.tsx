'use client';

import { motion } from 'framer-motion';
import { Shield, Database, Lock, Trash2, Code, Github } from 'lucide-react';

export default function PrivacyBanner() {
  return (
    <section className="py-12 bg-gradient-to-r from-green-50 via-emerald-50 to-teal-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-8"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-green-100 rounded-full border border-green-200 mb-4">
            <Shield className="w-5 h-5 text-green-600" />
            <span className="text-sm font-semibold text-green-700">
              Privacy-First Architecture
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-3">
            Your Data? We Don&apos;t Want It 🙅‍♂️
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Real talk: We literally don&apos;t store your resume data. Not because we&apos;re saints,
            but because we don&apos;t have that kind of storage budget. Your privacy is secure by poverty. 😅
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-green-100"
          >
            <Database className="w-8 h-8 text-green-600 mb-3" />
            <h3 className="font-bold text-gray-900 mb-2">No Database</h3>
            <p className="text-sm text-gray-600">
              Zero databases = zero data breaches. It&apos;s called &quot;serverless security&quot; (and being frugal) 💰
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-green-100"
          >
            <Lock className="w-8 h-8 text-green-600 mb-3" />
            <h3 className="font-bold text-gray-900 mb-2">Stateless API</h3>
            <p className="text-sm text-gray-600">
              Each request is a fresh start. Your resume goes in, analysis comes out, nothing stays behind. Clean AF. ✨
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-green-100"
          >
            <Trash2 className="w-8 h-8 text-green-600 mb-3" />
            <h3 className="font-bold text-gray-900 mb-2">Auto-Purged</h3>
            <p className="text-sm text-gray-600">
              Your file gets analyzed and immediately yeeted into the void. We couldn&apos;t recover it even if we tried. 🗑️
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-green-100"
          >
            <Code className="w-8 h-8 text-green-600 mb-3" />
            <h3 className="font-bold text-gray-900 mb-2">100% Open Source</h3>
            <p className="text-sm text-gray-600">
              Don&apos;t trust us? Check the code yourself. We&apos;re transparent like freshly cleaned glass. 🔍
            </p>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="text-center mt-8"
        >
          <a
            href="https://github.com/itslovepatel/Resume-ATS"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-green-700 hover:text-green-800 font-medium transition-colors"
          >
            <Github className="w-5 h-5" />
            <span>Audit our code on GitHub</span>
          </a>
        </motion.div>
      </div>
    </section>
  );
}
