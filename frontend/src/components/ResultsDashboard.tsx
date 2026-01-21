'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  ArrowLeft,
  Download,
  User,
  Mail,
  Phone,
  MapPin,
  Linkedin,
  Github,
  Target,
  Compass,
  Code2,
  FolderKanban,
  Briefcase,
  GraduationCap,
  AlertTriangle,
  Lightbulb,
  CheckCircle2,
  XCircle,
  TrendingUp,
  Loader2,
} from 'lucide-react';
import { AnalysisResult } from '@/types';
import ScoreCircle from './results/ScoreCircle';
import ScoreBreakdownCard from './results/ScoreBreakdownCard';
import SkillsCard from './results/SkillsCard';
import ExperienceCard from './results/ExperienceCard';
import ProjectsCard from './results/ProjectsCard';
import IssuesCard from './results/IssuesCard';
import SuggestionsCard from './results/SuggestionsCard';
import KeywordsCard from './results/KeywordsCard';

interface ResultsDashboardProps {
  results: AnalysisResult;
  onReset: () => void;
}

export default function ResultsDashboard({ results, onReset }: ResultsDashboardProps) {
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownloadReport = async () => {
    setIsDownloading(true);
    try {
      const response = await fetch('/api/download-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(results),
      });

      if (!response.ok) {
        throw new Error('Failed to generate report');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ats-resume-report-${results.candidate.name?.replace(/\s+/g, '-') || 'analysis'}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Download failed:', error);
      alert('Failed to download report. Please try again.');
    } finally {
      setIsDownloading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-success-600';
    if (score >= 60) return 'text-warning-600';
    return 'text-danger-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-success-50 border-success-200';
    if (score >= 60) return 'bg-warning-50 border-warning-200';
    return 'bg-danger-50 border-danger-200';
  };

  const getCategoryBadge = (category: string) => {
    switch (category) {
      case 'Excellent':
        return 'badge-success';
      case 'Good':
        return 'badge-info';
      case 'Needs Improvement':
        return 'badge-warning';
      default:
        return 'badge-danger';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8"
        >
          <div className="flex items-center gap-4">
            <button
              onClick={onReset}
              className="p-2 hover:bg-gray-200 rounded-xl transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-gray-600" />
            </button>
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold font-display text-gray-900">
                Resume Analysis Results
              </h1>
              <p className="text-gray-600">
                {results.candidate.name || 'Your Resume'} • Analyzed just now
              </p>
            </div>
          </div>
          <button 
            onClick={handleDownloadReport}
            disabled={isDownloading}
            className="btn-secondary flex items-center gap-2 disabled:opacity-50"
          >
            {isDownloading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Download className="w-4 h-4" />
            )}
            {isDownloading ? 'Generating...' : 'Download Report'}
          </button>
        </motion.div>

        {/* Main Score Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8"
        >
          {/* Score Card */}
          <div className={`card p-8 ${getScoreBgColor(results.ats_score)} border-2`}>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-1">
                  ATS Score
                </h2>
                <span className={`${getCategoryBadge(results.score_category)}`}>
                  {results.score_category}
                </span>
              </div>
              <ScoreCircle score={results.ats_score} size={120} />
            </div>
            <p className="text-sm text-gray-600">
              {results.ats_score >= 80
                ? 'Excellent! Your resume is well-optimized for ATS systems.'
                : results.ats_score >= 60
                ? 'Good start, but there\'s room for improvement.'
                : 'Your resume needs significant optimization for ATS.'}
            </p>
            {/* OCR Indicator */}
            {results.parsing_method === 'ocr' && (
              <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center gap-2 text-blue-700 text-sm">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <span className="font-medium">Scanned Document Detected</span>
                </div>
                <p className="text-xs text-blue-600 mt-1">
                  OCR was used to extract text. Confidence: {results.ocr_confidence || 'unknown'}
                </p>
              </div>
            )}
          </div>

          {/* Candidate Profile */}
          <div className="card p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-brand-100 rounded-xl flex items-center justify-center">
                <User className="w-5 h-5 text-brand-600" />
              </div>
              <h2 className="text-lg font-semibold text-gray-900">
                Candidate Profile
              </h2>
            </div>
            <div className="space-y-3">
              {results.candidate.name && (
                <div className="flex items-center gap-3 text-gray-700">
                  <User className="w-4 h-4 text-gray-400" />
                  <span className="font-medium">{results.candidate.name}</span>
                </div>
              )}
              {results.candidate.email && (
                <div className="flex items-center gap-3 text-gray-700">
                  <Mail className="w-4 h-4 text-gray-400" />
                  <span>{results.candidate.email}</span>
                </div>
              )}
              {results.candidate.phone && (
                <div className="flex items-center gap-3 text-gray-700">
                  <Phone className="w-4 h-4 text-gray-400" />
                  <span>{results.candidate.phone}</span>
                </div>
              )}
              {results.candidate.location && (
                <div className="flex items-center gap-3 text-gray-700">
                  <MapPin className="w-4 h-4 text-gray-400" />
                  <span>{results.candidate.location}</span>
                </div>
              )}
              {results.candidate.linkedin && (
                <div className="flex items-center gap-3 text-gray-700">
                  <Linkedin className="w-4 h-4 text-gray-400" />
                  <span className="text-sm truncate">{results.candidate.linkedin}</span>
                </div>
              )}
              {results.candidate.github && (
                <div className="flex items-center gap-3 text-gray-700">
                  <Github className="w-4 h-4 text-gray-400" />
                  <span className="text-sm truncate">{results.candidate.github}</span>
                </div>
              )}
            </div>
          </div>

          {/* Domain Detection */}
          <div className="card p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center">
                <Compass className="w-5 h-5 text-purple-600" />
              </div>
              <h2 className="text-lg font-semibold text-gray-900">
                Detected Domain
              </h2>
            </div>
            <div className="mb-4">
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {results.domain.primary}
              </div>
              <div className="flex items-center gap-2">
                <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-purple-500 rounded-full transition-all duration-500"
                    style={{ width: `${results.domain.confidence * 100}%` }}
                  />
                </div>
                <span className="text-sm text-gray-600">
                  {Math.round(results.domain.confidence * 100)}% confidence
                </span>
              </div>
            </div>
            {results.domain.secondary && (
              <div className="text-sm text-gray-600">
                <span className="font-medium">Secondary:</span>{' '}
                {results.domain.secondary}
              </div>
            )}
            {results.domain.keywords_matched.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {results.domain.keywords_matched.slice(0, 5).map((kw) => (
                  <span key={kw} className="badge-info text-xs">
                    {kw}
                  </span>
                ))}
              </div>
            )}
          </div>
        </motion.div>

        {/* Score Breakdown */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <ScoreBreakdownCard breakdown={results.score_breakdown} />
        </motion.div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Skills */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <SkillsCard skills={results.skills} />
          </motion.div>

          {/* Experience */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <ExperienceCard experience={results.experience} />
          </motion.div>

          {/* Projects */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <ProjectsCard projects={results.projects} />
          </motion.div>

          {/* Keywords Analysis */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <KeywordsCard keywords={results.keywords_analysis} />
          </motion.div>
        </div>

        {/* Issues and Suggestions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
          >
            <IssuesCard issues={results.issues} />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
          >
            <SuggestionsCard suggestions={results.suggestions} />
          </motion.div>
        </div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
          className="mt-12 text-center"
        >
          <div className="inline-flex flex-col sm:flex-row items-center gap-4">
            <button onClick={onReset} className="btn-primary">
              Analyze Another Resume
            </button>
            <button 
              onClick={handleDownloadReport}
              disabled={isDownloading}
              className="btn-secondary flex items-center gap-2 disabled:opacity-50"
            >
              {isDownloading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Download className="w-4 h-4" />
              )}
              {isDownloading ? 'Generating...' : 'Download Full Report'}
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
