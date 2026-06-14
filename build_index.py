import json
import io

# Load all data files
lectures = []
for file in ["data_l3.json", "data_l4.json", "data_l5.json", "data_l67.json"]:
    with open(file, 'r', encoding='utf-8') as f:
        lectures.append(json.load(f))

# Serialize to JSON
db_json = json.dumps(lectures, ensure_ascii=False)

# ─────────────────────────────────────────────
#  FULL HTML TEMPLATE  (NO % FORMAT CHARACTERS)
# ─────────────────────────────────────────────
HTML = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CommHub | Communication Skills Study Platform</title>
  <meta name="description" content="Premium bilingual study platform for Communication Skills university course. Features lecture notes, flashcards, quizzes, and exam preparation tools.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

<style>
/* =====================================================
   ROOT VARIABLES – LIGHT & DARK
===================================================== */
:root {
  --blue: #2563eb;
  --blue-dark: #1d4ed8;
  --blue-light: #eff6ff;
  --pink: #db2777;
  --green: #059669;
  --red: #dc2626;
  --yellow: #d97706;

  --bg: #f1f5f9;
  --surface: #ffffff;
  --surface2: #f8fafc;
  --border: #e2e8f0;
  --text: #0f172a;
  --text-muted: #64748b;
  --sidebar-w: 280px;
  --radius: 14px;
  --shadow: 0 1px 3px rgba(0,0,0,.08), 0 4px 16px rgba(0,0,0,.06);
  --shadow-lg: 0 8px 32px rgba(0,0,0,.12);
}
.dark {
  --bg: #0d1117;
  --surface: #161b22;
  --surface2: #21262d;
  --border: #30363d;
  --text: #e6edf3;
  --text-muted: #8b949e;
  --shadow: 0 1px 3px rgba(0,0,0,.4), 0 4px 16px rgba(0,0,0,.3);
  --shadow-lg: 0 8px 32px rgba(0,0,0,.5);
}

/* =====================================================
   RESET & BASE
===================================================== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; }
body {
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--text);
  height: 100vh;
  display: flex;
  overflow: hidden;
  transition: background .3s, color .3s;
  -webkit-font-smoothing: antialiased;
}
[dir="rtl"] body { font-family: 'Cairo', sans-serif; }
a { text-decoration: none; color: inherit; }

/* =====================================================
   SCROLLBAR
===================================================== */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* =====================================================
   SIDEBAR
===================================================== */
#sidebar {
  width: var(--sidebar-w);
  min-width: var(--sidebar-w);
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  transition: transform .3s cubic-bezier(.4,0,.2,1);
  z-index: 100;
  flex-shrink: 0;
}
[dir="rtl"] #sidebar { border-right: none; border-left: 1px solid var(--border); }

.sidebar-logo {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.logo-text {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--blue), var(--pink));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -.5px;
}
.sidebar-nav { flex: 1; overflow-y: auto; padding: 20px 12px; }
.nav-section-label {
  font-size: .7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  padding: 0 10px;
  margin: 20px 0 8px;
}
.nav-section-label:first-child { margin-top: 0; }
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  color: var(--text-muted);
  font-weight: 500;
  font-size: .9rem;
  cursor: pointer;
  transition: background .15s, color .15s;
  margin-bottom: 2px;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
}
[dir="rtl"] .nav-item { text-align: right; }
.nav-item:hover { background: var(--surface2); color: var(--text); }
.nav-item.active { background: var(--blue); color: #fff; }
.nav-item .ni-icon { width: 18px; text-align: center; flex-shrink: 0; }
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border);
  flex-shrink: 0;
}
.user-card { display: flex; align-items: center; gap: 12px; padding: 10px; border-radius: 10px; background: var(--surface2); }
.user-avatar {
  width: 38px; height: 38px; border-radius: 50%;
  background: linear-gradient(135deg, var(--blue), var(--pink));
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-weight: 700; font-size: 1rem; flex-shrink: 0;
}
.user-info p { font-size: .85rem; font-weight: 700; line-height: 1.3; }
.user-info span { font-size: .75rem; color: var(--text-muted); }

/* =====================================================
   MAIN AREA
===================================================== */
#mainArea {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  min-width: 0;
}

/* ─── TOPBAR ─── */
#topbar {
  height: 72px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  flex-shrink: 0;
  gap: 16px;
  position: sticky;
  top: 0;
  z-index: 50;
}
.topbar-left { display: flex; align-items: center; gap: 12px; flex: 1; }
#menuToggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text);
  font-size: 1.25rem;
  padding: 6px;
}
.search-wrap { position: relative; max-width: 340px; width: 100%; }
.search-wrap i { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: .9rem; pointer-events: none; }
[dir="rtl"] .search-wrap i { left: auto; right: 14px; }
#searchInput {
  width: 100%;
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 9px 14px 9px 38px;
  border-radius: 99px;
  font-family: inherit;
  font-size: .9rem;
  outline: none;
  transition: border-color .2s, box-shadow .2s;
}
[dir="rtl"] #searchInput { padding: 9px 38px 9px 14px; }
#searchInput:focus { border-color: var(--blue); box-shadow: 0 0 0 3px rgba(37,99,235,.15); }
.topbar-right { display: flex; align-items: center; gap: 8px; }
.tb-btn {
  width: 38px; height: 38px; border-radius: 50%;
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--text); cursor: pointer; display: flex;
  align-items: center; justify-content: center; font-size: .95rem;
  transition: background .15s, transform .15s;
}
.tb-btn:hover { background: var(--border); transform: translateY(-1px); }
.lang-btn { font-size: .75rem; font-weight: 700; letter-spacing: .5px; }

/* ─── CONTENT SCROLL ─── */
#contentScroll {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

/* =====================================================
   PAGE SECTIONS
===================================================== */
.page { display: none; max-width: 1100px; margin: 0 auto; }
.page.active { display: block; animation: slideUp .4s ease-out; }
@keyframes slideUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ─── HERO BANNER ─── */
.hero {
  border-radius: var(--radius);
  padding: 44px 48px;
  color: #fff;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
}
.hero-blue { background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%); }
.hero-green { background: linear-gradient(135deg, #059669 0%, #0d9488 100%); }
.hero::after {
  content: '';
  position: absolute;
  right: -60px; top: -60px;
  width: 220px; height: 220px;
  background: rgba(255,255,255,.07);
  border-radius: 50%;
}
.hero::before {
  content: '';
  position: absolute;
  right: 80px; bottom: -80px;
  width: 280px; height: 280px;
  background: rgba(255,255,255,.05);
  border-radius: 50%;
}
.hero-badge {
  display: inline-block;
  background: rgba(255,255,255,.2);
  backdrop-filter: blur(8px);
  padding: 4px 14px;
  border-radius: 99px;
  font-size: .8rem;
  font-weight: 600;
  margin-bottom: 16px;
  letter-spacing: .5px;
}
.hero h1 { font-size: 2.25rem; font-weight: 800; margin-bottom: 10px; line-height: 1.2; }
.hero p { font-size: 1.05rem; opacity: .85; max-width: 560px; }
@media (max-width: 600px) {
  .hero { padding: 28px 24px; }
  .hero h1 { font-size: 1.5rem; }
}

/* ─── STATS ROW ─── */
.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 28px; }
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  display: flex; align-items: center; gap: 16px;
  box-shadow: var(--shadow);
}
.stat-icon {
  width: 48px; height: 48px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.3rem; flex-shrink: 0;
}
.si-blue { background: rgba(37,99,235,.1); color: var(--blue); }
.si-green { background: rgba(5,150,105,.1); color: var(--green); }
.si-orange { background: rgba(234,88,12,.1); color: #ea580c; }
.stat-label { font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .8px; color: var(--text-muted); margin-bottom: 4px; }
.stat-value { font-size: 1.6rem; font-weight: 800; line-height: 1; }

/* ─── SECTION TITLE ─── */
.section-title { font-size: 1.25rem; font-weight: 800; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }

/* ─── GRID ─── */
.lec-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }
.lec-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 22px;
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: transform .2s, box-shadow .2s;
  position: relative;
  overflow: hidden;
}
.lec-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); }
.lec-card-id {
  display: inline-block;
  background: var(--blue-light);
  color: var(--blue);
  padding: 3px 10px;
  border-radius: 6px;
  font-size: .78rem;
  font-weight: 700;
  margin-bottom: 12px;
}
.dark .lec-card-id { background: rgba(37,99,235,.15); }
.lec-card h3 { font-size: 1.05rem; font-weight: 700; line-height: 1.4; margin-bottom: 10px; }
.lec-card-meta { font-size: .82rem; color: var(--text-muted); display: flex; align-items: center; gap: 6px; }
.lec-score { margin-left: auto; font-weight: 700; font-size: .82rem; color: var(--green); }
[dir="rtl"] .lec-score { margin-left: 0; margin-right: auto; }

