'use client';

import { FileText, Menu, X } from 'lucide-react';
import { useState } from 'react';

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-lg border-b border-gray-100">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-brand-500 to-brand-600 rounded-xl flex items-center justify-center shadow-lg shadow-brand-500/25">
              <FileText className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold font-display text-gray-900">
              ATS<span className="text-brand-600">Analyzer</span>
            </span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <a href="#how-it-works" className="text-gray-600 hover:text-brand-600 transition-colors font-medium">
              How It Works
            </a>
            <a href="#features" className="text-gray-600 hover:text-brand-600 transition-colors font-medium">
              Features
            </a>
            <a href="#upload" className="btn-primary">
              Analyze Resume
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6 text-gray-600" />
            ) : (
              <Menu className="w-6 h-6 text-gray-600" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-100">
            <div className="flex flex-col gap-4">
              <a
                href="#how-it-works"
                className="text-gray-600 hover:text-brand-600 transition-colors font-medium px-2 py-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                How It Works
              </a>
              <a
                href="#features"
                className="text-gray-600 hover:text-brand-600 transition-colors font-medium px-2 py-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                Features
              </a>
              <a
                href="#upload"
                className="btn-primary text-center"
                onClick={() => setMobileMenuOpen(false)}
              >
                Analyze Resume
              </a>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
}
