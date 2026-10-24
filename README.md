# Quizmondo

A fast, interactive, and competitive live trivia & brain gaming arena powered by the lightweight Python Flask engine and compiled Tailwind CSS. Built for standalone deployment or centralized orchestration via Portside Server Manager.

---

## Key Features

- **Live Trivia & Esports Battle Arena**:
  - Interactive JavaScript quiz arena with instant answer validation, streak counters, and XP rewards.
  - High-impact neon cyber-gaming styling and tournament leaderboards.
  - Dedicated trivia categories: Science & Cosmos, Gaming & Esports, and World Trivia.
- **WordPress-Style Publishing & Content Management**:
  - **Articles & Battle Guides**: Tournament highlights, trivia tactics, excerpts, and featured media.
  - **Pages**: Static pages with custom layouts, rules pages, and concierge contact desk.
  - **Modular Homepage Builder**: Re-order and toggle live modules (Hero arena, daily challenges, game mode grids, champions hall of fame).
  - **Navigation & Widgets**: Full control of arena navigation menus and footer widgets.
  - **SEO & Meta Engine**: Automated XML sitemaps, OpenGraph metadata, and indexing controls.
- **Compiled Tailwind CSS**:
  - Native production styling compiled with `@tailwindcss/cli`.
  - Zero external CDN dependencies.
- **SaaS & Portside Control Plane Ready**:
  - HMAC Single Sign-On (`/admin/sso`) for 1-click administrative access from Portside Server Manager.
  - Return-to-Control-Centre link and session impersonation fully preserved.

---

## Quickstart (Local Development)

### 1. Install Node Dependencies & Build CSS
```bash
npm install
npm run build:css
```
To auto-recompile CSS during frontend development:
```bash
npm run watch:css
```

### 2. Install Python Dependencies & Run
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python run.py
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

- **Admin Login**: [http://localhost:8000/admin/login](http://localhost:8000/admin/login)
- **Default Credentials**: `admin` / `admin123`

---

## Deployment via SaaS Panel & Coolify

SiteBuilder Express can be provisioned as a dedicated isolated service for any tenant:
- **Build Pack**: Dockerfile
- **Port**: `8000`
- **Environment Variables**:
  - `SECRET_KEY`: Random 64-character string
  - `DATABASE_URL`: `sqlite:///instance/sitebuilder.sqlite` or PostgreSQL connection string
  - `APP_PUBLIC_URL`: Tenant's custom domain (e.g. `https://mysite.com`)
  - `APP_SSO_SECRET`: Shared secret with the SaaS control plane for HMAC one-click admin sign-in