/* =====================================================
   LECTURE PAGE
===================================================== */
.breadcrumb { display: flex; align-items: center; gap: 8px; font-size: .85rem; color: var(--text-muted); margin-bottom: 20px; flex-wrap: wrap; }
.breadcrumb a { color: var(--text-muted); }
.breadcrumb a:hover { color: var(--blue); }
.breadcrumb .sep { font-size: .7rem; }
[dir="rtl"] .breadcrumb .sep { transform: scaleX(-1); display: inline-block; }
.breadcrumb .current { color: var(--blue); font-weight: 600; }

.lec-header { margin-bottom: 28px; }
.lec-header h1 { font-size: 2rem; font-weight: 800; line-height: 1.2; margin-bottom: 8px; }
.lec-header p { color: var(--text-muted); font-size: 1rem; }

/* ─── TABS ─── */
.tabs-bar {
  border-bottom: 1px solid var(--border);
  display: flex;
  gap: 0;
  margin-bottom: 28px;
  overflow-x: auto;
  scrollbar-width: none;
}
.tabs-bar::-webkit-scrollbar { display: none; }
.tab-btn {
  padding: 12px 20px;
  border: none; border-bottom: 3px solid transparent;
  background: none; color: var(--text-muted);
  font-family: inherit; font-size: .9rem; font-weight: 600;
  cursor: pointer; white-space: nowrap;
  display: flex; align-items: center; gap: 8px;
  transition: color .2s, border-color .2s;
  margin-bottom: -1px;
}
.tab-btn:hover { color: var(--text); }
.tab-btn.active { color: var(--blue); border-bottom-color: var(--blue); }

/* ─── TAB CONTENT PANELS ─── */
.tab-panel { display: none; }
.tab-panel.active { display: block; animation: fadeIn .3s ease-out; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* ─── CONTENT BOX ─── */
.content-box {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 32px;
  font-size: 1.05rem;
  line-height: 1.85;
  white-space: pre-wrap;
  word-break: break-word;
  box-shadow: var(--shadow);
}

/* ─── NOTES BOX ─── */
.notes-box {
  background: rgba(37,99,235,.04);
  border: 1px solid rgba(37,99,235,.15);
  border-radius: var(--radius);
  padding: 28px;
  font-size: 1.05rem;
  line-height: 1.85;
  white-space: pre-wrap;
  word-break: break-word;
  margin-bottom: 28px;
}
.dark .notes-box { background: rgba(37,99,235,.07); border-color: rgba(37,99,235,.2); }

/* ─── CONCEPT CARDS ─── */
.concepts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-bottom: 28px; }
.concept-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  border-left: 4px solid var(--blue);
  box-shadow: var(--shadow);
}
[dir="rtl"] .concept-card { border-left: none; border-right: 4px solid var(--blue); }
.concept-term { font-size: 1rem; font-weight: 700; color: var(--blue); margin-bottom: 8px; }
.concept-def { font-size: .92rem; line-height: 1.65; color: var(--text-muted); }

/* ─── EXAM NOTES ─── */
.exam-notes-box {
  background: rgba(220,38,38,.05);
  border: 1px solid rgba(220,38,38,.2);
  border-left: 4px solid var(--red);
  border-radius: 0 var(--radius) var(--radius) 0;
  padding: 20px 24px;
}
[dir="rtl"] .exam-notes-box { border-left: 1px solid rgba(220,38,38,.2); border-right: 4px solid var(--red); border-radius: var(--radius) 0 0 var(--radius); }
.dark .exam-notes-box { background: rgba(220,38,38,.07); }
.exam-notes-box li { font-size: .95rem; font-weight: 600; color: var(--text); line-height: 1.6; margin-bottom: 8px; list-style: disc; margin-left: 16px; }
[dir="rtl"] .exam-notes-box li { margin-left: 0; margin-right: 16px; }

/* ─── FLASHCARDS ─── */
.fc-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }
.fc-card { perspective: 1000px; height: 200px; cursor: pointer; }
.fc-inner {
  position: relative; width: 100%; height: 100%;
  transform-style: preserve-3d;
  transition: transform .55s cubic-bezier(.4,.2,.2,1);
}
.fc-card.flipped .fc-inner { transform: rotateY(180deg); }
.fc-face {
  position: absolute; width: 100%; height: 100%;
  backface-visibility: hidden;
  border-radius: var(--radius);
  display: flex; align-items: center; justify-content: center;
  padding: 20px; text-align: center;
  border: 1px solid var(--border);
}
.fc-front {
  background: var(--surface);
  box-shadow: var(--shadow);
  font-weight: 700; font-size: 1.05rem; color: var(--blue);
}
.fc-back {
  background: linear-gradient(135deg, var(--blue), #4f46e5);
  color: #fff; font-size: .97rem; font-weight: 500;
  transform: rotateY(180deg);
  box-shadow: var(--shadow);
}
.fc-hint {
  text-align: center; color: var(--text-muted); font-size: .85rem;
  margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 6px;
}

/* ─── QUIZ ENGINE ─── */
.quiz-info {
  background: rgba(79,70,229,.07);
  border: 1px solid rgba(79,70,229,.15);
  border-radius: var(--radius);
  padding: 16px 20px;
  display: flex; align-items: flex-start; gap: 12px;
  font-size: .92rem; line-height: 1.6; margin-bottom: 24px;
  color: var(--text);
}
.dark .quiz-info { background: rgba(79,70,229,.1); }
.quiz-info i { color: #6366f1; font-size: 1.1rem; margin-top: 2px; flex-shrink: 0; }

.quiz-section-hdr {
  font-size: 1.05rem; font-weight: 800; color: var(--text);
  padding: 10px 0 10px; margin: 28px 0 14px;
  border-bottom: 2px solid var(--border);
  display: flex; align-items: center; gap: 10px;
}
.quiz-section-hdr:first-child { margin-top: 0; }

.quiz-q {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: var(--shadow);
}
.quiz-q-text { font-size: 1rem; font-weight: 700; line-height: 1.6; margin-bottom: 16px; color: var(--text); }
.quiz-q-num { color: var(--blue); margin-right: 6px; }
[dir="rtl"] .quiz-q-num { margin-right: 0; margin-left: 6px; }

/* Options */
.opts-list { display: flex; flex-direction: column; gap: 10px; }
.opt {
  padding: 12px 16px;
  border: 2px solid var(--border);
  border-radius: 10px;
  cursor: pointer;
  font-size: .95rem;
  font-weight: 500;
  background: var(--surface2);
  color: var(--text);
  transition: border-color .15s, background .15s;
  user-select: none;
}
.opt:hover { border-color: var(--blue); background: var(--blue-light); }
.dark .opt:hover { background: rgba(37,99,235,.12); }
.opt.selected { border-color: var(--blue); background: rgba(37,99,235,.1); color: var(--blue); font-weight: 700; }
.dark .opt.selected { background: rgba(37,99,235,.18); }
.opt.correct { border-color: var(--green); background: rgba(5,150,105,.08); color: var(--green); font-weight: 700; }
.dark .opt.correct { background: rgba(5,150,105,.15); }
.opt.wrong { border-color: var(--red); background: rgba(220,38,38,.08); color: var(--red); font-weight: 700; }
.dark .opt.wrong { background: rgba(220,38,38,.15); }

/* Feedback */
.feedback {
  display: none;
  margin-top: 14px;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: .92rem;
  line-height: 1.6;
  border-left: 4px solid var(--blue);
  background: var(--surface2);
}
[dir="rtl"] .feedback { border-left: none; border-right: 4px solid var(--blue); }
.feedback.correct { border-left-color: var(--green); }
.feedback.wrong   { border-left-color: var(--red); }
[dir="rtl"] .feedback.correct { border-right-color: var(--green); border-left: none; }
[dir="rtl"] .feedback.wrong   { border-right-color: var(--red); border-left: none; }
.feedback .fb-label { font-weight: 700; display: block; margin-bottom: 4px; }
.fb-correct { color: var(--green); }
.fb-wrong   { color: var(--red); }

/* Written Answer */
.written-textarea {
  width: 100%;
  min-height: 130px;
  padding: 14px;
  border: 2px solid var(--border);
  border-radius: 10px;
  font-family: inherit;
  font-size: .97rem;
  line-height: 1.65;
  background: var(--surface2);
  color: var(--text);
  resize: vertical;
  transition: border-color .2s;
  outline: none;
}
.written-textarea:focus { border-color: var(--blue); }
.model-answer {
  display: none;
  margin-top: 14px;
  padding: 14px 18px;
  border-radius: 10px;
  background: rgba(5,150,105,.07);
  border: 1px solid rgba(5,150,105,.2);
}
.dark .model-answer { background: rgba(5,150,105,.1); }
.model-answer-label { font-weight: 700; color: var(--green); margin-bottom: 8px; display: flex; align-items: center; gap: 6px; font-size: .9rem; }
.model-answer-text { font-size: .95rem; line-height: 1.7; color: var(--text); }

/* ─── SUBMIT BAR ─── */
.submit-bar { margin-top: 28px; text-align: center; padding-top: 24px; border-top: 1px solid var(--border); }
.btn-submit {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 14px 36px;
  background: var(--blue); color: #fff;
  border: none; border-radius: 12px;
  font-family: inherit; font-size: 1rem; font-weight: 700;
  cursor: pointer;
  transition: background .2s, transform .2s, box-shadow .2s;
  box-shadow: 0 4px 12px rgba(37,99,235,.3);
}
.btn-submit:hover { background: var(--blue-dark); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(37,99,235,.4); }
.btn-submit-green { background: var(--green); box-shadow: 0 4px 12px rgba(5,150,105,.3); }
.btn-submit-green:hover { background: #047857; box-shadow: 0 8px 20px rgba(5,150,105,.4); }
.quiz-result { margin-top: 20px; font-size: 1.6rem; font-weight: 800; }

/* ─── EXPECTED QUESTIONS ─── */
.eq-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  margin-bottom: 16px;
  box-shadow: var(--shadow);
}
.eq-q {
  padding: 18px 20px;
  font-weight: 700; font-size: 1rem;
  display: flex; align-items: flex-start; gap: 10px;
  border-bottom: 1px solid var(--border);
}
.eq-q i { color: var(--yellow); flex-shrink: 0; margin-top: 3px; }
.eq-a { padding: 16px 20px; background: rgba(5,150,105,.05); }
.dark .eq-a { background: rgba(5,150,105,.08); }
.eq-a-label { font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .8px; color: var(--green); margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
.eq-a-text { font-size: .95rem; line-height: 1.7; }

/* ─── SECTION HEADER (within lecture) ─── */
.lec-section-title { font-size: 1.1rem; font-weight: 800; margin: 28px 0 14px; display: flex; align-items: center; gap: 8px; }
.lec-section-title i { font-size: .95rem; }

/* ─── TIMER MODAL ─── */
#timerModal {
  display: none;
  position: fixed;
  top: 84px; right: 20px;
  width: 260px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-lg);
  z-index: 200;
}
[dir="rtl"] #timerModal { right: auto; left: 20px; }
.timer-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.timer-head h3 { font-weight: 800; font-size: 1rem; }
.timer-close { background: none; border: none; cursor: pointer; color: var(--text-muted); font-size: 1rem; }
#timerDisplay {
  font-size: 3.2rem; font-weight: 800; text-align: center;
  color: var(--blue); margin-bottom: 14px;
  font-variant-numeric: tabular-nums; line-height: 1;
}
.timer-btns { display: flex; gap: 8px; }
.timer-btns button {
  flex: 1; padding: 9px;
  border-radius: 8px;
  border: none; font-family: inherit; font-weight: 700; font-size: .9rem; cursor: pointer;
  transition: background .2s;
}
#btnTimerStartStop { background: var(--blue); color: #fff; }
#btnTimerStartStop:hover { background: var(--blue-dark); }
#btnTimerReset { background: var(--surface2); color: var(--text); border: 1px solid var(--border); }
#btnTimerReset:hover { background: var(--border); }

