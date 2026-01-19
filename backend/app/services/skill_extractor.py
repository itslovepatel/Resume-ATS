"""
Skill Extractor Service - Identifies and categorizes skills from resume text
"""
import re
from typing import Dict, List, Set
from app.models.schemas import SkillsData, SkillCategory


class SkillExtractor:
    """Extract and categorize skills from resume text"""
    
    # Comprehensive skill databases
    PROGRAMMING_LANGUAGES = {
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c',
        'ruby', 'go', 'golang', 'rust', 'swift', 'kotlin', 'scala', 'php',
        'perl', 'r', 'matlab', 'julia', 'dart', 'lua', 'haskell', 'elixir',
        'clojure', 'f#', 'objective-c', 'groovy', 'vb.net', 'visual basic',
        'assembly', 'cobol', 'fortran', 'pascal', 'shell', 'bash', 'powershell',
        'sql', 'plsql', 'tsql', 'html', 'css', 'sass', 'scss', 'less'
    }
    
    FRAMEWORKS = {
        # Frontend
        'react', 'reactjs', 'react.js', 'angular', 'angularjs', 'vue', 'vuejs',
        'vue.js', 'svelte', 'next.js', 'nextjs', 'nuxt', 'nuxtjs', 'gatsby',
        'ember', 'backbone', 'jquery', 'bootstrap', 'tailwind', 'tailwindcss',
        'material-ui', 'mui', 'chakra', 'ant design', 'styled-components',
        # Backend
        'node.js', 'nodejs', 'express', 'expressjs', 'fastapi', 'django', 'flask',
        'spring', 'spring boot', 'springboot', '.net', 'asp.net', 'rails',
        'ruby on rails', 'laravel', 'symfony', 'fastify', 'koa', 'nest',
        'nestjs', 'hapi', 'gin', 'echo', 'fiber', 'actix', 'rocket',
        # Mobile
        'react native', 'flutter', 'ionic', 'xamarin', 'swiftui', 'jetpack compose',
        # Data/ML
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'sklearn', 'pandas',
        'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly', 'opencv',
        'nltk', 'spacy', 'huggingface', 'transformers', 'xgboost', 'lightgbm',
        # Testing
        'jest', 'mocha', 'jasmine', 'pytest', 'junit', 'selenium', 'cypress',
        'playwright', 'puppeteer', 'testng', 'rspec'
    }
    
    TOOLS = {
        # DevOps & Cloud
        'docker', 'kubernetes', 'k8s', 'aws', 'azure', 'gcp', 'google cloud',
        'heroku', 'vercel', 'netlify', 'digitalocean', 'terraform', 'ansible',
        'jenkins', 'circleci', 'travis', 'github actions', 'gitlab ci',
        'bamboo', 'teamcity', 'argo', 'helm', 'prometheus', 'grafana',
        'datadog', 'new relic', 'splunk', 'elk', 'elasticsearch', 'logstash',
        'kibana', 'cloudwatch', 'cloudformation', 'pulumi', 'vagrant',
        # Version Control
        'git', 'github', 'gitlab', 'bitbucket', 'svn', 'mercurial',
        # IDEs & Editors
        'vscode', 'visual studio code', 'intellij', 'pycharm', 'eclipse',
        'sublime', 'vim', 'neovim', 'emacs', 'atom', 'webstorm', 'android studio',
        'xcode',
        # Project Management
        'jira', 'confluence', 'trello', 'asana', 'notion', 'monday', 'linear',
        'clickup', 'basecamp', 'azure devops',
        # Design
        'figma', 'sketch', 'adobe xd', 'invision', 'zeplin', 'photoshop',
        'illustrator', 'canva', 'after effects', 'premiere pro', 'indesign',
        # Communication
        'slack', 'teams', 'discord', 'zoom',
        # API & Testing Tools
        'postman', 'insomnia', 'swagger', 'graphql', 'rest', 'grpc', 'soap',
        # Data & BI
        'webpack', 'vite', 'parcel', 'rollup', 'babel', 'eslint', 'prettier',
        'nginx', 'apache', 'redis', 'rabbitmq', 'kafka', 'celery', 'airflow',
        'spark', 'hadoop', 'hive', 'databricks', 'snowflake', 'dbt', 'looker',
        'tableau', 'power bi', 'metabase', 'superset', 'alteryx',
        # Marketing Tools
        'google analytics', 'hubspot', 'marketo', 'mailchimp', 'semrush',
        'ahrefs', 'moz', 'hootsuite', 'buffer', 'sprout social',
        # Finance Tools
        'bloomberg', 'reuters', 'sap', 'oracle', 'quickbooks', 'xero',
        'netsuite', 'sage', 'factset', 'capital iq',
        # HR Tools
        'workday', 'successfactors', 'bamboohr', 'adp', 'greenhouse',
        'lever', 'linkedin recruiter', 'ultipro', 'paychex', 'gusto',
        # Healthcare Tools
        'epic', 'cerner', 'meditech', 'allscripts', 'athenahealth',
        # Engineering Tools
        'solidworks', 'autocad', 'catia', 'creo', 'nx', 'ansys',
        'matlab', 'simulink', 'revit', 'civil 3d', 'etabs',
        'altium', 'eagle', 'kicad', 'orcad', 'labview',
        # Legal Tools
        'westlaw', 'lexisnexis', 'relativity', 'clio',
        # Real Estate Tools
        'mls', 'yardi', 'costar', 'argus',
        # Security Tools
        'splunk', 'wireshark', 'nmap', 'metasploit', 'burp suite',
        'crowdstrike', 'palo alto', 'okta', 'qualys', 'nessus'
    }
    
    DATABASES = {
        'mysql', 'postgresql', 'postgres', 'mongodb', 'sqlite', 'oracle',
        'sql server', 'mssql', 'mariadb', 'cassandra', 'dynamodb', 'firebase',
        'firestore', 'couchdb', 'neo4j', 'redis', 'memcached', 'elasticsearch',
        'supabase', 'planetscale', 'cockroachdb', 'timescaledb', 'influxdb',
        'arangodb', 'fauna', 'prisma', 'mongoose', 'sequelize', 'typeorm',
        'sqlalchemy', 'drizzle', 'knex'
    }
    
    SOFT_SKILLS = {
        'leadership', 'communication', 'teamwork', 'team player', 'collaboration',
        'problem solving', 'problem-solving', 'analytical', 'critical thinking',
        'creativity', 'adaptability', 'flexibility', 'time management',
        'project management', 'agile', 'scrum', 'kanban', 'public speaking',
        'presentation', 'negotiation', 'conflict resolution', 'mentoring',
        'coaching', 'decision making', 'decision-making', 'strategic thinking',
        'attention to detail', 'detail-oriented', 'self-motivated', 'initiative',
        'customer service', 'stakeholder management', 'cross-functional',
        'remote work', 'distributed teams', 'empathy', 'emotional intelligence',
        'active listening', 'interpersonal skills', 'organizational skills',
        'multitasking', 'work ethic', 'patience', 'cultural awareness',
        'networking', 'persuasion', 'accountability', 'resourcefulness'
    }
    
    # Industry-specific certifications
    CERTIFICATIONS = {
        # Technology
        'aws certified', 'azure certified', 'gcp certified', 'cka', 'ckad',
        'cissp', 'ceh', 'oscp', 'comptia', 'ccna', 'ccnp',
        # Project Management
        'pmp', 'prince2', 'csm', 'psm', 'safe', 'capm',
        # Data
        'google data analytics', 'databricks certified', 'snowflake certified',
        # Finance
        'cfa', 'cpa', 'cma', 'frm', 'series 7', 'series 63',
        # HR
        'shrm-cp', 'shrm-scp', 'phr', 'sphr',
        # Healthcare
        'bls', 'acls', 'rn', 'lpn', 'cna',
        # Quality
        'six sigma', 'lean six sigma', 'iso', 'pmp',
        # Marketing
        'google ads certified', 'hubspot certified', 'facebook blueprint'
    }
    
    def __init__(self):
        # Create lowercase versions for matching
        self.all_skills = {
            'programming_languages': {s.lower() for s in self.PROGRAMMING_LANGUAGES},
            'frameworks': {s.lower() for s in self.FRAMEWORKS},
            'tools': {s.lower() for s in self.TOOLS},
            'databases': {s.lower() for s in self.DATABASES},
            'soft_skills': {s.lower() for s in self.SOFT_SKILLS}
        }
    
    def extract(self, text: str) -> SkillsData:
        """Extract skills from resume text"""
        text_lower = text.lower()
        
        found_skills = {
            'programming_languages': [],
            'frameworks': [],
            'tools': [],
            'databases': [],
            'soft_skills': [],
            'other': []
        }
        
        # Extract skills from each category
        for category, skills_set in self.all_skills.items():
            for skill in skills_set:
                # Use word boundary matching to avoid partial matches
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    # Get original case version
                    original = self._get_original_case(skill, category)
                    if original not in found_skills[category]:
                        found_skills[category].append(original)
        
        # Sort skills
        for category in found_skills:
            found_skills[category].sort()
        
        # Calculate total count
        total_count = sum(len(skills) for skills in found_skills.values())
        
        # Create skill categories with strength
        skill_categories = self._create_skill_categories(found_skills)
        
        return SkillsData(
            programming_languages=found_skills['programming_languages'],
            frameworks=found_skills['frameworks'],
            tools=found_skills['tools'],
            databases=found_skills['databases'],
            soft_skills=found_skills['soft_skills'],
            other=found_skills['other'],
            total_count=total_count,
            skill_categories=skill_categories
        )
    
    def _get_original_case(self, skill: str, category: str) -> str:
        """Get the properly cased version of a skill"""
        skill_maps = {
            'programming_languages': self.PROGRAMMING_LANGUAGES,
            'frameworks': self.FRAMEWORKS,
            'tools': self.TOOLS,
            'databases': self.DATABASES,
            'soft_skills': self.SOFT_SKILLS
        }
        
        source_set = skill_maps.get(category, set())
        for s in source_set:
            if s.lower() == skill:
                return s
        return skill.title()
    
    def _create_skill_categories(self, found_skills: Dict[str, List[str]]) -> List[SkillCategory]:
        """Create categorized skill entries with strength ratings"""
        categories = []
        
        category_names = {
            'programming_languages': 'Programming Languages',
            'frameworks': 'Frameworks & Libraries',
            'tools': 'Tools & Platforms',
            'databases': 'Databases',
            'soft_skills': 'Soft Skills'
        }
        
        for key, display_name in category_names.items():
            skills = found_skills.get(key, [])
            if skills:
                # Determine strength based on count and relevance
                strength = self._calculate_strength(len(skills), key)
                categories.append(SkillCategory(
                    name=display_name,
                    skills=skills,
                    strength=strength
                ))
        
        return categories
    
    def _calculate_strength(self, count: int, category: str) -> str:
        """Calculate skill strength for a category"""
        thresholds = {
            'programming_languages': {'strong': 3, 'moderate': 2},
            'frameworks': {'strong': 4, 'moderate': 2},
            'tools': {'strong': 5, 'moderate': 3},
            'databases': {'strong': 2, 'moderate': 1},
            'soft_skills': {'strong': 4, 'moderate': 2}
        }
        
        t = thresholds.get(category, {'strong': 3, 'moderate': 2})
        
        if count >= t['strong']:
            return 'Strong'
        elif count >= t['moderate']:
            return 'Moderate'
        else:
            return 'Weak'
    
    def get_skill_suggestions(self, found_skills: SkillsData, domain: str) -> List[str]:
        """Get skill suggestions based on domain - covers 25+ industries"""
        domain_skills = {
            # Technology
            'Software / IT': ['Python', 'JavaScript', 'React', 'Node.js', 'Docker', 'AWS', 'Git', 'TypeScript'],
            'Data Science / AI': ['Python', 'TensorFlow', 'PyTorch', 'SQL', 'Pandas', 'Machine Learning', 'Statistics', 'Tableau'],
            'Cybersecurity': ['Splunk', 'SIEM', 'Penetration Testing', 'Firewalls', 'Security Frameworks', 'CISSP', 'Kali Linux'],
            
            # Business
            'Marketing': ['Google Analytics', 'SEO', 'Content Strategy', 'Social Media', 'HubSpot', 'Marketing Automation', 'Google Ads'],
            'Finance / Banking': ['Excel', 'Financial Modeling', 'SQL', 'Bloomberg', 'Risk Analysis', 'Python', 'VBA', 'CFA'],
            'Sales': ['CRM', 'Salesforce', 'Pipeline Management', 'Negotiation', 'Lead Generation', 'Cold Calling', 'HubSpot'],
            'Human Resources': ['HRIS', 'ATS', 'Recruiting', 'Employee Relations', 'Compliance', 'Workday', 'LinkedIn Recruiter'],
            'Operations / Supply Chain': ['SAP', 'Lean Six Sigma', 'Inventory Management', 'Procurement', 'ERP', 'Excel', 'Project Management'],
            'Consulting': ['PowerPoint', 'Excel', 'Financial Modeling', 'Stakeholder Management', 'Strategy', 'Problem Solving'],
            'Project Management': ['Jira', 'PMP', 'Agile', 'Scrum', 'MS Project', 'Risk Management', 'Stakeholder Communication'],
            
            # Healthcare
            'Healthcare / Medical': ['Epic', 'Cerner', 'HIPAA', 'Medical Terminology', 'EMR/EHR', 'Patient Care', 'Clinical Documentation'],
            'Pharmaceutical / Biotech': ['SAS', 'R', 'Clinical Trials', 'GMP', 'Regulatory Affairs', 'FDA', 'Quality Assurance'],
            
            # Creative
            'Design / UX': ['Figma', 'Adobe Creative Suite', 'UI/UX', 'Prototyping', 'Design Systems', 'User Research', 'Sketch'],
            'Content / Media': ['WordPress', 'SEO Writing', 'Adobe Premiere', 'Content Strategy', 'Social Media', 'Copywriting'],
            
            # Engineering
            'Mechanical Engineering': ['SolidWorks', 'AutoCAD', 'CATIA', 'ANSYS', 'GD&T', 'FEA', 'Manufacturing'],
            'Electrical / Electronics': ['Altium', 'MATLAB', 'Embedded C', 'PCB Design', 'FPGA', 'Verilog', 'Circuit Analysis'],
            'Civil / Construction': ['AutoCAD', 'Revit', 'Civil 3D', 'Primavera', 'Structural Analysis', 'Project Management'],
            
            # Other Industries
            'Legal': ['Westlaw', 'LexisNexis', 'Contract Management', 'Legal Research', 'Drafting', 'Compliance'],
            'Education / Academia': ['Curriculum Development', 'LMS', 'Assessment Design', 'Classroom Management', 'Google Classroom'],
            'Hospitality / Tourism': ['Opera PMS', 'Customer Service', 'Event Planning', 'Reservation Systems', 'Revenue Management'],
            'Retail / E-commerce': ['Shopify', 'Inventory Management', 'POS Systems', 'Merchandising', 'Google Analytics', 'Customer Service'],
            'Government / Public Sector': ['Policy Analysis', 'Grant Writing', 'Public Speaking', 'Compliance', 'Stakeholder Engagement'],
            'Non-Profit / NGO': ['Grant Writing', 'Donor Management', 'Fundraising', 'Volunteer Coordination', 'Salesforce Nonprofit'],
            'Real Estate': ['MLS', 'Property Management', 'CoStar', 'Financial Analysis', 'Contract Negotiation', 'CRM'],
            
            # Entry Level
            'Student / Fresher': ['Microsoft Office', 'Communication', 'Problem Solving', 'Teamwork', 'Time Management', 'Adaptability']
        }
        
        current_skills = set(
            s.lower() for s in 
            found_skills.programming_languages + found_skills.frameworks + 
            found_skills.tools + found_skills.databases
        )
        
        suggestions = []
        domain_recommended = domain_skills.get(domain, domain_skills.get('Student / Fresher', []))
        
        for skill in domain_recommended:
            if skill.lower() not in current_skills:
                suggestions.append(skill)
        
        return suggestions[:5]
