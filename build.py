"""Generate the profile README + light/dark SVG assets. Usage: python3 build.py <github-username>"""
import sys, pathlib
from html import escape as e

USER = sys.argv[1] if len(sys.argv) > 1 else "newpheeraphat"
ROOT = pathlib.Path(__file__).parent
W = 1000
THEMES = {
    "": dict(ink="#1F2328", muted="#59636E", dim="#8C959F", rule="#D0D7DE", accent="#0969DA"),
    "dark/": dict(ink="#E6EDF3", muted="#9198A1", dim="#656C76", rule="#3D444D", accent="#4493F8"),
}

def svg(h, body, label, t):
    return f'''<svg viewBox="0 0 {W} {h}" width="{W}" height="{h}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{e(label)}">
<style>
.m{{font-family:ui-monospace,"SFMono-Regular","SF Mono",Menlo,Consolas,"Liberation Mono",monospace}}
.r{{opacity:0;animation:r .7s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes r{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.blink{{animation:b 1.1s steps(1) infinite}}@keyframes b{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.r{{animation:none;opacity:1}}.blink{{animation:none}}}}
</style>
{body.format(**t)}
</svg>
'''

def txt(x, y, s, size=15, fill="ink", d=0.1, extra=""):
    return f'<text class="m r" style="animation-delay:{d:.2f}s" x="{x}" y="{y}" font-size="{size}" fill="{{{fill}}}" {extra}>{e(s)}</text>'

def rule(y, d=0.1):
    return f'<line class="r" style="animation-delay:{d:.2f}s" x1="48" y1="{y}" x2="952" y2="{y}" stroke="{{rule}}" stroke-width="1"/>'

def section(n, title):
    body = (txt(48, 34, f"{n:02d}", 13, "accent", 0, 'letter-spacing="2"')
            + txt(84, 34, "—", 13, "dim", 0) + txt(110, 34, title, 13, "muted", 0, 'letter-spacing="3"')
            + f'<line x1="{126 + len(title) * 10}" y1="30" x2="952" y2="30" stroke="{{rule}}" stroke-width="1"/>')
    return 48, body, f"{n:02d} — {title}"

def kv(rows, top=36, step=34, key_w=150):
    out, y = [], top
    for i, (k, v, color) in enumerate(rows):
        d = 0.1 + i * 0.12
        out.append(txt(48, y, k.upper(), 11, "muted", d, 'letter-spacing="2.5"'))
        out.append(txt(48 + key_w, y, v, 15, color, d))
        y += step
    return y - step + 24, "".join(out)

# ---------- content ----------
HEADER = (60 + 120,
    txt(48, 70, "PHEERAPHAT PRISAN", 40, "ink", 0, 'font-weight="700" letter-spacing="6"')
    + txt(48, 108, "software engineer · backend & platform · thailand", 16, "muted", .2)
    + txt(48, 146, "$ whoami --verbose", 14, "accent", .4)
    + '<rect class="blink" x="218" y="134" width="9" height="16" fill="{accent}"/>',
    "Pheeraphat Prisan — software engineer")

WHOAMI_TOP = [
    ("I build the money-and-tax parts of a cloud accounting platform for Thai SMEs.", "ink"),
    ("Mostly .NET services behind Angular, iOS and Android clients, from schema to rollout.", "ink"),
    ("I like boring, reversible deploys: feature flags, characterization tests, runbooks.", "muted"),
]
WHOAMI_KV = [
    ("focus", "tax compliance · billing & subscriptions · caching · AI-augmented SDLC", "ink"),
    ("now", "electronic tax documents — signing, batch submission, cancellation flows", "accent"),
    ("school", "Mahidol University", "ink"),
    ("habits", "test first · design doc before code · small, single-purpose PRs", "ink"),
]

WORK = [
    ("Electronic tax documents", "digitally signed invoices and receipts sent to the tax authority,",
     "queue-based worker pipeline, batch submit/cancel, audit trail"),
    ("Profile API migration", "per-field Redis cache, commit-then-invalidate,",
     "flag-gated rollout across many consumers within a latency budget"),
    ("Usage-based billing", "metered usage events, live usage updates in the app,",
     "add-on gating and quota handling"),
    ("Onboarding & permissions", "identity verification, team invites, role permissions —",
     "one rule set shipped to web, iOS and Android"),
    ("Agentic SDLC tooling", "Claude Code agent teams driving design docs, TDD loops,",
     "PR review and deploy runbooks"),
]

PROJECTS = [
    ("leave-management", "C#", "leave requests on Clean Architecture"),
    ("expense-tracker-ai", "TypeScript", "personal finance tracker · Next.js 14 + Tailwind"),
    ("flowaccount.pdfmake.workspace", "JavaScript", "client/server PDF printing"),
    ("rabbitmq-basic", "JavaScript", "messaging patterns, publish/consume, retries"),
    ("design-pattern", "C#", "GoF patterns, worked one by one"),
    ("ticket-booking", "C#", "seat booking API"),
    ("student-management", "C#", "CRUD + auth starter"),
]

STACK = [
    ("languages", "C# · TypeScript · JavaScript · Kotlin · Swift · Python · SQL"),
    ("backend", ".NET · ASP.NET Core · EF Core · Node.js · RabbitMQ"),
    ("data", "SQL Server · PostgreSQL · MongoDB · Redis / Valkey · Elasticsearch"),
    ("frontend", "Angular · NgRx · React · Next.js · Tailwind"),
    ("cloud & ops", "AWS (ECS, S3, Lambda, Secrets Manager) · Docker · Jenkins · GitHub Actions"),
    ("testing", "xUnit · Moq · Jest · Playwright · Testcontainers"),
    ("ai", "Claude Code · multi-agent workflows · MCP"),
]