/* ─── SIDEBAR OVERLAY (mobile) ─── */
#sidebarOverlay {
  display: none;
  position: fixed; inset: 0;
  background: rgba(0,0,0,.45);
  z-index: 90;
}

/* ─── DEVICE‑SPECIFIC STYLING ─── */
/* iPhone – glass‑morphism (Safari supports -webkit-backdrop-filter) */
@media screen and (max-width: 600px) and (hover: none) and (pointer: coarse) {
  /* Dark Theme Glass */
  [data-theme="dark"] body.ios-glass .sidebar, 
  [data-theme="dark"] body.ios-glass .card {
    background: rgba(255,255,255,.05) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255,255,255,.1) !important;
  }
  /* Light Theme Glass */
  [data-theme="light"] body.ios-glass .sidebar, 
  [data-theme="light"] body.ios-glass .card,
  body.ios-glass .sidebar, 
  body.ios-glass .card {
    background: rgba(255,255,255,.7) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(0,0,0,.05) !important;
  }
  
  body.ios-glass .sidebar {
    box-shadow: 0 8px 32px rgba(0,0,0,.15) !important;
  }
}

/* Android – keep current solid look but add subtle elevation */
body.android .sidebar {
  box-shadow: 0 4px 12px rgba(0,0,0,.25);
}

/* Desktop – richer gradients & neumorphic accents */
@media screen and (min-width: 901px) {
  .hero {
    background: linear-gradient(135deg, #1e3a8a 0%, #7e22ce 100%);
    border-radius: 16px;
    box-shadow: 0 12px 36px rgba(0,0,0,.35);
  }
  .card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.1);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 8px 24px rgba(0,0,0,.25);
    border-radius: 20px;
  }
}

/* =====================================================
   WELCOME SCREEN
===================================================== */
#welcomeScreen {
  position: fixed;
  inset: 0;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}
#welcomeCard {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.12);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-radius: 24px;
  padding: 48px 40px;
  width: 100%;
  max-width: 440px;
  text-align: center;
  box-shadow: 0 24px 64px rgba(0,0,0,.5);
  animation: wcSlideIn .6s cubic-bezier(.4,0,.2,1);
}
@keyframes wcSlideIn {
  from { opacity:0; transform:translateY(32px) scale(.96); }
  to   { opacity:1; transform:translateY(0) scale(1); }
}
#wc-logo {
  width: 72px; height: 72px;
  background: linear-gradient(135deg, #2563eb, #db2777);
  border-radius: 20px;
  display: flex; align-items: center; justify-content: center;
  font-size: 2rem; color: #fff;
  margin: 0 auto 20px;
  box-shadow: 0 8px 24px rgba(37,99,235,.4);
}
#wc-title {
  font-size: 2.2rem; font-weight: 800;
  background: linear-gradient(135deg, #60a5fa, #f472b6);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 6px;
}
#wc-sub {
  font-size: .9rem; color: rgba(255,255,255,.5);
  margin-bottom: 32px; letter-spacing: .3px;
}
#wc-prompt {
  font-size: 1rem; font-weight: 600; color: rgba(255,255,255,.85);
  margin-bottom: 14px; font-family: 'Cairo', sans-serif;
}
#wc-input-wrap {
  position: relative; margin-bottom: 18px;
}
#wc-input-wrap i {
  position: absolute; left: 16px; top: 50%; transform: translateY(-50%);
  color: rgba(255,255,255,.4); font-size: 1rem;
}
#studentNameInput {
  width: 100%;
  padding: 14px 18px 14px 44px;
  background: rgba(255,255,255,.08);
  border: 1.5px solid rgba(255,255,255,.15);
  border-radius: 12px;
  color: #fff;
  font-family: 'Cairo', 'Inter', sans-serif;
  font-size: 1.05rem;
  outline: none;
  transition: border-color .2s, background .2s;
  text-align: right;
  direction: rtl;
}
#studentNameInput::placeholder { color: rgba(255,255,255,.3); }
#studentNameInput:focus {
  border-color: #3b82f6;
  background: rgba(255,255,255,.12);
}
#wc-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #2563eb, #4f46e5);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-family: 'Cairo', 'Inter', sans-serif;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 10px;
  transition: transform .2s, box-shadow .2s;
  box-shadow: 0 6px 20px rgba(37,99,235,.45);
  margin-bottom: 24px;
  direction: rtl;
}
#wc-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(37,99,235,.55); }
#wc-btn:active { transform: translateY(0); }
#wc-error {
  color: #f87171;
  font-size: .88rem;
  margin-top: -12px;
  margin-bottom: 14px;
  display: none;
  font-family: 'Cairo', sans-serif;
}
#wc-footer {
  font-size: .8rem; color: rgba(255,255,255,.35);
  margin-top: 0;
}
#wc-footer a { color: #f472b6; text-decoration: none; }
#wc-footer a:hover { text-decoration: underline; }

#appWrapper { display: none; width: 100%; height: 100%; overflow: hidden; }

/* =====================================================
   RESPONSIVE
===================================================== */
@media (max-width: 900px) {
  #sidebar {
    position: fixed;
    top: 0; left: 0; bottom: 0;
    transform: translateX(-100%);
  }
  [dir="rtl"] #sidebar { left: auto; right: 0; transform: translateX(100%); }
  #sidebar.open { transform: translateX(0); }
  #menuToggle { display: flex; }
  #contentScroll { padding: 20px; }
}
@media (max-width: 560px) {
  .hero { padding: 24px 20px; }
  .hero h1 { font-size: 1.4rem; }
  #contentScroll { padding: 16px; }
  .content-box { padding: 20px; }
  .quiz-q { padding: 16px; }
  .tabs-bar { gap: 0; }
  .tab-btn { padding: 10px 14px; font-size: .83rem; }
  .btn-submit { padding: 12px 24px; font-size: .92rem; }
}
</style>
</head>
<body>

