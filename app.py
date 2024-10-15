from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from random import sample
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('signup'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully. Please log in.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/research-instructions')
@login_required
def research_instructions():
    return render_template('research_instructions.html')

@app.route('/research-guides')
@login_required
def research_guides():
    guides = [
        {
            "title": "Getting Started with Research",
            "description": "Learn the basics of conducting academic research.",
            "icon": "<circle cx='12' cy='12' r='10'/><line x1='12' y1='16' x2='12' y2='12'/><line x1='12' y1='8' x2='12' y2='8'/>"
        },
        {
            "title": "Literature Review Techniques",
            "description": "Master the art of writing comprehensive literature reviews.",
            "icon": "<path d='M4 19.5A2.5 2.5 0 0 1 6.5 17H20'/><path d='M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z'/>"
        },
        {
            "title": "Research Methodologies",
            "description": "Explore various research methodologies and when to use them.",
            "icon": "<polygon points='12 2 2 7 12 12 22 7 12 2'/><polyline points='2 17 12 22 22 17'/><polyline points='2 12 12 17 22 12'/>"
        },
        {
            "title": "Data Analysis Tools",
            "description": "Learn about popular data analysis tools and techniques.",
            "icon": "<line x1='18' y1='20' x2='18' y2='10'/><line x1='12' y1='20' x2='12' y2='4'/><line x1='6' y1='20' x2='6' y2='14'/>"
        }
    ]
    return render_template('research_guides.html', guides=guides)

@app.route('/academic-journals')
@login_required
def academic_journals():
    journals = [
        {
            "title": "Journal of Economic Literature",
            "field": "Economics",
            "impact_factor": 10.075,
            "image": "https://img.freepik.com/premium-photo/book-with-green-background-that-says-word-it_866549-869.jpg?w=1060"
        },
        {
            "title": "Quarterly Journal of Economics",
            "field": "Economics",
            "impact_factor": 8.545,
            "image": "https://img.freepik.com/premium-photo/book-with-green-background-that-says-word-it_866549-869.jpg?w=1060"
        },
        {
            "title": "Journal of Finance",
            "field": "Finance",
            "impact_factor": 6.201,
            "image": "https://img.freepik.com/premium-photo/book-with-green-background-that-says-word-it_866549-869.jpg?w=1060"
        },
        {
            "title": "Academy of Management Journal",
            "field": "Management",
            "impact_factor": 7.191,
            "image": "https://img.freepik.com/premium-photo/book-with-green-background-that-says-word-it_866549-869.jpg?w=1060"
        },
        {
            "title": "Journal of Marketing",
            "field": "Marketing",
            "impact_factor": 7.959,
            "image": "https://img.freepik.com/premium-photo/book-with-green-background-that-says-word-it_866549-869.jpg?w=1060"
        },
        {
            "title": "Journal of Business Ethics",
            "field": "Business",
            "impact_factor": 4.141,
            "image": "https://img.freepik.com/premium-photo/book-with-green-background-that-says-word-it_866549-869.jpg?w=1060"
        }
    ]
    return render_template('academic_journals.html', journals=journals)

@app.route('/research-tools')
@login_required
def research_tools():
    tool_categories = [
        {
            "id": "data-analysis",
            "name": "Data Analysis",
            "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>',
            "tools": [
                {
                    "name": "StatsPro",
                    "description": "Advanced statistical analysis tool with machine learning capabilities.",
                    "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>',
                    "url": "#",
                    "ai_feature": True
                },
                {
                    "name": "DataViz",
                    "description": "Interactive data visualization tool for creating stunning charts and graphs.",
                    "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"></path>',
                    "url": "#",
                    "ai_feature": False
                }
            ]
        },
        {
            "id": "literature-review",
            "name": "Literature Review",
            "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>',
            "tools": [
                {
                    "name": "LitAI",
                    "description": "AI-powered literature review assistant that summarizes and analyzes research papers.",
                    "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>',
                    "url": "#",
                    "ai_feature": True
                },
                {
                    "name": "CitationPro",
                    "description": "Automated citation generator and bibliography manager.",
                    "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>',
                    "url": "#",
                    "ai_feature": False
                }
            ]
        },
        {
            "id": "writing-editing",
            "name": "Writing & Editing",
            "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>',
            "tools": [
                {
                    "name": "AcademicWriter",
                    "description": "AI-powered academic writing assistant that helps improve clarity and structure.",
                    "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>',
                    "url": "#",
                    "ai_feature": True
                },
                {
                    "name": "ProofreadPro",
                    "description": "Advanced proofreading tool with grammar and style suggestions.",
                    "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>',
                    "url": "#",
                    "ai_feature": False
                }
            ]
        },
        {
            "id": "collaboration",
            "name": "Collaboration",
            "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>',
            "tools": [
                {
                    "name": "ResearchConnect",
                    "description": "Platform for finding and collaborating with researchers worldwide.",
                    "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>',
                    "url": "#",
                    "ai_feature": False
                },
                {
                    "name": "ProjectSync",
                    "description": "Real-time project management and collaboration tool for research teams.",
                    "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path>',
                    "url": "#",
                    "ai_feature": False
                }
            ]
        }
    ]

    featured_tool = {
        "name": "AI-Powered Research Assistant",
        "description": "Leverage artificial intelligence to streamline your research process, from literature review to data analysis.",
        "usage_time": "Save up to 40% research time",
        "user_count": "50,000+",
        "url": "#",
        "image_url": "https://example.com/ai-research-assistant.jpg"
    }

    return render_template('research_tools.html',
                           tool_categories=tool_categories,
                           featured_tool=featured_tool)

@app.route('/api/filter-tools', methods=['POST'])
@login_required
def filter_tools():
    category = request.json.get('category')
    search_query = request.json.get('search_query')

    filtered_tools = [tool for tool in research_tools if 
                      (category == 'All' or tool['category'] == category) and
                      (not search_query or search_query.lower() in tool['name'].lower() or search_query.lower() in tool['description'].lower())]

    return jsonify(filtered_tools)

@app.route('/api/compare-tools', methods=['POST'])
@login_required
def compare_tools():
    tool_ids = request.json.get('tool_ids')
    
    compared_tools = [tool for tool in research_tools if tool['id'] in tool_ids]
    
    return jsonify(compared_tools)

@app.route('/academic-services')
@login_required
def academic_services():
    economists = [
        {"name": "Paul Krugman", "specialty": "International Economics", "image": "static/paul-krugman.webp"},
        {"name": "Janet Yellen", "specialty": "Macroeconomics", "image": "static/janet-yellen.webp"},
        {"name": "Thomas Piketty", "specialty": "Economic Inequality", "image": "static/thomas-piketty.webp"},
        {"name": "Esther Duflo", "specialty": "Development Economics", "image": "static/esther-duflo.webp"},
        {"name": "Nouriel Roubini", "specialty": "Global Economics", "image": "static/nouriel-roubini.webp"},
        {"name": "Daron Acemoglu", "specialty": "Political Economy", "image": "static/daron-acemoglu.webp"},
        {"name": "Amartya Sen", "specialty": "Welfare Economics", "image": "static/amartya-sen.webp"},
        {"name": "Carmen Reinhart", "specialty": "International Finance", "image": "static/carmen-reinhert.webp"},
    ]
    
    business_resources = [
        {"title": "Effective Leadership Strategies", "description": "Learn key principles of leadership in modern business."},
        {"title": "Financial Planning for Startups", "description": "Master the basics of financial planning for new ventures."},
        {"title": "Digital Marketing Essentials", "description": "Discover the latest trends and techniques in digital marketing."},
        {"title": "Supply Chain Optimization", "description": "Explore strategies to streamline your supply chain operations."},
        {"title": "Data-Driven Decision Making", "description": "Harness the power of data analytics for better business decisions."},
        {"title": "Sustainable Business Practices", "description": "Implement eco-friendly strategies for long-term success."},
    ]
    
    tags = [
        "ProductStrategy", "DesignThinking", "FrontendDevelopment", "UXResearch",
        "GrowthMarketing", "CustomerSuccess", "PeopleManagement", "FinancialPlanning",
        "ContractLaw", "MarketResearch", "DataAnalytics", "MachineLearning",
        "BlockchainTechnology", "CorporateGovernance", "SupplyChainManagement"
    ]


    
    featured_course = {
        "title": "Master Business Strategy",
        "description": "Learn from industry experts and apply proven strategies to drive your business forward.",
        "enrollment_link": "#"  # Replace with actual link
    }
    
    return render_template('academic_services.html',
                           economists=economists,
                           business_resources=business_resources,
                           tags=tags,
                           featured_course=featured_course)

@app.route('/ai-research')
@login_required
def ai_research():
    applications = [
        {
            "id": "economic-forecasting",
            "title": "Economic Forecasting",
            "summary": "AI-powered models for accurate economic predictions.",
            "description": "Generative AI models can analyze vast amounts of historical and real-time economic data to produce more accurate and nuanced forecasts, helping policymakers and businesses make informed decisions.",
            "features": [
                "Analysis of large-scale economic datasets",
                "Real-time data integration",
                "Multi-variable forecasting models",
                "Scenario-based predictions"
            ],
            "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path>'
        },
        {
            "id": "policy-simulation",
            "title": "Policy Simulation",
            "summary": "Simulate economic impacts of policy decisions.",
            "description": "AI-powered simulations can model complex economic systems and predict the potential outcomes of various policy decisions, allowing for more effective policy-making and risk assessment.",
            "features": [
                "Complex system modeling",
                "Policy impact prediction",
                "Risk assessment tools",
                "Interactive simulation environments"
            ],
            "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path>'
        },
        {
            "id": "market-analysis",
            "title": "Market Analysis",
            "summary": "Deep insights into market trends and behaviors.",
            "description": "Generative AI can process and analyze market trends, consumer behavior, and economic indicators to provide deep insights for investment strategies and economic planning.",
            "features": [
                "Pattern recognition in market data",
                "Sentiment analysis of market participants",
                "Predictive modeling of market movements",
                "Automated report generation"
            ],
            "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>'
        },
        {
            "id": "automated-reporting",
            "title": "Automated Report Generation",
            "summary": "AI-generated comprehensive economic reports.",
            "description": "AI systems can generate comprehensive economic reports, summarizing key findings and trends from large datasets, saving time and reducing human error in data interpretation.",
            "features": [
                "Natural language generation",
                "Data visualization creation",
                "Customizable report templates",
                "Multi-lingual report options"
            ],
            "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>'
        },
        {
            "id": "scenario-planning",
            "title": "Scenario Planning",
            "summary": "AI-driven economic scenario generation.",
            "description": "Generative AI can create multiple economic scenarios based on different variables, helping organizations prepare for various potential future economic conditions.",
            "features": [
                "Multiple scenario generation",
                "Variable sensitivity analysis",
                "Probability-weighted outcomes",
                "Strategic planning tools"
            ],
            "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>'
        }
    ]

    return render_template('ai_research.html', applications=applications)


@app.route('/api/search-suggestions')
@login_required
def search_suggestions():
    # This is a mock implementation. In a real-world scenario, you'd query a database.
    all_suggestions = [
        "Paul Krugman", "Janet Yellen", "Thomas Piketty", "Esther Duflo",
        "Nouriel Roubini", "Daron Acemoglu", "Amartya Sen", "Carmen Reinhart",
        "Effective Leadership", "Financial Planning", "Digital Marketing",
        "Supply Chain Optimization", "Data-Driven Decision Making",
        "Sustainable Business Practices", "Product Strategy", "Design Thinking"
    ]
    return jsonify(sample(all_suggestions, 5))  # Return 5 random suggestions

@app.route('/economist/<name>')
@login_required
def economist_profile(name):
    economists = {
        "Paul Krugman": {
            "name": "Paul Krugman",
            "specialty": "International Economics",
            "image": "https://example.com/paul_krugman.jpg",
            "bio": "Paul Krugman is an American economist, professor, and columnist. He was awarded the Nobel Memorial Prize in Economic Sciences for his work on New Trade Theory and New Economic Geography.",
            "publications": [
                "The Return of Depression Economics and the Crisis of 2008",
                "The Conscience of a Liberal",
                "End This Depression Now!"
            ],
            "awards": ["Nobel Prize in Economics (2008)", "John Bates Clark Medal (1991)"]
        },
        # Add more economists here...
    }
    
    economist = economists.get(name)
    if economist:
        return render_template('economist_profile.html', economist=economist)
    else:
        return "Economist not found", 404
    
@app.route('/my-library')
@login_required
def my_library():
    # Mock data for papers and drafts
    papers = [
        {
            "title": "The Impact of AI on Economic Growth",
            "description": "An analysis of how artificial intelligence affects economic growth in developed countries.",
            "last_edited": "2023-04-15"
        },
        {
            "title": "Sustainable Urban Development",
            "description": "Exploring strategies for sustainable urban development in rapidly growing cities.",
            "last_edited": "2023-04-10"
        }
    ]
    
    drafts = [
        {
            "title": "Blockchain in Supply Chain Management",
            "description": "Investigating the potential of blockchain technology in improving supply chain efficiency.",
            "last_edited": "2023-04-18"
        },
        {
            "title": "The Future of Remote Work",
            "description": "Analyzing the long-term effects of remote work on productivity and work-life balance.",
            "last_edited": "2023-04-20"
        }
    ]
    
    return render_template('my_library.html', papers=papers, drafts=drafts)


@app.route('/edit-paper/<paper_id>', methods=['GET', 'POST'])
@login_required
def edit_paper(paper_id):
    # In a real application, you would fetch the paper from a database
    # For this example, we'll use a mock paper with additional data
    paper = {
        "id": paper_id,
        "title": "The Impact of AI on Economic Growth",
        "content": "Artificial Intelligence (AI) has emerged as a transformative force in the global economy...",
        "progress": 45,  # Percentage of completion
        "word_count": 1500,  # Current word count
        "time_spent": 8,  # Hours spent on the paper
        "deadlines": [
            {"title": "First Draft", "date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")},
            {"title": "Peer Review", "date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")},
            {"title": "Final Submission", "date": (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d")}
        ]
    }

    if request.method == 'POST':
        # Update the paper content
        paper['title'] = request.form['title']
        paper['content'] = request.form['content']
        
        # Update progress and word count
        words = paper['content'].split()
        paper['word_count'] = len(words)
        paper['progress'] = min(100, round((paper['word_count'] / 2000) * 100))  # Assuming 2000 words is 100%
        
        # In a real application, you would save these updates to the database
        flash('Paper updated successfully!', 'success')
        return redirect(url_for('my_library'))

    return render_template('edit_paper.html', paper=paper)

@app.route('/api/paper-stats/<paper_id>')
@login_required
def paper_stats(paper_id):
    # In a real application, you would fetch this data from the database
    stats = {
        "word_count": 1500,
        "time_spent": 8,
        "progress": 45
    }
    return jsonify(stats)

@app.route('/api/update-paper-progress/<paper_id>', methods=['POST'])
@login_required
def update_paper_progress(paper_id):
    # In a real application, you would update the database
    word_count = request.json.get('word_count', 0)
    progress = min(100, round((word_count / 2000) * 100))  # Assuming 2000 words is 100%
    
    # Update the database (mock update for this example)
    # db.papers.update_one({"id": paper_id}, {"$set": {"word_count": word_count, "progress": progress}})
    
    return jsonify({"success": True, "progress": progress})

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback = request.form.get('feedback')
        # Here you can process the feedback, e.g., save it to a database
        # For now, we'll just print it
        print(f"Received feedback: {feedback}")
        return redirect(url_for('thank_you'))
    return render_template('feedback.html')

@app.route('/thank-you')
def thank_you():
    return "Thank you for your feedback!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    
