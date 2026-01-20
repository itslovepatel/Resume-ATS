import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ATS Resume Analyzer - Free Resume Score & ATS Compatibility Check',
  description: 'Upload your resume and get instant ATS compatibility score, skills analysis, and recruiter-level insights. Free AI-powered resume analyzer, no signup required.',
  keywords: 'ATS resume checker, resume analyzer, ATS score, resume optimization, job search, career tools, free resume scanner, applicant tracking system, resume parser, CV analyzer, job application, resume tips, ATS friendly resume, resume keywords',
  authors: [{ name: 'Love Patel', url: 'https://github.com/itslovepatel' }],
  creator: 'Love Patel',
  publisher: 'ATS Resume Analyzer',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    title: 'ATS Resume Analyzer - See Your Resume Through an ATS Lens',
    description: 'Get your free ATS score and actionable insights to improve your resume. AI-powered analysis for job seekers.',
    type: 'website',
    locale: 'en_US',
    siteName: 'ATS Resume Analyzer',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ATS Resume Analyzer - Free Resume Score & ATS Check',
    description: 'Upload your resume and get instant ATS compatibility score, skills analysis, and recruiter-level insights.',
  },
  category: 'Career Tools',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="theme-color" content="#3B82F6" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'WebApplication',
              name: 'ATS Resume Analyzer',
              description: 'Free AI-powered resume analyzer that helps job seekers understand how ATS systems read their resumes.',
              applicationCategory: 'BusinessApplication',
              operatingSystem: 'Any',
              offers: {
                '@type': 'Offer',
                price: '0',
                priceCurrency: 'USD',
              },
              author: {
                '@type': 'Person',
                name: 'Love Patel',
                url: 'https://github.com/itslovepatel',
              },
            }),
          }}
        />
      </head>
      <body className="min-h-screen bg-gray-50">
        {children}
      </body>
    </html>
  );
}
