"""
ATS Scorer Service - Calculates ATS compatibility score and provides insights
"""
import re
from typing import Dict, List, Any
from app.models.schemas import (
    SkillsData, DomainInfo, ScoreBreakdown, 
    ATSIssue, Suggestion, KeywordsAnalysis
)


class ATSScorer:
    """Calculate ATS score and provide improvement suggestions"""
    
    # Important keywords by domain
    DOMAIN_KEYWORDS = {
        'Software / IT': [
            'developed', 'built', 'implemented', 'designed', 'architected',
            'optimized', 'deployed', 'integrated', 'automated', 'tested',
            'scalable', 'performance', 'api', 'database', 'cloud', 'agile'
        ],
        'Data / AI': [
            'analyzed', 'modeled', 'predicted', 'visualized', 'processed',
            'accuracy', 'precision', 'recall', 'f1', 'auc', 'training',
            'dataset', 'feature', 'pipeline', 'insight', 'recommendation'
        ],
        'Marketing': [
            'campaign', 'engagement', 'conversion', 'roi', 'reach',
            'impression', 'click-through', 'brand', 'content', 'strategy',
            'audience', 'growth', 'optimization', 'analytics', 'social'
        ],
        'Finance': [
            'analyzed', 'forecasted', 'modeled', 'valued', 'audited',
            'budgeted', 'reported', 'compliance', 'risk', 'revenue',
            'cost reduction', 'profit', 'investment', 'portfolio', 'reconciled'
        ],
        'General': [
            'managed', 'led', 'achieved', 'improved', 'increased',
            'reduced', 'delivered', 'collaborated', 'created', 'developed',
            'implemented', 'designed', 'analyzed', 'optimized', 'trained'
        ]
    }
    
    # Required sections for a complete resume
    REQUIRED_SECTIONS = [
        'experience', 'education', 'skills'
    ]
    
    RECOMMENDED_SECTIONS = [
        'summary', 'projects', 'certifications'
    ]
    
    def calculate_score(
        self, 
        parsed_data: Dict, 
        skills: SkillsData, 
        domain: DomainInfo,
        parsing_method: str = "standard",
        ocr_confidence: str = None
    ) -> Dict[str, Any]:
        """Calculate comprehensive ATS score
        
        Args:
            parsed_data: Parsed resume data
            skills: Extracted skills
            domain: Classified domain
            parsing_method: "standard" | "ocr" | "ocr_unavailable"
            ocr_confidence: "low" | "medium" | "high" (only when OCR used)
        """
        
        # OCR adjustment factors (reduce strictness for OCR text)
        is_ocr = parsing_method == "ocr"
        ocr_penalty_reduction = 0.7 if is_ocr else 1.0  # Reduce penalties by 30% for OCR
        ocr_min_score_floor = 25 if is_ocr else 0  # Minimum score floor for OCR
        
        raw_text = parsed_data.get('raw_text', '')
        sections = parsed_data.get('sections', {})
        formatting = parsed_data.get('formatting', {})
        candidate = parsed_data.get('candidate', {})
        experience = parsed_data.get('experience', {})
        projects = parsed_data.get('projects', [])
        
        # Calculate individual scores
        keyword_score = self._calculate_keyword_score(raw_text, domain.primary)
        section_score = self._calculate_section_score(sections, candidate)
        formatting_score = self._calculate_formatting_score(
            formatting, raw_text, is_ocr=is_ocr, penalty_factor=ocr_penalty_reduction
        )
        skill_score = self._calculate_skill_score(skills)
        experience_score = self._calculate_experience_score(experience)
        project_score = self._calculate_project_score(projects)
        
        # Create breakdown
        breakdown = ScoreBreakdown(
            keyword_relevance=keyword_score,
            section_completeness=section_score,
            formatting_score=formatting_score,
            skill_relevance=skill_score,
            experience_clarity=experience_score,
            project_impact=project_score
        )
        
        # Calculate weighted final score
        weights = {
            'keyword_relevance': 0.20,
            'section_completeness': 0.20,
            'formatting_score': 0.15,
            'skill_relevance': 0.20,
            'experience_clarity': 0.15,
            'project_impact': 0.10
        }
        
        final_score = int(
            keyword_score * weights['keyword_relevance'] +
            section_score * weights['section_completeness'] +
            formatting_score * weights['formatting_score'] +
            skill_score * weights['skill_relevance'] +
            experience_score * weights['experience_clarity'] +
            project_score * weights['project_impact']
        )
        
        # Apply OCR minimum score floor
        if is_ocr and final_score < ocr_min_score_floor:
            final_score = ocr_min_score_floor
        
        # Determine category
        category = self._get_score_category(final_score)
        
        # Identify issues
        issues = self._identify_issues(
            raw_text, sections, formatting, 
            skills, candidate, experience
        )
        
        # Add OCR notice if applicable
        if is_ocr:
            ocr_notice = ATSIssue(
                type='parsing',
                severity='Low',
                description=f'Resume was processed using OCR (scanned document detected). Confidence: {ocr_confidence or "unknown"}.',
                suggestion='For best results, upload a text-based PDF or DOCX file rather than a scanned document.'
            )
            issues.insert(0, ocr_notice)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(
            raw_text, domain.primary, skills, 
            sections, experience, projects
        )
        
        # Keywords analysis
        keywords_analysis = self._analyze_keywords(raw_text, domain.primary)
        
        return {
            'score': final_score,
            'breakdown': breakdown,
            'category': category,
            'issues': issues,
            'suggestions': suggestions,
            'keywords_analysis': keywords_analysis
        }
    
    def _calculate_keyword_score(self, text: str, domain: str) -> int:
        """Score based on keyword presence and relevance"""
        text_lower = text.lower()
        keywords = self.DOMAIN_KEYWORDS.get(domain, self.DOMAIN_KEYWORDS['General'])
        
        found = sum(1 for kw in keywords if kw in text_lower)
        
        # Also check for general action verbs
        action_verbs = [
            'achieved', 'built', 'created', 'delivered', 'enhanced',
            'generated', 'improved', 'launched', 'managed', 'optimized'
        ]
        verb_count = sum(1 for v in action_verbs if v in text_lower)
        
        keyword_ratio = found / len(keywords)
        verb_ratio = min(1.0, verb_count / 5)
        
        score = int((keyword_ratio * 60) + (verb_ratio * 40))
        return min(100, score)
    
    def _calculate_section_score(self, sections: Dict, candidate: Any) -> int:
        """Score based on section completeness"""
        score = 0
        
        # Required sections (60 points)
        for section in self.REQUIRED_SECTIONS:
            if section in sections and len(sections[section].strip()) > 50:
                score += 20
        
        # Contact info (20 points)
        candidate_dict = candidate.dict() if hasattr(candidate, 'dict') else candidate
        if candidate_dict.get('email'):
            score += 10
        if candidate_dict.get('phone'):
            score += 10
        
        # Recommended sections (20 points)
        for section in self.RECOMMENDED_SECTIONS:
            if section in sections and len(sections[section].strip()) > 20:
                score += 7
        
        return min(100, score)
    
    def _calculate_formatting_score(
        self, 
        formatting: Dict, 
        text: str,
        is_ocr: bool = False,
        penalty_factor: float = 1.0
    ) -> int:
        """Score based on formatting quality
        
        Args:
            formatting: Formatting metadata
            text: Raw resume text
            is_ocr: Whether text was extracted via OCR
            penalty_factor: Multiplier for penalties (reduced for OCR)
        """
        score = 100
        
        # Penalize for tables (reduced for OCR since detection may be inaccurate)
        if formatting.get('has_tables'):
            score -= int(15 * penalty_factor)
        
        # Penalize for images (reduced for OCR)
        if formatting.get('has_images'):
            score -= int(10 * penalty_factor)
        
        # Check word count (too short or too long)
        # More lenient for OCR since extraction may miss some text
        word_count = formatting.get('word_count', len(text.split()))
        min_words = 150 if is_ocr else 200
        if word_count < min_words:
            score -= int(20 * penalty_factor)
        elif word_count > 1500:
            score -= int(10 * penalty_factor)
        
        # Check for good structure (bullet points)
        # More lenient for OCR since bullet detection may fail
        bullet_count = text.count('•') + text.count('●') + text.count('-')
        min_bullets = 3 if is_ocr else 5
        if bullet_count < min_bullets:
            score -= int(10 * penalty_factor)
        elif bullet_count > 50:
            score -= int(5 * penalty_factor)
        
        # Check for special characters that might cause issues
        # Skip this check for OCR since it introduces artifacts
        if not is_ocr:
            special_chars = ['→', '★', '☆', '✓', '✔', '✗', '❖', '◆']
            for char in special_chars:
                if char in text:
                    score -= 3
        
        return max(0, min(100, score))
    
    def _calculate_skill_score(self, skills: SkillsData) -> int:
        """Score based on skills quality"""
        score = 0
        
        # Base score on skill count
        if skills.total_count >= 15:
            score += 40
        elif skills.total_count >= 10:
            score += 30
        elif skills.total_count >= 5:
            score += 20
        else:
            score += 10
        
        # Bonus for technical skills
        if skills.programming_languages:
            score += 15
        if skills.frameworks:
            score += 15
        if skills.tools:
            score += 10
        if skills.databases:
            score += 10
        
        # Bonus for soft skills
        if skills.soft_skills:
            score += 10
        
        return min(100, score)
    
    def _calculate_experience_score(self, experience: Any) -> int:
        """Score based on experience quality"""
        if not experience:
            return 30
        
        exp_dict = experience.dict() if hasattr(experience, 'dict') else experience
        positions = exp_dict.get('positions', [])
        
        if not positions:
            return 30
        
        score = 30  # Base score
        
        # Score for number of positions
        if len(positions) >= 3:
            score += 20
        elif len(positions) >= 2:
            score += 15
        else:
            score += 10
        
        # Score for bullet quality
        avg_quality = exp_dict.get('overall_quality', 0)
        score += int(avg_quality * 0.5)
        
        return min(100, score)
    
    def _calculate_project_score(self, projects: List) -> int:
        """Score based on projects quality"""
        if not projects:
            return 40  # No projects is not terrible
        
        score = 50  # Base score for having projects
        
        # Score based on project count and quality
        for project in projects[:5]:
            project_dict = project.dict() if hasattr(project, 'dict') else project
            project_score = project_dict.get('score', 0)
            score += project_score * 0.1
        
        return min(100, int(score))
    
    def _get_score_category(self, score: int) -> str:
        """Get score category label"""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Needs Improvement'
        else:
            return 'Poor'
    
    def _identify_issues(
        self, text: str, sections: Dict, formatting: Dict,
        skills: SkillsData, candidate: Any, experience: Any
    ) -> List[ATSIssue]:
        """Identify ATS compatibility issues"""
        issues = []
        
        # Formatting issues
        if formatting.get('has_tables'):
            issues.append(ATSIssue(
                type='formatting',
                severity='High',
                description='Tables detected in resume',
                suggestion='Replace tables with simple bullet points. ATS systems often cannot parse table content correctly.'
            ))
        
        if formatting.get('has_images'):
            issues.append(ATSIssue(
                type='formatting',
                severity='Medium',
                description='Images or graphics detected',
                suggestion='Remove images, logos, and icons. Use text-only formatting for better ATS compatibility.'
            ))
        
        # Contact info issues
        candidate_dict = candidate.dict() if hasattr(candidate, 'dict') else candidate
        if not candidate_dict.get('email'):
            issues.append(ATSIssue(
                type='contact',
                severity='High',
                description='Email address not detected',
                suggestion='Add a clearly formatted email address at the top of your resume.'
            ))
        
        if not candidate_dict.get('phone'):
            issues.append(ATSIssue(
                type='contact',
                severity='Medium',
                description='Phone number not detected',
                suggestion='Add a phone number in standard format (e.g., (555) 123-4567).'
            ))
        
        # Section issues
        if 'experience' not in sections:
            issues.append(ATSIssue(
                type='section',
                severity='High',
                description='Work Experience section not detected',
                suggestion='Add a clearly labeled "Experience" or "Work Experience" section header.'
            ))
        
        if 'education' not in sections:
            issues.append(ATSIssue(
                type='section',
                severity='Medium',
                description='Education section not detected',
                suggestion='Add a clearly labeled "Education" section header.'
            ))
        
        if 'skills' not in sections:
            issues.append(ATSIssue(
                type='section',
                severity='Medium',
                description='Skills section not detected',
                suggestion='Add a dedicated "Skills" section to highlight your technical and soft skills.'
            ))
        
        # Skills issues
        if skills.total_count < 5:
            issues.append(ATSIssue(
                type='skills',
                severity='Medium',
                description='Limited skills detected',
                suggestion='Add more relevant skills. Include programming languages, tools, and soft skills.'
            ))
        
        # Content issues
        text_lower = text.lower()
        word_count = len(text.split())
        
        if word_count < 200:
            issues.append(ATSIssue(
                type='content',
                severity='High',
                description='Resume appears too short',
                suggestion='Add more detail about your experience, projects, and achievements.'
            ))
        
        # Check for generic descriptions
        generic_phrases = [
            'responsible for', 'duties included', 'helped with',
            'worked on', 'assisted in'
        ]
        generic_count = sum(1 for p in generic_phrases if p in text_lower)
        if generic_count >= 3:
            issues.append(ATSIssue(
                type='content',
                severity='Medium',
                description='Generic job descriptions detected',
                suggestion='Replace generic phrases like "responsible for" with action verbs like "developed", "led", or "implemented".'
            ))
        
        # Check for metrics
        has_metrics = bool(re.search(r'\d+%|\$[\d,]+|\d+\s*(users|customers|clients|employees|projects)', text))
        if not has_metrics:
            issues.append(ATSIssue(
                type='content',
                severity='Medium',
                description='No quantifiable achievements detected',
                suggestion='Add metrics and numbers to demonstrate impact (e.g., "Increased sales by 25%", "Managed team of 5").'
            ))
        
        return issues
    
    def _generate_suggestions(
        self, text: str, domain: str, skills: SkillsData,
        sections: Dict, experience: Any, projects: List
    ) -> List[Suggestion]:
        """Generate improvement suggestions"""
        suggestions = []
        text_lower = text.lower()
        
        # Skill suggestions
        missing_skills = self._get_missing_skills(skills, domain)
        if missing_skills:
            suggestions.append(Suggestion(
                category='Skills',
                title='Add in-demand skills',
                description=f'Consider adding these high-demand skills for {domain} roles:',
                priority='High',
                examples=missing_skills[:5]
            ))
        
        # Action verb suggestions
        weak_verbs = ['helped', 'worked', 'assisted', 'was responsible']
        strong_verbs = ['developed', 'implemented', 'architected', 'delivered', 'optimized']
        
        has_weak_verbs = any(v in text_lower for v in weak_verbs)
        if has_weak_verbs:
            suggestions.append(Suggestion(
                category='Content',
                title='Use stronger action verbs',
                description='Replace weak verbs with powerful action verbs to make your achievements stand out.',
                priority='High',
                examples=[f'Instead of "helped develop", use "developed"',
                         f'Instead of "worked on", use "led" or "implemented"',
                         f'Instead of "was responsible for", use "managed" or "oversaw"']
            ))
        
        # Quantification suggestions
        if not re.search(r'\d+%', text):
            suggestions.append(Suggestion(
                category='Impact',
                title='Add quantifiable achievements',
                description='Include specific metrics and numbers to demonstrate your impact.',
                priority='High',
                examples=['Increased efficiency by 40%',
                         'Reduced costs by $50,000 annually',
                         'Managed team of 8 engineers',
                         'Delivered 15 projects on time']
            ))
        
        # Section suggestions
        if 'summary' not in sections:
            suggestions.append(Suggestion(
                category='Structure',
                title='Add a professional summary',
                description='A 2-3 sentence summary at the top helps recruiters quickly understand your value proposition.',
                priority='Medium',
                examples=[f'Results-driven {domain} professional with X years of experience...']
            ))
        
        # Project suggestions
        if not projects or len(projects) < 2:
            suggestions.append(Suggestion(
                category='Projects',
                title='Highlight more projects',
                description='Adding 2-3 relevant projects can significantly strengthen your resume.',
                priority='Medium',
                examples=['Include project name, technologies used, and measurable impact']
            ))
        
        # Keywords suggestions
        domain_keywords = self.DOMAIN_KEYWORDS.get(domain, self.DOMAIN_KEYWORDS['General'])
        missing_keywords = [kw for kw in domain_keywords if kw not in text_lower][:5]
        if missing_keywords:
            suggestions.append(Suggestion(
                category='Keywords',
                title='Add industry keywords',
                description=f'These keywords are commonly used in {domain} job descriptions:',
                priority='Medium',
                examples=missing_keywords
            ))
        
        return suggestions
    
    def _get_missing_skills(self, skills: SkillsData, domain: str) -> List[str]:
        """Get skills that are commonly required but missing"""
        domain_skills = {
            'Software / IT': ['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'Git', 'SQL', 'REST API'],
            'Data / AI': ['Python', 'SQL', 'TensorFlow', 'Pandas', 'Machine Learning', 'Statistics', 'Tableau'],
            'Marketing': ['Google Analytics', 'SEO', 'Content Strategy', 'HubSpot', 'Social Media Marketing'],
            'Finance': ['Excel', 'Financial Modeling', 'SQL', 'Power BI', 'Risk Analysis'],
            'Design': ['Figma', 'Adobe XD', 'User Research', 'Prototyping', 'Design Systems'],
            'HR': ['Workday', 'ATS', 'Recruiting', 'Employee Relations', 'HRIS'],
            'Sales': ['Salesforce', 'CRM', 'Pipeline Management', 'Negotiation', 'Cold Calling']
        }
        
        required = domain_skills.get(domain, domain_skills['Software / IT'])
        current = set(
            s.lower() for s in 
            skills.programming_languages + skills.frameworks + 
            skills.tools + skills.databases + skills.soft_skills
        )
        
        missing = [s for s in required if s.lower() not in current]
        return missing
    
    def _analyze_keywords(self, text: str, domain: str) -> KeywordsAnalysis:
        """Analyze keyword presence and recommendations"""
        text_lower = text.lower()
        
        # Get domain keywords
        domain_keywords = self.DOMAIN_KEYWORDS.get(domain, self.DOMAIN_KEYWORDS['General'])
        
        found = [kw for kw in domain_keywords if kw in text_lower]
        missing = [kw for kw in domain_keywords if kw not in text_lower]
        
        # Recommended keywords from other domains that might be relevant
        general_keywords = self.DOMAIN_KEYWORDS['General']
        recommended = [kw for kw in general_keywords if kw not in text_lower and kw not in missing]
        
        return KeywordsAnalysis(
            found=found,
            missing=missing[:10],
            recommended=recommended[:5]
        )
