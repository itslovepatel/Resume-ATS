'use client';

import { motion } from 'framer-motion';
import { Upload, Cpu, BarChart3 } from 'lucide-react';

const steps = [
  {
    icon: Upload,
    title: 'Upload Resume',
    description: 'Drag & drop your PDF or DOCX resume file',
    color: 'from-blue-500 to-blue-600',
  },
  {
    icon: Cpu,
    title: 'AI Analyzes',
    description: 'Our AI parses and scores your resume in seconds',
    color: 'from-purple-500 to-purple-600',
  },
  {
    icon: BarChart3,
    title: 'Get Insights',
    description: 'Receive detailed ATS score and improvement tips',
    color: 'from-green-500 to-green-600',
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="section-title text-3xl sm:text-4xl">How It Works</h2>
          <p className="section-subtitle max-w-2xl mx-auto">
            Get your ATS score in three simple steps. No signup, no hassle.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="relative"
            >
              {/* Connector Line */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-16 left-full w-full h-0.5 bg-gradient-to-r from-gray-200 to-gray-100 -translate-x-1/2" />
              )}

              <div className="card-hover p-8 text-center relative">
                {/* Step Number */}
                <div className="absolute top-4 right-4 w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                  <span className="text-sm font-bold text-gray-500">
                    {index + 1}
                  </span>
                </div>

                {/* Icon */}
                <div
                  className={`w-16 h-16 mx-auto mb-6 rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center shadow-lg`}
                >
                  <step.icon className="w-8 h-8 text-white" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  {step.title}
                </h3>
                <p className="text-gray-600">{step.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
