"""
Report Generator Service - Generates PDF reports from analysis results
"""
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


class ReportGenerator:
    """Generate PDF reports from resume analysis"""
    
    def __init__(self):
        self.width, self.height = A4
        self.margin = 50
        
    def generate_pdf(self, analysis_data: dict) -> bytes:
        """Generate a PDF report from analysis data"""
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Page 1: Summary
        self._draw_header(c, analysis_data)
        self._draw_score_section(c, analysis_data)
        self._draw_candidate_section(c, analysis_data)
        self._draw_skills_section(c, analysis_data)
        
        c.showPage()
        
        # Page 2: Issues & Suggestions
        self._draw_issues_section(c, analysis_data)
        self._draw_suggestions_section(c, analysis_data)
        
        c.save()
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _draw_header(self, c, data):
        """Draw report header"""
        # Title
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(HexColor('#2563EB'))
        c.drawString(self.margin, self.height - 50, "ATS Resume Analysis Report")
        
        # Date
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor('#6B7280'))
        c.drawString(self.margin, self.height - 75, 
                    f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        
        # Line separator
        c.setStrokeColor(HexColor('#E5E7EB'))
        c.line(self.margin, self.height - 85, self.width - self.margin, self.height - 85)
    
    def _draw_score_section(self, c, data):
        """Draw ATS score section"""
        score = data.get('ats_score', 0)
        category = data.get('score_category', 'Unknown')
        
        y_start = self.height - 110
        
        # Score box color
        if score >= 80:
            color = HexColor('#22C55E')  # Green
        elif score >= 60:
            color = HexColor('#F59E0B')  # Orange
        else:
            color = HexColor('#EF4444')  # Red
        
        # Draw score box
        c.setFillColor(color)
        c.rect(self.margin, y_start - 80, 100, 80, fill=1, stroke=0)
        
        # Score number
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 36)
        c.drawString(self.margin + 15, y_start - 55, str(score))
        c.setFont("Helvetica", 14)
        c.drawString(self.margin + 60, y_start - 55, "/100")
        
        # Category label
        c.setFont("Helvetica", 10)
        c.drawString(self.margin + 15, y_start - 72, category)
        
        # Score breakdown
        breakdown = data.get('score_breakdown', {})
        x_start = self.margin + 120
        
        c.setFillColor(HexColor('#1F2937'))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_start, y_start - 15, "Score Breakdown:")
        
        y_pos = y_start - 32
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor('#4B5563'))
        
        breakdown_items = [
            ('Keyword Relevance', breakdown.get('keyword_relevance', 0)),
            ('Section Completeness', breakdown.get('section_completeness', 0)),
            ('Formatting', breakdown.get('formatting_score', 0)),
            ('Skill Relevance', breakdown.get('skill_relevance', 0)),
            ('Experience Clarity', breakdown.get('experience_clarity', 0)),
            ('Project Impact', breakdown.get('project_impact', 0)),
        ]
        
        for label, value in breakdown_items:
            c.drawString(x_start, y_pos, f"• {label}: {value}/100")
            y_pos -= 12
    
    def _draw_candidate_section(self, c, data):
        """Draw candidate information section"""
        candidate = data.get('candidate', {})
        y_start = self.height - 220
        
        c.setFillColor(HexColor('#1F2937'))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.margin, y_start, "Candidate Information")
        
        c.setStrokeColor(HexColor('#2563EB'))
        c.setLineWidth(2)
        c.line(self.margin, y_start - 5, self.margin + 150, y_start - 5)
        
        y_pos = y_start - 25
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor('#4B5563'))
        
        if candidate.get('name'):
            c.drawString(self.margin, y_pos, f"Name: {candidate['name']}")
            y_pos -= 15
        if candidate.get('email'):
            c.drawString(self.margin, y_pos, f"Email: {candidate['email']}")
            y_pos -= 15
        if candidate.get('phone'):
            c.drawString(self.margin, y_pos, f"Phone: {candidate['phone']}")
            y_pos -= 15
        if candidate.get('location'):
            c.drawString(self.margin, y_pos, f"Location: {candidate['location']}")
            y_pos -= 15
        
        # Domain
        domain = data.get('domain', {})
        y_pos -= 10
        c.drawString(self.margin, y_pos, 
                    f"Detected Domain: {domain.get('primary', 'Unknown')} ({int(domain.get('confidence', 0) * 100)}% confidence)")
    
    def _draw_skills_section(self, c, data):
        """Draw skills section"""
        skills = data.get('skills', {})
        y_start = self.height - 350
        
        c.setFillColor(HexColor('#1F2937'))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.margin, y_start, "Skills Detected")
        
        c.setStrokeColor(HexColor('#2563EB'))
        c.setLineWidth(2)
        c.line(self.margin, y_start - 5, self.margin + 100, y_start - 5)
        
        y_pos = y_start - 25
        
        skill_categories = [
            ('Programming Languages', skills.get('programming_languages', [])),
            ('Frameworks', skills.get('frameworks', [])),
            ('Tools', skills.get('tools', [])),
            ('Databases', skills.get('databases', [])),
            ('Soft Skills', skills.get('soft_skills', [])),
        ]
        
        for category, skill_list in skill_categories:
            if skill_list:
                skills_text = ', '.join(skill_list[:8])
                if len(skill_list) > 8:
                    skills_text += f" (+{len(skill_list) - 8} more)"
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(HexColor('#1F2937'))
                c.drawString(self.margin, y_pos, f"{category}:")
                y_pos -= 12
                c.setFont("Helvetica", 9)
                c.setFillColor(HexColor('#6B7280'))
                c.drawString(self.margin + 10, y_pos, skills_text)
                y_pos -= 18
        
        # Experience summary
        experience = data.get('experience', {})
        y_pos -= 10
        c.setFillColor(HexColor('#1F2937'))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.margin, y_pos, "Experience Summary")
        
        c.setStrokeColor(HexColor('#2563EB'))
        c.line(self.margin, y_pos - 5, self.margin + 130, y_pos - 5)
        y_pos -= 25
        
        total_years = experience.get('total_years', 0)
        positions = experience.get('positions', [])
        quality = experience.get('overall_quality', 0)
        
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor('#4B5563'))
        c.drawString(self.margin, y_pos, f"Total Experience: {total_years} years")
        y_pos -= 15
        c.drawString(self.margin, y_pos, f"Positions Found: {len(positions)}")
        y_pos -= 15
        c.drawString(self.margin, y_pos, f"Content Quality Score: {quality}/100")
        
        # Keywords
        keywords = data.get('keywords_analysis', {})
        y_pos -= 30
        c.setFillColor(HexColor('#1F2937'))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.margin, y_pos, "Keywords Analysis")
        
        c.setStrokeColor(HexColor('#2563EB'))
        c.line(self.margin, y_pos - 5, self.margin + 120, y_pos - 5)
        y_pos -= 25
        
        found = keywords.get('found', [])
        missing = keywords.get('missing', [])
        
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor('#16A34A'))
        c.drawString(self.margin, y_pos, f"Found ({len(found)}): {', '.join(found[:6])}")
        y_pos -= 15
        c.setFillColor(HexColor('#DC2626'))
        c.drawString(self.margin, y_pos, f"Missing ({len(missing)}): {', '.join(missing[:6])}")
    
    def _draw_issues_section(self, c, data):
        """Draw issues section on page 2"""
        issues = data.get('issues', [])
        
        # Header
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(HexColor('#DC2626'))
        c.drawString(self.margin, self.height - 50, "ATS Issues Detected")
        
        c.setStrokeColor(HexColor('#E5E7EB'))
        c.line(self.margin, self.height - 60, self.width - self.margin, self.height - 60)
        
        y_pos = self.height - 85
        
        if not issues:
            c.setFont("Helvetica", 11)
            c.setFillColor(HexColor('#16A34A'))
            c.drawString(self.margin, y_pos, "No major issues detected! Your resume is ATS-friendly.")
            return
        
        for issue in issues[:8]:
            severity = issue.get('severity', 'Medium')
            if severity == 'High':
                c.setFillColor(HexColor('#DC2626'))
            elif severity == 'Medium':
                c.setFillColor(HexColor('#D97706'))
            else:
                c.setFillColor(HexColor('#6B7280'))
            
            c.setFont("Helvetica-Bold", 10)
            desc = issue.get('description', '')[:70]
            c.drawString(self.margin, y_pos, f"[{severity}] {desc}")
            y_pos -= 14
            
            # Suggestion
            suggestion = issue.get('suggestion', '')
            if len(suggestion) > 80:
                suggestion = suggestion[:77] + "..."
            c.setFont("Helvetica", 8)
            c.setFillColor(HexColor('#6B7280'))
            c.drawString(self.margin + 15, y_pos, f"-> {suggestion}")
            y_pos -= 20
    
    def _draw_suggestions_section(self, c, data):
        """Draw suggestions section"""
        suggestions = data.get('suggestions', [])
        
        y_start = self.height - 400
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(HexColor('#2563EB'))
        c.drawString(self.margin, y_start, "Improvement Suggestions")
        
        c.setStrokeColor(HexColor('#E5E7EB'))
        c.line(self.margin, y_start - 10, self.width - self.margin, y_start - 10)
        
        y_pos = y_start - 35
        
        if not suggestions:
            c.setFont("Helvetica", 11)
            c.setFillColor(HexColor('#16A34A'))
            c.drawString(self.margin, y_pos, "Your resume is well-optimized! No major improvements needed.")
            return
        
        for i, suggestion in enumerate(suggestions[:6], 1):
            category = suggestion.get('category', '')
            title = suggestion.get('title', '')
            
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(HexColor('#1F2937'))
            c.drawString(self.margin, y_pos, f"{i}. [{category}] {title}")
            y_pos -= 14
            
            description = suggestion.get('description', '')
            if len(description) > 90:
                description = description[:87] + "..."
            c.setFont("Helvetica", 8)
            c.setFillColor(HexColor('#6B7280'))
            c.drawString(self.margin + 15, y_pos, description)
            y_pos -= 12
            
            # Examples
            examples = suggestion.get('examples', [])[:2]
            for example in examples:
                if len(example) > 70:
                    example = example[:67] + "..."
                c.drawString(self.margin + 25, y_pos, f"- {example}")
                y_pos -= 11
            
            y_pos -= 8
        
        # Footer
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor('#9CA3AF'))
        c.drawString(self.margin, 45, "Generated by ATS Resume Analyzer")
        c.drawString(self.margin, 35, "https://ats.lovexog.me | https://resume-ats-mu.vercel.app")
        c.drawString(self.margin, 25, "Open Source: https://github.com/itslovepatel/Resume-ATS | LinkedIn: https://linkedin.com/in/love-patel-")
        c.setFillColor(HexColor('#EF4444'))
        c.drawString(self.margin, 15, "Built with ❤️ for job seekers everywhere")
