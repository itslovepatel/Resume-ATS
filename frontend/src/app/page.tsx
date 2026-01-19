'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import Hero from '@/components/Hero';
import HowItWorks from '@/components/HowItWorks';
import Features from '@/components/Features';
import UploadSection from '@/components/UploadSection';
import ResultsDashboard from '@/components/ResultsDashboard';
import Footer from '@/components/Footer';
import LoadingOverlay from '@/components/LoadingOverlay';
import { AnalysisResult } from '@/types';

export default function Home() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (file: File) => {
    setIsAnalyzing(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze resume');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <main className="min-h-screen">
      <Header />
      
      {isAnalyzing && <LoadingOverlay />}
      
      {results ? (
        <ResultsDashboard results={results} onReset={handleReset} />
      ) : (
        <>
          <Hero />
          <UploadSection onAnalyze={handleAnalyze} error={error} />
          <HowItWorks />
          <Features />
        </>
      )}
      
      <Footer />
    </main>
  );
}
