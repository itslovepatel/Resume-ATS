'use client';

import { Suggestion } from '@/types';
import { Lightbulb, ArrowRight, Sparkles } from 'lucide-react';

interface SuggestionsCardProps {
  suggestions: Suggestion[];
}

export default function SuggestionsCard({ suggestions }: SuggestionsCardProps) {
  const getPriorityStyles = (priority: string) => {
    switch (priority) {
      case 'High':
        return 'border-l-brand-500 bg-brand-50';
      case 'Medium':
        return 'border-l-purple-500 bg-purple-50';
      default:
        return 'border-l-gray-400 bg-gray-50';
    }
  };

  const getCategoryIcon = (category: string) => {
    return Sparkles;
  };

  return (
    <div className="card p-6 h-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-yellow-100 rounded-xl flex items-center justify-center">
            <Lightbulb className="w-5 h-5 text-yellow-600" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              AI Improvement Suggestions
            </h2>
            <p className="text-sm text-gray-500">{suggestions.length} suggestions</p>
          </div>
        </div>
      </div>

      {suggestions.length > 0 ? (
        <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
          {suggestions.map((suggestion, index) => {
            const IconComponent = getCategoryIcon(suggestion.category);

            return (
              <div
                key={index}
                className={`p-4 rounded-xl border-l-4 ${getPriorityStyles(suggestion.priority)}`}
              >
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center shadow-sm">
                    <IconComponent className="w-4 h-4 text-brand-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-semibold text-gray-900 text-sm">
                        {suggestion.title}
                      </span>
                      <span className="text-xs px-2 py-0.5 bg-white rounded-full text-gray-500 font-medium">
                        {suggestion.category}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">
                      {suggestion.description}
                    </p>

                    {suggestion.examples.length > 0 && (
                      <div className="space-y-2">
                        {suggestion.examples.slice(0, 3).map((example, i) => (
                          <div
                            key={i}
                            className="flex items-start gap-2 text-sm text-gray-700 bg-white rounded-lg px-3 py-2"
                          >
                            <ArrowRight className="w-4 h-4 text-brand-500 flex-shrink-0 mt-0.5" />
                            <span>{example}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="text-center py-8">
          <div className="w-16 h-16 mx-auto mb-4 bg-success-100 rounded-full flex items-center justify-center">
            <Lightbulb className="w-8 h-8 text-success-600" />
          </div>
          <p className="text-gray-600 font-medium">Your resume is well-optimized!</p>
          <p className="text-sm text-gray-500">No major improvements needed</p>
        </div>
      )}
    </div>
  );
}