# ---------- builders ----------
def whoami():
    out, y = [], 32
    for i, (s, c) in enumerate(WHOAMI_TOP):
        out.append(txt(48, y, s, 16 if c == "ink" else 15, c, .1 + i * .1)); y += 28
    out.append(rule(y - 8, .4))
    h, body = kv(WHOAMI_KV, top=y + 26)
    return h, "".join(out) + body, "About Pheeraphat"

def work():
    out, y = [], 36
    for i, (title, a, b) in enumerate(WORK):
        d = .1 + i * .12
        out.append(txt(48, y, f"[{i + 1}]", 13, "accent", d))
        out.append(txt(90, y, title, 16, "ink", d, 'font-weight="600"'))
        out.append(txt(90, y + 24, a, 14, "muted", d))
        out.append(txt(90, y + 44, b, 14, "muted", d))
        y += 78
    return y - 30, "".join(out), "What I ship at work"

def projects():
    out, y = [], 34
    out.append(txt(48, y, "REPO", 11, "dim", 0, 'letter-spacing="2.5"'))
    out.append(txt(390, y, "LANG", 11, "dim", 0, 'letter-spacing="2.5"'))
    out.append(txt(520, y, "WHAT", 11, "dim", 0, 'letter-spacing="2.5"'))
    out.append(rule(y + 12, 0)); y += 42
    for i, (name, lang, what) in enumerate(PROJECTS):
        d = .1 + i * .08
        out.append(txt(48, y, name, 15, "ink", d))
        out.append(txt(390, y, lang, 14, "accent", d))
        out.append(txt(520, y, what, 14, "muted", d))
        y += 32
    return y - 12, "".join(out), f"{len(PROJECTS)} side projects"

def stack():
    h, body = kv([(k, v, "ink") for k, v in STACK], key_w=160)
    return h, body, "Technical stack"

def footer():
    return 92, (rule(20, 0)
        + txt(48, 56, "● building", 14, "accent", .1)
        + txt(190, 56, "tax compliance · billing · agentic delivery — bangkok, TH", 14, "muted", .2)
        + txt(952, 56, f"github.com/{USER}", 13, "dim", .3, 'text-anchor="end"')), "Current status"

VISUALS = [("header", HEADER), ("s01", section(1, "whoami")), ("whoami", whoami()),
           ("s02", section(2, "what i ship")), ("work", work()),
           ("s03", section(3, "projects")), ("projects", projects()),
           ("s04", section(4, "telemetry")),
           ("s05", section(5, "stack")), ("stack", stack()), ("footer", footer())]

for prefix, t in THEMES.items():
    (ROOT / "assets" / prefix).mkdir(parents=True, exist_ok=True)
    for name, (h, body, label) in VISUALS:
        (ROOT / "assets" / prefix / f"{name}.svg").write_text(svg(h, body, label, t))

def pic(name, label, width=""):
    w = f' width="{width}"' if width else ""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/{name}.svg"/>'
            f'<img src="assets/{name}.svg"{w} alt="{e(label)}"/></picture>')

def badge(text, href, logo=""):
    lg = f"&logo={logo}" if logo else ""
    u = "https://img.shields.io/badge/{}-{}?style=flat-square{}&logoColor={}"
    return (f'<a href="{href}"><picture><source media="(prefers-color-scheme: dark)" srcset="{u.format(text, "0d1117", lg, "ffffff")}"/>'
            f'<img src="{u.format(text, "ffffff", lg, "000000")}" alt="{text.title()}"/></picture></a>')

labels = dict((n, v[2]) for n, v in VISUALS)
graph = ("https://github-readme-activity-graph.vercel.app/graph?username=" + USER
         + "&bg_color=00000000&color={c}&line={c}&point={c}&area_color={c}&area=true&hide_border=true&radius=0&custom_title=CONTRIBUTION%20TELEMETRY")
dual = lambda url, alt: (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{url.format(c="e6edf3")}"/>'
                         f'<img src="{url.format(c="1f2328")}" width="97%" alt="{alt}"/></picture>')

README = f"""<div align="center">

{pic("header", labels["header"])}

{badge("GITHUB", f"https://github.com/{USER}", "github")}
{badge("LINKEDIN", "https://www.linkedin.com/in/pprisan/", "linkedin")}
{badge("EMAIL", "mailto:peraput2545@gmail.com", "gmail")}
{badge("FLOWACCOUNT", "https://flowaccount.com")}

</div>

{pic("s01", labels["s01"])}
{pic("whoami", labels["whoami"])}
{pic("s02", labels["s02"])}
{pic("work", labels["work"])}
{pic("s03", labels["s03"])}
{pic("projects", labels["projects"])}
{pic("s04", labels["s04"])}

<div align="center">

{dual(graph, "GitHub contribution activity")}

</div>

{pic("s05", labels["s05"])}
{pic("stack", labels["stack"])}
{pic("footer", labels["footer"])}
"""
(ROOT / "README.md").write_text(README)
assert all((ROOT / "assets" / p / f"{n}.svg").exists() for p in THEMES for n, _ in VISUALS)
print("ok", USER)
