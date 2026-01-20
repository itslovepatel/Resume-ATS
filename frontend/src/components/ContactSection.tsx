'use client';

import { useState } from 'react';
import { Send, Mail, Github, Building2, CheckCircle, Loader2 } from 'lucide-react';

export default function ContactSection() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    message: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Create mailto link with form data
    const subject = encodeURIComponent(`Custom ATS Solution Inquiry from ${formData.company || formData.name}`);
    const body = encodeURIComponent(
      `Name: ${formData.name}\nEmail: ${formData.email}\nCompany: ${formData.company}\n\nMessage:\n${formData.message}`
    );
    
    // Open email client
    window.location.href = `mailto:Lovepatelforwork@gmail.com?subject=${subject}&body=${body}`;
    
    // Simulate submission delay for UX
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSubmitted(true);
      setTimeout(() => setIsSubmitted(false), 5000);
    }, 1000);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <section id="contact" className="py-24 bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Left Content */}
          <div>
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-brand-50 border border-brand-200 rounded-full text-brand-700 text-sm font-medium mb-6">
              <Building2 className="w-4 h-4" />
              <span>For Enterprises & Businesses</span>
            </div>
            
            <h2 className="text-4xl lg:text-5xl font-bold font-display text-gray-900 mb-6">
              Need a <span className="text-brand-600">Custom ATS</span> Solution?
            </h2>
            
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              Looking to build a customized Applicant Tracking System or resume parsing 
              solution for your company? I can help you create tailored solutions that 
              fit your specific hiring workflow and requirements.
            </p>

            <div className="space-y-4 mb-8">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-brand-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <CheckCircle className="w-5 h-5 text-brand-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">Custom ATS Development</h4>
                  <p className="text-gray-600">Tailored applicant tracking systems built for your workflow</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-brand-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <CheckCircle className="w-5 h-5 text-brand-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">Resume Parsing APIs</h4>
                  <p className="text-gray-600">Integrate AI-powered resume parsing into your existing systems</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-brand-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <CheckCircle className="w-5 h-5 text-brand-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">White-label Solutions</h4>
                  <p className="text-gray-600">Rebrand and customize this tool for your organization</p>
                </div>
              </div>
            </div>

            {/* Contact Info */}
            <div className="flex flex-wrap items-center gap-6">
              <a
                href="mailto:Lovepatelforwork@gmail.com"
                className="flex items-center gap-2 text-gray-700 hover:text-brand-600 transition-colors"
              >
                <Mail className="w-5 h-5" />
                <span>Lovepatelforwork@gmail.com</span>
              </a>
              <a
                href="https://github.com/itslovepatel/Resume-ATS"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-gray-700 hover:text-brand-600 transition-colors"
              >
                <Github className="w-5 h-5" />
                <span>github.com/itslovepatel</span>
              </a>
            </div>
          </div>

          {/* Right - Contact Form */}
          <div className="bg-white rounded-3xl shadow-xl border border-gray-100 p-8 lg:p-10">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Get in Touch</h3>
            
            {isSubmitted ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-8 h-8 text-green-600" />
                </div>
                <h4 className="text-xl font-semibold text-gray-900 mb-2">Email Client Opened!</h4>
                <p className="text-gray-600">
                  Please send the email from your mail client. I'll get back to you soon!
                </p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                    Your Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all outline-none"
                    placeholder="John Doe"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all outline-none"
                    placeholder="john@company.com"
                  />
                </div>

                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
                    Company Name
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all outline-none"
                    placeholder="Acme Inc."
                  />
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                    Project Details *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    required
                    rows={4}
                    value={formData.message}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all outline-none resize-none"
                    placeholder="Tell me about your project requirements..."
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full py-4 bg-gradient-to-r from-brand-600 to-brand-500 text-white font-semibold rounded-xl hover:from-brand-700 hover:to-brand-600 transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-70"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>Opening Email Client...</span>
                    </>
                  ) : (
                    <>
                      <Send className="w-5 h-5" />
                      <span>Send Message</span>
                    </>
                  )}
                </button>

                <p className="text-sm text-gray-500 text-center">
                  This will open your default email client to send the message.
                </p>
              </form>
            )}
          </div>
        </div>

        {/* GitHub CTA */}
        <div className="mt-20 bg-gradient-to-r from-gray-900 to-gray-800 rounded-3xl p-8 lg:p-12 text-center">
          <Github className="w-12 h-12 text-white mx-auto mb-4" />
          <h3 className="text-2xl lg:text-3xl font-bold text-white mb-4">
            Open Source & Free Forever
          </h3>
          <p className="text-gray-300 text-lg max-w-2xl mx-auto mb-8">
            This project is open source! Feel free to star, fork, or contribute to make it even better. 
            Check out the code and help improve the resume analysis algorithms.
          </p>
          <a
            href="https://github.com/itslovepatel/Resume-ATS"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-3 px-8 py-4 bg-white text-gray-900 font-semibold rounded-xl hover:bg-gray-100 transition-colors"
          >
            <Github className="w-5 h-5" />
            <span>View on GitHub</span>
          </a>
        </div>
      </div>
    </section>
  );
}
