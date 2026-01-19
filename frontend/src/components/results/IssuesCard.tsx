'use client';

import { ATSIssue } from '@/types';
import { AlertTriangle, AlertCircle, Info, ChevronRight } from 'lucide-react';

interface IssuesCardProps {
  issues: ATSIssue[];
}

export default function IssuesCard({ issues }: IssuesCardProps) {
  const getSeverityStyles = (severity: string) => {
    switch (severity) {
      case 'High':
        return {
          icon: AlertTriangle,
          bg: 'bg-danger-50',
          border: 'border-danger-200',
          iconColor: 'text-danger-500',
          badge: 'bg-danger-100 text-danger-700',
        };
      case 'Medium':
        return {
          icon: AlertCircle,
          bg: 'bg-warning-50',
          border: 'border-warning-200',
          iconColor: 'text-warning-500',
          badge: 'bg-warning-100 text-warning-700',
        };
      default:
        return {
          icon: Info,
          bg: 'bg-blue-50',
          border: 'border-blue-200',
          iconColor: 'text-blue-500',
          badge: 'bg-blue-100 text-blue-700',
        };
    }
  };

  const highIssues = issues.filter((i) => i.severity === 'High');
  const mediumIssues = issues.filter((i) => i.severity === 'Medium');
  const lowIssues = issues.filter((i) => i.severity === 'Low');

  const sortedIssues = [...highIssues, ...mediumIssues, ...lowIssues];

  return (
    <div className="card p-6 h-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center">
            <AlertTriangle className="w-5 h-5 text-red-600" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">ATS Issues Detected</h2>
            <p className="text-sm text-gray-500">{issues.length} issues found</p>
          </div>
        </div>
        <div className="flex gap-2">
          {highIssues.length > 0 && (
            <span className="text-xs px-2 py-1 bg-danger-100 text-danger-700 rounded-full font-medium">
              {highIssues.length} High
            </span>
          )}
          {mediumIssues.length > 0 && (
            <span className="text-xs px-2 py-1 bg-warning-100 text-warning-700 rounded-full font-medium">
              {mediumIssues.length} Medium
            </span>
          )}
        </div>
      </div>

      {sortedIssues.length > 0 ? (
        <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2">
          {sortedIssues.map((issue, index) => {
            const styles = getSeverityStyles(issue.severity);
            const IconComponent = styles.icon;

            return (
              <div
                key={index}
                className={`p-4 rounded-xl border ${styles.bg} ${styles.border}`}
              >
                <div className="flex items-start gap-3">
                  <IconComponent className={`w-5 h-5 flex-shrink-0 mt-0.5 ${styles.iconColor}`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-semibold text-gray-900 text-sm">
                        {issue.description}
                      </span>
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${styles.badge}`}>
                        {issue.severity}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">{issue.suggestion}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="text-center py-8">
          <div className="w-16 h-16 mx-auto mb-4 bg-success-100 rounded-full flex items-center justify-center">
            <AlertTriangle className="w-8 h-8 text-success-600" />
          </div>
          <p className="text-gray-600 font-medium">No major issues detected!</p>
          <p className="text-sm text-gray-500">Your resume looks ATS-friendly</p>
        </div>
      )}
    </div>
  );
}