<!-- ── WELCOME SCREEN ── -->
<div id="welcomeScreen">
  <div id="welcomeCard">
    <div id="wc-logo">
      <i class="fa-solid fa-graduation-cap"></i>
    </div>
    <h1 id="wc-title">CommHub</h1>
    <p id="wc-sub">Communication Skills &bull; COMM 101</p>
    <p id="wc-prompt">&#x0623;&#x062f;&#x062e;&#x0644; &#x0627;&#x0633;&#x0645;&#x0643; &#x0644;&#x0644;&#x0628;&#x062f;&#x0621;</p>
    <div id="wc-input-wrap">
      <i class="fa-solid fa-user"></i>
      <input type="text" id="studentNameInput" maxlength="50" placeholder="&#x0645;&#x062b;&#x0627;&#x0644;: &#x0645;&#x062d;&#x0645;&#x062f; &#x0639;&#x0644;&#x064a;">
    </div>
    <button id="wc-btn" onclick="enterPlatform()">
      <span>&#x0627;&#x062f;&#x062e;&#x0644; &#x0627;&#x0644;&#x0645;&#x0646;&#x0635;&#x0629;</span>
      <i class="fa-solid fa-arrow-right"></i>
    </button>
    <p id="wc-footer">&#x0645;&#x0639;&#x0632; &nbsp;<i class="fa-brands fa-instagram" style="color:#e1306c"></i>&nbsp;<a href="https://instagram.com/mvii3.a" target="_blank" style="color:#e1306c">mvii3.a</a></p>
  </div>
</div>

<!-- ── APP WRAPPER (hidden until login) ── -->
<div id="appWrapper">

<!-- ── SIDEBAR OVERLAY ── -->
<div id="sidebarOverlay" onclick="closeSidebar()"></div>

<!-- ── SIDEBAR ── -->
<aside id="sidebar">
  <div class="sidebar-logo">
    <span class="logo-text">CommHub</span>
    <button class="tb-btn" onclick="closeSidebar()" id="closeSidebarBtn" title="Close menu" style="display:none">
      <i class="fa-solid fa-xmark"></i>
    </button>
  </div>

  <nav class="sidebar-nav">
    <div class="nav-section-label" data-i18n="nav_section_main">Main</div>

    <button class="nav-item active" id="nav-dashboard" onclick="showPage('dashboard',this)">
      <i class="fa-solid fa-chart-pie ni-icon"></i>
      <span data-i18n="nav_dashboard">Dashboard</span>
    </button>

    <div class="nav-section-label" data-i18n="nav_section_modules">Modules</div>
    <div id="navModules"></div>

    <div class="nav-section-label" data-i18n="nav_section_exams">Exams</div>
    <button class="nav-item" id="nav-final" onclick="showPage('final_exam',this); buildFinalExam();">
      <i class="fa-solid fa-trophy ni-icon" style="color:#d97706"></i>
      <span data-i18n="nav_final">Final Exam</span>
    </button>
    <button class="nav-item" id="nav-expected-exam" onclick="showPage('expected_exam',this); buildExpectedExam();">
      <i class="fa-solid fa-star ni-icon" style="color:var(--pink)"></i>
      <span data-i18n="nav_expected_exam">Expected Qs Exam</span>
    </button>
  </nav>

  <div class="sidebar-footer">
    <div class="user-card" style="margin-bottom:12px;">
      <div class="user-avatar" id="sidebarAvatar">S</div>
      <div class="user-info">
        <p id="sidebarStudentName" data-i18n="user_name">University Student</p>
        <span data-i18n="user_course">Communication Skills</span>
      </div>
    </div>
    <div style="display:flex; align-items:center; justify-content:space-between; padding-top:10px; border-top:1px solid var(--border);">
      <div style="display:flex; align-items:center; gap:6px;">
        <span style="font-weight:700; color:var(--text); font-size:0.85rem;">معز</span>
        <a href="https://instagram.com/mvii3.a" target="_blank" style="color:var(--pink); font-size:1rem; display:flex; align-items:center; gap:4px; font-weight:600; text-decoration:none;" title="Instagram @mvii3.a">
          <i class="fa-brands fa-instagram"></i>
          <span style="font-size:0.75rem;">mvii3.a</span>
        </a>
      </div>
      <button onclick="changeStudentName()" title="تغيير الاسم" style="background:none; border:1px solid var(--border); border-radius:8px; padding:4px 8px; color:var(--text-muted); cursor:pointer; font-size:0.75rem; transition:all .2s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text-muted)'">
        <i class="fa-solid fa-pen"></i>
      </button>
    </div>
  </div>
</aside>

