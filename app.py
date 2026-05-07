from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
import uuid
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = "joggle_jobs_secret_2024"

DATA_FILE = "data/jobs.json"
ADMIN_PASSWORD = "admin1234"

# ── helpers ──────────────────────────────────────────────────────────────────

def load_jobs():
    if not os.path.exists(DATA_FILE):
        return seed_jobs()
    with open(DATA_FILE) as f:
        return json.load(f)

def save_jobs(jobs):
    with open(DATA_FILE, "w") as f:
        json.dump(jobs, f, indent=2, default=str)

def seed_jobs():
    """Return and persist a rich set of demo jobs."""
    now = datetime.now()

    jobs = [
        # ── Nigeria ────────────────────────────────────────────────────────
        {
            "id": str(uuid.uuid4()), "title": "Senior Software Engineer",
            "company": "Flutterwave", "location": "Lagos, Nigeria",
            "type": "Full-time", "category": "Technology", "region": "nigeria",
            "salary": "₦800,000 – ₦1,200,000/mo",
            "description": "Join Africa's leading payments technology company. Build scalable APIs and microservices powering millions of transactions across the continent.",
            "requirements": "5+ yrs Python/Node.js, REST APIs, PostgreSQL, cloud infrastructure (AWS/GCP).",
            "logo": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=80&h=80&fit=crop",
            "apply_url": "https://flutterwave.com/us/careers",
            "posted": (now - timedelta(hours=3)).isoformat(), "featured": True, "source": "Flutterwave Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "Product Manager",
            "company": "Paystack", "location": "Lagos, Nigeria",
            "type": "Full-time", "category": "Product", "region": "nigeria",
            "salary": "₦600,000 – ₦900,000/mo",
            "description": "Shape the future of payments for African businesses. Own product roadmap, coordinate cross-functional teams, and drive adoption of Paystack's suite.",
            "requirements": "3+ yrs product management, fintech/payments background preferred, strong analytical mindset.",
            "logo": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=80&h=80&fit=crop",
            "apply_url": "https://paystack.com/careers",
            "posted": (now - timedelta(hours=6)).isoformat(), "featured": True, "source": "Paystack Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "UX/UI Designer",
            "company": "Andela", "location": "Remote (Nigeria)",
            "type": "Remote", "category": "Design", "region": "nigeria",
            "salary": "₦400,000 – ₦650,000/mo",
            "description": "Craft beautiful, user-centric experiences for our global talent platform. Conduct research, design flows, and collaborate with engineers.",
            "requirements": "Portfolio of shipped products, Figma proficiency, mobile-first design thinking.",
            "logo": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=80&h=80&fit=crop",
            "apply_url": "https://andela.com/careers/",
            "posted": (now - timedelta(hours=10)).isoformat(), "featured": False, "source": "Andela Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "Data Analyst",
            "company": "Konga", "location": "Abuja, Nigeria",
            "type": "Full-time", "category": "Data", "region": "nigeria",
            "salary": "₦250,000 – ₦400,000/mo",
            "description": "Analyse e-commerce data to uncover growth opportunities. Build dashboards, run A/B tests, and present insights to stakeholders.",
            "requirements": "SQL, Python/R, Power BI or Tableau, 2+ yrs analytics experience.",
            "logo": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=80&h=80&fit=crop",
            "apply_url": "https://www.konga.com/careers",
            "posted": (now - timedelta(days=1)).isoformat(), "featured": False, "source": "Konga Jobs"
        },
        {
            "id": str(uuid.uuid4()), "title": "DevOps Engineer",
            "company": "Interswitch Group", "location": "Lagos, Nigeria",
            "type": "Full-time", "category": "Technology", "region": "nigeria",
            "salary": "₦500,000 – ₦750,000/mo",
            "description": "Maintain and improve CI/CD pipelines, Kubernetes clusters, and cloud infrastructure for Nigeria's premier digital payment ecosystem.",
            "requirements": "Kubernetes, Terraform, CI/CD (Jenkins/GitLab), 3+ yrs DevOps.",
            "logo": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=80&h=80&fit=crop",
            "apply_url": "https://www.interswitchgroup.com/ng/careers",
            "posted": (now - timedelta(days=1, hours=4)).isoformat(), "featured": False, "source": "Interswitch Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "Digital Marketing Manager",
            "company": "Jumia Nigeria", "location": "Lagos, Nigeria",
            "type": "Full-time", "category": "Marketing", "region": "nigeria",
            "salary": "₦350,000 – ₦500,000/mo",
            "description": "Lead performance marketing campaigns across SEO, SEM, social, and email for Africa's largest e-commerce platform.",
            "requirements": "Google Ads, Meta Ads, GA4, content strategy, 4+ yrs digital marketing.",
            "logo": "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=80&h=80&fit=crop",
            "apply_url": "https://group.jumia.com/careers",
            "posted": (now - timedelta(days=2)).isoformat(), "featured": True, "source": "Jumia Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "Backend Engineer (Node.js)",
            "company": "PiggyVest", "location": "Remote (Nigeria)",
            "type": "Remote", "category": "Technology", "region": "nigeria",
            "salary": "₦450,000 – ₦700,000/mo",
            "description": "Build the savings infrastructure that empowers over 4 million Nigerians. Work on high-availability APIs and financial integrations.",
            "requirements": "Node.js, TypeScript, MongoDB, Redis, 3+ yrs backend.",
            "logo": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=80&h=80&fit=crop",
            "apply_url": "https://piggyvest.com/jobs",
            "posted": (now - timedelta(days=2, hours=5)).isoformat(), "featured": False, "source": "PiggyVest Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "HR Business Partner",
            "company": "MTN Nigeria", "location": "Lagos, Nigeria",
            "type": "Full-time", "category": "Human Resources", "region": "nigeria",
            "salary": "₦400,000 – ₦600,000/mo",
            "description": "Partner with business leaders to deliver HR strategies, manage talent pipelines, and foster an inclusive culture at Nigeria's largest telco.",
            "requirements": "CIPM/SHRM certification, 5+ yrs HR BP experience, labour law knowledge.",
            "logo": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=80&h=80&fit=crop",
            "apply_url": "https://www.mtnonline.com/careers/",
            "posted": (now - timedelta(days=3)).isoformat(), "featured": False, "source": "MTN Careers"
        },
        # ── International ──────────────────────────────────────────────────
        {
            "id": str(uuid.uuid4()), "title": "Machine Learning Engineer",
            "company": "Google DeepMind", "location": "London, UK",
            "type": "Full-time", "category": "Technology", "region": "international",
            "salary": "£95,000 – £140,000/yr",
            "description": "Advance the state of AI research and deploy ML models at global scale within one of the world's foremost AI labs.",
            "requirements": "PhD or equivalent, PyTorch/JAX, RL or generative modelling, published research preferred.",
            "logo": "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=80&h=80&fit=crop",
            "apply_url": "https://deepmind.google/about/careers/",
            "posted": (now - timedelta(hours=2)).isoformat(), "featured": True, "source": "Google Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "Full-Stack Developer",
            "company": "Shopify", "location": "Remote (Global)",
            "type": "Remote", "category": "Technology", "region": "international",
            "salary": "$120,000 – $160,000/yr",
            "description": "Build commerce tools used by millions of merchants worldwide. Ship full-stack features across React frontends and Ruby/Go backends.",
            "requirements": "React, Ruby on Rails or Go, GraphQL, PostgreSQL, 4+ yrs full-stack.",
            "logo": "https://images.unsplash.com/photo-1611162616475-46b635cb6868?w=80&h=80&fit=crop",
            "apply_url": "https://www.shopify.com/careers",
            "posted": (now - timedelta(hours=8)).isoformat(), "featured": True, "source": "Shopify Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "Cloud Solutions Architect",
            "company": "Amazon Web Services", "location": "Dubai, UAE",
            "type": "Full-time", "category": "Technology", "region": "international",
            "salary": "AED 35,000 – 55,000/mo",
            "description": "Help enterprise clients in the Middle East design and implement cloud solutions on AWS. Pre-sales, architecture reviews, and proof-of-concepts.",
            "requirements": "AWS Solutions Architect Professional cert, 6+ yrs cloud architecture, C-suite communication.",
            "logo": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=80&h=80&fit=crop",
            "apply_url": "https://www.amazon.jobs/en/teams/aws",
            "posted": (now - timedelta(hours=12)).isoformat(), "featured": False, "source": "AWS Jobs"
        },
        {
            "id": str(uuid.uuid4()), "title": "Cybersecurity Analyst",
            "company": "Deloitte", "location": "Toronto, Canada",
            "type": "Full-time", "category": "Technology", "region": "international",
            "salary": "CAD $85,000 – $110,000/yr",
            "description": "Protect clients from cyber threats through threat intelligence, incident response, and security architecture assessments.",
            "requirements": "CISSP/CISM, SIEM tools, penetration testing, 3+ yrs security.",
            "logo": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=80&h=80&fit=crop",
            "apply_url": "https://www2.deloitte.com/global/en/careers.html",
            "posted": (now - timedelta(days=1, hours=2)).isoformat(), "featured": False, "source": "Deloitte Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "Financial Analyst",
            "company": "JPMorgan Chase", "location": "New York, USA",
            "type": "Full-time", "category": "Finance", "region": "international",
            "salary": "$90,000 – $120,000/yr",
            "description": "Support investment banking deal teams with financial modelling, valuation, and market analysis across sectors.",
            "requirements": "CFA Level I+, advanced Excel/VBA, DCF/LBO modelling, 2+ yrs IB/PE.",
            "logo": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=80&h=80&fit=crop",
            "apply_url": "https://careers.jpmorgan.com/",
            "posted": (now - timedelta(days=1, hours=8)).isoformat(), "featured": True, "source": "JPMorgan Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "Content Strategist",
            "company": "HubSpot", "location": "Remote (Europe)",
            "type": "Remote", "category": "Marketing", "region": "international",
            "salary": "€55,000 – €75,000/yr",
            "description": "Own content strategy for HubSpot's EMEA blog, webinars, and thought-leadership programmes. Grow organic traffic and inbound pipeline.",
            "requirements": "SEO expertise, B2B SaaS content, editorial calendar management, 3+ yrs content strategy.",
            "logo": "https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=80&h=80&fit=crop",
            "apply_url": "https://www.hubspot.com/jobs",
            "posted": (now - timedelta(days=2, hours=2)).isoformat(), "featured": False, "source": "HubSpot Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "Operations Manager",
            "company": "DHL Express", "location": "Johannesburg, South Africa",
            "type": "Full-time", "category": "Operations", "region": "international",
            "salary": "ZAR 45,000 – 65,000/mo",
            "description": "Oversee daily express logistics operations, manage a team of 50+, and drive KPI improvements across the Southern Africa hub.",
            "requirements": "Supply chain management degree, 5+ yrs logistics ops, P&L accountability.",
            "logo": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=80&h=80&fit=crop",
            "apply_url": "https://careers.dhl.com/",
            "posted": (now - timedelta(days=2, hours=10)).isoformat(), "featured": False, "source": "DHL Careers"
        },
        {
            "id": str(uuid.uuid4()), "title": "React Native Developer",
            "company": "Revolut", "location": "Remote (Global)",
            "type": "Remote", "category": "Technology", "region": "international",
            "salary": "$100,000 – $140,000/yr",
            "description": "Build the mobile banking experience for 40+ million Revolut customers. Own features end-to-end from design to App Store.",
            "requirements": "React Native, TypeScript, CI/CD for mobile, 4+ yrs mobile dev.",
            "logo": "https://images.unsplash.com/photo-1601597111158-2fceff292cdc?w=80&h=80&fit=crop",
            "apply_url": "https://www.revolut.com/careers/",
            "posted": (now - timedelta(days=3)).isoformat(), "featured": True, "source": "Revolut Careers"
        },
    ]
    save_jobs(jobs)
    return jobs


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    jobs = load_jobs()
    featured = [j for j in jobs if j.get("featured")][:6]
    stats = {
        "total": len(jobs),
        "nigeria": len([j for j in jobs if j["region"] == "nigeria"]),
        "international": len([j for j in jobs if j["region"] == "international"]),
        "remote": len([j for j in jobs if j["type"] == "Remote"]),
    }
    return render_template("index.html", featured=featured, stats=stats)


