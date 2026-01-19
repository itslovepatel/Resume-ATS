"""
Domain Classifier Service - Classifies resume into job domain categories
Supports 20+ industries for comprehensive resume analysis
"""
import re
from typing import Dict, List, Tuple
from app.models.schemas import DomainInfo, SkillsData


class DomainClassifier:
    """Classify resume into job domain categories across all major industries"""
    
    # Comprehensive domain keywords covering 20+ industries
    DOMAIN_KEYWORDS = {
        # ==================== TECHNOLOGY ====================
        'Software / IT': {
            'keywords': [
                'software', 'developer', 'engineer', 'programming', 'coding',
                'web', 'frontend', 'backend', 'fullstack', 'full-stack',
                'api', 'devops', 'cloud', 'microservices', 'architecture',
                'agile', 'scrum', 'sprint', 'deployment', 'ci/cd',
                'testing', 'debugging', 'algorithm', 'data structure',
                'mobile', 'ios', 'android', 'app development', 'saas',
                'system design', 'scalability', 'performance optimization'
            ],
            'skills': [
                'python', 'java', 'javascript', 'react', 'angular', 'vue',
                'node.js', 'docker', 'kubernetes', 'aws', 'git', 'linux',
                'typescript', 'golang', 'rust', 'c++', 'c#'
            ],
            'titles': [
                'software engineer', 'developer', 'programmer', 'sde',
                'tech lead', 'engineering manager', 'devops engineer',
                'solutions architect', 'cto', 'full stack developer'
            ]
        },
        'Data Science / AI': {
            'keywords': [
                'data', 'machine learning', 'ml', 'artificial intelligence', 'ai',
                'deep learning', 'neural network', 'nlp', 'computer vision',
                'analytics', 'statistics', 'modeling', 'prediction',
                'big data', 'etl', 'pipeline', 'warehouse', 'visualization',
                'business intelligence', 'bi', 'mining', 'clustering',
                'regression', 'classification', 'recommendation system',
                'a/b testing', 'hypothesis', 'feature engineering'
            ],
            'skills': [
                'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas',
                'numpy', 'sql', 'spark', 'hadoop', 'tableau', 'power bi',
                'r', 'sas', 'databricks', 'snowflake', 'airflow', 'dbt'
            ],
            'titles': [
                'data scientist', 'data analyst', 'ml engineer', 'data engineer',
                'ai engineer', 'research scientist', 'analytics manager',
                'business analyst', 'quantitative analyst'
            ]
        },
        'Cybersecurity': {
            'keywords': [
                'security', 'cybersecurity', 'infosec', 'penetration testing',
                'vulnerability', 'threat', 'incident response', 'soc',
                'firewall', 'encryption', 'authentication', 'authorization',
                'compliance', 'audit', 'risk assessment', 'forensics',
                'malware', 'phishing', 'intrusion detection', 'siem',
                'zero trust', 'identity management', 'access control'
            ],
            'skills': [
                'splunk', 'wireshark', 'nmap', 'metasploit', 'burp suite',
                'kali linux', 'nessus', 'crowdstrike', 'palo alto',
                'okta', 'azure ad', 'cissp', 'ceh', 'oscp'
            ],
            'titles': [
                'security analyst', 'security engineer', 'penetration tester',
                'soc analyst', 'ciso', 'information security', 'cybersecurity analyst'
            ]
        },

        # ==================== BUSINESS ====================
        'Marketing': {
            'keywords': [
                'marketing', 'campaign', 'brand', 'branding', 'digital marketing',
                'social media', 'content', 'seo', 'sem', 'ppc', 'advertising',
                'email marketing', 'automation', 'lead generation', 'funnel',
                'conversion', 'engagement', 'audience', 'influencer',
                'copywriting', 'creative', 'strategy', 'growth', 'viral',
                'market research', 'competitive analysis', 'roi'
            ],
            'skills': [
                'google analytics', 'hubspot', 'marketo', 'mailchimp',
                'facebook ads', 'google ads', 'hootsuite', 'buffer',
                'salesforce marketing cloud', 'adobe creative', 'semrush',
                'ahrefs', 'moz', 'canva', 'wordpress'
            ],
            'titles': [
                'marketing manager', 'digital marketer', 'content strategist',
                'seo specialist', 'growth marketer', 'brand manager',
                'cmo', 'marketing director', 'social media manager'
            ]
        },
        'Finance / Banking': {
            'keywords': [
                'finance', 'financial', 'accounting', 'investment', 'banking',
                'trading', 'portfolio', 'risk', 'compliance', 'audit',
                'budgeting', 'forecasting', 'valuation', 'equity', 'fixed income',
                'derivatives', 'hedge fund', 'private equity', 'venture capital',
                'tax', 'treasury', 'credit', 'underwriting', 'actuarial',
                'mergers', 'acquisitions', 'm&a', 'ipo', 'due diligence'
            ],
            'skills': [
                'excel', 'financial modeling', 'bloomberg', 'vba',
                'sql', 'sap', 'oracle financials', 'quickbooks',
                'tableau', 'alteryx', 'python', 'cfa', 'cpa', 'frm'
            ],
            'titles': [
                'financial analyst', 'accountant', 'investment banker',
                'portfolio manager', 'risk analyst', 'controller', 'cfo',
                'auditor', 'tax consultant', 'wealth manager', 'trader'
            ]
        },
        'Sales': {
            'keywords': [
                'sales', 'selling', 'revenue', 'quota', 'pipeline',
                'prospecting', 'closing', 'negotiation', 'account',
                'client', 'customer', 'relationship', 'territory',
                'b2b', 'b2c', 'enterprise', 'solution selling',
                'cold calling', 'outreach', 'demo', 'proposal',
                'upselling', 'cross-selling', 'churn', 'retention'
            ],
            'skills': [
                'salesforce', 'hubspot', 'linkedin sales navigator',
                'outreach', 'salesloft', 'gong', 'chorus', 'zoominfo',
                'pipedrive', 'zoho crm', 'apollo'
            ],
            'titles': [
                'sales representative', 'account executive', 'sales manager',
                'business development', 'sales director', 'account manager',
                'sales engineer', 'vp sales', 'inside sales'
            ]
        },
        'Human Resources': {
            'keywords': [
                'human resources', 'hr', 'recruiting', 'talent acquisition',
                'onboarding', 'employee relations', 'compensation', 'benefits',
                'payroll', 'training', 'development', 'performance management',
                'hris', 'workforce', 'retention', 'engagement', 'culture',
                'diversity', 'inclusion', 'labor relations', 'compliance',
                'succession planning', 'organizational development'
            ],
            'skills': [
                'workday', 'successfactors', 'bamboohr', 'adp',
                'greenhouse', 'lever', 'linkedin recruiter', 'ultipro',
                'paychex', 'gusto', 'namely', 'shrm-cp'
            ],
            'titles': [
                'hr manager', 'recruiter', 'talent acquisition', 'hr business partner',
                'hr generalist', 'hr director', 'people operations', 'chro',
                'compensation analyst', 'hrbp'
            ]
        },
        'Operations / Supply Chain': {
            'keywords': [
                'operations', 'supply chain', 'logistics', 'procurement',
                'inventory', 'warehouse', 'distribution', 'fulfillment',
                'manufacturing', 'production', 'quality control', 'lean',
                'six sigma', 'process improvement', 'vendor management',
                'demand planning', 'forecasting', 'sourcing', 'transportation',
                'erp', 'mrp', 'just-in-time', 'kaizen'
            ],
            'skills': [
                'sap', 'oracle', 'netsuite', 'microsoft dynamics',
                'tableau', 'power bi', 'excel', 'sql',
                'lean six sigma', 'pmp', 'apics', 'cscp'
            ],
            'titles': [
                'operations manager', 'supply chain manager', 'logistics coordinator',
                'procurement manager', 'warehouse manager', 'plant manager',
                'coo', 'director of operations', 'production manager'
            ]
        },
        'Consulting': {
            'keywords': [
                'consulting', 'strategy', 'advisory', 'management consulting',
                'business transformation', 'change management', 'stakeholder',
                'client engagement', 'proposal', 'deliverable', 'workstream',
                'due diligence', 'market entry', 'cost optimization',
                'organizational design', 'process reengineering', 'benchmarking'
            ],
            'skills': [
                'powerpoint', 'excel', 'tableau', 'sql',
                'mece', 'case study', 'financial modeling',
                'project management', 'stakeholder management'
            ],
            'titles': [
                'consultant', 'associate', 'senior consultant', 'manager',
                'principal', 'partner', 'director', 'engagement manager',
                'strategy consultant', 'management consultant'
            ]
        },
        'Project Management': {
            'keywords': [
                'project management', 'program management', 'pmo',
                'agile', 'scrum', 'waterfall', 'kanban', 'sprint',
                'milestone', 'timeline', 'budget', 'resource allocation',
                'risk management', 'stakeholder', 'deliverable', 'gantt',
                'scope', 'requirements', 'change management', 'backlog'
            ],
            'skills': [
                'jira', 'asana', 'trello', 'monday', 'ms project',
                'smartsheet', 'confluence', 'pmp', 'prince2',
                'agile certified', 'scrum master', 'safe'
            ],
            'titles': [
                'project manager', 'program manager', 'scrum master',
                'product owner', 'pmo director', 'delivery manager',
                'technical project manager', 'agile coach'
            ]
        },

        # ==================== HEALTHCARE ====================
        'Healthcare / Medical': {
            'keywords': [
                'healthcare', 'medical', 'clinical', 'patient', 'hospital',
                'diagnosis', 'treatment', 'therapy', 'nursing', 'physician',
                'pharmacy', 'surgical', 'emergency', 'icu', 'outpatient',
                'inpatient', 'telemedicine', 'ehr', 'emr', 'hipaa',
                'medical records', 'insurance', 'claims', 'billing'
            ],
            'skills': [
                'epic', 'cerner', 'meditech', 'allscripts', 'hl7', 'fhir',
                'icd-10', 'cpt', 'medical terminology', 'bls', 'acls',
                'registered nurse', 'licensed practical nurse'
            ],
            'titles': [
                'nurse', 'physician', 'doctor', 'surgeon', 'pharmacist',
                'medical assistant', 'healthcare administrator', 'clinical director',
                'nursing manager', 'medical technologist', 'therapist'
            ]
        },
        'Pharmaceutical / Biotech': {
            'keywords': [
                'pharmaceutical', 'biotech', 'drug development', 'clinical trial',
                'fda', 'regulatory', 'research', 'laboratory', 'bioinformatics',
                'genomics', 'proteomics', 'molecular biology', 'cell culture',
                'gmp', 'glp', 'quality assurance', 'validation', 'formulation'
            ],
            'skills': [
                'sas', 'r', 'python', 'spss', 'prism',
                'veeva', 'lims', 'pcr', 'elisa', 'hplc',
                'mass spectrometry', 'bioreactor'
            ],
            'titles': [
                'research scientist', 'clinical research associate', 'regulatory affairs',
                'quality assurance', 'medical science liaison', 'lab technician',
                'biostatistician', 'pharmacovigilance', 'medical writer'
            ]
        },

        # ==================== CREATIVE ====================
        'Design / UX': {
            'keywords': [
                'design', 'ui', 'ux', 'user experience', 'user interface',
                'visual design', 'graphic design', 'product design',
                'interaction design', 'wireframe', 'prototype', 'mockup',
                'typography', 'color theory', 'layout', 'responsive',
                'usability', 'accessibility', 'design system', 'branding',
                'user research', 'persona', 'journey map', 'information architecture'
            ],
            'skills': [
                'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
                'invision', 'principle', 'framer', 'after effects', 'zeplin',
                'miro', 'figjam', 'protopie', 'origami'
            ],
            'titles': [
                'designer', 'ux designer', 'ui designer', 'product designer',
                'graphic designer', 'creative director', 'visual designer',
                'ux researcher', 'design lead', 'head of design'
            ]
        },
        'Content / Media': {
            'keywords': [
                'content', 'writing', 'editing', 'journalism', 'media',
                'publishing', 'copywriting', 'blogging', 'storytelling',
                'video production', 'podcast', 'social media', 'engagement',
                'editorial', 'press', 'communications', 'public relations',
                'seo writing', 'technical writing', 'documentation'
            ],
            'skills': [
                'wordpress', 'contentful', 'medium', 'hubspot',
                'adobe premiere', 'final cut pro', 'audacity',
                'grammarly', 'hemingway', 'ap style', 'chicago manual'
            ],
            'titles': [
                'content writer', 'copywriter', 'editor', 'journalist',
                'content manager', 'content strategist', 'technical writer',
                'communications manager', 'pr specialist', 'social media manager'
            ]
        },

        # ==================== ENGINEERING ====================
        'Mechanical Engineering': {
            'keywords': [
                'mechanical', 'engineering', 'cad', 'design', 'manufacturing',
                'prototype', 'testing', 'simulation', 'fea', 'cfd',
                'thermodynamics', 'fluid dynamics', 'materials', 'tolerancing',
                'gd&t', 'machining', 'assembly', 'hvac', 'automotive'
            ],
            'skills': [
                'solidworks', 'autocad', 'catia', 'creo', 'nx',
                'ansys', 'matlab', 'simulink', 'inventor',
                'gd&t', 'fea', 'cfd', 'cam'
            ],
            'titles': [
                'mechanical engineer', 'design engineer', 'manufacturing engineer',
                'project engineer', 'product engineer', 'r&d engineer',
                'test engineer', 'quality engineer', 'cae engineer'
            ]
        },
        'Electrical / Electronics': {
            'keywords': [
                'electrical', 'electronics', 'circuit', 'pcb', 'embedded',
                'firmware', 'fpga', 'microcontroller', 'power systems',
                'control systems', 'signal processing', 'rf', 'wireless',
                'semiconductor', 'vlsi', 'asic', 'iot', 'sensors'
            ],
            'skills': [
                'altium', 'eagle', 'kicad', 'orcad', 'spice',
                'verilog', 'vhdl', 'matlab', 'labview',
                'c', 'c++', 'python', 'arduino', 'raspberry pi'
            ],
            'titles': [
                'electrical engineer', 'electronics engineer', 'hardware engineer',
                'embedded engineer', 'firmware engineer', 'rf engineer',
                'power systems engineer', 'control systems engineer'
            ]
        },
        'Civil / Construction': {
            'keywords': [
                'civil', 'construction', 'structural', 'building', 'infrastructure',
                'surveying', 'geotechnical', 'transportation', 'environmental',
                'concrete', 'steel', 'foundation', 'highway', 'bridge',
                'project management', 'site supervision', 'estimating', 'safety'
            ],
            'skills': [
                'autocad', 'revit', 'civil 3d', 'etabs', 'staad pro',
                'primavera', 'ms project', 'bluebeam', 'procore',
                'gis', 'arcgis', 'structural analysis'
            ],
            'titles': [
                'civil engineer', 'structural engineer', 'construction manager',
                'project engineer', 'site engineer', 'estimator',
                'geotechnical engineer', 'transportation engineer'
            ]
        },

        # ==================== LEGAL ====================
        'Legal': {
            'keywords': [
                'legal', 'law', 'attorney', 'litigation', 'contract',
                'compliance', 'regulatory', 'intellectual property', 'patent',
                'trademark', 'corporate law', 'mergers', 'acquisitions',
                'due diligence', 'dispute resolution', 'arbitration',
                'employment law', 'privacy', 'gdpr', 'legal research'
            ],
            'skills': [
                'westlaw', 'lexisnexis', 'contract management',
                'document review', 'legal research', 'drafting',
                'jd', 'bar admission', 'paralegal certification'
            ],
            'titles': [
                'attorney', 'lawyer', 'legal counsel', 'paralegal',
                'compliance officer', 'general counsel', 'legal associate',
                'contract manager', 'ip specialist', 'litigation support'
            ]
        },

        # ==================== EDUCATION ====================
        'Education / Academia': {
            'keywords': [
                'education', 'teaching', 'learning', 'curriculum', 'instruction',
                'student', 'classroom', 'assessment', 'academic', 'research',
                'professor', 'lecturer', 'pedagogy', 'e-learning', 'lms',
                'higher education', 'k-12', 'special education', 'tutoring'
            ],
            'skills': [
                'canvas', 'blackboard', 'moodle', 'google classroom',
                'zoom', 'microsoft teams', 'powerpoint', 'lesson planning',
                'curriculum development', 'assessment design'
            ],
            'titles': [
                'teacher', 'professor', 'instructor', 'tutor',
                'curriculum developer', 'instructional designer', 'principal',
                'dean', 'education coordinator', 'academic advisor'
            ]
        },

        # ==================== HOSPITALITY / RETAIL ====================
        'Hospitality / Tourism': {
            'keywords': [
                'hospitality', 'hotel', 'restaurant', 'tourism', 'travel',
                'guest services', 'customer service', 'front desk', 'concierge',
                'event planning', 'catering', 'food and beverage', 'housekeeping',
                'reservation', 'booking', 'revenue management', 'occupancy'
            ],
            'skills': [
                'opera pms', 'micros', 'sabre', 'amadeus',
                'reservations', 'guest management', 'pos systems',
                'food safety', 'servsafe'
            ],
            'titles': [
                'hotel manager', 'restaurant manager', 'event coordinator',
                'front desk agent', 'concierge', 'chef', 'server',
                'travel agent', 'tourism manager', 'hospitality director'
            ]
        },
        'Retail / E-commerce': {
            'keywords': [
                'retail', 'e-commerce', 'store', 'merchandising', 'inventory',
                'sales', 'customer service', 'visual merchandising', 'pos',
                'omnichannel', 'fulfillment', 'dropshipping', 'amazon',
                'shopify', 'conversion rate', 'basket size', 'shrinkage'
            ],
            'skills': [
                'shopify', 'magento', 'woocommerce', 'salesforce commerce',
                'sap retail', 'oracle retail', 'google analytics',
                'inventory management', 'pos systems'
            ],
            'titles': [
                'store manager', 'retail manager', 'e-commerce manager',
                'merchandiser', 'buyer', 'category manager', 'sales associate',
                'visual merchandiser', 'inventory manager'
            ]
        },

        # ==================== GOVERNMENT / NON-PROFIT ====================
        'Government / Public Sector': {
            'keywords': [
                'government', 'public sector', 'policy', 'administration',
                'regulatory', 'compliance', 'legislation', 'grants',
                'public affairs', 'civil service', 'municipal', 'federal',
                'state', 'local government', 'public administration'
            ],
            'skills': [
                'policy analysis', 'grant writing', 'public speaking',
                'legislation tracking', 'constituent services',
                'government procurement', 'clearance'
            ],
            'titles': [
                'policy analyst', 'program manager', 'government affairs',
                'public administrator', 'civil servant', 'legislative aide',
                'grants manager', 'compliance officer'
            ]
        },
        'Non-Profit / NGO': {
            'keywords': [
                'non-profit', 'nonprofit', 'ngo', 'charity', 'foundation',
                'fundraising', 'grant', 'donor', 'volunteer', 'outreach',
                'community', 'advocacy', 'social impact', 'sustainability',
                'development', 'humanitarian', 'philanthropy'
            ],
            'skills': [
                'salesforce nonprofit', 'bloomerang', 'raiser edge',
                'grant writing', 'donor management', 'volunteer coordination',
                'event planning', 'community outreach'
            ],
            'titles': [
                'executive director', 'development director', 'fundraiser',
                'program manager', 'grant writer', 'volunteer coordinator',
                'outreach coordinator', 'advocacy manager'
            ]
        },

        # ==================== REAL ESTATE ====================
        'Real Estate': {
            'keywords': [
                'real estate', 'property', 'commercial', 'residential',
                'leasing', 'tenant', 'landlord', 'mortgage', 'appraisal',
                'valuation', 'investment', 'development', 'construction',
                'property management', 'brokerage', 'mls'
            ],
            'skills': [
                'mls', 'yardi', 'costar', 'argus', 'excel',
                'property management software', 'cre license',
                'real estate license', 'financial modeling'
            ],
            'titles': [
                'real estate agent', 'broker', 'property manager',
                'leasing agent', 'real estate analyst', 'appraiser',
                'development manager', 'asset manager'
            ]
        },

        # ==================== ENTRY LEVEL ====================
        'Student / Fresher': {
            'keywords': [
                'student', 'fresher', 'graduate', 'university', 'college',
                'intern', 'internship', 'campus', 'academic', 'thesis',
                'coursework', 'gpa', 'cgpa', 'bachelor', 'master',
                'degree', 'certification', 'learning', 'project',
                'entry level', 'junior', 'associate', 'trainee'
            ],
            'skills': [],
            'titles': [
                'intern', 'trainee', 'fresher', 'graduate', 'entry level',
                'junior', 'associate', 'apprentice'
            ]
        }
    }
    
    def classify(self, text: str, skills: SkillsData) -> DomainInfo:
        """Classify resume into a domain category"""
        text_lower = text.lower()
        
        # Calculate scores for each domain
        domain_scores: Dict[str, float] = {}
        keywords_matched: Dict[str, List[str]] = {}
        
        for domain, data in self.DOMAIN_KEYWORDS.items():
            score, matched = self._calculate_domain_score(
                text_lower, 
                data, 
                skills
            )
            domain_scores[domain] = score
            keywords_matched[domain] = matched
        
        # Sort by score
        sorted_domains = sorted(
            domain_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Get primary and secondary domains
        primary_domain = sorted_domains[0][0]
        primary_score = sorted_domains[0][1]
        secondary_domain = sorted_domains[1][0] if len(sorted_domains) > 1 else None
        secondary_score = sorted_domains[1][1] if len(sorted_domains) > 1 else 0
        
        # Calculate confidence (0-1)
        total_score = sum(domain_scores.values())
        confidence = (primary_score / total_score) if total_score > 0 else 0.5
        
        # If scores are too close, lower confidence
        if secondary_score > 0 and (primary_score - secondary_score) < primary_score * 0.2:
            confidence *= 0.8
        
        return DomainInfo(
            primary=primary_domain,
            confidence=round(confidence, 2),
            secondary=secondary_domain if secondary_score > primary_score * 0.5 else None,
            keywords_matched=keywords_matched.get(primary_domain, [])[:10]
        )
    
    def _calculate_domain_score(
        self, 
        text: str, 
        domain_data: Dict, 
        skills: SkillsData
    ) -> Tuple[float, List[str]]:
        """Calculate score for a domain"""
        score = 0.0
        matched = []
        
        # Check keywords (weight: 1)
        for keyword in domain_data['keywords']:
            if keyword in text:
                score += 1
                matched.append(keyword)
        
        # Check titles (weight: 3 - more important)
        for title in domain_data['titles']:
            if title in text:
                score += 3
                matched.append(title)
        
        # Check domain-specific skills (weight: 2)
        all_user_skills = set(
            s.lower() for s in 
            skills.programming_languages + skills.frameworks + 
            skills.tools + skills.databases
        )
        
        for skill in domain_data['skills']:
            if skill.lower() in all_user_skills:
                score += 2
                matched.append(skill)
        
        return score, matched
    
    def get_domain_description(self, domain: str) -> str:
        """Get description for a domain"""
        descriptions = {
            # Technology
            'Software / IT': 'Software development, web/mobile applications, and IT infrastructure',
            'Data Science / AI': 'Data science, machine learning, analytics, and artificial intelligence',
            'Cybersecurity': 'Information security, threat detection, and compliance',
            
            # Business
            'Marketing': 'Digital marketing, brand management, and growth strategies',
            'Finance / Banking': 'Financial analysis, accounting, investment, and risk management',
            'Sales': 'Sales, business development, and account management',
            'Human Resources': 'Talent acquisition, employee relations, and people operations',
            'Operations / Supply Chain': 'Logistics, procurement, manufacturing, and process optimization',
            'Consulting': 'Strategy, management consulting, and business transformation',
            'Project Management': 'Project/program management, agile methodologies, and delivery',
            
            # Healthcare
            'Healthcare / Medical': 'Clinical care, patient services, and healthcare administration',
            'Pharmaceutical / Biotech': 'Drug development, clinical trials, and research',
            
            # Creative
            'Design / UX': 'UI/UX design, visual design, and product design',
            'Content / Media': 'Content creation, journalism, and communications',
            
            # Engineering
            'Mechanical Engineering': 'Mechanical design, manufacturing, and product development',
            'Electrical / Electronics': 'Circuit design, embedded systems, and electronics',
            'Civil / Construction': 'Structural engineering, construction, and infrastructure',
            
            # Other
            'Legal': 'Legal practice, compliance, and contract management',
            'Education / Academia': 'Teaching, curriculum development, and academic research',
            'Hospitality / Tourism': 'Hotel management, restaurants, and travel services',
            'Retail / E-commerce': 'Retail operations, merchandising, and online commerce',
            'Government / Public Sector': 'Public administration, policy, and government affairs',
            'Non-Profit / NGO': 'Non-profit management, fundraising, and social impact',
            'Real Estate': 'Property management, brokerage, and real estate investment',
            
            # Entry Level
            'Student / Fresher': 'Entry-level position with academic focus'
        }
        return descriptions.get(domain, 'General professional role')
