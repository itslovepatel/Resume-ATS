'use client';

import { ScoreBreakdown } from '@/types';
import { Target, FileCheck, Layout, Code2, Briefcase, FolderKanban } from 'lucide-react';

interface ScoreBreakdownCardProps {
  breakdown: ScoreBreakdown;
}

const breakdownItems = [
  { key: 'keyword_relevance', label: 'Keyword Relevance', icon: Target, color: 'bg-blue-500' },
  { key: 'section_completeness', label: 'Section Completeness', icon: FileCheck, color: 'bg-purple-500' },
  { key: 'formatting_score', label: 'Formatting', icon: Layout, color: 'bg-green-500' },
  { key: 'skill_relevance', label: 'Skill Relevance', icon: Code2, color: 'bg-orange-500' },
  { key: 'experience_clarity', label: 'Experience Clarity', icon: Briefcase, color: 'bg-pink-500' },
  { key: 'project_impact', label: 'Project Impact', icon: FolderKanban, color: 'bg-indigo-500' },
];

export default function ScoreBreakdownCard({ breakdown }: ScoreBreakdownCardProps) {
  const getBarColor = (score: number) => {
    if (score >= 80) return 'bg-success-500';
    if (score >= 60) return 'bg-warning-500';
    return 'bg-danger-500';
  };

  return (
    <div className="card p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-6">Score Breakdown</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {breakdownItems.map((item) => {
          const score = breakdown[item.key as keyof ScoreBreakdown];
          return (
            <div key={item.key} className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className={`w-8 h-8 ${item.color} rounded-lg flex items-center justify-center`}>
                    <item.icon className="w-4 h-4 text-white" />
                  </div>
                  <span className="text-sm font-medium text-gray-700">{item.label}</span>
                </div>
                <span className="text-sm font-bold text-gray-900">{score}</span>
              </div>
              <div className="progress-bar">
                <div
                  className={`progress-fill ${getBarColor(score)}`}
                  style={{ width: `${score}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