<!-- ── MAIN AREA ── -->
<div id="mainArea">

  <!-- TOPBAR -->
  <header id="topbar">
    <div class="topbar-left">
      <button id="menuToggle" onclick="openSidebar()" title="Menu">
        <i class="fa-solid fa-bars"></i>
      </button>
      <div class="search-wrap">
        <i class="fa-solid fa-magnifying-glass"></i>
        <input type="search" id="searchInput" data-i18n-placeholder="search_ph" placeholder="Search course content...">
      </div>
    </div>
    <div class="topbar-right">
      <button class="tb-btn" onclick="toggleTimer()" title="Pomodoro Timer">
        <i class="fa-regular fa-clock"></i>
      </button>
      <button class="tb-btn lang-btn" onclick="toggleLang()" title="Switch Language">
        EN/ع
      </button>
      <button class="tb-btn" onclick="toggleTheme()" id="themeBtn" title="Toggle Theme">
        <i class="fa-solid fa-moon" id="themeIcon"></i>
      </button>
    </div>
  </header>

  <!-- PAGE CONTENT -->
  <div id="contentScroll">

    <!-- ══════════════ DASHBOARD ══════════════ -->
    <div id="page-dashboard" class="page active">

      <div class="hero hero-blue">
        <span class="hero-badge" data-i18n="course_code">COMM 101</span>
        <h1 data-i18n="dash_h1">Master Communication Skills</h1>
        <p data-i18n="dash_sub">A premium bilingual study platform — covering Lectures 3, 4, 5, and 6-7 with interactive quizzes, flashcards, and exam prep tools.</p>
      </div>

      <!-- EXAM COUNTDOWN BANNER -->
      <div id="examCountdownBanner" style="background:linear-gradient(135deg, #10b981 0%, #059669 100%); color:white; border-radius:16px; padding:20px; margin-bottom:24px; text-align:center; box-shadow:0 8px 24px rgba(16, 185, 129, 0.3);">
        <h2 style="font-size:1.4rem; font-weight:800; margin-bottom:12px;"><i class="fa-solid fa-stopwatch" style="margin-inline-end:8px;"></i><span data-i18n="countdown_title">Final Exam Countdown</span></h2>
        <div id="examCountdown" style="display:flex; justify-content:center; gap:16px; font-family:'Inter', sans-serif;">
          <div style="background:rgba(255,255,255,0.2); padding:10px 16px; border-radius:12px; min-width:70px;">
            <div id="cd-hours" style="font-size:2rem; font-weight:800; line-height:1;">00</div>
            <div data-i18n="cd_hours" style="font-size:0.8rem; opacity:0.9; margin-top:4px;">Hours</div>
          </div>
          <div style="background:rgba(255,255,255,0.2); padding:10px 16px; border-radius:12px; min-width:70px;">
            <div id="cd-minutes" style="font-size:2rem; font-weight:800; line-height:1;">00</div>
            <div data-i18n="cd_minutes" style="font-size:0.8rem; opacity:0.9; margin-top:4px;">Mins</div>
          </div>
          <div style="background:rgba(255,255,255,0.2); padding:10px 16px; border-radius:12px; min-width:70px;">
            <div id="cd-seconds" style="font-size:2rem; font-weight:800; line-height:1;">00</div>
            <div data-i18n="cd_seconds" style="font-size:0.8rem; opacity:0.9; margin-top:4px;">Secs</div>
          </div>
        </div>
      </div>

      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-icon si-blue"><i class="fa-solid fa-book-open"></i></div>
          <div>
            <div class="stat-label" data-i18n="stat_lec">Lectures</div>
            <div class="stat-value" id="statLec">4</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon si-green"><i class="fa-solid fa-bullseye"></i></div>
          <div>
            <div class="stat-label" data-i18n="stat_score">Avg. Score</div>
            <div class="stat-value" id="statScore">—</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon si-orange"><i class="fa-solid fa-fire"></i></div>
          <div>
            <div class="stat-label" data-i18n="stat_streak">Streak</div>
            <div class="stat-value" id="statStreak">Day 1</div>
          </div>
        </div>
      </div>

      <div class="section-title">
        <i class="fa-solid fa-graduation-cap" style="color:var(--blue)"></i>
        <span data-i18n="dash_choose">Choose a Module</span>
      </div>
      <div class="lec-grid" id="dashGrid"></div>
    </div>

    <!-- ══════════════ LECTURE ══════════════ -->
    <div id="page-lecture" class="page">

      <div class="breadcrumb">
        <a href="#" onclick="showPage('dashboard', document.getElementById('nav-dashboard'))">
          <i class="fa-solid fa-house"></i>
        </a>
        <i class="fa-solid fa-chevron-right sep"></i>
        <span data-i18n="nav_section_modules">Modules</span>
        <i class="fa-solid fa-chevron-right sep"></i>
        <span class="current" id="lecBreadcrumb"></span>
      </div>

      <div class="lec-header">
        <h1 id="lecTitle"></h1>
        <p data-i18n="lec_sub">Use the tabs below to explore content, notes, flashcards, quiz, and expected questions.</p>
      </div>

      <div class="tabs-bar" id="lecTabsBar">
        <button class="tab-btn active" data-tab="content">
          <i class="fa-solid fa-book-open"></i>
          <span data-i18n="tab_content">Content</span>
        </button>
        <button class="tab-btn" data-tab="notes">
          <i class="fa-solid fa-file-lines"></i>
          <span data-i18n="tab_notes">Notes</span>
        </button>
        <button class="tab-btn" data-tab="flashcards">
          <i class="fa-solid fa-layer-group"></i>
          <span data-i18n="tab_fc">Flashcards</span>
        </button>
        <button class="tab-btn" data-tab="quiz">
          <i class="fa-solid fa-clipboard-check"></i>
          <span data-i18n="tab_quiz">Quiz</span>
        </button>
        <button class="tab-btn" data-tab="expected">
          <i class="fa-solid fa-star" style="color:var(--yellow)"></i>
          <span data-i18n="tab_expected">Expected</span>
        </button>
      </div>

      <!-- Content Panel -->
      <div class="tab-panel active" id="panel-content">
        <div class="content-box" id="lecContent"></div>
      </div>

      <!-- Notes Panel -->
      <div class="tab-panel" id="panel-notes">
        <div class="notes-box" id="lecNotes"></div>

        <div class="lec-section-title">
          <i class="fa-solid fa-lightbulb" style="color:var(--yellow)"></i>
          <span data-i18n="sec_concepts">Key Concepts</span>
        </div>
        <div class="concepts-grid" id="lecConcepts"></div>

        <div class="lec-section-title">
          <i class="fa-solid fa-triangle-exclamation" style="color:var(--red)"></i>
          <span data-i18n="sec_exam_notes">Important Exam Notes</span>
        </div>
        <div class="exam-notes-box">
          <ul id="lecExamNotes"></ul>
        </div>
      </div>

      <!-- Flashcards Panel -->
      <div class="tab-panel" id="panel-flashcards">
        <p class="fc-hint">
          <i class="fa-regular fa-hand-pointer"></i>
          <span data-i18n="fc_hint">Click a card to flip it</span>
        </p>
        <div class="fc-grid" id="lecFlashcards"></div>
      </div>

      <!-- Quiz Panel -->
      <div class="tab-panel" id="panel-quiz">
        <div class="quiz-info">
          <i class="fa-solid fa-circle-info"></i>
          <span data-i18n="quiz_info">This quiz contains Multiple Choice, True/False, and Written questions. For written questions, type your answer and compare with the model answer shown after submitting.</span>
        </div>
        <div id="lecQuizBox"></div>
        <div class="submit-bar">
          <button class="btn-submit" id="btnSubmitLecQuiz">
            <i class="fa-solid fa-check-double"></i>
            <span data-i18n="btn_grade">Submit & Grade</span>
          </button>
          <div class="quiz-result" id="lecQuizResult" style="color:var(--blue)"></div>
        </div>
      </div>

      <!-- Expected Panel -->
      <div class="tab-panel" id="panel-expected">
        <div style="background:rgba(217,119,6,.07); border:1px solid rgba(217,119,6,.2); border-radius:var(--radius); padding:14px 18px; margin-bottom:20px; font-size:.92rem; line-height:1.6;">
          <i class="fa-solid fa-star" style="color:var(--yellow);margin-right:6px"></i>
          <span data-i18n="eq_info">These questions are based on the professor's focus areas and are highly likely to appear on the actual exam.</span>
        </div>
        <div id="lecExpected"></div>
      </div>
    </div>

    <!-- ══════════════ EXPECTED EXAM ══════════════ -->
    <div id="page-expected_exam" class="page">
      <div class="hero" style="background: linear-gradient(135deg, #db2777 0%, #9d174d 100%); margin-bottom:28px; text-align:center;">
        <i class="fa-solid fa-star" style="font-size:2.5rem; opacity:.8; margin-bottom:12px; display:block;"></i>
        <h1 data-i18n="expected_exam_h1">Expected Questions Exam</h1>
        <p data-i18n="expected_exam_sub">This exam contains ONLY the questions highly expected by the professor. Focus on these!</p>
      </div>
      <div id="expectedExamBox"></div>
      <div class="submit-bar">
        <button class="btn-submit" style="background:var(--pink); box-shadow: 0 4px 12px rgba(219,39,119,.3);" id="btnSubmitExpectedExam">
          <i class="fa-solid fa-flag-checkered"></i>
          <span data-i18n="btn_finish">Finish & Submit Exam</span>
        </button>
        <div class="quiz-result" id="expectedExamResult" style="color:var(--pink)"></div>
      </div>
    </div>

    <!-- ══════════════ FINAL EXAM ══════════════ -->
    <div id="page-final_exam" class="page">
      <div class="hero hero-green" style="margin-bottom:28px; text-align:center;">
        <i class="fa-solid fa-graduation-cap" style="font-size:2.5rem; opacity:.8; margin-bottom:12px; display:block;"></i>
        <h1 data-i18n="final_h1">Comprehensive Final Exam</h1>
        <p data-i18n="final_sub">Questions are pulled from all modules. This simulates the real university exam environment.</p>
      </div>
      <div id="finalQuizBox"></div>
      <div class="submit-bar">
        <button class="btn-submit btn-submit-green" id="btnSubmitFinal">
          <i class="fa-solid fa-flag-checkered"></i>
          <span data-i18n="btn_finish">Finish & Submit Exam</span>
        </button>
        <div class="quiz-result" id="finalResult" style="color:var(--green)"></div>
      </div>
    </div>

  </div><!-- /contentScroll -->
</div><!-- /mainArea -->

</div><!-- /appWrapper -->

<!-- POMODORO TIMER -->
<div id="timerModal">
  <div class="timer-head">
    <h3><i class="fa-solid fa-stopwatch" style="color:var(--blue);margin-right:8px"></i>Pomodoro</h3>
    <button class="timer-close" onclick="toggleTimer()"><i class="fa-solid fa-xmark"></i></button>
  </div>
  <div id="timerDisplay">25:00</div>
  <div class="timer-btns">
    <button id="btnTimerStartStop">Start</button>
    <button id="btnTimerReset">Reset</button>
  </div>
</div>

<!-- ══════════════ JAVASCRIPT ══════════════ -->
<script>
// ─────────────────────────────────────────
//  DATABASE
// ─────────────────────────────────────────
const DB = DATABASE_PLACEHOLDER;

// ─────────────────────────────────────────
//  STATE
// ─────────────────────────────────────────
let lang    = localStorage.getItem('ch-lang')  || 'en';
let theme   = localStorage.getItem('ch-theme') || 'light';
let curLec  = null;
let timerInterval = null;
let timerSecs = 1500; // 25 min
let timerRunning = false;

