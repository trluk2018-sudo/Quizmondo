"""Module registry, default configurations, and layout seeding for SiteBuilder Express."""

import copy

MODULE_DEFINITIONS = {
    'hero': {
        'type': 'hero',
        'name': 'Hero Banner',
        'icon': 'hero',
        'badge': 'Hero Header',
        'description': 'Full-width hero section with headline, subtext, dual action buttons, and verified metrics.',
        'default_placement': 'above',
        'default_config': {
            'badge': 'Award-Winning IT Solutions & Digital Services',
            'headline': 'Enterprise IT Solutions & Technology Services',
            'subtext': 'We enable constant enterprise transformation at speed and scale with award-winning digital solutions, cyber security, and managed cloud infrastructure.',
            'primary_btn_text': 'Explore Solutions',
            'primary_btn_url': '#services',
            'secondary_btn_text': 'Client Stories',
            'secondary_btn_url': '#case-studies',
            'metric_val_1': '25+', 'metric_lbl_1': 'Years Experience',
            'metric_val_2': '1.5k+', 'metric_lbl_2': 'Projects Delivered',
            'metric_val_3': '99.98%', 'metric_lbl_3': 'Service Uptime',
            'metric_val_4': '24/7/365', 'metric_lbl_4': 'Expert NOC Support',
            'cert_text': 'ISO 27001 & Cyber Essentials Plus Certified',
            'bg_style': 'gradient-navy',  # gradient-navy, deep-slate, crimson-dark, white
            'yt_enabled': '0',
            'yt_video_url': '',
            'yt_start': '',
            'yt_end': '',
            'yt_overlay_color': '#022d62',
            'yt_overlay_opacity': '75',
        }
    },
    'features_strip': {
        'type': 'features_strip',
        'name': 'Features Highlight Strip',
        'icon': 'strip',
        'badge': '3-Column Highlights',
        'description': '3-column highlights showcasing core features, capabilities, or differentiators.',
        'default_placement': 'above',
        'default_config': {
            'item1_title': 'Cyber Security & Defense',
            'item1_text': 'Proactive threat hunting, automated compliance, and real-time security operations.',
            'item1_icon': 'shield',
            'item2_title': 'Cloud Infrastructure & DevOps',
            'item2_text': 'High-availability Kubernetes clusters, infrastructure as code, and zero-downtime CI/CD.',
            'item2_icon': 'cloud',
            'item3_title': 'Enterprise Systems Integration',
            'item3_text': 'Resilient API orchestration, legacy modernization, and unified telemetry pipelines.',
            'item3_icon': 'cpu',
            'bg_style': 'white',  # white, slate-50, navy
        }
    },
    'about': {
        'type': 'about',
        'name': 'About & Capabilities',
        'icon': 'about',
        'badge': 'Brand Narrative',
        'description': 'Brand narrative story, established milestone, checkmarks, and key metrics.',
        'default_placement': 'above',
        'default_config': {
            'badge': 'Enterprise Engineering',
            'headline': 'From a Small Startup to a Leading Global Firm in 10 Years',
            'subtext': 'Scaling an enterprise technology firm requires unwavering adherence to architectural reliability, transparent engineering SLAs, and continuous reinvestment in automated infrastructure.',
            'year_established': '2010',
            'check_1': 'Zero-trust perimeter architecture as standard on all deployments',
            'check_2': 'Dedicated 24/7 UK-based Network Operations Centre (NOC)',
            'check_3': 'Predictable fixed-cost managed services with strict SLA guarantees',
            'stat1_val': '500+', 'stat1_lbl': 'Enterprise Workloads Managed',
            'stat2_val': '99.99%', 'stat2_lbl': 'Historical Availability Record',
        }
    },
    'services': {
        'type': 'services',
        'name': 'Services & Disciplines Grid',
        'icon': 'services',
        'badge': '6-Card Grid',
        'description': 'Multi-column card grid showcasing core services, disciplines, or programs.',
        'default_placement': 'above',
        'default_config': {
            'badge': 'Core Capabilities',
            'headline': 'Comprehensive IT Solutions & Managed Services',
            'subtext': 'End-to-end technical expertise designed to accelerate agility, defend critical assets, and drive business continuity.',
            'srv1_title': 'Managed Cloud & Kubernetes',
            'srv1_text': 'Scalable multi-cloud container orchestration with Coolify, Docker, and auto-scaling telemetry.',
            'srv2_title': 'Cyber Security & Zero Trust',
            'srv2_text': 'Penetration testing, identity governance, zero-trust network access, and ISO 27001 readiness.',
            'srv3_title': 'Data Architecture & Streaming',
            'srv3_text': 'High-throughput event-driven microservices and real-time telemetry processing.',
            'srv4_title': 'Enterprise DevOps & CI/CD',
            'srv4_text': 'Automated release pipelines, regression test harnesses, and automated rollback triggers.',
            'srv5_title': 'Systems Modernization',
            'srv5_text': 'Transforming legacy codebases into high-velocity Python and compiled Tailwind architectures.',
            'srv6_title': '24/7 NOC & Incident Defense',
            'srv6_text': 'Rapid-response incident remediation, proactive monitoring, and guaranteed 15-minute response SLAs.',
        }
    },
    'case_studies': {
        'type': 'case_studies',
        'name': 'Case Studies & Success Stories',
        'icon': 'cases',
        'badge': 'Impact Stories',
        'description': 'Real-world customer results, case studies, or student/athlete outcomes.',
        'default_placement': 'below',
        'default_config': {
            'badge': 'Proven Deliveries',
            'headline': 'Client Case Studies & Technical Impact',
            'subtext': 'Real-world results delivered for international financial institutions, logistics carriers, and clinical platforms.',
            'cs1_tag': 'FinTech / High-Frequency Data',
            'cs1_title': 'Scaling Telemetry Ingest for Global Payment Gateway',
            'cs1_result': '400% throughput increase with sub-10ms processing latency.',
            'cs2_tag': 'Healthcare / Zero-Trust',
            'cs2_title': 'Zero-Trust Perimeters for NHS Integrated Care Provider',
            'cs2_result': '100% Caldicott & ISO 27001 audit compliance with zero downtime.',
            'cs3_tag': 'Logistics / Cloud Migration',
            'cs3_title': 'Coolify Container Orchestration for Fleet Tracking',
            'cs3_result': '85% infrastructure footprint reduction and zero single points of failure.',
        }
    },
    'posts': {
        'type': 'posts',
        'name': 'Latest News & Articles',
        'icon': 'news',
        'badge': 'Dynamic Feed',
        'description': 'Dynamic feed of recent blog dispatches and announcements.',
        'default_placement': 'below',
        'default_config': {
            'badge': 'Technical Dispatches',
            'headline': 'Latest Insights & Engineering Whitepapers',
            'subtext': 'Articles, architecture guides, and technical commentary from our principal consultants.',
            'count': '3',
        }
    },
    'testimonials': {
        'type': 'testimonials',
        'name': 'Reviews & Testimonials',
        'icon': 'reviews',
        'badge': 'Verified Reviews',
        'description': 'Verified customer reviews, ratings, and quotes from clients or members.',
        'default_placement': 'below',
        'default_config': {
            'badge': 'Client Endorsements',
            'headline': 'Trusted by Technology Leaders',
            'subtext': 'What chief technology officers and engineering directors say about our delivery standards.',
            't1_quote': 'Their team re-architected our entire backend platform without a single minute of downtime. The performance leap was immediate.',
            't1_author': 'David Chen',
            't1_role': 'CTO, Meridian Financial Systems',
            't2_quote': 'SiteBuilder Express and their containerized architecture gave us sub-100ms TTFB and complete peace of mind on regulatory audits.',
            't2_author': 'Sarah Jenkins',
            't2_role': 'Director of Engineering, Apex Logistics',
        }
    },
    'trust_strip': {
        'type': 'trust_strip',
        'name': 'Trust & Certification Strip',
        'icon': 'trust',
        'badge': 'Accreditations',
        'description': 'Partner badges, certifications, and accreditation strip.',
        'default_placement': 'below',
        'default_config': {
            'headline': 'Certified & Compliant Enterprise Standards',
            'badge1': 'Microsoft Azure Silver Partner',
            'badge2': 'AWS Advanced Consulting Partner',
            'badge3': 'ISO 27001 Certified Security',
            'badge4': 'Cyber Essentials Plus Certified',
        }
    },
    'contact_cards': {
        'type': 'contact_cards',
        'name': 'Contact Info Cards (3-Column)',
        'icon': 'cards',
        'badge': 'Contact Channels',
        'description': 'The 3 distinct info cards: Headquarters, Telephone, and Email Inquiries with custom icons and notes.',
        'default_placement': 'above',
        'default_config': {
            'card1_title': 'Headquarters',
            'card1_text': '100 Bishopsgate, London EC2N 4AG, United Kingdom',
            'card1_icon': 'location',
            'card2_title': 'Direct Telephone',
            'card2_text': '+44 (0) 20 7946 0912',
            'card2_subtext': 'Mon – Fri: 08:30 – 18:00 GMT',
            'card2_icon': 'phone',
            'card3_title': 'Email Inquiries',
            'card3_text': 'info@sitebuilder-express.co.uk',
            'card3_subtext': 'Guaranteed SLA response within 4 hours',
            'card3_icon': 'email',
        }
    },
    'contact_form': {
        'type': 'contact_form',
        'name': 'Contact & Inquiry Desk',
        'icon': 'form',
        'badge': 'Inquiry Form',
        'description': 'Direct project or membership inquiry submission form and contact office notice block.',
        'default_placement': 'below',
        'default_config': {
            'badge': 'Consultation Request',
            'headline': 'Send Us Your Technical Brief',
            'subtext': 'Whether you are planning a migration to modern cloud infrastructure, upgrading legacy software, or auditing your cybersecurity perimeter, our architects are ready to assist.',
            'noc_title': 'Need Immediate Emergency NOC Support?',
            'noc_text': 'Enterprise customers with active SLA agreements can route tickets directly through their dedicated portal.',
            'button_text': 'Submit Request →',
        }
    },
    'text': {
        'type': 'text',
        'name': 'Text & Excerpt Block',
        'icon': 'text',
        'badge': 'Text & Excerpt',
        'description': 'Rich text content section featuring an optional styled excerpt / lead callout, headline, and body.',
        'default_placement': 'above',
        'default_config': {
            'badge': 'Enterprise Overview',
            'headline': 'Modern Digital Solutions Engineered for Resilience',
            'excerpt': 'We engineer robust digital architectures that empower modern organizations with high reliability, rapid scaling, and zero-trust security.',
            'body': '<p>Our cross-functional teams build scalable platforms combining enterprise reliability with developer velocity. From cloud orchestration to real-time telemetry, every component is rigorously tested and optimized for peak operational efficiency.</p>',
            'bg_style': 'white',  # white, slate-50, navy, blue-50
            'button_text': 'Learn More',
            'button_url': '/about',
        }
    },
    'rich_text': {
        'type': 'rich_text',
        'name': 'Custom Content & Callout Block',
        'icon': 'text',
        'badge': 'Flexible Content',
        'description': 'Add custom headings, optional styled excerpt, rich text/HTML body, or custom highlighted announcements.',
        'default_placement': 'below',
        'default_config': {
            'badge': 'Announcement',
            'headline': 'Special Feature or Information',
            'excerpt': '',
            'body': '<p>Add any custom announcements, marketing copy, rich descriptions, or embedded media here.</p>',
            'bg_style': 'slate-50',  # slate-50, white, navy, blue-50
            'button_text': '',
            'button_url': '',
        }
    }
}


def get_default_config(module_type: str) -> dict:
    defn = MODULE_DEFINITIONS.get(module_type)
    if defn and 'default_config' in defn:
        return copy.deepcopy(defn['default_config'])
    return {}


def get_module_definition(module_type: str) -> dict:
    return MODULE_DEFINITIONS.get(module_type, {
        'type': module_type,
        'name': module_type.replace('_', ' ').title(),
        'icon': 'cube',
        'badge': 'Custom Module',
        'description': '',
        'default_placement': 'above',
        'default_config': {}
    })
