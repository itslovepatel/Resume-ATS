"""
Report Generator Service - Generates PDF reports from analysis results
"""
from io import BytesIO
from datetime import datetime
import fitz  # PyMuPDF


class ReportGenerator:
    """Generate PDF reports from resume analysis"""
    
    def generate_pdf(self, analysis_data: dict) -> bytes:
        """Generate a PDF report from analysis data"""
        doc = fitz.open()
        
        # Page 1: Summary
        page = doc.new_page(width=595, height=842)  # A4 size
        
        # Header
        self._draw_header(page, analysis_data)
        
        # ATS Score Section
        self._draw_score_section(page, analysis_data)
        
        # Candidate Info
        self._draw_candidate_section(page, analysis_data)
        
        # Domain & Skills
        self._draw_skills_section(page, analysis_data)
        
        # Page 2: Issues & Suggestions
        page2 = doc.new_page(width=595, height=842)
        self._draw_issues_section(page2, analysis_data)
        self._draw_suggestions_section(page2, analysis_data)
        
        # Save to bytes
        pdf_bytes = doc.tobytes()
        doc.close()
        
        return pdf_bytes
    
    def _draw_header(self, page, data):
        """Draw report header"""
        # Title
        page.insert_text(
            (50, 50),
            "ATS Resume Analysis Report",
            fontsize=24,
            fontname="helv",
            color=(0.15, 0.3, 0.9)
        )
        
        # Date
        page.insert_text(
            (50, 75),
            f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            fontsize=10,
            fontname="helv",
            color=(0.5, 0.5, 0.5)
        )
        
        # Line separator
        page.draw_line((50, 85), (545, 85), color=(0.8, 0.8, 0.8), width=1)
    
    def _draw_score_section(self, page, data):
        """Draw ATS score section"""
        score = data.get('ats_score', 0)
        category = data.get('score_category', 'Unknown')
        
        # Score box
        y_start = 110
        
        # Background rectangle for score
        if score >= 80:
            color = (0.13, 0.77, 0.37)  # Green
        elif score >= 60:
            color = (0.96, 0.62, 0.04)  # Orange
        else:
            color = (0.94, 0.27, 0.27)  # Red
        
        page.draw_rect(fitz.Rect(50, y_start, 150, y_start + 80), color=color, fill=color)
        
        # Score number
        page.insert_text(
            (70, y_start + 50),
            str(score),
            fontsize=36,
            fontname="helv",
            color=(1, 1, 1)
        )
        page.insert_text(
            (115, y_start + 50),
            "/100",
            fontsize=14,
            fontname="helv",
            color=(1, 1, 1)
        )
        
        # Category label
        page.insert_text(
            (70, y_start + 70),
            category,
            fontsize=10,
            fontname="helv",
            color=(1, 1, 1)
        )
        
        # Score breakdown
        breakdown = data.get('score_breakdown', {})
        x_start = 170
        y_pos = y_start + 15
        
        page.insert_text((x_start, y_pos), "Score Breakdown:", fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
        y_pos += 20
        
        breakdown_items = [
            ('Keyword Relevance', breakdown.get('keyword_relevance', 0)),
            ('Section Completeness', breakdown.get('section_completeness', 0)),
            ('Formatting', breakdown.get('formatting_score', 0)),
            ('Skill Relevance', breakdown.get('skill_relevance', 0)),
            ('Experience Clarity', breakdown.get('experience_clarity', 0)),
            ('Project Impact', breakdown.get('project_impact', 0)),
        ]
        
        for label, value in breakdown_items:
            page.insert_text((x_start, y_pos), f"• {label}: {value}/100", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
            y_pos += 12
    
    def _draw_candidate_section(self, page, data):
        """Draw candidate information section"""
        candidate = data.get('candidate', {})
        y_start = 210
        
        page.insert_text((50, y_start), "Candidate Information", fontsize=14, fontname="helv", color=(0.2, 0.2, 0.2))
        page.draw_line((50, y_start + 5), (200, y_start + 5), color=(0.15, 0.3, 0.9), width=2)
        
        y_pos = y_start + 25
        
        if candidate.get('name'):
            page.insert_text((50, y_pos), f"Name: {candidate['name']}", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
            y_pos += 15
        if candidate.get('email'):
            page.insert_text((50, y_pos), f"Email: {candidate['email']}", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
            y_pos += 15
        if candidate.get('phone'):
            page.insert_text((50, y_pos), f"Phone: {candidate['phone']}", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
            y_pos += 15
        if candidate.get('location'):
            page.insert_text((50, y_pos), f"Location: {candidate['location']}", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
            y_pos += 15
        
        # Domain
        domain = data.get('domain', {})
        y_pos += 10
        page.insert_text((50, y_pos), f"Detected Domain: {domain.get('primary', 'Unknown')} ({int(domain.get('confidence', 0) * 100)}% confidence)", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    
    def _draw_skills_section(self, page, data):
        """Draw skills section"""
        skills = data.get('skills', {})
        y_start = 330
        
        page.insert_text((50, y_start), "Skills Detected", fontsize=14, fontname="helv", color=(0.2, 0.2, 0.2))
        page.draw_line((50, y_start + 5), (150, y_start + 5), color=(0.15, 0.3, 0.9), width=2)
        
        y_pos = y_start + 25
        
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
                page.insert_text((50, y_pos), f"{category}:", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                y_pos += 12
                page.insert_text((60, y_pos), skills_text, fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
                y_pos += 18
        
        # Experience summary
        experience = data.get('experience', {})
        y_pos += 10
        page.insert_text((50, y_pos), "Experience Summary", fontsize=14, fontname="helv", color=(0.2, 0.2, 0.2))
        page.draw_line((50, y_pos + 5), (180, y_pos + 5), color=(0.15, 0.3, 0.9), width=2)
        y_pos += 25
        
        total_years = experience.get('total_years', 0)
        positions = experience.get('positions', [])
        quality = experience.get('overall_quality', 0)
        
        page.insert_text((50, y_pos), f"Total Experience: {total_years} years", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        y_pos += 15
        page.insert_text((50, y_pos), f"Positions Found: {len(positions)}", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        y_pos += 15
        page.insert_text((50, y_pos), f"Content Quality Score: {quality}/100", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        
        # Keywords
        keywords = data.get('keywords_analysis', {})
        y_pos += 30
        page.insert_text((50, y_pos), "Keywords Analysis", fontsize=14, fontname="helv", color=(0.2, 0.2, 0.2))
        page.draw_line((50, y_pos + 5), (170, y_pos + 5), color=(0.15, 0.3, 0.9), width=2)
        y_pos += 25
        
        found = keywords.get('found', [])
        missing = keywords.get('missing', [])
        
        page.insert_text((50, y_pos), f"✓ Found ({len(found)}): {', '.join(found[:6])}", fontsize=9, fontname="helv", color=(0.13, 0.55, 0.13))
        y_pos += 15
        page.insert_text((50, y_pos), f"✗ Missing ({len(missing)}): {', '.join(missing[:6])}", fontsize=9, fontname="helv", color=(0.8, 0.2, 0.2))
    
    def _draw_issues_section(self, page2, data):
        """Draw issues section on page 2"""
        issues = data.get('issues', [])
        
        # Header
        page2.insert_text((50, 50), "ATS Issues Detected", fontsize=18, fontname="helv", color=(0.8, 0.2, 0.2))
        page2.draw_line((50, 60), (545, 60), color=(0.8, 0.8, 0.8), width=1)
        
        y_pos = 85
        
        if not issues:
            page2.insert_text((50, y_pos), "✓ No major issues detected! Your resume is ATS-friendly.", fontsize=11, fontname="helv", color=(0.13, 0.55, 0.13))
            return 120
        
        for issue in issues[:8]:
            severity = issue.get('severity', 'Medium')
            if severity == 'High':
                color = (0.8, 0.2, 0.2)
                marker = "●"
            elif severity == 'Medium':
                color = (0.85, 0.55, 0.0)
                marker = "●"
            else:
                color = (0.4, 0.4, 0.4)
                marker = "○"
            
            page2.insert_text((50, y_pos), f"{marker} [{severity}] {issue.get('description', '')}", fontsize=10, fontname="helv", color=color)
            y_pos += 14
            
            # Suggestion in lighter color
            suggestion = issue.get('suggestion', '')
            if suggestion and len(suggestion) > 80:
                suggestion = suggestion[:77] + "..."
            page2.insert_text((65, y_pos), f"→ {suggestion}", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
            y_pos += 20
        
        return y_pos
    
    def _draw_suggestions_section(self, page2, data):
        """Draw suggestions section"""
        suggestions = data.get('suggestions', [])
        
        y_start = 380
        page2.insert_text((50, y_start), "Improvement Suggestions", fontsize=18, fontname="helv", color=(0.15, 0.3, 0.9))
        page2.draw_line((50, y_start + 10), (545, y_start + 10), color=(0.8, 0.8, 0.8), width=1)
        
        y_pos = y_start + 35
        
        if not suggestions:
            page2.insert_text((50, y_pos), "✓ Your resume is well-optimized! No major improvements needed.", fontsize=11, fontname="helv", color=(0.13, 0.55, 0.13))
            return
        
        for i, suggestion in enumerate(suggestions[:6], 1):
            category = suggestion.get('category', '')
            title = suggestion.get('title', '')
            
            page2.insert_text((50, y_pos), f"{i}. [{category}] {title}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            y_pos += 14
            
            description = suggestion.get('description', '')
            if len(description) > 90:
                description = description[:87] + "..."
            page2.insert_text((65, y_pos), description, fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
            y_pos += 12
            
            # Examples
            examples = suggestion.get('examples', [])[:2]
            for example in examples:
                if len(example) > 70:
                    example = example[:67] + "..."
                page2.insert_text((75, y_pos), f"• {example}", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))
                y_pos += 11
            
            y_pos += 8
        
        # Footer
        page2.insert_text((50, 800), "Generated by ATS Resume Analyzer | www.atsanalyzer.com", fontsize=8, fontname="helv", color=(0.6, 0.6, 0.6))