@app.route("/jobs")
def jobs_page():
    jobs = load_jobs()
    query   = request.args.get("q", "").lower()
    region  = request.args.get("region", "all")
    cat     = request.args.get("category", "all")
    jtype   = request.args.get("type", "all")
    page    = int(request.args.get("page", 1))
    per_page = 12

    filtered = jobs
    if query:
        filtered = [j for j in filtered if
                    query in j["title"].lower() or
                    query in j["company"].lower() or
                    query in j["location"].lower()]
    if region != "all":
        filtered = [j for j in filtered if j["region"] == region]
    if cat != "all":
        filtered = [j for j in filtered if j["category"] == cat]
    if jtype != "all":
        filtered = [j for j in filtered if j["type"] == jtype]

    filtered.sort(key=lambda x: x["posted"], reverse=True)

    total   = len(filtered)
    start   = (page - 1) * per_page
    paged   = filtered[start:start + per_page]
    pages   = (total + per_page - 1) // per_page

    categories = sorted(set(j["category"] for j in jobs))
    return render_template("jobs.html", jobs=paged, total=total,
                           page=page, pages=pages, categories=categories,
                           query=query, region=region, cat=cat, jtype=jtype)


@app.route("/job/<job_id>")
def job_detail(job_id):
    jobs = load_jobs()
    job = next((j for j in jobs if j["id"] == job_id), None)
    if not job:
        return redirect(url_for("jobs_page"))
    related = [j for j in jobs if j["category"] == job["category"] and j["id"] != job_id][:3]
    return render_template("job_detail.html", job=job, related=related)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact", methods=["POST"])