// ─────────────────────────────────────────
//  TRANSLATIONS
// ─────────────────────────────────────────
const T = {
  en: {
    nav_section_main: 'Main', nav_section_modules: 'Modules', nav_section_exams: 'Exams',
    nav_dashboard: 'Dashboard', nav_final: 'Final Exam', nav_expected_exam: 'Expected Qs Exam',
    dev_credit: 'Moaz', expected_exam_h1: 'Expected Questions Exam', expected_exam_sub: 'This exam contains ONLY the questions highly expected by the professor. Focus on these!',
    user_name: 'University Student', user_course: 'Communication Skills',
    course_code: 'COMM 101',
    countdown_title: 'Final Exam Countdown', cd_hours: 'Hours', cd_minutes: 'Mins', cd_seconds: 'Secs',
    dash_h1: 'Master Communication Skills',
    dash_sub: 'A premium bilingual study platform — covering Lectures 3, 4, 5, and 6-7 with interactive quizzes, flashcards, and exam prep tools.',
    stat_lec: 'Lectures', stat_score: 'Avg. Score', stat_streak: 'Streak',
    dash_choose: 'Choose a Module',
    lec_sub: 'Use the tabs below to explore content, notes, flashcards, quiz, and expected questions.',
    tab_content: 'Content', tab_notes: 'Notes', tab_fc: 'Flashcards', tab_quiz: 'Quiz', tab_expected: 'Expected',
    sec_concepts: 'Key Concepts', sec_exam_notes: 'Important Exam Notes',
    fc_hint: 'Click a card to flip it',
    quiz_info: 'This quiz contains Multiple Choice, True/False, and Written questions. For written questions, type your answer and compare with the model answer shown after submitting.',
    btn_grade: 'Submit & Grade', btn_finish: 'Finish & Submit Exam',
    eq_info: "These questions are based on the professor's focus areas and are highly likely to appear on the actual exam.",
    final_h1: 'Comprehensive Final Exam',
    final_sub: 'Questions are pulled from all modules. This simulates the real university exam environment.',
    model_answer: 'Model Answer',
    not_answered: 'Not answered.',
    search_ph: 'Search course content...',
    score_msg: 'Score: ',
    true_btn: 'True', false_btn: 'False',
    sec_mcq: 'Multiple Choice Questions', sec_tf: 'True or False', sec_written: 'Written Questions (Definitions & Short Answer)',
    q_qs: 'Practice Questions',
  },
  ar: {
    nav_section_main: 'الرئيسية', nav_section_modules: 'الوحدات', nav_section_exams: 'الامتحانات',
    nav_dashboard: 'لوحة القيادة', nav_final: 'الامتحان النهائي', nav_expected_exam: 'امتحان المتوقعة',
    dev_credit: 'معز', expected_exam_h1: 'امتحان الأسئلة المتوقعة الشامل', expected_exam_sub: 'هذا الامتحان يحتوي فقط على الأسئلة التي ركزت عليها الدكتورة والمتوقعة بنسبة كبيرة في الامتحان.',
    user_name: 'طالب جامعي', user_course: 'مهارات التواصل',
    course_code: 'COMM 101',
    countdown_title: 'متبقي على الامتحان النهائي', cd_hours: 'ساعات', cd_minutes: 'دقائق', cd_seconds: 'ثواني',
    dash_h1: 'أتقن مهارات التواصل',
    dash_sub: 'منصة دراسية ثنائية اللغة - تغطي المحاضرات 3 و4 و5 و6-7 مع اختبارات تفاعلية وبطاقات دراسية وأدوات الاستعداد للامتحان.',
    stat_lec: 'المحاضرات', stat_score: 'متوسط الدرجات', stat_streak: 'أيام متتالية',
    dash_choose: 'اختر وحدة دراسية',
    lec_sub: 'استخدم التبويبات أدناه لاستعراض المحتوى والملاحظات والبطاقات التعليمية والاختبار والأسئلة المتوقعة.',
    tab_content: 'المحتوى', tab_notes: 'الملاحظات', tab_fc: 'البطاقات', tab_quiz: 'الاختبار', tab_expected: 'المتوقع',
    sec_concepts: 'المفاهيم الأساسية', sec_exam_notes: 'ملاحظات هامة للامتحان',
    fc_hint: 'انقر على البطاقة لقلبها',
    quiz_info: 'يحتوي هذا الاختبار على أسئلة اختيارية وصح/خطأ وأسئلة كتابية. في الأسئلة الكتابية، اكتب إجابتك وقارنها مع الإجابة النموذجية بعد التسليم.',
    btn_grade: 'إرسال وتصحيح', btn_finish: 'إنهاء وتسليم الامتحان',
    eq_info: 'هذه الأسئلة مبنية على تركيز الدكتور وأسئلة متوقعة في الامتحان الفعلي.',
    final_h1: 'الامتحان النهائي الشامل',
    final_sub: 'تُسحب الأسئلة من جميع الوحدات. هذا يحاكي بيئة الامتحان الجامعي الحقيقي.',
    model_answer: 'الإجابة النموذجية',
    not_answered: 'لم تتم الإجابة.',
    search_ph: 'ابحث في محتوى المادة...',
    score_msg: 'الدرجة: ',
    true_btn: 'صح', false_btn: 'خطأ',
    sec_mcq: 'أسئلة الاختيار من متعدد', sec_tf: 'الصح والخطأ', sec_written: 'الأسئلة الكتابية (التعريفات والمقالي)',
    q_qs: 'أسئلة تدريبية',
  }
};

// ─────────────────────────────────────────
//  HELPERS
// ─────────────────────────────────────────
const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

function t(key) { return T[lang][key] || key; }

function applyI18n() {
  document.documentElement.lang = lang;
  document.documentElement.dir  = lang === 'ar' ? 'rtl' : 'ltr';
  $$('[data-i18n]').forEach(el => {
    const k = el.getAttribute('data-i18n');
    if (T[lang][k] !== undefined) el.textContent = T[lang][k];
  });
  $$('[data-i18n-placeholder]').forEach(el => {
    const k = el.getAttribute('data-i18n-placeholder');
    if (T[lang][k] !== undefined) el.placeholder = T[lang][k];
  });
}

function applyTheme() {
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
    $('#themeIcon').className = 'fa-solid fa-sun';
  } else {
    document.documentElement.classList.remove('dark');
    $('#themeIcon').className = 'fa-solid fa-moon';
  }
}

// ─────────────────────────────────────────
//  INIT
// ─────────────────────────────────────────
function init() {
  applyTheme();
  applyI18n();
  buildSidebar();
  buildDashboard();
  hookTabs();
  initTimer();
}

// ─────────────────────────────────────────
//  SIDEBAR
// ─────────────────────────────────────────
function buildSidebar() {
  const navModules = $('#navModules');
  DB.forEach((lec, i) => {
    const title = lec['title_' + lang];
    const btn = document.createElement('button');
    btn.className = 'nav-item';
    btn.id = 'nav-lec-' + i;
    btn.innerHTML = `<i class="fa-regular fa-file-lines ni-icon" style="color:var(--blue)"></i><span>${title}</span>`;
    btn.onclick = () => { showPage('lecture', btn); loadLecture(i); };
    navModules.appendChild(btn);
  });
}

function openSidebar() {
  $('#sidebar').classList.add('open');
  $('#sidebarOverlay').style.display = 'block';
  $('#closeSidebarBtn').style.display = 'flex';
}
function closeSidebar() {
  $('#sidebar').classList.remove('open');
  $('#sidebarOverlay').style.display = 'none';
  $('#closeSidebarBtn').style.display = 'none';
}

// ─────────────────────────────────────────
//  PAGE ROUTING
// ─────────────────────────────────────────
function showPage(pageId, navBtn) {
  $$('.page').forEach(p => p.classList.remove('active'));
  $$('.nav-item').forEach(n => n.classList.remove('active'));
  const page = $('#page-' + pageId);
  if (page) page.classList.add('active');
  if (navBtn) navBtn.classList.add('active');
  $('#contentScroll').scrollTop = 0;
  closeSidebar();
}

// ─────────────────────────────────────────
//  DASHBOARD
// ─────────────────────────────────────────
function buildDashboard() {
  const grid = $('#dashGrid');
  grid.innerHTML = '';
  let totalPct = 0, scored = 0;
  DB.forEach((lec, i) => {
    const title = lec['title_' + lang];
    const saved = localStorage.getItem('quiz-score-' + i);
    if (saved !== null) { totalPct += parseInt(saved); scored++; }
    const card = document.createElement('div');
    card.className = 'lec-card';
    card.innerHTML = `
      <div class="lec-card-id">${lec.id}</div>
      <h3>${title}</h3>
      <div class="lec-card-meta">
        <i class="fa-solid fa-circle-question" style="color:var(--blue)"></i>
        <span>${(lec.quizzes.mcq || []).length + (lec.quizzes.tf || []).length} ${t('q_qs')}</span>
        ${saved !== null ? `<span class="lec-score"><i class="fa-solid fa-check"></i> ${saved}%</span>` : ''}
      </div>`;
    card.onclick = () => {
      showPage('lecture', $('#nav-lec-' + i));
      loadLecture(i);
    };
    grid.appendChild(card);
  });
  if (scored > 0) {
    $('#statScore').textContent = Math.round(totalPct / scored) + '%';
  }
}

