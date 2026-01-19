import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ATS Resume Analyzer - Free Resume Score & ATS Compatibility Check',
  description: 'Upload your resume and get instant ATS compatibility score, skills analysis, and recruiter-level insights. Free, no signup required.',
  keywords: 'ATS resume checker, resume analyzer, ATS score, resume optimization, job search, career tools',
  openGraph: {
    title: 'ATS Resume Analyzer - See Your Resume Through an ATS Lens',
    description: 'Get your free ATS score and actionable insights to improve your resume.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        {children}
      </body>
    </html>
  );
}