def contact_post():
    return render_template("contact.html", success=True)


# ── Admin ──────────────────────────────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        error = "Invalid password. Try again."
    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/admin")
@admin_required
def admin_dashboard():
    jobs = load_jobs()
    stats = {
        "total": len(jobs),
        "nigeria": len([j for j in jobs if j["region"] == "nigeria"]),
        "international": len([j for j in jobs if j["region"] == "international"]),
        "featured": len([j for j in jobs if j.get("featured")]),
    }
    recent = sorted(jobs, key=lambda x: x["posted"], reverse=True)[:20]
    return render_template("admin_dashboard.html", jobs=recent, stats=stats)


@app.route("/admin/add", methods=["GET", "POST"])
@admin_required
def admin_add():
    if request.method == "POST":
        jobs = load_jobs()
        new_job = {
            "id": str(uuid.uuid4()),
            "title": request.form["title"],
            "company": request.form["company"],
            "location": request.form["location"],
            "type": request.form["type"],
            "category": request.form["category"],
            "region": request.form["region"],
            "salary": request.form.get("salary", "Negotiable"),
            "description": request.form["description"],
            "requirements": request.form.get("requirements", ""),
            "logo": request.form.get("logo", ""),
            "posted": datetime.now().isoformat(),
            "featured": "featured" in request.form,
            "apply_url": request.form.get("apply_url", ""),
            "source": "Admin Upload",
        }
        jobs.insert(0, new_job)
        save_jobs(jobs)
        return redirect(url_for("admin_dashboard"))
    return render_template("admin_add.html")


