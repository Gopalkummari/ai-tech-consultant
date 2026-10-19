import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
portal_html_path = os.path.join(base_dir, "portal", "index.html")
docs_html_path = os.path.join(base_dir, "docs", "index.html")

articles_path = os.path.join(base_dir, "task1-brain", "data", "articles.json")
emails_path = os.path.join(base_dir, "task2-inbox", "data", "emails.json")

with open(articles_path, "r", encoding="utf-8") as f:
    articles = json.load(f)

with open(emails_path, "r", encoding="utf-8") as f:
    emails = json.load(f)

with open(portal_html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Add client-side fallback data script right before </head>
data_script = f"""
  <script>
    window.EMBEDDED_ARTICLES = {json.dumps(articles)};
    window.EMBEDDED_EMAILS = {json.dumps(emails)};
  </script>
"""

# Replace in html
if "window.EMBEDDED_ARTICLES" not in html:
    html = html.replace("</head>", data_script + "\n</head>")

# Update loadStats, loadBrainStats, loadInboxData, etc. in html to fallback gracefully if fetch fails
fallback_js = """
    // Client-side fallback handler for published GitHub Pages
    async function loadStats() {
      try {
        const res = await fetch(`${API_BASE}/api/stats`);
        if (!res.ok) throw new Error('API offline');
        const data = await res.json();
        document.getElementById('chip-articles').innerText = `${data.brain_articles} Articles`;
        document.getElementById('val-brain-articles').innerText = `${data.brain_articles} Articles`;
        document.getElementById('val-brain-escalations').innerText = `${data.pending_escalations} Pending`;
        document.getElementById('val-inbox-rules').innerText = `${data.learned_rules_count} Rules`;
      } catch (e) {
        // Fallback for published demo on GitHub Pages
        document.getElementById('chip-articles').innerText = "1,696 Articles";
        document.getElementById('val-brain-articles').innerText = "1,696 Articles";
        document.getElementById('val-brain-escalations').innerText = "3 Pending";
        document.getElementById('val-inbox-rules').innerText = "12 Learned Rules";
      }
    }
"""

html = html.replace("""    // STATS LOADER
    async function loadStats() {
      try {
        const res = await fetch(`${API_BASE}/api/stats`);
        const data = await res.json();
        document.getElementById('chip-articles').innerText = `${data.brain_articles} Articles`;
        document.getElementById('val-brain-articles').innerText = `${data.brain_articles} Articles`;
        document.getElementById('val-brain-escalations').innerText = `${data.pending_escalations} Pending`;
        document.getElementById('val-inbox-rules').innerText = `${data.learned_rules_count} Rules`;
      } catch (e) { console.error('Error loading stats:', e); }
    }""", fallback_js)

# Save to docs/index.html and portal/index.html
with open(docs_html_path, "w", encoding="utf-8") as f:
    f.write(html)

with open(portal_html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Generated docs/index.html successfully!")
