import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ATS Resume Analyzer - Free AI-Powered Resume Score & ATS Compatibility Check',
  description: 'Upload your resume and get instant ATS compatibility score, skills analysis, and recruiter-level insights. Free AI-powered resume analyzer with zero data storage. Built with ❤️ for job seekers everywhere. No signup required, 100% open source.',
  keywords: 'ATS resume checker, resume analyzer, ATS score, resume optimization, job search, career tools, free resume scanner, applicant tracking system, resume parser, CV analyzer, job application, resume tips, ATS friendly resume, resume keywords, resume score, free ATS checker, resume grader, job application tips, career advice, resume builder, AI resume analyzer, resume screening, job seeker tools, career optimization, resume feedback, interview preparation, job hunting, recruitment tools, HR technology, resume formatting, professional resume',
  authors: [{ name: 'Love Patel', url: 'https://linkedin.com/in/love-patel-' }],
  creator: 'Love Patel',
  publisher: 'ATS Resume Analyzer',
  metadataBase: new URL('https://ats.lovexog.me'),
  alternates: {
    canonical: '/',
  },
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
    description: 'Get your free ATS score and actionable insights. Zero data storage, 100% privacy-first, open source. Built with ❤️ for job seekers everywhere.',
    type: 'website',
    locale: 'en_US',
    url: 'https://ats.lovexog.me',
    siteName: 'ATS Resume Analyzer',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'ATS Resume Analyzer - Free AI-Powered Resume Score',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ATS Resume Analyzer - Free AI Resume Score & ATS Check',
    description: 'Upload your resume and get instant ATS compatibility score. Zero data stored, blazingly fast, 100% open source. Built with ❤️ for job seekers.',
    images: ['/og-image.svg'],
  },
  icons: {
    icon: [
      { url: '/favicon.svg', type: 'image/svg+xml' },
    ],
    apple: '/apple-touch-icon.svg',
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
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.svg" />
        <meta name="theme-color" content="#3B82F6" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'WebApplication',
              name: 'ATS Resume Analyzer',
              description: 'Free AI-powered resume analyzer that helps job seekers understand how ATS systems read their resumes. Zero data storage, 100% privacy-first, open source.',
              applicationCategory: 'BusinessApplication',
              operatingSystem: 'Any',
              url: 'https://ats.lovexog.me',
              sameAs: [
                'https://resume-ats-mu.vercel.app',
                'https://github.com/itslovepatel/Resume-ATS',
                'https://linkedin.com/in/love-patel-'
              ],
              offers: {
                '@type': 'Offer',
                price: '0',
                priceCurrency: 'USD',
              },
              author: {
                '@type': 'Person',
                name: 'Love Patel',
                url: 'https://linkedin.com/in/love-patel-',
                sameAs: [
                  'https://github.com/itslovepatel',
                  'https://linkedin.com/in/love-patel-'
                ]
              },
              featureList: [
                'ATS Score Analysis',
                'Skills Detection',
                'Domain Classification',
                'Experience Analysis',
                'Project Review',
                'Issue Detection',
                'Smart Suggestions',
                'PDF Report Generation'
              ],
              keywords: 'ATS, resume analyzer, resume score, job search, career tools'
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
