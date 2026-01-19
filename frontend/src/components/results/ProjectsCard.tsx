'use client';

import { Project } from '@/types';
import { FolderKanban, Code, Star } from 'lucide-react';

interface ProjectsCardProps {
  projects: Project[];
}

export default function ProjectsCard({ projects }: ProjectsCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 70) return 'text-success-600 bg-success-50';
    if (score >= 50) return 'text-warning-600 bg-warning-50';
    return 'text-danger-600 bg-danger-50';
  };

  return (
    <div className="card p-6 h-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-pink-100 rounded-xl flex items-center justify-center">
            <FolderKanban className="w-5 h-5 text-pink-600" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Projects</h2>
            <p className="text-sm text-gray-500">{projects.length} projects detected</p>
          </div>
        </div>
      </div>

      {projects.length > 0 ? (
        <div className="space-y-4">
          {projects.map((project, index) => (
            <div
              key={index}
              className="p-4 bg-gray-50 rounded-xl border border-gray-100"
            >
              <div className="flex items-start justify-between gap-4 mb-3">
                <h3 className="font-semibold text-gray-900 line-clamp-2">
                  {project.title}
                </h3>
                <div className={`flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-semibold ${getScoreColor(project.score)}`}>
                  <Star className="w-3.5 h-3.5" />
                  {project.score}
                </div>
              </div>

              {project.technologies.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mb-3">
                  {project.technologies.slice(0, 5).map((tech) => (
                    <span
                      key={tech}
                      className="inline-flex items-center gap-1 px-2 py-0.5 bg-brand-50 text-brand-700 rounded text-xs"
                    >
                      <Code className="w-3 h-3" />
                      {tech}
                    </span>
                  ))}
                </div>
              )}

              {project.description && (
                <p className="text-sm text-gray-600 line-clamp-2">
                  {project.description}
                </p>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          <FolderKanban className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>No projects detected</p>
          <p className="text-sm">Add a Projects section to showcase your work</p>
        </div>
      )}
    </div>
  );
}