// ─────────────────────────────────────────
//  LECTURE LOADER
// ─────────────────────────────────────────
function loadLecture(idx) {
  curLec = { data: DB[idx], idx };
  const lec = DB[idx];
  const title = lec['title_' + lang];

  $('#lecTitle').textContent = title;
  $('#lecBreadcrumb').textContent = title;

  // ── Content ──
  $('#lecContent').textContent = lec['content_' + lang];

  // ── Notes ──
  $('#lecNotes').textContent = lec['simplified_notes_' + lang];

  // ── Concepts ──
  const conceptsEl = $('#lecConcepts');
  conceptsEl.innerHTML = '';
  lec.key_concepts.forEach(c => {
    const d = document.createElement('div');
    d.className = 'concept-card';
    d.innerHTML = `<div class="concept-term">${c['term_' + lang]}</div><div class="concept-def">${c['def_' + lang]}</div>`;
    conceptsEl.appendChild(d);
  });

  // ── Exam Notes ──
  const enEl = $('#lecExamNotes');
  enEl.innerHTML = '';
  lec['exam_notes_' + lang].forEach(n => {
    const li = document.createElement('li');
    li.textContent = n;
    enEl.appendChild(li);
  });

  // ── Flashcards ──
  const fcEl = $('#lecFlashcards');
  fcEl.innerHTML = '';
  lec.flashcards.forEach(fc => {
    const card = document.createElement('div');
    card.className = 'fc-card';
    card.innerHTML = `
      <div class="fc-inner">
        <div class="fc-face fc-front">${fc['q_' + lang]}</div>
        <div class="fc-face fc-back">${fc['a_' + lang]}</div>
      </div>`;
    card.onclick = () => card.classList.toggle('flipped');
    fcEl.appendChild(card);
  });

  // ── Expected ──
  const eqEl = $('#lecExpected');
  eqEl.innerHTML = '';
  lec.expected_questions.forEach(eq => {
    const d = document.createElement('div');
    d.className = 'eq-card';
    d.innerHTML = `
      <div class="eq-q"><i class="fa-solid fa-circle-question"></i><span>${eq['q_' + lang]}</span></div>
      <div class="eq-a">
        <div class="eq-a-label"><i class="fa-solid fa-check-double"></i>${t('model_answer')}</div>
        <div class="eq-a-text">${eq['a_' + lang]}</div>
      </div>`;
    eqEl.appendChild(d);
  });

  // ── Quiz ──
  buildQuiz(lec.quizzes, '#lecQuizBox');
  $('#lecQuizResult').textContent = '';
  $('#btnSubmitLecQuiz').onclick = () => {
    const score = gradeQuiz('#lecQuizBox');
    if (score !== null) {
      const pct = score.pct;
      $('#lecQuizResult').textContent = t('score_msg') + pct + '%';
      localStorage.setItem('quiz-score-' + idx, pct);
      buildDashboard(); // refresh stats
    }
  };

  // Reset to first tab
  activateTab('content');
}

// ─────────────────────────────────────────
//  TAB SYSTEM
// ─────────────────────────────────────────
function hookTabs() {
  $$('.tab-btn', $('#lecTabsBar')).forEach(btn => {
    btn.onclick = () => activateTab(btn.getAttribute('data-tab'));
  });
}

function activateTab(tabId) {
  $$('.tab-btn', $('#lecTabsBar')).forEach(b => b.classList.remove('active'));
  $$('.tab-panel').forEach(p => p.classList.remove('active'));
  const btn = $(`[data-tab="${tabId}"]`, $('#lecTabsBar'));
  if (btn) btn.classList.add('active');
  const panel = $('#panel-' + tabId);
  if (panel) panel.classList.add('active');
}

// ─────────────────────────────────────────
//  QUIZ BUILDER
// ─────────────────────────────────────────
function buildQuiz(quizzes, containerSel) {
  const container = $(containerSel);
  container.innerHTML = '';

  let allQ = [];
  if (quizzes.mcq)        quizzes.mcq.forEach(q => allQ.push({ type: 'mcq',     ...q }));
  if (quizzes.tf)         quizzes.tf.forEach(q => allQ.push({ type: 'tf',      ...q }));
  if (quizzes.definitions)  quizzes.definitions.forEach(q => allQ.push({ type: 'written', ...q }));
  if (quizzes.short_answer) quizzes.short_answer.forEach(q => allQ.push({ type: 'written', ...q }));

  // Store question data on element
  container.dataset.questions = JSON.stringify(allQ);

  let mcqHTML = '', tfHTML = '', wHTML = '', mcqCount = 1, tfCount = 1, wCount = 1;

  allQ.forEach((q, i) => {
    const qText = q['q_' + lang];
    let inner = `<div class="quiz-q" data-qi="${i}">
      <div class="quiz-q-text"><span class="quiz-q-num">${i + 1}.</span>${qText}</div>
      <div class="opts-list">`;

    if (q.type === 'mcq') {
      const opts = q['options_' + lang];
      opts.forEach((opt, oi) => {
        inner += `<div class="opt" data-oi="${oi}" onclick="selectOpt(this)">${opt}</div>`;
      });
      inner += `</div><div class="feedback"></div></div>`;
      mcqHTML += inner;

    } else if (q.type === 'tf') {
      inner += `<div class="opt" data-oi="true" onclick="selectOpt(this)">${t('true_btn')}</div>`;
      inner += `<div class="opt" data-oi="false" onclick="selectOpt(this)">${t('false_btn')}</div>`;
      inner += `</div><div class="feedback"></div></div>`;
      tfHTML += inner;

    } else if (q.type === 'written') {
      inner += `<textarea class="written-textarea" placeholder="${t('search_ph').replace('Search', 'Write').replace('ابحث', 'اكتب')}..." style="width:100%;"></textarea>`;
      inner += `</div>
        <div class="model-answer">
          <div class="model-answer-label"><i class="fa-solid fa-check-double"></i>${t('model_answer')}</div>
          <div class="model-answer-text"></div>
        </div>
      </div>`;
      wHTML += inner;
    }
  });

  let finalHTML = '';
  if (mcqHTML) finalHTML += `<div class="quiz-section-hdr"><i class="fa-solid fa-list-check" style="color:var(--blue)"></i>${t('sec_mcq')}</div>` + mcqHTML;
  if (tfHTML)  finalHTML += `<div class="quiz-section-hdr"><i class="fa-solid fa-circle-half-stroke" style="color:var(--green)"></i>${t('sec_tf')}</div>` + tfHTML;
  if (wHTML)   finalHTML += `<div class="quiz-section-hdr"><i class="fa-solid fa-pen-to-square" style="color:var(--yellow)"></i>${t('sec_written')}</div>` + wHTML;

  container.innerHTML = finalHTML;
}

function selectOpt(el) {
  const siblings = $$('.opt', el.closest('.opts-list'));
  siblings.forEach(s => s.classList.remove('selected'));
  el.classList.add('selected');
}

function gradeQuiz(containerSel) {
  const container = $(containerSel);
  const allQ = JSON.parse(container.dataset.questions);
  let score = 0, total = 0;

  allQ.forEach((q, i) => {
    const block = $(`[data-qi="${i}"]`, container);
    if (!block) return;

    if (q.type === 'written') {
      const maBox = block.querySelector('.model-answer');
      const maText = block.querySelector('.model-answer-text');
      if (maBox && maText) {
        maBox.style.display = 'block';
        maText.textContent = q['a_' + lang];
      }
      return;
    }

    total++;
    const sel = block.querySelector('.opt.selected');
    const fb  = block.querySelector('.feedback');
    fb.style.display = 'block';

    if (!sel) {
      fb.className = 'feedback wrong';
      fb.innerHTML = `<span class="fb-label fb-wrong"><i class="fa-solid fa-circle-xmark"></i> ${t('not_answered')}</span>`;
      return;
    }

    const ans = sel.getAttribute('data-oi');
    let correct = false;
    if (q.type === 'mcq') correct = parseInt(ans) === q.answer_index;
    if (q.type === 'tf')  correct = (ans === 'true') === q.answer;

    const exp = q['explanation_' + lang] || '';
    if (correct) {
      score++;
      sel.classList.add('correct');
      fb.className = 'feedback correct';
      fb.innerHTML = `<span class="fb-label fb-correct"><i class="fa-solid fa-circle-check"></i> Correct!</span>${exp}`;
    } else {
      sel.classList.add('wrong');
      fb.className = 'feedback wrong';
      fb.innerHTML = `<span class="fb-label fb-wrong"><i class="fa-solid fa-circle-xmark"></i> Incorrect.</span>${exp}`;
    }
  });

  if (total === 0) return null;
  return { score, total, pct: Math.round((score / total) * 100) };
}

// ─────────────────────────────────────────
//  FINAL EXAM
// ─────────────────────────────────────────
let finalBuilt = false;
function buildFinalExam() {
  if (finalBuilt) return;
  finalBuilt = true;

  const combined = { mcq: [], tf: [], definitions: [], short_answer: [] };
  DB.forEach(lec => {
    if (lec.quizzes.mcq)          combined.mcq.push(...lec.quizzes.mcq);
    if (lec.quizzes.tf)           combined.tf.push(...lec.quizzes.tf);
    if (lec.quizzes.definitions)  combined.definitions.push(...lec.quizzes.definitions);
    if (lec.quizzes.short_answer) combined.short_answer.push(...lec.quizzes.short_answer);
  });

  // Shuffle all
  ['mcq','tf','definitions','short_answer'].forEach(k => {
    combined[k] = combined[k].sort(() => Math.random() - .5);
  });

  buildQuiz(combined, '#finalQuizBox');

  $('#btnSubmitFinal').onclick = () => {
    const result = gradeQuiz('#finalQuizBox');
    if (result) {
      const el = $('#finalResult');
      el.textContent = t('score_msg') + result.pct + '% (' + result.score + '/' + result.total + ')';
      $('#contentScroll').scrollTop = $('#contentScroll').scrollHeight;
    }
  };
}

