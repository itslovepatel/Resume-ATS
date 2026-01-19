'use client';

import { SkillsData } from '@/types';
import { Code2, CheckCircle2 } from 'lucide-react';

interface SkillsCardProps {
  skills: SkillsData;
}

export default function SkillsCard({ skills }: SkillsCardProps) {
  const getStrengthBadge = (strength: string) => {
    switch (strength) {
      case 'Strong':
        return 'badge-success';
      case 'Moderate':
        return 'badge-warning';
      default:
        return 'badge-danger';
    }
  };

  return (
    <div className="card p-6 h-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-orange-100 rounded-xl flex items-center justify-center">
            <Code2 className="w-5 h-5 text-orange-600" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Skills & Tech Stack</h2>
            <p className="text-sm text-gray-500">{skills.total_count} skills detected</p>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        {skills.skill_categories.map((category) => (
          <div key={category.name}>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-semibold text-gray-700">{category.name}</h3>
              <span className={`${getStrengthBadge(category.strength)} text-xs`}>
                {category.strength}
              </span>
            </div>
            <div className="flex flex-wrap gap-2">
              {category.skills.map((skill) => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1 px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors"
                >
                  <CheckCircle2 className="w-3.5 h-3.5 text-success-500" />
                  {skill}
                </span>
              ))}
            </div>
          </div>
        ))}

        {skills.soft_skills.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">Soft Skills</h3>
            <div className="flex flex-wrap gap-2">
              {skills.soft_skills.map((skill) => (
                <span
                  key={skill}
                  className="px-3 py-1.5 bg-purple-50 text-purple-700 rounded-lg text-sm font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
