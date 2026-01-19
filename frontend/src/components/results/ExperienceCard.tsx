'use client';

import { ExperienceSummary } from '@/types';
import { Briefcase, TrendingUp, Hash, Zap } from 'lucide-react';

interface ExperienceCardProps {
  experience: ExperienceSummary;
}

export default function ExperienceCard({ experience }: ExperienceCardProps) {
  const getQualityColor = (quality: number) => {
    if (quality >= 70) return 'text-success-600 bg-success-50';
    if (quality >= 50) return 'text-warning-600 bg-warning-50';
    return 'text-danger-600 bg-danger-50';
  };

  return (
    <div className="card p-6 h-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center">
            <Briefcase className="w-5 h-5 text-indigo-600" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Work Experience</h2>
            <p className="text-sm text-gray-500">
              {experience.total_years > 0
                ? `${experience.total_years} years total`
                : 'Experience detected'}
            </p>
          </div>
        </div>
        <div className={`px-3 py-1.5 rounded-lg font-semibold text-sm ${getQualityColor(experience.overall_quality)}`}>
          Quality: {experience.overall_quality}%
        </div>
      </div>

      {experience.positions.length > 0 ? (
        <div className="space-y-4">
          {experience.positions.map((position, index) => (
            <div
              key={index}
              className="p-4 bg-gray-50 rounded-xl border border-gray-100"
            >
              <div className="flex items-start justify-between gap-4 mb-3">
                <div>
                  <h3 className="font-semibold text-gray-900">
                    {position.role || 'Role not detected'}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {position.company || 'Company not detected'}
                  </p>
                </div>
                {position.duration && (
                  <span className="text-xs text-gray-500 bg-gray-200 px-2 py-1 rounded-full whitespace-nowrap">
                    {position.duration}
                  </span>
                )}
              </div>

              <div className="flex flex-wrap gap-3 text-xs">
                <div className="flex items-center gap-1.5 text-gray-600">
                  <TrendingUp className="w-3.5 h-3.5" />
                  <span>Bullet Quality: {position.bullet_quality}%</span>
                </div>
                <div className="flex items-center gap-1.5 text-gray-600">
                  <Zap className="w-3.5 h-3.5" />
                  <span>Action Verbs: {position.action_verbs_count}</span>
                </div>
                {position.has_metrics && (
                  <div className="flex items-center gap-1.5 text-success-600">
                    <Hash className="w-3.5 h-3.5" />
                    <span>Has Metrics</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          <Briefcase className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>No work experience entries detected</p>
          <p className="text-sm">Make sure your experience section is clearly labeled</p>
        </div>
      )}
    </div>
  );
}