// ─────────────────────────────────────────
//  EXPECTED EXAM
// ─────────────────────────────────────────
let expectedBuilt = false;
function buildExpectedExam() {
  if (expectedBuilt) return;
  expectedBuilt = true;

  const combined = { short_answer: [] };
  
  DB.forEach(lec => {
    if (lec.expected_questions) {
      lec.expected_questions.forEach(eq => {
        combined.short_answer.push({
          q_en: eq.q_en,
          q_ar: eq.q_ar,
          a_en: eq.a_en,
          a_ar: eq.a_ar
        });
      });
    }
  });

  buildQuiz(combined, '#expectedExamBox');

  $('#btnSubmitExpectedExam').onclick = () => {
    gradeQuiz('#expectedExamBox');
    $('#expectedExamResult').textContent = t('score_msg') + (lang === 'en' ? 'Self-Graded (Check model answers)' : 'تم التصحيح الذاتي (راجع الإجابات النموذجية)');
    $('#contentScroll').scrollTop = $('#contentScroll').scrollHeight;
  };
}

// ─────────────────────────────────────────
//  EXAM COUNTDOWN & WELCOME SCREEN
// ─────────────────────────────────────────
function initCountdown() {
  const examDate = new Date("2026-06-15T11:00:00+03:00").getTime();
  const updateCd = () => {
    const now = new Date().getTime();
    const dist = examDate - now;
    if (dist < 0) {
      const banner = $('#examCountdownBanner');
      if (banner) banner.style.display = 'none';
      return;
    }
    const h = Math.floor(dist / (1000 * 60 * 60));
    const m = Math.floor((dist % (1000 * 60 * 60)) / (1000 * 60));
    const s = Math.floor((dist % (1000 * 60)) / 1000);
    
    const elH = $('#cd-hours'); if (elH) elH.textContent = h.toString().padStart(2, '0');
    const elM = $('#cd-minutes'); if (elM) elM.textContent = m.toString().padStart(2, '0');
    const elS = $('#cd-seconds'); if (elS) elS.textContent = s.toString().padStart(2, '0');
  };
  updateCd();
  setInterval(updateCd, 1000);
}

function updateSidebarName(name) {
  const av = $('#sidebarAvatar');
  const nm = $('#sidebarStudentName');
  if (av) av.textContent = name.charAt(0).toUpperCase();
  if (nm) nm.textContent = name;
  $$('.user-info p').forEach(el => { el.textContent = name; });
}

function enterPlatform() {
  const nameInput = $('#studentNameInput');
  const name = nameInput ? nameInput.value.trim() : '';

  let errEl = $('#wc-error');
  if (!errEl) {
    errEl = document.createElement('p');
    errEl.id = 'wc-error';
    errEl.style.cssText = 'color:#f87171;font-size:.88rem;margin-bottom:10px;font-family:Cairo,sans-serif;';
    errEl.textContent = 'الرجاء كتابة اسمك أولاً';
    $('#wc-btn').insertAdjacentElement('beforebegin', errEl);
  }

  if (!name) {
    errEl.style.display = 'block';
    if (nameInput) nameInput.focus();
    return;
  }

  errEl.style.display = 'none';
  localStorage.setItem('ch-student-name', name);
  updateSidebarName(name);

  const ws = $('#welcomeScreen');
  ws.style.transition = 'opacity .4s ease, transform .4s ease';
  ws.style.opacity = '0';
  ws.style.transform = 'scale(1.04)';
  setTimeout(() => {
    ws.style.display = 'none';
    $('#appWrapper').style.display = 'flex';
  }, 400);
}

function changeStudentName() {
  localStorage.removeItem('ch-student-name');
  $('#appWrapper').style.display = 'none';
  const ws = $('#welcomeScreen');
  ws.style.cssText = 'position:fixed;inset:0;background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#0f172a 100%);display:flex;align-items:center;justify-content:center;z-index:9999;padding:20px;opacity:1;transform:scale(1);';
  const inp = $('#studentNameInput');
  if (inp) { inp.value = ''; setTimeout(() => inp.focus(), 100); }
}

// Boot logic
document.addEventListener('DOMContentLoaded', () => {
  const inp = $('#studentNameInput');
  if (inp) inp.addEventListener('keydown', e => { if (e.key === 'Enter') enterPlatform(); });

  const ua = navigator.userAgent || navigator.vendor || window.opera;
  if (/iPad|iPhone|iPod/.test(ua) && !window.MSStream) document.body.classList.add('ios-glass');
  else if (/Android/.test(ua)) document.body.classList.add('android');
  else document.body.classList.add('desktop');

  const savedName = localStorage.getItem('ch-student-name');
  if (savedName) {
    $('#welcomeScreen').style.display = 'none';
    $('#appWrapper').style.display = 'flex';
    updateSidebarName(savedName);
  } else {
    $('#welcomeScreen').style.display = 'flex';
    $('#appWrapper').style.display = 'none';
  }
  
  initCountdown();
});

// ─────────────────────────────────────────
//  THEME / LANG
// ─────────────────────────────────────────
function toggleTheme() {
  theme = theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('ch-theme', theme);
  applyTheme();
}

function toggleLang() {
  lang = lang === 'en' ? 'ar' : 'en';
  localStorage.setItem('ch-lang', lang);
  location.reload();
}

// ─────────────────────────────────────────
//  SEARCH
// ─────────────────────────────────────────
$('#searchInput').addEventListener('input', function () {
  const q = this.value.trim().toLowerCase();
  if (!q) { $$('.lec-card').forEach(c => c.style.display = ''); return; }
  $$('.lec-card').forEach(c => {
    const text = c.textContent.toLowerCase();
    c.style.display = text.includes(q) ? '' : 'none';
  });
});

// ─────────────────────────────────────────
//  POMODORO TIMER
// ─────────────────────────────────────────
function initTimer() {
  updateTimerDisplay();

  $('#btnTimerStartStop').onclick = () => {
    if (timerRunning) {
      clearInterval(timerInterval);
      timerRunning = false;
      $('#btnTimerStartStop').textContent = 'Resume';
    } else {
      timerRunning = true;
      $('#btnTimerStartStop').textContent = 'Pause';
      timerInterval = setInterval(() => {
        if (timerSecs > 0) {
          timerSecs--;
          updateTimerDisplay();
        } else {
          clearInterval(timerInterval);
          timerRunning = false;
          $('#btnTimerStartStop').textContent = 'Start';
        }
      }, 1000);
    }
  };

  $('#btnTimerReset').onclick = () => {
    clearInterval(timerInterval);
    timerRunning = false;
    timerSecs = 1500;
    updateTimerDisplay();
    $('#btnTimerStartStop').textContent = 'Start';
  };
}

function updateTimerDisplay() {
  const m = Math.floor(timerSecs / 60).toString().padStart(2, '0');
  const s = (timerSecs % 60).toString().padStart(2, '0');
  $('#timerDisplay').textContent = m + ':' + s;
}

function toggleTimer() {
  const modal = $('#timerModal');
  modal.style.display = modal.style.display === 'block' ? 'none' : 'block';
}

// ─────────────────────────────────────────
//  BOOT
// ─────────────────────────────────────────
// ─────────────────────────────────────────
//  WELCOME SCREEN
// ─────────────────────────────────────────
function enterPlatform() {
  const nameInput = $('#studentNameInput');
  const name = nameInput ? nameInput.value.trim() : '';

  // Show error if name is empty
  let errEl = $('#wc-error');
  if (!errEl) {
    errEl = document.createElement('p');
    errEl.id = 'wc-error';
    errEl.textContent = 'الرجاء كتابة اسمك أولاً';
    $('#wc-btn').before(errEl);
  }

  if (!name) {
    errEl.style.display = 'block';
    nameInput.focus();
    return;
  }

  errEl.style.display = 'none';
  localStorage.setItem('ch-student-name', name);

  // Animate out welcome screen
  const ws = $('#welcomeScreen');
  ws.style.transition = 'opacity .4s ease, transform .4s ease';
  ws.style.opacity = '0';
  ws.style.transform = 'scale(1.04)';
  setTimeout(() => {
    ws.style.display = 'none';
    const app = $('#appWrapper');
    app.style.display = 'flex';
    // Update user card name
    $$('.user-info p').forEach(el => { el.textContent = name; });
  }, 400);
}

// Allow Enter key to submit
document.addEventListener('DOMContentLoaded', () => {
  const inp = $('#studentNameInput');
  if (inp) inp.addEventListener('keydown', e => { if (e.key === 'Enter') enterPlatform(); });

  // If already logged in, skip welcome screen
  const savedName = localStorage.getItem('ch-student-name');
  if (savedName) {
    $('#welcomeScreen').style.display = 'none';
    const app = $('#appWrapper');
    app.style.display = 'flex';
    $$('.user-info p').forEach(el => { el.textContent = savedName; });
  }
});

window.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>"""

# Replace the placeholder with real JSON data
HTML = HTML.replace('DATABASE_PLACEHOLDER', db_json)

with io.open("index.html", "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"Build complete. index.html = {len(HTML):,} chars")
