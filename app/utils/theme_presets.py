"""
Theme Presets Engine
Defines complete, authentic design presets, typography, brand assets,
and modular home content for all 5 native themes.
"""

THEME_PRESETS = {
    'hisoft': {
        'key': 'hisoft',
        'name': 'Business Enterprise',
        'badge': 'Corporate B2B',
        'category': 'Cloud Architecture & Managed IT Solutions',
        'description': 'High-impact corporate B2B technology layout with navy & crimson palette, live metrics, capability cards, case studies, and enterprise inquiry form.',
        'color': '#022d62',
        'accent': '#ef3139',
        'settings': {
            'site_title': 'Tek Club',
            'site_tagline': 'Enterprise Cloud & Managed IT Solutions',
            'site_logo': '/static/img/tekclub_logo.svg',
            'header_style': 'classic_sticky',
            'header_bg_color': '#ffffff',
            'header_bg_opacity': '100',
            'header_text_color': '#022d62',
            'header_text_opacity': '100',
            'header_accent_color': '#ef3139',
            'header_accent_opacity': '100',
            'header_font_style': 'sans',
            'header_show_topbar': '1',
            'header_cta_text': 'Get a Quote',
            'header_cta_url': '/contact',
            'footer_bg_color': '#022d62',
            'footer_bg_opacity': '100',
            'footer_text_color': '#cbd5e1',
            'footer_text_opacity': '100',
            'footer_accent_color': '#ef3139',
            'footer_accent_opacity': '100',
            'footer_logo': '/static/img/tekclub_logo_white.svg',
            'footer_about_text': 'Delivering cutting-edge enterprise IT solutions, cloud architectures, managed services, and scalable digital consulting for global industry leaders.',
            'footer_copyright': '© 2026 Tek Club Ltd. All rights reserved.',
            'home_hero_title': 'Enterprise IT Solutions & Technology Services',
            'home_hero_subtitle': 'We enable constant enterprise transformation at speed and scale with award-winning digital solutions, cyber security, and managed cloud infrastructure.',
            'home_hero_button_label': 'Explore Solutions',
            'home_hero_button_url': '/#services',
            'layout_accent_color': '#ef3139',
            'footer_attribution': 'Images & Media courtesy of Pixabay / Freepik (Free Commercial License with Attribution)',
        },
        'menu_header': [
            ('Home', '/'),
            ('Solutions', '/#services'),
            ('Services', '/#services'),
            ('Articles', '/posts'),
            ('About', '/about'),
            ('Contact', '/contact'),
        ],
        'menu_footer': [
            ('Home', '/'),
            ('IT Solutions', '/#services'),
            ('Articles', '/posts'),
            ('About', '/about'),
            ('Contact Us', '/contact'),
        ],
        'menu_solutions': [
            ('Cloud Computing & DevOps', '/#services'),
            ('Cyber Security & Compliance', '/#services'),
            ('Data Analytics & Sync', '/#services'),
            ('Enterprise Software Engineering', '/#services'),
            ('24/7 Managed IT Support', '/#services'),
        ],
        'modules': [
            {
                'module_type': 'hero',
                'title': 'Hero Banner',
                'sort_order': 1,
                'config': {
                    'badge': 'High-Impact Enterprise IT',
                    'headline': 'Enterprise IT Solutions & Technology Services',
                    'subtext': 'We enable constant enterprise transformation at speed and scale with award-winning digital solutions, cyber security, and managed cloud infrastructure.',
                    'primary_btn_text': 'Explore Solutions',
                    'primary_btn_url': '/#services',
                    'secondary_btn_text': 'Book Consultation',
                    'secondary_btn_url': '/contact',
                    'metric_val_1': '15+',
                    'metric_lbl_1': 'Years Experience',
                    'metric_val_2': '99.99%',
                    'metric_lbl_2': 'Service Uptime',
                    'metric_val_3': '450+',
                    'metric_lbl_3': 'Cloud Migrations',
                    'metric_val_4': '24/7',
                    'metric_lbl_4': 'Support NOC',
                    'cert_text': 'Verified Enterprise SLA Provider • SOC2 & ISO 27001 Certified',
                    'bg_style': 'gradient-navy',
                    'font_color': '#ffffff',
                    'font_opacity': '100',
                    'accent_color': '#ef3139',
                    'accent_opacity': '100'
                }
            },
            {
                'module_type': 'features_strip',
                'title': 'Features Highlight Strip',
                'sort_order': 2,
                'config': {
                    'col1_title': 'Enterprise Cyber Defense',
                    'col1_desc': 'Zero-trust architecture, automated vulnerability scanning, and 24/7 SOC perimeter monitoring.',
                    'col2_title': 'Multi-Cloud Architecture',
                    'col2_desc': 'Hyperscale migrations across AWS, Azure, and private Kubernetes clusters with zero downtime.',
                    'col3_title': 'Real-Time Data Pipelines',
                    'col3_desc': 'Sub-millisecond data pipelines, event streaming, and resilient business continuity failovers.',
                    'bg_style': 'slate-50',
                    'font_color': '#1e293b',
                    'accent_color': '#ef3139'
                }
            },
            {
                'module_type': 'about',
                'title': 'About & Capabilities',
                'sort_order': 3,
                'config': {
                    'kicker': 'About Tek Club',
                    'headline': 'Decade of Engineering Excellence & Mission-Critical Architecture',
                    'story_1': 'Since 2010, Tek Club has engineered scalable digital foundations for global industry leaders across finance, healthcare, and logistics.',
                    'story_2': 'Our cross-functional teams combine certified DevOps architects, cybersecurity specialists, and full-stack software engineers dedicated to high-availability delivery.',
                    'check_1': 'ISO 27001 & Cyber Essentials Certified Perimeters',
                    'check_2': '100% Infrastructure-as-Code Reproducibility',
                    'check_3': 'Transparent SLAs with Dedicated Incident Command',
                    'year_established': '2010',
                    'established_label': 'Years Driving Enterprise Innovation',
                    'bg_style': 'white',
                    'font_color': '#1e293b',
                    'accent_color': '#ef3139'
                }
            },
            {
                'module_type': 'services',
                'title': 'IT Services & Solutions Grid',
                'sort_order': 4,
                'config': {
                    'kicker': 'Our Capabilities',
                    'headline': 'Comprehensive IT Solutions Tailored for Enterprise Scale',
                    'subhead': 'End-to-end capabilities covering the entire digital infrastructure lifecycle.',
                    's1_title': 'Cloud Migration & Kubernetes',
                    's1_desc': 'Seamless infrastructure transitions with automated CI/CD pipelines, container orchestration, and zero downtime.',
                    's2_title': 'Cybersecurity & Perimeters',
                    's2_desc': 'Continuous threat monitoring, zero-trust network access, penetration testing, and regulatory compliance.',
                    's3_title': 'Enterprise Software Engineering',
                    's3_desc': 'Robust web applications and microservices engineered in high-performance Python, Go, and compiled assets.',
                    's4_title': 'Database & Telemetry Streaming',
                    's4_desc': 'High-throughput database clusters, PostgreSQL replication, automated failovers, and analytics pipelines.',
                    's5_title': '24/7 Managed NOC & Support',
                    's5_desc': 'Round-the-clock engineer-staffed network operations center with 15-minute SLA response guarantees.',
                    's6_title': 'SaaS & API Platform Architecture',
                    's6_desc': 'Scalable multi-tenant platforms with role-based access, SSO integration, and billing telemetry.',
                    'bg_style': 'slate-50',
                    'font_color': '#1e293b',
                    'accent_color': '#ef3139'
                }
            },
            {
                'module_type': 'case_studies',
                'title': 'Client Case Studies',
                'sort_order': 5,
                'config': {
                    'kicker': 'Proven Track Record',
                    'headline': 'Real Outcomes Engineered for Industry Leaders',
                    'c1_tag': 'FinTech & Banking',
                    'c1_title': 'Migrating Tier-1 Payment Processing to Micro-Kubernetes',
                    'c1_desc': 'Reduced transaction latency by 68% and achieved 100% PCI-DSS compliance under high-frequency spikes.',
                    'c2_tag': 'Global Logistics',
                    'c2_desc': 'Unified 14 regional distribution warehouses into a resilient streaming telemetry pipeline.',
                    'c2_title': 'Real-Time Fleet Fleet Telemetry at Scale',
                    'c3_tag': 'HealthTech',
                    'c3_title': 'ISO 27001 Secure Patient Health Record Architecture',
                    'c3_desc': 'Zero-trust perimeter protecting 3M+ active patient records with end-to-end encrypted storage.',
                    'bg_style': 'white',
                    'accent_color': '#ef3139'
                }
            },
            {
                'module_type': 'posts',
                'title': 'Latest News & Articles',
                'sort_order': 6,
                'config': {
                    'kicker': 'Knowledge Base',
                    'headline': 'Latest Technical Dispatches & Engineering Insights',
                    'subhead': 'Deep dives into modern containerization, cybersecurity compliance, and cloud architecture.',
                    'bg_style': 'slate-50',
                    'accent_color': '#ef3139'
                }
            },
            {
                'module_type': 'testimonials',
                'title': 'Client Testimonials',
                'sort_order': 7,
                'config': {
                    'kicker': 'Verified Reviews',
                    'headline': 'Trusted by Chief Technology Officers & Operations Heads',
                    't1_quote': 'Tek Club modernized our entire legacy stack in less than six months with zero downtime. Their architects are truly top-tier.',
                    't1_name': 'Marcus Vance',
                    't1_role': 'CTO, FinEdge Payments',
                    't2_quote': 'Their 24/7 incident response SLA has saved us millions during Black Friday surges. We trust them completely with our cloud infrastructure.',
                    't2_name': 'Sarah Jenkins',
                    't2_role': 'VP Engineering, TransGlobal Freight',
                    't3_quote': 'The best engineering partner we have ever engaged with. Transparent, disciplined, and deeply knowledgeable in cybersecurity.',
                    't3_name': 'Dr. Alistair Chen',
                    't3_role': 'Head of Digital, MediVault Bio',
                    'bg_style': 'white',
                    'accent_color': '#ef3139'
                }
            },
            {
                'module_type': 'trust_strip',
                'title': 'Trust & Certification Strip',
                'sort_order': 8,
                'config': {
                    'label': 'Trusted by Global Leaders & Accredited by Industry Standards',
                    'b1_title': 'ISO 27001',
                    'b1_sub': 'Information Security',
                    'b2_title': 'AWS Partner',
                    'b2_sub': 'DevOps Competency',
                    'b3_title': 'Kubernetes',
                    'b3_sub': 'Certified Service Provider',
                    'b4_title': 'Cyber Essentials+',
                    'b4_sub': 'Government Accredited',
                    'bg_style': 'slate-50',
                    'accent_color': '#ef3139'
                }
            },
            {
                'module_type': 'contact_form',
                'title': 'Strategy Consultation Form',
                'sort_order': 9,
                'config': {
                    'kicker': 'Get Started',
                    'headline': 'Request an Enterprise Consultation & Architecture Audit',
                    'subhead': 'Direct project brief submission and office location details.',
                    'submit_btn_text': 'Submit Consultation Request',
                    'bg_style': 'white',
                    'accent_color': '#ef3139'
                }
            }
        ],
        'sidebar_widgets': {
            'recent_posts_title': 'Recent Dispatches',
            'categories_title': 'Practice Areas',
        },
        'pages': [
            {
                'slug': 'about',
                'title': 'About Tek Club Enterprise',
                'excerpt': 'High-impact enterprise IT, cloud infrastructure, and zero-trust cybersecurity for multinational businesses.',
                'template': 'default',
                'content': '<p>Tek Club Enterprise is a tier-one technology consultancy dedicated to modernizing mission-critical legacy architectures, engineering resilient multi-cloud systems, and defending enterprise digital perimeters with zero-trust protocols.</p><h2>Our Engineering Standards</h2><p>With 450+ successful cloud migrations and a verified 99.99% service SLA, our systems architects and 24/7 NOC engineers empower global organizations to innovate without friction.</p><h3>Core Capabilities</h3><ul><li>Zero-Downtime Multi-Cloud Migrations (AWS, Azure, GCP, Kubernetes)</li><li>Zero-Trust Enterprise Perimeter Hardening &amp; ISO 27001 Compliance</li><li>Sub-millisecond Real-Time Data Streaming &amp; Telemetry Pipelines</li><li>24/7 Managed NOC Dispatch &amp; Proactive Incident Remediation</li></ul>'
            },
            {
                'slug': 'contact',
                'title': 'Contact Enterprise Solutions',
                'excerpt': 'Engage our enterprise architecture team for cloud migrations, cybersecurity audits, or 24/7 NOC support.',
                'template': 'contact',
                'content': '<p>Whether you require a multi-cloud architecture audit, rapid zero-trust security deployment, or 24/7 managed infrastructure support, our senior enterprise consultants are available.</p>'
            }
        ],
        'categories': [
            {'name': 'Cyber Security', 'slug': 'cyber-security', 'description': 'Zero-trust architecture, perimeter defense, and enterprise compliance.'},
            {'name': 'Cloud Infrastructure', 'slug': 'cloud-infrastructure', 'description': 'Container orchestration, hyperscale migrations, and hybrid cloud.'},
            {'name': 'DevOps & Telemetry', 'slug': 'devops-telemetry', 'description': 'Automated CI/CD pipelines, observability, and sub-millisecond MTTR.'}
        ],
        'posts': [
            {
                'title': 'Zero-Trust Architecture: Defending the Modern Multi-Cloud Perimeter',
                'slug': 'zero-trust-architecture-defending-multi-cloud-perimeter',
                'excerpt': 'Why traditional perimeter defenses fail in distributed environments, and how identity-driven zero-trust protocols protect hybrid workloads.',
                'featured_image': '/static/img/tekclub_post1.svg',
                'category_slug': 'cyber-security',
                'content': '<p>Traditional network perimeter security assumes that everything inside the corporate firewall can be trusted. In modern distributed cloud topologies, this assumption is fundamentally flawed.</p><p>Implementing micro-segmentation, automated identity attestation, and ephemeral credential rotation minimizes blast radiuses and ensures audit readiness under ISO 27001 standards.</p><h2>Identity as the New Perimeter</h2><p>By enforcing mutual TLS (mTLS) and fine-grained role-based access control at every service hop, Tek Club clients eliminate lateral movement vectors.</p>'
            },
            {
                'title': 'Accelerating Enterprise CI/CD Pipelines: Lessons from 450+ Cloud Migrations',
                'slug': 'accelerating-enterprise-cicd-pipelines',
                'excerpt': 'Architectural patterns for high-throughput containerized deployments with automated rollback safety.',
                'featured_image': '/static/img/tekclub_post2.svg',
                'category_slug': 'cloud-infrastructure',
                'content': '<p>Scaling deployment velocity without sacrificing uptime is the hallmark of modern software engineering. By standardizing container builds and leveraging automated integration testing, teams reduce release lead times from weeks to minutes.</p><p>Our engineers detail the exact staging and canary rollout strategies deployed across 450+ mission-critical Kubernetes environments.</p>'
            },
            {
                'title': 'Real-Time Telemetry and Observability: Slashing Incident MTTR to Under 3 Minutes',
                'slug': 'real-time-telemetry-and-observability',
                'excerpt': 'How sub-millisecond event streaming and unified telemetry dashboards eliminate production blind spots.',
                'featured_image': '/static/img/tekclub_post3.svg',
                'category_slug': 'devops-telemetry',
                'content': '<p>High-frequency data streaming demands low latency, predictable resource boundaries, and automated self-healing.</p><p>By leveraging lightweight telemetry workers and automated alert aggregation, our NOC teams detect anomalies and trigger self-healing failovers before end users experience degraded latency.</p>'
            }
        ]
    },

    'nest': {
        'key': 'nest',
        'name': 'VitalGreens Organic',
        'badge': 'Food & Wellness',
        'category': 'Organic Living, Nutrition & Recipe Cards',
        'description': 'Fresh botanical layout with sage & emerald palette, farm-to-table nutrition highlights, recipe cards, meal plan showcases, and organic certifications.',
        'color': '#064e3b',
        'accent': '#10b981',
        'settings': {
            'site_title': 'VitalGreens',
            'site_tagline': 'Organic Living, Whole Nutrition & Farm-Fresh Recipes',
            'site_logo': '/static/img/vitalgreens_logo.svg',
            'header_style': 'centered_stacked',
            'header_bg_color': '#ffffff',
            'header_bg_opacity': '100',
            'header_text_color': '#064e3b',
            'header_text_opacity': '100',
            'header_accent_color': '#10b981',
            'header_accent_opacity': '100',
            'header_font_style': 'sans',
            'header_show_topbar': '1',
            'header_cta_text': 'Order Farm Box',
            'header_cta_url': '/contact',
            'footer_bg_color': '#064e3b',
            'footer_bg_opacity': '100',
            'footer_text_color': '#e2e8f0',
            'footer_text_opacity': '100',
            'footer_accent_color': '#10b981',
            'footer_accent_opacity': '100',
            'footer_logo': '/static/img/vitalgreens_logo_white.svg',
            'footer_about_text': 'VitalGreens connects conscious households with 100% certified organic farms, personalized whole-food meal plans, and nutrient-dense seasonal recipes.',
            'footer_copyright': '© 2026 VitalGreens Organic & Wellness. All rights reserved.',
            'home_hero_title': '100% Certified Organic Food & Whole-Body Wellness',
            'home_hero_subtitle': 'Nourish your vitality with handpicked farm-to-table harvests, nutritionist-approved meal plans, and clean living essentials.',
            'home_hero_button_label': 'Explore Meal Plans',
            'home_hero_button_url': '/#services',
            'layout_accent_color': '#10b981',
            'footer_attribution': 'Images & Media courtesy of Pixabay / Freepik (Free Commercial License with Attribution)',
        },
        'menu_header': [
            ('Home', '/'),
            ('Nutrition Plans', '/#services'),
            ('Farm Produce', '/#services'),
            ('Wellness Blog', '/posts'),
            ('Our Farms', '/about'),
            ('Contact Us', '/contact'),
        ],
        'menu_footer': [
            ('Home', '/'),
            ('Nutrition Plans', '/#services'),
            ('Wellness Blog', '/posts'),
            ('Our Farms', '/about'),
            ('Contact Us', '/contact'),
        ],
        'menu_solutions': [
            ('Weekly Organic Farm Boxes', '/#services'),
            ('Personalized Meal Plans', '/#services'),
            ('Whole-Food Nutrition Coaching', '/#services'),
            ('Gut Health & Detox Protocols', '/#services'),
            ('Seasonal Chef Recipe Cards', '/#services'),
        ],
        'modules': [
            {
                'module_type': 'hero',
                'title': 'Organic Harvest & Wholesome Farm Hero',
                'sort_order': 1,
                'config': {
                    'badge': '100% Organic & Farm Fresh',
                    'headline': 'Pure Organic Harvests & Wholesome Vitality Plans',
                    'subtext': 'Nourish your body with pesticide-free, sustainably harvested produce, holistic nutrition coaching, and delicious whole-food recipe plans delivered fresh.',
                    'primary_btn_text': 'Explore Meal Plans',
                    'primary_btn_url': '/#services',
                    'secondary_btn_text': 'Browse Healthy Recipes',
                    'secondary_btn_url': '/posts',
                    'metric_val_1': '100%',
                    'metric_lbl_1': 'Certified Organic',
                    'metric_val_2': '48 hrs',
                    'metric_lbl_2': 'Farm-to-Door Delivery',
                    'metric_val_3': '8,500+',
                    'metric_lbl_3': 'Happy Families',
                    'metric_val_4': '0%',
                    'metric_lbl_4': 'Artificial Additives',
                    'cert_text': 'Soil Association Certified • Non-GMO Project Verified • Zero Synthetic Sprays',
                    'bg_style': 'white',
                    'font_color': '#064e3b',
                    'font_opacity': '100',
                    'accent_color': '#10b981',
                    'accent_opacity': '100'
                }
            },
            {
                'module_type': 'features_strip',
                'title': 'Regenerative Farming & Eco Highlights',
                'sort_order': 2,
                'config': {
                    'col1_title': 'Ethical Local Farmers',
                    'col1_desc': 'Direct partnerships with certified regenerative growers who practice soil restoration and natural biodiversity.',
                    'col2_title': 'Nutrient-Dense Living',
                    'col2_desc': 'Produce harvested at peak ripeness to ensure maximum vitamins, minerals, and phytonutrients for your cells.',
                    'col3_title': 'Eco-Friendly Packaging',
                    'col3_desc': '100% compostable and recyclable plant-based packaging with zero single-use petroleum plastics.',
                    'bg_style': 'blue-50',
                    'font_color': '#064e3b',
                    'accent_color': '#10b981'
                }
            },
            {
                'module_type': 'about',
                'title': 'About VitalGreens Farm & Food Philosophy',
                'sort_order': 3,
                'config': {
                    'kicker': 'Our Philosophy',
                    'headline': 'Real Food As Medicine: Restoring Connection with Nature',
                    'story_1': 'VitalGreens was founded on the belief that real, unadulterated whole food is the ultimate foundation for human longevity, cognitive focus, and everyday energy.',
                    'story_2': 'We eliminate the middlemen between regenerative organic family farms and your dining table, bringing you harvest-fresh produce picked within 48 hours.',
                    'check_1': '100% Certified Soil Association Organic Produce',
                    'check_2': 'Personalized Nutrition & Macronutrient Guides',
                    'check_3': 'Carbon-Neutral Cold Chain Home Delivery',
                    'year_established': '2016',
                    'established_label': 'Years Cultivating Healthy Lifestyles',
                    'bg_style': 'white',
                    'font_color': '#064e3b',
                    'accent_color': '#10b981'
                }
            },
            {
                'module_type': 'services',
                'title': 'Farm Boxes & Dietary Wellness Programs Grid',
                'sort_order': 4,
                'config': {
                    'kicker': 'Wellness Programs',
                    'headline': 'Holistic Nutrition, Meal Preparation & Organic Delivery',
                    'subhead': 'Carefully curated dietary programs tailored to your lifestyle and metabolic wellness.',
                    's1_title': 'Weekly Organic Farm Boxes',
                    's1_desc': 'Handpicked seasonal heirloom fruits, crisp greens, root vegetables, and fresh culinary herbs delivered weekly.',
                    's2_title': 'Personalized Meal Plans',
                    's2_desc': 'Custom dietary roadmaps for Mediterranean, Ketogenic, Plant-Based, or Anti-Inflammatory living with shopping lists.',
                    's3_title': '1-on-1 Nutritionist Consultations',
                    's3_desc': 'Certified clinical nutritionists who evaluate your lifestyle, gut health biomarkers, and metabolic goals.',
                    's4_title': 'Seasonal Chef Recipe Cards',
                    's4_desc': 'Easy 20-minute gourmet recipes designed by holistic chefs to make weeknight wholesome dining effortless.',
                    's5_title': 'Gut Health & Detox Protocols',
                    's5_desc': 'Evidence-based microbiome support programs using prebiotic fiber, fermented foods, and digestive enzymes.',
                    's6_title': 'Family Wellness & Kids Boxes',
                    's6_desc': 'Delicious whole-food lunchbox snacks and finger foods that children love, with zero refined sugars or food dyes.',
                    'bg_style': 'blue-50',
                    'font_color': '#064e3b',
                    'accent_color': '#10b981'
                }
            },
            {
                'module_type': 'case_studies',
                'title': 'Member Turnarounds & Health Stories',
                'sort_order': 5,
                'config': {
                    'kicker': 'Transformation Stories',
                    'headline': 'Real Health Turnarounds from VitalGreens Members',
                    'c1_tag': 'Metabolic Health',
                    'c1_title': 'Reversing Fatigue & Brain Fog with Whole Plant Nutrition',
                    'c1_desc': 'How switching to daily organic green juices and low-glycemic meal prep restored Laura’s natural vitality in 30 days.',
                    'c2_tag': 'Family Health',
                    'c2_title': 'Transitioning a Family of Four to 100% Organic Meals',
                    'c2_desc': 'Simplified meal prep boxes that saved 6 hours weekly while cutting household grocery waste by over 45%.',
                    'c3_tag': 'Athletic Wellness',
                    'c3_title': 'Plant-Powered Athletic Recovery & Anti-Inflammatory Protocol',
                    'c3_desc': 'Marathon runner achieved personal best times while lowering systemic inflammation biomarkers by 38%.',
                    'bg_style': 'white',
                    'accent_color': '#10b981'
                }
            },
            {
                'module_type': 'posts',
                'title': 'Seasonal Harvest Recipes & Clean Living Journal',
                'sort_order': 6,
                'config': {
                    'kicker': 'Clean Living Journal',
                    'headline': 'Seasonal Recipes, Nutrition Science & Herbalism',
                    'subhead': 'Discover kitchen tips, antioxidant guides, and seasonal farmer updates.',
                    'bg_style': 'blue-50',
                    'accent_color': '#10b981'
                }
            },
            {
                'module_type': 'testimonials',
                'title': 'Community & Family Testimonials',
                'sort_order': 7,
                'config': {
                    'kicker': 'Member Reviews',
                    'headline': 'Loved by Over 8,500 Health-Conscious Homes',
                    't1_quote': 'The flavor difference in the heirloom tomatoes and wild kale is astounding. You can literally taste the clean soil and sunlight.',
                    't1_name': 'Emma Richardson',
                    't1_role': 'Yoga Instructor & Mother of 2',
                    't2_quote': 'The personalized meal plans took all the guesswork out of dinner. My husband and I feel energized, light, and sleep so much better.',
                    't2_name': 'David Miller',
                    't2_role': 'Architect, London',
                    't3_quote': 'As an integrative GP, I recommend VitalGreens to all my patients looking to reduce chronic inflammation through diet.',
                    't3_name': 'Dr. Fiona Campbell',
                    't3_role': 'Integrative Medicine Physician',
                    'bg_style': 'white',
                    'accent_color': '#10b981'
                }
            },
            {
                'module_type': 'trust_strip',
                'title': 'Organic & Non-GMO Certification Strip',
                'sort_order': 8,
                'config': {
                    'label': 'Strictly Certified Standards for Your Family’s Safety',
                    'b1_title': 'Soil Association',
                    'b1_sub': '100% Certified Organic',
                    'b2_title': 'Non-GMO Project',
                    'b2_sub': 'Verified Purity',
                    'b3_title': 'Fair Trade',
                    'b3_sub': 'Ethical Farming Partner',
                    'b4_title': 'B Corp Certified',
                    'b4_sub': 'Environmental Impact',
                    'bg_style': 'blue-50',
                    'accent_color': '#10b981'
                }
            },
            {
                'module_type': 'contact_form',
                'title': 'Farm Delivery & Nutrition Inquiries Desk',
                'sort_order': 9,
                'config': {
                    'kicker': 'Start Your Journey',
                    'headline': 'Consult with a VitalGreens Nutrition Specialist',
                    'subhead': 'Tell us about your dietary goals and we’ll customize your first organic farm delivery plan.',
                    'submit_btn_text': 'Book Nutrition Consultation',
                    'bg_style': 'white',
                    'accent_color': '#10b981'
                }
            }
        ],
        'sidebar_widgets': {
            'recent_posts_title': 'Seasonal Recipes & Guides',
            'categories_title': 'Whole Nutrition',
        },
        'pages': [
            {
                'slug': 'about',
                'title': 'About VitalGreens Organic Studio',
                'excerpt': 'Whole nutrition, organic farm partnerships, clinical nutrition meal planning, and holistic healthy living.',
                'template': 'default',
                'content': '<p>VitalGreens is an organic nutrition collective connecting families and wellness seekers directly with certified regenerative farms, clinical dietitians, and wholesome recipe crafters.</p><h2>Our Organic Philosophy</h2><p>We believe true vitality begins with nutrient-dense, chemical-free whole foods. Every fruit, vegetable, cold-pressed juice, and meal recipe in the VitalGreens ecosystem is 100% Soil Association and non-GMO verified.</p><h3>What Sets VitalGreens Apart</h3><ul><li>Direct Farm-to-Table Partnerships with 40+ Certified Organic Growers</li><li>Clinical Nutritionist Curated 7-Day and 14-Day Meal Plans</li><li>Zero Artificial Preservatives, Refined Sugars, or Synthetic Additives</li><li>Eco-Friendly Biodegradable Packaging for All Farm Boxes</li></ul>'
            },
            {
                'slug': 'contact',
                'title': 'Contact Our Nutrition Specialists',
                'excerpt': 'Consult our certified nutritionists, arrange farm box deliveries, or discuss dietary plans.',
                'template': 'contact',
                'content': '<p>Have questions about your dietary lifestyle, organic farm delivery schedules, or personalized recipe plans? Our clinical nutrition team is here to support your healthy living journey.</p>'
            }
        ],
        'categories': [
            {'name': 'Organic Nutrition', 'slug': 'organic-nutrition', 'description': 'Whole-food nutrients, micronutrient profiles, and seasonal harvest insights.'},
            {'name': 'Farm-to-Table Recipes', 'slug': 'farm-to-table-recipes', 'description': 'Delicious chef-crafted meals made exclusively with unrefined organic ingredients.'},
            {'name': 'Holistic Wellness', 'slug': 'holistic-wellness', 'description': 'Gut health, detox protocols, and mindful lifestyle guidance.'}
        ],
        'posts': [
            {
                'title': 'Seasonal Harvest Guide: Unlocking Maximum Micronutrients in Autumn Greens',
                'slug': 'seasonal-harvest-guide-micronutrients',
                'excerpt': 'Discover which leafy greens and root vegetables pack the highest antioxidant density this season.',
                'featured_image': '/static/img/vitalgreens_post1.svg',
                'category_slug': 'organic-nutrition',
                'content': '<p>As the weather cools, organic kale, Swiss chard, and heritage carrots undergo a natural frost-sweetening process that concentrates beneficial flavonoids and polyphenols.</p><p>Consuming vegetables harvested at peak seasonal ripeness provides up to 3x higher bioavailable vitamin C and sulforaphane compared to long-transit supermarket produce.</p><h2>Optimal Prep Techniques</h2><p>Gentle light steaming with extra virgin cold-pressed olive oil enhances the bioavailability of fat-soluble vitamins A, E, and K.</p>'
            },
            {
                'title': 'Cold-Pressed Cleanses vs Whole Smoothies: What Certified Nutritionists Recommend',
                'slug': 'cold-pressed-cleanses-vs-whole-smoothies',
                'excerpt': 'A clinical comparison between cold-pressed liquid nutrition and high-fiber blending.',
                'featured_image': '/static/img/vitalgreens_post2.svg',
                'category_slug': 'holistic-wellness',
                'content': '<p>Both cold-pressed juices and whole blended smoothies offer distinct biochemical benefits. Cold-pressed juices deliver an immediate infusion of micronutrients without taxing the digestive tract, making them ideal for morning resets.</p><p>Whole green smoothies retain prebiotic dietary fiber, supporting sustained insulin sensitivity and nourishing diverse gut microbiome flora.</p>'
            },
            {
                'title': '7-Day Gut Reset: Whole-Food Recipes for Sustained Daily Energy',
                'slug': '7-day-gut-reset-whole-food-recipes',
                'excerpt': 'A 7-day plant-rich culinary plan designed to reduce inflammation and restore natural digestion.',
                'featured_image': '/static/img/vitalgreens_post3.svg',
                'category_slug': 'farm-to-table-recipes',
                'content': '<p>Resetting gut health does not require deprivation or synthetic supplements. By focusing on fermented vegetables, probiotic kefir, organic bone broths, and high-polyphenol berries, your digestive barrier can rapidly regenerate.</p><p>Our kitchen team shares 21 complete breakfast, lunch, and dinner recipes made entirely from seasonal farm produce.</p>'
            }
        ]
    },

    'quizhub': {
        'key': 'quizhub',
        'name': 'Quizmondo Cosmic Arena',
        'badge': 'Gaming & Trivia',
        'category': 'Interactive Quizzes, Brain Games & Tournaments',
        'description': 'Vibrant neon cyber-gaming arena with electric violet & cyan accents, daily trivia challenge cards, multiplayer competition leaderboards, and tournament prize pools.',
        'color': '#130924',
        'accent': '#8b5cf6',
        'settings': {
            'site_title': 'Quizmondo.com',
            'site_tagline': 'The Cosmic Arcade Trivia Arena & Multiplayer Brain Showdowns',
            'site_logo': '/static/img/quizmondo_logo.svg',
            'header_style': 'split_nav',
            'header_bg_color': '#0f0728',
            'header_bg_opacity': '100',
            'header_text_color': '#f3e8ff',
            'header_text_opacity': '100',
            'header_accent_color': '#8b5cf6',
            'header_accent_opacity': '100',
            'header_font_style': 'bold-display',
            'header_show_topbar': '1',
            'header_cta_text': 'Play Arena Duels',
            'header_cta_url': '/arena/',
            'footer_bg_color': '#090317',
            'footer_bg_opacity': '100',
            'footer_text_color': '#d8b4fe',
            'footer_text_opacity': '100',
            'footer_accent_color': '#06b6d4',
            'footer_accent_opacity': '100',
            'footer_logo': '/static/img/quizmondo_logo.svg',
            'footer_about_text': 'Quizmondo is the premier gamified brain arena featuring turn-based WhatsApp duels, weekly pub quiz leagues, community quiz decks, and prize vault rewards.',
            'footer_copyright': '© 2026 Quizmondo.com. All rights reserved.',
            'home_hero_title': 'The Cosmic Brain Arena: Challenge Friends & Climb the Leaderboards',
            'home_hero_subtitle': 'Battle head-to-head in turn-based trivia duels, join weekly live pub quiz leagues, and author community quiz decks. 100% free with WhatsApp invitations!',
            'home_hero_button_label': 'Play Daily Challenge ⚡',
            'home_hero_button_url': '/arena/',
            'layout_accent_color': '#8b5cf6',
            'footer_attribution': 'Images & Media courtesy of Pixabay / Freepik (Free Commercial License with Attribution)',
        },
        'menu_header': [
            ('Arena Home', '/'),
            ('Play Duels', '/arena/'),
            ('Trivia Decks', '/arena/packs'),
            ('Pub Leagues', '/arena/leagues'),
            ('Leaderboard', '/arena/leaderboard'),
            ('Quiz Studio', '/arena/create'),
            ('Articles', '/posts'),
        ],
        'menu_footer': [
            ('Arena Home', '/'),
            ('Play Duels', '/arena/'),
            ('Trivia Decks', '/arena/packs'),
            ('Pub Leagues', '/arena/leagues'),
            ('Leaderboard', '/arena/leaderboard'),
            ('Quiz Studio', '/arena/create'),
            ('Articles', '/posts'),
        ],
        'menu_solutions': [
            ('Daily Brain Challenge', '/#services'),
            ('Multiplayer eSports Leagues', '/#services'),
            ('Science & Tech Cups', '/#services'),
            ('Pop Culture & Cinema Faceoff', '/#services'),
            ('Corporate Team Quiz Arenas', '/#services'),
        ],
        'modules': [
            {
                'module_type': 'hero',
                'title': 'Arcade & Live Trivia Arena',
                'sort_order': 1,
                'config': {
                    'badge': 'Live Multiplayer Arena Active',
                    'headline': 'Battle Live in the Ultimate Trivia & Esports Brain Arena',
                    'subtext': 'Compete head-to-head in high-stakes live quizzes, win weekly cash tournament pools, and prove your intellectual supremacy on the global leaderboard.',
                    'primary_btn_text': 'Play Daily Challenge',
                    'primary_btn_url': '/#services',
                    'secondary_btn_text': 'Browse Tournaments',
                    'secondary_btn_url': '/contact',
                    'metric_val_1': '50K+',
                    'metric_lbl_1': 'Active Competitors',
                    'metric_val_2': '1,200+',
                    'metric_lbl_2': 'Live Daily Quizzes',
                    'metric_val_3': '£10,000',
                    'metric_lbl_3': 'Monthly Prize Pool',
                    'metric_val_4': '99.8%',
                    'metric_lbl_4': 'Anti-Cheat FairPlay',
                    'cert_text': 'Certified eSports Fair Play • Instant Secure Prize Payouts • Low Latency Engine',
                    'bg_style': 'deep-slate',
                    'font_color': '#f8fafc',
                    'font_opacity': '100',
                    'accent_color': '#8b5cf6',
                    'accent_opacity': '100'
                }
            },
            {
                'module_type': 'features_strip',
                'title': 'Live Gameplay & Tournament Highlights',
                'sort_order': 2,
                'config': {
                    'col1_title': 'Instant Live Matchmaking',
                    'col1_desc': 'Match against players of identical skill levels in under 5 seconds with zero server lag or question delay.',
                    'col2_title': 'Verified Cash Tournaments',
                    'col2_desc': 'Weekly and monthly prize leagues with transparent leaderboards and direct automated bank payouts.',
                    'col3_title': 'ProctorGuard Anti-Cheat',
                    'col3_desc': 'Proprietary biometric response telemetry ensuring genuine human play and zero automated bot cheating.',
                    'bg_style': 'slate-50',
                    'font_color': '#1e293b',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'about',
                'title': 'About Trivia Stadium & Fair-Play Rules',
                'sort_order': 3,
                'config': {
                    'kicker': 'The Gaming Revolution',
                    'headline': 'Where Intellectual Agility Meets eSports Competition',
                    'story_1': 'TriviaMatrix was created to elevate trivia and knowledge sports into an authentic competitive arena with broadcast-grade spectator modes and instant payouts.',
                    'story_2': 'Over 50,000 registered quiz gladiators battle daily across general knowledge, computer science, medicine, cinema, and world history.',
                    'check_1': 'Over 250,000 Peer-Reviewed Validated Trivia Questions',
                    'check_2': 'Sub-15ms Real-Time Multiplayer WebSocket Infrastructure',
                    'check_3': 'Global ELO Ranking System with Divisional Tiers',
                    'year_established': '2023',
                    'established_label': 'Years Powering Competitive Gaming',
                    'bg_style': 'white',
                    'font_color': '#0f0728',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'services',
                'title': 'Quiz Disciplines & Game Modes Grid',
                'sort_order': 4,
                'config': {
                    'kicker': 'Game Modes',
                    'headline': 'Choose Your Battleground: 6 Intense Competition Formats',
                    'subhead': 'From lightning 60-second speed rounds to marathon tournament championships.',
                    's1_title': 'Daily Speed Blitz',
                    's1_desc': '10 rapid-fire questions in 60 seconds. High multipliers for speed streaks with daily leaderboard trophies.',
                    's2_title': 'Live Weekend Tournaments',
                    's2_desc': 'Single-elimination bracket tournaments with £2,500 weekend cash pools and live twitch spectator streams.',
                    's3_title': 'Science & Technology Cup',
                    's3_desc': 'Hardcore trivia covering quantum physics, machine learning, aerospace, and software architecture.',
                    's4_title': 'Pop Culture & Cinema League',
                    's4_desc': 'Deep trivia covering cinematic universes, 80s & 90s music, gaming lore, and comic book history.',
                    's5_title': '1v1 High-Roller Duels',
                    's5_desc': 'Wager points against friends or rivals in private duel rooms with custom category picks and timers.',
                    's6_title': 'Corporate Team Arenas',
                    's6_desc': 'Gamified company trivia events and team-building tournaments with custom corporate branding.',
                    'bg_style': 'slate-50',
                    'font_color': '#0f0728',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'case_studies',
                'title': 'Tournament Hall of Fame & Champions',
                'sort_order': 5,
                'config': {
                    'kicker': 'Hall of Fame',
                    'headline': 'Legendary Champions & Tournament Records',
                    'c1_tag': 'UK Championship',
                    'c1_title': 'Winning the £5,000 Summer Brain Invitational',
                    'c1_desc': 'How player "NeuralViper" answered 48 out of 50 speed questions in 42 seconds to claim the trophy.',
                    'c2_tag': 'Corporate League',
                    'c2_title': 'Enterprise Trivia Championship with 1,500 Live Employees',
                    'c2_desc': 'Global tech company boosted remote employee engagement scores by 74% with weekly live team arenas.',
                    'c3_tag': 'Universities',
                    'c3_title': 'Inter-Collegiate Knowledge Olympiad',
                    'c3_desc': '32 universities competed in an automated 4-week league streamed to over 40,000 live spectators.',
                    'bg_style': 'white',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'posts',
                'title': 'Arena Dispatches & Trivia Tactics',
                'sort_order': 6,
                'config': {
                    'kicker': 'Arena News',
                    'headline': 'Tournament Announcements, Patch Notes & Strategy Guides',
                    'subhead': 'Stay up to date with new question drops, season resets, and prize pool expansions.',
                    'bg_style': 'slate-50',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'testimonials',
                'title': 'Player Reviews & Champion Quotes',
                'sort_order': 7,
                'config': {
                    'kicker': 'Player Feedback',
                    'headline': 'What Competitive Quiz Enthusiasts Are Saying',
                    't1_quote': 'The thrill of the final countdown in the Sunday Major is unmatched. The payouts are instant and the questions are genuinely brilliant.',
                    't1_name': 'Liam Davies',
                    't1_role': 'Grandmaster Division Player, Manchester',
                    't2_quote': 'We host all our company town hall trivia sessions on TriviaMatrix. Flawless latency and our staff absolutely look forward to it all week.',
                    't2_name': 'Chloe Martinez',
                    't2_role': 'Head of People, FinScale Cloud',
                    't3_quote': 'Finally a trivia platform with zero bots and serious anti-cheat. The ranking system is fair and immensely addictive.',
                    't3_name': 'Oliver Thorne',
                    't3_role': 'University Quiz Team Captain',
                    'bg_style': 'white',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'trust_strip',
                'title': 'Fair-Play & Anti-Cheat Certification Strip',
                'sort_order': 8,
                'config': {
                    'label': 'Trusted by Competitive Esports Clubs & Certified Fair Play',
                    'b1_title': 'Instant Payouts',
                    'b1_sub': 'Direct Bank & Stripe Verified',
                    'b2_title': 'Anti-Cheat AI',
                    'b2_sub': 'Zero Bot Tolerance',
                    'b3_title': 'Sub-15ms Latency',
                    'b3_sub': 'Real-Time WebSockets',
                    'b4_title': 'FairPlay 2026',
                    'b4_sub': 'Certified eSports Rules',
                    'bg_style': 'slate-50',
                    'accent_color': '#8b5cf6'
                }
            },
            {
                'module_type': 'contact_form',
                'title': 'Host a League or Tournament Desk',
                'sort_order': 9,
                'config': {
                    'kicker': 'Host an Event',
                    'headline': 'Host a Private Tournament or Corporate Trivia Arena',
                    'subhead': 'Inquire about branded quiz leagues, custom question packs, and private enterprise servers.',
                    'submit_btn_text': 'Request Tournament Hosting',
                    'bg_style': 'white',
                    'accent_color': '#8b5cf6'
                }
            }
        ],
        'sidebar_widgets': {
            'recent_posts_title': 'Arena Match Logs',
            'categories_title': 'Battle Categories',
        },
        'pages': [
            {
                'slug': 'about',
                'title': 'About TriviaMatrix Arena',
                'excerpt': 'The premier live multiplayer brain gaming, esports trivia arena, and competitive knowledge championships.',
                'template': 'default',
                'content': '<p>TriviaMatrix Arena is the ultimate digital stadium for competitive brain gaming, live multiplayer trivia tournaments, and global knowledge showdowns.</p><h2>The Arena Engine</h2><p>Our real-time matchmaking engine pairs competitors across 50+ specialized categories, from quantum physics to cinematic history, delivering millisecond-accurate buzzer response and anti-cheat verification.</p><h3>Arena Highlights</h3><ul><li>Live Multiplayer Daily Cups with Real-Time Leaderboards</li><li>Ranked Elo Matchmaking &amp; Verified Grandmaster Divisions</li><li>Adaptive Difficulty Algorithms Tailored to Player Elo</li><li>Cryptographically Signed Tournament Cups &amp; Cash Prizes</li></ul>'
            },
            {
                'slug': 'contact',
                'title': 'Arena Match Operations & Tournament Support',
                'excerpt': 'Inquire about tournament sponsorships, corporate team leagues, or arena account support.',
                'template': 'contact',
                'content': '<p>Contact the TriviaMatrix Arena Match Directors for tournament schedule inquiries, custom corporate trivia leagues, or competitive referee support.</p>'
            }
        ],
        'categories': [
            {'name': 'Tournament Announcements', 'slug': 'tournament-announcements', 'description': 'Official schedules, prize pool releases, and bracket updates.'},
            {'name': 'Pro Trivia Tactics', 'slug': 'pro-trivia-tactics', 'description': 'Speed-round cognitive techniques, buzzer optimization, and memory mnemonics.'},
            {'name': 'Community Spotlights', 'slug': 'community-spotlights', 'description': 'Profiles of arena grandmasters, record streaks, and trivia legends.'}
        ],
        'posts': [
            {
                'title': 'World Trivia Championship 2026: Arena Registration Now Open',
                'slug': 'world-trivia-championship-2026-registration',
                'excerpt': 'Compete against 10,000 global players across 10 qualifier stages for the $50,000 championship trophy.',
                'featured_image': '/static/img/triviamatrix_post1.svg',
                'category_slug': 'tournament-announcements',
                'content': '<p>The annual World Trivia Championship kicks off next month in the TriviaMatrix Arena. Featuring double-elimination brackets and speed-buzzer showdowns, this year’s tournament spans 8 core disciplines.</p><p>Qualifiers will stream live to hundreds of thousands of spectators with live studio commentary and real-time interactive audience polls.</p>'
            },
            {
                'title': 'Mastering Speed-Round Tactics: How Top Arena Players Think Under 5 Seconds',
                'slug': 'mastering-speed-round-tactics',
                'excerpt': 'Cognitive priming and rapid deduction strategies used by top-ranked Grandmasters.',
                'featured_image': '/static/img/triviamatrix_post2.svg',
                'category_slug': 'pro-trivia-tactics',
                'content': '<p>In high-stakes arena trivia, knowledge alone is only half the equation. Response latency under 4.5 seconds determines who takes the buzzer lead.</p><p>Grandmasters utilize keyword scanning, predictive phonetics, and associative mnemonics to isolate the correct option before the question prompt finishes animating.</p>'
            },
            {
                'title': 'Community Spotlight: Inside the 48-Win Streak of Matrix Grandmaster \'VortexMind\'',
                'slug': 'community-spotlight-vortexmind-streak',
                'excerpt': 'An exclusive interview with the highest Elo player in TriviaMatrix Arena history.',
                'featured_image': '/static/img/triviamatrix_post3.svg',
                'category_slug': 'community-spotlights',
                'content': '<p>VortexMind has captivated the esports trivia community with an unprecedented 48 consecutive tournament victories. In this candid profile, they break down their daily memory training routines, favorite question categories, and mental resilience under pressure.</p>'
            }
        ]
    },

    'gym': {
        'key': 'gym',
        'name': 'ApexFit Performance',
        'badge': 'Athletics & Club',
        'category': 'Athletic Conditioning & Training Studio',
        'description': 'High-intensity athletic carbon aesthetic with blazing atomic orange accents, elite coach spotlights, class schedules, and athlete transformation records.',
        'color': '#09090b',
        'accent': '#f97316',
        'settings': {
            'site_title': 'ApexFit',
            'site_tagline': 'Elite Athletic Training, Strength & Performance Conditioning',
            'site_logo': '/static/img/apexfit_logo.svg',
            'header_style': 'classic_sticky',
            'header_bg_color': '#09090b',
            'header_bg_opacity': '100',
            'header_text_color': '#fafafa',
            'header_text_opacity': '100',
            'header_accent_color': '#f97316',
            'header_accent_opacity': '100',
            'header_font_style': 'bold-display',
            'header_show_topbar': '1',
            'header_cta_text': 'Free Trial Pass',
            'header_cta_url': '/contact',
            'footer_bg_color': '#09090b',
            'footer_bg_opacity': '100',
            'footer_text_color': '#a1a1aa',
            'footer_text_opacity': '100',
            'footer_accent_color': '#f97316',
            'footer_accent_opacity': '100',
            'footer_logo': '/static/img/apexfit_logo.svg',
            'footer_about_text': 'ApexFit is a state-of-the-art strength and athletic conditioning club dedicated to building resilient, high-performance athletes through science-backed training protocols.',
            'footer_copyright': '© 2026 ApexFit Performance Club. All rights reserved.',
            'home_hero_title': 'Forged in Discipline: Unleash Your Peak Athletic Performance',
            'home_hero_subtitle': 'Olympic coaching, world-class strength apparatus, and athletic recovery protocols engineered for serious progress.',
            'home_hero_button_label': 'Claim Free 7-Day Pass',
            'home_hero_button_url': '/#services',
            'layout_accent_color': '#f97316',
            'footer_attribution': 'Images & Media courtesy of Pixabay / Freepik (Free Commercial License with Attribution)',
        },
        'menu_header': [
            ('Home', '/'),
            ('Training Programs', '/#services'),
            ('Classes', '/#services'),
            ('Fitness Insights', '/posts'),
            ('The Facility', '/about'),
            ('Join Now', '/contact'),
        ],
        'menu_footer': [
            ('Home', '/'),
            ('Training Programs', '/#services'),
            ('Classes', '/#services'),
            ('The Facility', '/about'),
            ('Join Now', '/contact'),
        ],
        'menu_solutions': [
            ('Olympic Strength & Conditioning', '/#services'),
            ('High-Intensity Athletic HIIT', '/#services'),
            ('Mobility & Injury Prehab', '/#services'),
            ('Cryotherapy & Recovery Suite', '/#services'),
            ('Personalized 1-on-1 Coaching', '/#services'),
        ],
        'modules': [
            {
                'module_type': 'hero',
                'title': 'High-Performance Conditioning & Strength Hero',
                'sort_order': 1,
                'config': {
                    'badge': 'Forged in Discipline',
                    'headline': 'Unleash Your Peak Athletic & Strength Performance',
                    'subtext': 'State-of-the-art Olympic barbell platforms, world-class athletic coaches, and sports science recovery suites engineered to take your body to elite levels.',
                    'primary_btn_text': 'Claim Free 7-Day Pass',
                    'primary_btn_url': '/#services',
                    'secondary_btn_text': 'View Class Schedule',
                    'secondary_btn_url': '/contact',
                    'metric_val_1': '24/7',
                    'metric_lbl_1': 'Club Access',
                    'metric_val_2': '45+',
                    'metric_lbl_2': 'Olympic Coaches',
                    'metric_val_3': '10,000+',
                    'metric_lbl_3': 'Workouts Logged',
                    'metric_val_4': '98%',
                    'metric_lbl_4': 'Goal Attainment',
                    'cert_text': 'Hammer Strength Official Training Center • NASM & CSCS Certified Coaches',
                    'bg_style': 'deep-slate',
                    'font_color': '#ffffff',
                    'font_opacity': '100',
                    'accent_color': '#f97316',
                    'accent_opacity': '100'
                }
            },
            {
                'module_type': 'features_strip',
                'title': 'Facility Specs & Athletic Highlights',
                'sort_order': 2,
                'config': {
                    'col1_title': 'Custom Periodized Programs',
                    'col1_desc': 'Progressive overload training cycles designed to prevent plateaus and maximize hypertrophy and athletic power.',
                    'col2_title': 'Athletic Recovery Lab',
                    'col2_desc': 'Infrared saunas, whole-body cryotherapy, and compression boots to accelerate muscular repair and reduce soreness.',
                    'col3_title': 'InBody Body Composition',
                    'col3_desc': 'Medical-grade monthly bio-impedance scans to track exact skeletal muscle mass gains and visceral fat reductions.',
                    'bg_style': 'white',
                    'font_color': '#09090b',
                    'accent_color': '#f97316'
                }
            },
            {
                'module_type': 'about',
                'title': 'ApexFit Philosophy & Olympic Standards',
                'sort_order': 3,
                'config': {
                    'kicker': 'The Apex Standard',
                    'headline': 'Built for Champions, Accessible to Every Committed Individual',
                    'story_1': 'ApexFit was built on a simple truth: real results require discipline, verified movement mechanics, and an inspiring community that refuses to accept mediocrity.',
                    'story_2': 'Whether you are an aspiring powerlifter, a competitive field athlete, or a busy professional reclaiming your health, our coaches guide every rep with precision.',
                    'check_1': 'Olympic Competition Barbells & Eleiko Platforms',
                    'check_2': 'Comprehensive Functional Movement Screening',
                    'check_3': 'Tailored Daily Macronutrient & Recovery Strategies',
                    'year_established': '2015',
                    'established_label': 'Years Forging Stronger Bodies',
                    'bg_style': 'slate-50',
                    'font_color': '#09090b',
                    'accent_color': '#f97316'
                }
            },
            {
                'module_type': 'services',
                'title': 'Strength & Conditioning Programs Grid',
                'sort_order': 4,
                'config': {
                    'kicker': 'Training Disciplines',
                    'headline': 'Engineered Programs for Hypertrophy, Speed & Endurance',
                    'subhead': 'Scientifically structured classes and private coaching programs.',
                    's1_title': 'Olympic Lifting & Strength',
                    's1_desc': 'Master the clean, snatch, deadlift, and squat with video bio-mechanic feedback and certified lifting masters.',
                    's2_title': 'Athletic Conditioning & HIIT',
                    's2_desc': 'High-output metabolic conditioning utilizing sleds, assault bikes, rowing ergometers, and kettlebells.',
                    's3_title': '1-on-1 Elite Personal Coaching',
                    's3_desc': 'Dedicated coach accountability with customized workout routines, form checks, and weekly nutrition audits.',
                    's4_title': 'Functional Mobility & Prehab',
                    's4_desc': 'Targeted joint decompression and flexibility work designed to eliminate lower back pain and joint stiffness.',
                    's5_title': 'Athletic Recovery Suite',
                    's5_desc': 'Infrared sauna sessions, cold plunge contrast therapy, and percussion therapy to optimize sleep and nervous recovery.',
                    's6_title': 'Youth Athlete Development',
                    's6_desc': 'Foundation movement patterns, deceleration mechanics, and agility conditioning for young competitive athletes.',
                    'bg_style': 'white',
                    'font_color': '#09090b',
                    'accent_color': '#f97316'
                }
            },
            {
                'module_type': 'case_studies',
                'title': 'Athlete Transformations & PR Milestones',
                'sort_order': 5,
                'config': {
                    'kicker': 'Athlete Triumphs',
                    'headline': 'Documented Transformations & Personal Bests',
                    'c1_tag': 'Strength Athlete',
                    'c1_title': 'Adding 45kg to Deadlift While Dropping 8% Body Fat',
                    'c1_desc': 'Client rebuilt his posterior chain in 16 weeks through structured periodization and sports nutrition.',
                    'c2_tag': 'Executive Wellness',
                    'c2_title': 'From Sedentary Desk Worker to First Half-Marathon Finish',
                    'c2_desc': 'Restored cardiovascular fitness and eliminated chronic postural neck pain with 3 weekly morning sessions.',
                    'c3_tag': 'Powerlifting',
                    'c3_title': 'Regional Powerlifting Gold Medal & Bench Record',
                    'c3_desc': 'Master athlete broke the national M40 bench press record after 9 months of targeted peaking cycles.',
                    'bg_style': 'slate-50',
                    'accent_color': '#f97316'
                }
            },
            {
                'module_type': 'posts',
                'title': 'Periodization & Strength Training Logs',
                'sort_order': 6,
                'config': {
                    'kicker': 'Training Intel',
                    'headline': 'Strength Science, Workout Protocols & Fueling Guides',
                    'subhead': 'Articles authored by our sports scientists and certified strength coaches.',
                    'bg_style': 'white',
                    'accent_color': '#f97316'
                }
            },
            {
                'module_type': 'testimonials',
                'title': 'Athlete Reviews & Member Quotes',
                'sort_order': 7,
                'config': {
                    'kicker': 'Member Reviews',
                    'headline': 'Voices from the Training Floor',
                    't1_quote': 'ApexFit is not just another gym—it is a world-class training cathedral. The coaches care deeply and the equipment is the best money can buy.',
                    't1_name': 'James Sterling',
                    't1_role': 'Competitive Athlete, London',
                    't2_quote': 'I was intimidated to start lifting at age 42. The coaches taught me proper form and I am in the best shape of my adult life.',
                    't2_name': 'Rachel Green',
                    't2_role': 'Executive Director',
                    't3_quote': 'The recovery suite alone is worth the membership. Cold plunges and infrared sauna have made my recovery twice as fast.',
                    't3_name': 'Marcus Cole',
                    't3_role': 'Rugby Union Player',
                    'bg_style': 'slate-50',
                    'accent_color': '#f97316'
                }
            },
            {
                'module_type': 'trust_strip',
                'title': 'CSCS Coaching & Equipment Standards Strip',
                'sort_order': 8,
                'config': {
                    'label': 'Equipped by World Leaders in Athletic Conditioning',
                    'b1_title': 'Hammer Strength',
                    'b1_sub': 'Official Training Center',
                    'b2_title': 'Eleiko Sweden',
                    'b2_sub': 'Certified Olympic Equipment',
                    'b3_title': 'NASM & CSCS',
                    'b3_sub': 'Accredited Coaching Staff',
                    'b4_title': 'InBody 770',
                    'b4_sub': 'Medical Composition Tracking',
                    'bg_style': 'white',
                    'accent_color': '#f97316'
                }
            },
            {
                'module_type': 'contact_form',
                'title': 'Floor Desk & Training Consultation Form',
                'sort_order': 9,
                'config': {
                    'kicker': 'Join the Team',
                    'headline': 'Claim Your Complimentary 7-Day Performance Pass',
                    'subhead': 'Experience the facility, meet our coaches, and receive a free functional movement assessment.',
                    'submit_btn_text': 'Claim 7-Day Pass Now',
                    'bg_style': 'slate-50',
                    'accent_color': '#f97316'
                }
            }
        ],
        'sidebar_widgets': {
            'recent_posts_title': 'WOD & Training Logs',
            'categories_title': 'Training Disciplines',
        },
        'pages': [
            {
                'slug': 'about',
                'title': 'About ApexFit Performance Gym',
                'excerpt': 'High-performance athletic conditioning, Olympic barbell training, and contrast recovery suites.',
                'template': 'default',
                'content': '<p>ApexFit Performance Gym is an elite training facility engineered for athletes, strength competitors, and disciplined fitness enthusiasts who demand measurable physical transformation.</p><h2>Our Training Standard</h2><p>We reject fitness fads in favor of biomechanical precision, progressive barbell overload, and cutting-edge recovery science. Our facility is equipped with competition-grade Eleiko plates, custom rigs, and contrast ice plunge suites.</p><h3>Club Facilities</h3><ul><li>Competition Olympic Lifting Platforms &amp; Calibrated Steel Plates</li><li>High-Octane HYROX &amp; Functional Athletic Conditioning Zones</li><li>Cold-Plunge Cryo Suites (3°C) and Traditional Cedar Saunas (85°C)</li><li>Licensed Sports Nutritionists &amp; Strength Coaches with Decades of Experience</li></ul>'
            },
            {
                'slug': 'contact',
                'title': 'Book Your Assessment & Gym Tour',
                'excerpt': 'Schedule your free 7-day trial pass, coach consultation, or recovery suite tour.',
                'template': 'contact',
                'content': '<p>Ready to elevate your training? Speak with an ApexFit coach to schedule your initial biomechanical movement screening, personal tour, or trial pass.</p>'
            }
        ],
        'categories': [
            {'name': 'Strength & Conditioning', 'slug': 'strength-conditioning', 'description': 'Barbell programming, hypertrophy science, and compound lift mastery.'},
            {'name': 'Recovery & Longevity', 'slug': 'recovery-longevity', 'description': 'Contrast baths, sleep optimization, and mobility prehab.'},
            {'name': 'Nutrition & Fuel', 'slug': 'nutrition-fuel', 'description': 'Macronutrient timing, sports supplementation, and muscle protein synthesis.'}
        ],
        'posts': [
            {
                'title': 'The Science of Hypertrophy: Progressive Overload in Olympic Barbell Training',
                'slug': 'science-of-hypertrophy-progressive-overload',
                'excerpt': 'How periodized volume, mechanical tension, and strict bar path drive maximum muscular development.',
                'featured_image': '/static/img/apexfit_post1.svg',
                'category_slug': 'strength-conditioning',
                'content': '<p>Progressive overload is the undeniable physiological foundation of strength and muscular hypertrophy. Without systematic increases in mechanical tension, adaptation stagnates.</p><p>Our head strength coach breaks down RPE programming, micro-loading protocols, and compound movement execution for long-term athletic durability.</p>'
            },
            {
                'title': 'Contrast Therapy: Why Ice Plunge and Infrared Sauna Accelerate Muscle Recovery',
                'slug': 'contrast-therapy-ice-plunge-infrared-sauna',
                'excerpt': 'The cardiovascular and lymphatic benefits of combining 3°C cold water immersion with 85°C heat.',
                'featured_image': '/static/img/apexfit_post2.svg',
                'category_slug': 'recovery-longevity',
                'content': '<p>Alternating between extreme cold and deep infrared heat induces rapid vasodilation and vasoconstriction, flushing metabolic byproducts from hard-worked muscle tissue.</p><p>Studies demonstrate that contrast therapy reduces delayed-onset muscle soreness (DOMS) by up to 40% while significantly boosting parasympathetic tone for restorative sleep.</p>'
            },
            {
                'title': 'Pre-Workout Fueling: Macronutrient Timing for High-Intensity Interval Sessions',
                'slug': 'pre-workout-fueling-macronutrient-timing',
                'excerpt': 'How carbohydrate glycogen loading and essential amino acids prevent intra-workout catabolism.',
                'featured_image': '/static/img/apexfit_post3.svg',
                'category_slug': 'nutrition-fuel',
                'content': '<p>Intense athletic conditioning demands immediate glycogen availability. Training fasted during high-intensity intervals degrades peak power output and elevates cortisol.</p><p>Learn how to time complex carbohydrates, electrolytes, and branched-chain amino acids 90 minutes before your workout for sustained output.</p>'
            }
        ]
    },

    'course': {
        'key': 'course',
        'name': 'SkillForge Academy',
        'badge': 'Education & LMS',
        'category': 'Online Masterclasses & Professional Certifications',
        'description': 'Distinguished academy layout with deep royal blue & gold palette, accredited course catalog, interactive curriculum roadmap, and verified instructor credentials.',
        'color': '#0f172a',
        'accent': '#3b82f6',
        'settings': {
            'site_title': 'SkillForge',
            'site_tagline': 'Accelerate Your Career with Industry-Led Masterclasses',
            'site_logo': '/static/img/skillforge_logo.svg',
            'header_style': 'classic_sticky',
            'header_bg_color': '#0f172a',
            'header_bg_opacity': '100',
            'header_text_color': '#f8fafc',
            'header_text_opacity': '100',
            'header_accent_color': '#3b82f6',
            'header_accent_opacity': '100',
            'header_font_style': 'sans',
            'header_show_topbar': '1',
            'header_cta_text': 'Browse Courses',
            'header_cta_url': '/#services',
            'footer_bg_color': '#0f172a',
            'footer_bg_opacity': '100',
            'footer_text_color': '#94a3b8',
            'footer_text_opacity': '100',
            'footer_accent_color': '#f59e0b',
            'footer_accent_opacity': '100',
            'footer_logo': '/static/img/skillforge_logo_white.svg',
            'footer_about_text': 'SkillForge Academy delivers career-defining online masterclasses, verified professional certifications, and hands-on lab training instructed by senior Silicon Valley and Tech City engineers.',
            'footer_copyright': '© 2026 SkillForge Academy Ltd. All rights reserved.',
            'home_hero_title': 'Master High-Demand Tech, Cloud & AI Skills from Top Industry Leaders',
            'home_hero_subtitle': 'Accredited Certifications • Hands-on Project Labs • 1-on-1 Mentorship',
            'home_hero_button_label': 'Browse All Masterclasses',
            'home_hero_button_url': '/#services',
            'layout_accent_color': '#3b82f6',
            'footer_attribution': 'Images & Media courtesy of Pixabay / Freepik (Free Commercial License with Attribution)',
        },
        'menu_header': [
            ('Home', '/'),
            ('Academic Tracks', '/#services'),
            ('Masterclasses', '/#services'),
            ('Learning Hub', '/posts'),
            ('Faculty & Campus', '/about'),
            ('Admissions', '/contact'),
        ],
        'menu_footer': [
            ('Home', '/'),
            ('Academic Tracks', '/#services'),
            ('Masterclasses', '/#services'),
            ('Faculty & Campus', '/about'),
            ('Admissions', '/contact'),
        ],
        'menu_solutions': [
            ('Cloud Architecture Masterclass', '/#services'),
            ('Full-Stack Python & React Engineering', '/#services'),
            ('Applied Generative AI & LLMs', '/#services'),
            ('Cybersecurity & Ethical Hacking', '/#services'),
            ('Product Leadership & Strategy', '/#services'),
        ],
        'modules': [
            {
                'module_type': 'hero',
                'title': 'Accredited Masterclasses & Tech Tracks Hero',
                'sort_order': 1,
                'config': {
                    'badge': 'Accredited Career Accelerators',
                    'headline': 'Master High-Demand Tech, Cloud & AI Skills from Industry Leaders',
                    'subtext': 'Step into high-paying engineering, cybersecurity, and cloud careers with cohort-based masterclasses, real portfolio projects, and direct hiring partner referrals.',
                    'primary_btn_text': 'Browse All Masterclasses',
                    'primary_btn_url': '/#services',
                    'secondary_btn_text': 'Start Free 14-Day Trial',
                    'secondary_btn_url': '/contact',
                    'metric_val_1': '120+',
                    'metric_lbl_1': 'Accredited Courses',
                    'metric_val_2': '250K+',
                    'metric_lbl_2': 'Graduated Alumni',
                    'metric_val_3': '94%',
                    'metric_lbl_3': 'Career Placement Rate',
                    'metric_val_4': '4.9/5',
                    'metric_lbl_4': 'Student Satisfaction',
                    'cert_text': 'CPD Accredited Provider • AWS Training Partner • GitHub Campus Verified',
                    'bg_style': 'deep-slate',
                    'font_color': '#ffffff',
                    'font_opacity': '100',
                    'accent_color': '#3b82f6',
                    'accent_opacity': '100'
                }
            },
            {
                'module_type': 'features_strip',
                'title': 'Curriculum Pillars & Cloud Labs Strip',
                'sort_order': 2,
                'config': {
                    'col1_title': 'Hands-On Interactive Labs',
                    'col1_desc': 'Build real-world systems directly in cloud sandboxes with automated code grading and instant feedback.',
                    'col2_title': 'Senior Industry Mentors',
                    'col2_desc': 'Weekly 1-on-1 code reviews and career guidance from lead engineers working at top tech firms.',
                    'col3_title': 'Verified Digital Badges',
                    'col3_desc': 'Cryptographically verified certificates easily shareable on LinkedIn and recognized by corporate recruiters.',
                    'bg_style': 'white',
                    'font_color': '#0f172a',
                    'accent_color': '#3b82f6'
                }
            },
            {
                'module_type': 'about',
                'title': 'Pedagogy & Senior Faculty Standards',
                'sort_order': 3,
                'config': {
                    'kicker': 'Education Reimagined',
                    'headline': 'Bridging the Gap Between Academic Theory & Modern Industry Needs',
                    'story_1': 'SkillForge was founded by senior software architects frustrated with outdated university computer science curricula that failed to prepare students for modern cloud stacks.',
                    'story_2': 'Our curriculum updates every quarter in collaboration with top engineering hiring managers, ensuring you learn the exact tools, architectures, and design patterns used in production today.',
                    'check_1': 'Interactive Browser-Based Code & Cloud Terminals',
                    'check_2': 'Direct Career Placement with 300+ Partner Companies',
                    'check_3': 'Lifetime Access to Course Updates & Alumni Network',
                    'year_established': '2018',
                    'established_label': 'Years Empowering Modern Careers',
                    'bg_style': 'slate-50',
                    'font_color': '#0f172a',
                    'accent_color': '#3b82f6'
                }
            },
            {
                'module_type': 'services',
                'title': 'Engineering Tracks & Specializations Grid',
                'sort_order': 4,
                'config': {
                    'kicker': 'Curriculum Tracks',
                    'headline': 'Top Career Accelerators in Cloud, AI, and Software Engineering',
                    'subhead': 'Cohort-based masterclasses with hands-on capstone projects and mentor office hours.',
                    's1_title': 'Cloud Architecture & DevOps Masterclass',
                    's1_desc': 'Kubernetes orchestration, Terraform IaC, multi-region CI/CD pipelines, and AWS/Azure certification readiness.',
                    's2_title': 'Full-Stack Software Engineering',
                    's2_desc': 'High-performance Python backends, asynchronous APIs, database indexing, and modern reactive frontends.',
                    's3_title': 'Applied AI & LLM Systems',
                    's3_desc': 'Fine-tuning open weights, vector retrieval (RAG), multimodal prompt routing, and autonomous agent orchestration.',
                    's4_title': 'Cybersecurity & Perimeters',
                    's4_desc': 'Offensive security, network penetration testing, digital forensics, and zero-trust perimeter auditing.',
                    's5_title': 'Modern Product Management Bootcamp',
                    's5_desc': 'Product discovery, telemetry analytics, agile engineering leadership, and user behavioral roadmapping.',
                    's6_title': 'Enterprise Technical Leadership',
                    's6_desc': 'Transitioning from senior engineer to engineering manager, architectural governance, and team hiring.',
                    'bg_style': 'white',
                    'font_color': '#0f172a',
                    'accent_color': '#3b82f6'
                }
            },
            {
                'module_type': 'case_studies',
                'title': 'Alumni Career Transitions & Outcomes',
                'sort_order': 5,
                'config': {
                    'kicker': 'Graduate Outcomes',
                    'headline': 'From Novice to Lead Engineer: Real Alumni Journeys',
                    'c1_tag': 'Career Pivot',
                    'c1_title': 'Transitioning from Accountant to Cloud Solutions Architect',
                    'c1_desc': 'Graduated in 5 months and landed a £75k cloud engineer role at a FTSE 100 enterprise.',
                    'c2_tag': 'Upskilling',
                    'c2_title': 'Senior Engineer Promoted to Head of Architecture',
                    'c2_desc': 'Mastered Kubernetes and distributed systems to lead an international team of 24 engineers.',
                    'c3_tag': 'AI Innovation',
                    'c3_title': 'Building an Autonomous AI SaaS Startup During Capstone',
                    'c3_desc': 'Alumni secured seed funding for an automated document processing engine built on course foundations.',
                    'bg_style': 'slate-50',
                    'accent_color': '#3b82f6'
                }
            },
            {
                'module_type': 'posts',
                'title': 'Curriculum Roadmaps & Technical Dispatches',
                'sort_order': 6,
                'config': {
                    'kicker': 'Academy Journal',
                    'headline': 'Career Roadmaps, Architecture Tutorials & Tech Trends',
                    'subhead': 'Technical tutorials and career advice written by our staff engineers and guest instructors.',
                    'bg_style': 'white',
                    'accent_color': '#3b82f6'
                }
            },
            {
                'module_type': 'testimonials',
                'title': 'Graduate Reviews & Verified Badges',
                'sort_order': 7,
                'config': {
                    'kicker': 'Alumni Reviews',
                    'headline': 'Rated 4.9/5 by Over 250,000 Enrolled Students',
                    't1_quote': 'The hands-on labs were miles ahead of anything else I tried online. Within two months of graduating, I had two senior offers.',
                    't1_name': 'Daniel Thorne',
                    't1_role': 'DevOps Engineer at CloudScale',
                    't2_quote': 'The mentor feedback on my pull requests gave me the confidence to pass every technical whiteboard interview with ease.',
                    't2_name': 'Amina Patel',
                    't2_role': 'Software Engineer at Monzo',
                    't3_quote': 'We sponsor all our junior engineers through SkillForge because their curriculum perfectly matches what we build in production.',
                    't3_name': 'Robert Sterling',
                    't3_role': 'VP Engineering, FinTech Group',
                    'bg_style': 'slate-50',
                    'accent_color': '#3b82f6'
                }
            },
            {
                'module_type': 'trust_strip',
                'title': 'Hiring Partners & Industry Accreditations Strip',
                'sort_order': 8,
                'config': {
                    'label': 'Accredited by International Education Standards',
                    'b1_title': 'CPD Accredited',
                    'b1_sub': 'Continuous Professional Development',
                    'b2_title': 'AWS Partner',
                    'b2_sub': 'Authorized Curriculum',
                    'b3_title': 'GitHub Campus',
                    'b3_sub': 'Verified Partner',
                    'b4_title': 'ISO 9001',
                    'b4_sub': 'Quality Education Standards',
                    'bg_style': 'white',
                    'accent_color': '#3b82f6'
                }
            },
            {
                'module_type': 'contact_form',
                'title': 'Admissions & Syllabus Advisory Desk',
                'sort_order': 9,
                'config': {
                    'kicker': 'Take the Next Step',
                    'headline': 'Schedule a Free Career Roadmap Session',
                    'subhead': 'Meet with an admissions advisor to discuss your career background and discover the best masterclass track for your goals.',
                    'submit_btn_text': 'Book Free Roadmap Session',
                    'bg_style': 'slate-50',
                    'accent_color': '#3b82f6'
                }
            }
        ],
        'sidebar_widgets': {
            'recent_posts_title': 'Curriculum Updates',
            'categories_title': 'Specializations',
        },
        'pages': [
            {
                'slug': 'about',
                'title': 'About SkillForge Academy',
                'excerpt': 'Accredited online tech masterclasses, verified cryptographic diplomas, and industry-led curriculum.',
                'template': 'default',
                'content': '<p>SkillForge Academy empowers modern software engineers, cloud architects, and data scientists with rigorous, industry-accredited masterclasses designed by senior engineers from leading tech companies.</p><h2>Curriculum Built for the Real World</h2><p>Our courses replace passive video watching with interactive coding sandboxes, pull-request code reviews by experienced mentors, and production capstone projects deployed to live cloud infrastructure.</p><h3>Academy Advantages</h3><ul><li>Verifiable Cryptographic Diplomas with LinkedIn Credential Badging</li><li>1-on-1 Mentor Code Reviews from Staff and Principal Engineers</li><li>Hands-On Cloud Labs with Real Compute Instances &amp; Dockerized Sandboxes</li><li>Dedicated Career Placement Support with Hiring Partner Network</li></ul>'
            },
            {
                'slug': 'contact',
                'title': 'Admissions & Corporate Training',
                'excerpt': 'Reach out regarding cohort start dates, syllabus previews, or team training programs.',
                'template': 'contact',
                'content': '<p>Have questions about prerequisites, tuition financing, or enterprise group enrollments? The SkillForge Academy admissions office is ready to guide you.</p>'
            }
        ],
        'categories': [
            {'name': 'AI & Data Science', 'slug': 'ai-data-science', 'description': 'Deep learning, LLMs, model quantization, and production ML pipelines.'},
            {'name': 'Systems & Cloud', 'slug': 'systems-cloud', 'description': 'Rust, Go, Kubernetes cluster architecture, and distributed systems.'},
            {'name': 'Full-Stack Engineering', 'slug': 'fullstack-engineering', 'description': 'Modern web architectures, Python backends, and responsive UI engineering.'}
        ],
        'posts': [
            {
                'title': 'From Python Fundamentals to Production LLMs: The 2026 Curriculum',
                'slug': 'from-python-fundamentals-to-production-llms',
                'excerpt': 'A complete learning pathway from Python basics to fine-tuning and deploying quantized large language models.',
                'featured_image': '/static/img/skillforge_post1.svg',
                'category_slug': 'ai-data-science',
                'content': '<p>The software engineering landscape has transformed with the advent of generative AI. Today\'s engineers must understand not just how to prompt models, but how to fine-tune weights, configure vector retrieval databases, and deploy low-latency inference pipelines.</p><p>We detail our step-by-step roadmap for mastering transformer architectures and building scalable AI-powered applications.</p>'
            },
            {
                'title': 'The Rise of Rust in Distributed Systems: Why Modern Engineers Are Migrating',
                'slug': 'rise-of-rust-in-distributed-systems',
                'excerpt': 'How compile-time memory safety and zero-cost abstractions make Rust the ideal language for hyperscale infra.',
                'featured_image': '/static/img/skillforge_post2.svg',
                'category_slug': 'systems-cloud',
                'content': '<p>Garbage collection pauses in high-throughput systems can introduce unpredictable latency spikes. Rust provides C++ speed and memory control while eliminating segmentation faults and data races at compile time.</p><p>Our systems faculty explores why cloud infrastructure leaders are rewriting critical network proxies and storage engines in Rust.</p>'
            },
            {
                'title': 'Securing Microservices Mesh: Zero-Trust mTLS for Kubernetes Clusters',
                'slug': 'securing-microservices-mesh-zero-trust-kubernetes',
                'excerpt': 'Architecting encrypted inter-service communication and identity certificates with Istio and SPIFFE.',
                'featured_image': '/static/img/skillforge_post3.svg',
                'category_slug': 'systems-cloud',
                'content': '<p>In a cloud-native microservices architecture, pod-to-pod network traffic cannot be assumed secure. Implementing mutual TLS (mTLS) with automated certificate rotation guarantees confidentiality and cryptographic service identity.</p><p>Walk through practical configuration manifests for zero-trust service meshes in production Kubernetes.</p>'
            }
        ]
    }
}


def apply_theme_preset(theme_key):
    """
    Applies the full design preset, colors, header/footer configuration,
    modular homepage sections, pages, posts, and widgets for the chosen theme.
    """
    from ..models import db, SiteSetting, PageModule, SidebarWidget, MenuItem, Page, Post, Category, User

    preset = THEME_PRESETS.get(theme_key)
    if not preset:
        return False, f"Unknown theme preset: {theme_key}"

    # 1. Update Core Site Settings
    SiteSetting.set('active_theme', theme_key)
    for k, v in preset['settings'].items():
        SiteSetting.set(k, v)

    # 2. Overwrite Homepage Modules for this Theme
    # Cleanly remove all existing homepage modules
    PageModule.query.filter(PageModule.is_home == True).delete()

    # Also clean any stale modules attached to standard pages (about, contact)
    default_page_ids = [p.id for p in Page.query.filter(Page.slug.in_(['about', 'contact'])).all()]
    if default_page_ids:
        PageModule.query.filter(PageModule.page_id.in_(default_page_ids)).delete()

    # Recreate homepage modules matching theme preset
    for m_data in preset['modules']:
        m = PageModule(
            is_home=True,
            theme=theme_key,
            module_type=m_data['module_type'],
            title=m_data['title'],
            placement='above',
            sort_order=m_data['sort_order'],
            is_enabled=True
        )
        m.set_config(m_data['config'])
        db.session.add(m)

    # 3. Update / Seed Footer Column Widgets
    SidebarWidget.query.filter(SidebarWidget.sidebar_id.like('footer-%')).delete()

    # Footer Col 1: Brand Logo Widget
    w1 = SidebarWidget(
        sidebar_id='footer-1',
        widget_type='brand_logo',
        title=f"About {preset['settings']['site_title']}",
        sort_order=1
    )
    w1.set_config({
        'logo_url': preset['settings'].get('footer_logo') or preset['settings']['site_logo'],
        'description': preset['settings']['footer_about_text'],
        'phone': SiteSetting.get('contact_phone', '+44 (0) 20 7946 0912'),
        'email': SiteSetting.get('contact_email', 'solutions@tekclub.co.uk'),
        'font_color': preset['settings']['footer_text_color'],
        'font_opacity': '100',
        'accent_color': preset['settings']['footer_accent_color'],
        'accent_opacity': '100',
        'bg_color': '#ffffff',
        'bg_opacity': '0',
        'font_style': preset['settings'].get('header_font_style', 'sans')
    })

    # Footer Col 2: Solutions / Practice Areas Menu Widget
    w2 = SidebarWidget(
        sidebar_id='footer-2',
        widget_type='menu_widget',
        title='Practice Areas' if theme_key == 'hisoft' else ('Nutrition Focus' if theme_key == 'nest' else ('Disciplines & Modes' if theme_key == 'quizhub' else ('Training Programs' if theme_key == 'gym' else 'Academic Tracks'))),
        sort_order=1
    )
    w2.set_config({
        'menu_location': 'solutions',
        'font_color': preset['settings']['footer_text_color'],
        'font_opacity': '100',
        'accent_color': preset['settings']['footer_accent_color'],
        'accent_opacity': '100',
        'bg_color': '#ffffff',
        'bg_opacity': '0',
        'font_style': 'sans'
    })

    # Footer Col 3: Quick Links Menu Widget
    w3 = SidebarWidget(
        sidebar_id='footer-3',
        widget_type='menu_widget',
        title='Quick Links',
        sort_order=1
    )
    w3.set_config({
        'menu_location': 'footer',
        'font_color': preset['settings']['footer_text_color'],
        'font_opacity': '100',
        'accent_color': preset['settings']['footer_accent_color'],
        'accent_opacity': '100',
        'bg_color': '#ffffff',
        'bg_opacity': '0',
        'font_style': 'sans'
    })

    # Footer Col 4: Newsletter Widget
    w4 = SidebarWidget(
        sidebar_id='footer-4',
        widget_type='newsletter',
        title='Newsletter',
        content=f"Subscribe to our weekly briefing for {preset['settings']['site_title']} announcements and updates.",
        sort_order=1
    )
    w4.set_config({
        'font_color': preset['settings']['footer_text_color'],
        'font_opacity': '100',
        'accent_color': preset['settings']['footer_accent_color'],
        'accent_opacity': '100',
        'bg_color': '#ffffff',
        'bg_opacity': '0',
        'font_style': 'sans'
    })
    db.session.add_all([w1, w2, w3, w4])

    # 4. Update or Create Standard Pages (About, Contact) for this theme
    if 'pages' in preset:
        for p_data in preset['pages']:
            existing_page = Page.query.filter_by(slug=p_data['slug']).first()
            if existing_page:
                existing_page.title = p_data['title']
                existing_page.content = p_data['content']
                existing_page.excerpt = p_data.get('excerpt', '')
                if 'template' in p_data:
                    existing_page.template = p_data['template']
            else:
                new_page = Page(
                    title=p_data['title'],
                    slug=p_data['slug'],
                    content=p_data['content'],
                    excerpt=p_data.get('excerpt', ''),
                    template=p_data.get('template', 'default'),
                    status='publish'
                )
                db.session.add(new_page)

    # 5. Update Categories & Replace Blog Posts for this Theme
    cat_map = {}
    if 'categories' in preset:
        for c_data in preset['categories']:
            cat = Category.query.filter_by(slug=c_data['slug']).first()
            if not cat:
                cat = Category(
                    name=c_data['name'],
                    slug=c_data['slug'],
                    description=c_data.get('description', '')
                )
                db.session.add(cat)
                db.session.flush()
            cat_map[c_data['slug']] = cat.id

    first_user = User.query.first()
    author_id = first_user.id if first_user else None

    if 'posts' in preset:
        # Cleanly replace sample posts with active theme's authentic articles
        Post.query.delete()
        for post_data in preset['posts']:
            cat_id = cat_map.get(post_data.get('category_slug'))
            new_post = Post(
                title=post_data['title'],
                slug=post_data['slug'],
                content=post_data['content'],
                excerpt=post_data.get('excerpt', ''),
                featured_image=post_data.get('featured_image', ''),
                category_id=cat_id,
                author_id=author_id,
                status='publish'
            )
            db.session.add(new_post)

    # 6. Update Sidebar Right Widget Titles to Match Theme Vertical
    sw_cfg = preset.get('sidebar_widgets', {})
    recent_widget = SidebarWidget.query.filter_by(sidebar_id='sidebar-right', widget_type='recent_posts').first()
    if recent_widget and sw_cfg.get('recent_posts_title'):
        recent_widget.title = sw_cfg['recent_posts_title']
    cat_widget = SidebarWidget.query.filter_by(sidebar_id='sidebar-right', widget_type='categories').first()
    if cat_widget and sw_cfg.get('categories_title'):
        cat_widget.title = sw_cfg['categories_title']

    # 7. Update Solutions Submenu Items to match Theme Vertical
    preset_sol = preset.get('menu_solutions', [])
    if preset_sol:
        sol_items = MenuItem.query.filter_by(location='solutions', parent_id=None)\
            .order_by(MenuItem.sort_order.asc(), MenuItem.id.asc()).all()
        for idx, (lbl, url) in enumerate(preset_sol):
            if idx < len(sol_items):
                sol_items[idx].title = lbl
                sol_items[idx].url = url
                sol_items[idx].sort_order = idx + 1
            else:
                db.session.add(MenuItem(
                    title=lbl,
                    url=url,
                    location='solutions',
                    sort_order=idx + 1
                ))
        if len(sol_items) > len(preset_sol):
            for extra in sol_items[len(preset_sol):]:
                db.session.delete(extra)

    # 8. Update Header Menu to match Theme Vertical (Preserving user-added submenus)
    preset_header = preset.get('menu_header', [])
    if preset_header:
        header_roots = MenuItem.query.filter_by(location='header', parent_id=None)\
            .order_by(MenuItem.sort_order.asc(), MenuItem.id.asc()).all()
        for idx, (lbl, url) in enumerate(preset_header):
            if idx < len(header_roots):
                header_roots[idx].title = lbl
                header_roots[idx].url = url
                header_roots[idx].sort_order = idx + 1
            else:
                db.session.add(MenuItem(
                    title=lbl,
                    url=url,
                    location='header',
                    sort_order=idx + 1
                ))

    # 9. Update Footer Menu to match Theme Vertical
    preset_footer = preset.get('menu_footer', [])
    if preset_footer:
        footer_roots = MenuItem.query.filter_by(location='footer', parent_id=None)\
            .order_by(MenuItem.sort_order.asc(), MenuItem.id.asc()).all()
        for idx, (lbl, url) in enumerate(preset_footer):
            if idx < len(footer_roots):
                footer_roots[idx].title = lbl
                footer_roots[idx].url = url
                footer_roots[idx].sort_order = idx + 1
            else:
                db.session.add(MenuItem(
                    title=lbl,
                    url=url,
                    location='footer',
                    sort_order=idx + 1
                ))
        if len(footer_roots) > len(preset_footer):
            for extra in footer_roots[len(preset_footer):]:
                db.session.delete(extra)

    db.session.commit()
    return True, f"Theme successfully switched to {preset['name']}! Preset layout, colors, pages, posts, and modules have been imported."