@app.route("/admin/delete/<job_id>", methods=["POST"])
@admin_required
def admin_delete(job_id):
    jobs = load_jobs()
    jobs = [j for j in jobs if j["id"] != job_id]
    save_jobs(jobs)
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/toggle-featured/<job_id>", methods=["POST"])
@admin_required
def toggle_featured(job_id):
    jobs = load_jobs()
    for j in jobs:
        if j["id"] == job_id:
            j["featured"] = not j.get("featured", False)
    save_jobs(jobs)
    return redirect(url_for("admin_dashboard"))


# ── API ────────────────────────────────────────────────────────────────────────

@app.route("/api/jobs")
def api_jobs():
    jobs = load_jobs()
    return jsonify(jobs)


@app.route("/api/scrape", methods=["POST"])
@admin_required
def api_scrape():
    """Simulate live scraping with freshly timestamped jobs."""
    jobs = load_jobs()
    now = datetime.now()
    scraped = [
        {
            "id": str(uuid.uuid4()),
            "title": "Software Engineer II",
            "company": "Zenith Bank Digital",
            "location": "Lagos, Nigeria",
            "type": "Full-time",
            "category": "Technology",
            "region": "nigeria",
            "salary": "₦350,000 – ₦500,000/mo",
            "description": "Join the digital banking transformation team at Zenith Bank. Build internal tools and customer-facing apps.",
            "requirements": "Java or Python, Spring Boot, Oracle DB, 3+ yrs banking domain preferred.",
            "logo": "",
            "posted": now.isoformat(),
            "featured": False,
            "apply_url": "https://www.zenithbank.com/about-us/careers/",
            "source": "Jobberman.com (scraped)"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Blockchain Developer",
            "company": "Yellow Card Financial",
            "location": "Remote (Africa)",
            "type": "Remote",
            "category": "Technology",
            "region": "nigeria",
            "salary": "$4,000 – $7,000/mo",
            "description": "Build crypto exchange infrastructure powering fiat-to-crypto on-ramps across 20+ African markets.",
            "requirements": "Solidity/Rust, DeFi protocols, Web3.js, 3+ yrs blockchain dev.",
            "logo": "",
            "posted": now.isoformat(),
            "featured": False,
            "apply_url": "https://yellowcard.io/careers",
            "source": "LinkedIn Nigeria (scraped)"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "iOS Developer",
            "company": "Wise",
            "location": "Remote (Global)",
            "type": "Remote",
            "category": "Technology",
            "region": "international",
            "salary": "$95,000 – $130,000/yr",
            "description": "Build the Wise iOS app used by 16 million customers for international money transfers.",
            "requirements": "Swift, SwiftUI, XCTest, Combine, 4+ yrs iOS.",
            "logo": "",
            "posted": now.isoformat(),
            "featured": False,
            "apply_url": "https://wise.com/gb/careers/",
            "source": "We Work Remotely (scraped)"
        },
    ]
    # avoid duplicates
    existing_titles = {j["title"] + j["company"] for j in jobs}
    new_jobs = [j for j in scraped if j["title"] + j["company"] not in existing_titles]
    jobs = new_jobs + jobs
    save_jobs(jobs)
    return jsonify({"added": len(new_jobs), "message": f"Scraped {len(new_jobs)} new jobs"})


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app.run(debug=True, port=5050)
