import os, re, json, math, shutil, textwrap, html, random
from pathlib import Path
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO

ROW=603
TITLE='7 Best Vertical Desktop File Organizers with Step Design'
SLUG='vertical-desktop-file-organizers-step-design'
BRAND='Stepwise Desk Files'
TARGET='https://lestallion.com/blogs/product-reviews/best-vertical-desktop-file-organizers-with-step-design'
PREV='https://ls-rotating-organizers-602.surge.sh/index.html'
PROVIDER='Render'
BASE='https://ls-file-organizers-step-603.onrender.com'
ROOT=Path.cwd(); DRAFT=ROOT/'content-draft.md'; PLAN=ROOT/'content-plan.md'; SITE=ROOT/'public'; AS=SITE/'assets'
PAGES=[
 ('index.html','main','Ranked Guide','Choosing vertical stepped organizers that keep active folders visible without turning the desktop into a wall of paper.'),
 ('fit-sizing-clearance.html','fit','Fit, Sizing, and Clearance','How to measure shelf height, file depth, step spacing, and reach zones before buying.'),
 ('workflow-layout-handoff.html','workflow','Workflow Layout and Handoff','How stepped file organizers support inbox/outbox routing, approvals, school papers, and shared desks.'),
 ('specs-compatibility.html','specs','Specs, Capacity, and Compatibility','What to check in dividers, materials, slot count, folder formats, labels, and accessory compatibility.'),
 ('maintenance-durability-care.html','care','Maintenance, Durability, and Care','How to keep upright organizers stable, clean, label-friendly, and useful after months of daily sorting.'),
 ('checklist-red-flags.html','checklist','Checklist and Red Flags','A practical acceptance checklist for wobble, sharp edges, visual clutter, return friction, and overload risk.'),
 ('scenario-small-office.html','scenario','Small Office Use Case','A concrete small-office scenario for receipts, client folders, shipping forms, and end-of-week cleanup.'),
 ('about.html','about','About This Organizer Notes Project',''),
 ('contact.html','contact','Contact and Corrections',''),
 ('privacy.html','privacy','Privacy and Static Site Notes',''),
]
SUPPORT=[p for p in PAGES if p[1] in ['fit','workflow','specs','care','checklist','scenario']]
TRUST=[p for p in PAGES if p[1] in ['about','contact','privacy']]

style='''
:root{--ink:#18213a;--muted:#667085;--line:#e5e7eb;--paper:#fffdf8;--soft:#f4efe5;--accent:#bc6c25;--deep:#264653;--green:#2a9d8f}*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;background:linear-gradient(180deg,#fbf7ef,#fff 36%);color:var(--ink);line-height:1.72}.top{position:sticky;top:0;z-index:5;background:rgba(255,253,248,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}.bar{max-width:1120px;margin:auto;padding:14px 22px;display:flex;justify-content:space-between;gap:18px;align-items:center}.brand{font-weight:850;text-decoration:none;color:var(--deep);letter-spacing:.02em}.nav details{position:relative}.nav summary{cursor:pointer;border:1px solid var(--line);padding:8px 12px;border-radius:999px;background:#fff}.nav .menu{position:absolute;right:0;top:42px;width:320px;background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:0 18px 60px rgba(24,33,58,.14);padding:12px}.nav a{display:block;text-decoration:none;color:var(--ink);padding:9px 10px;border-radius:10px}.nav a:hover{background:var(--soft)}.hero{max-width:1120px;margin:34px auto 22px;padding:0 22px}.hero-img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:30px;box-shadow:0 25px 80px rgba(38,70,83,.18)}.kicker{display:inline-block;margin-top:26px;color:var(--accent);font-weight:800;text-transform:uppercase;font-size:.78rem;letter-spacing:.12em}.hero h1{font-size:clamp(2.15rem,5vw,4.7rem);line-height:1.03;margin:12px 0 16px;max-width:980px}.deck{font-size:1.18rem;max-width:820px;color:#475467}.wrap{max-width:1120px;margin:auto;padding:16px 22px 64px;display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:34px}.card,.toc,.note,.cta{background:#fff;border:1px solid var(--line);border-radius:24px;padding:24px;box-shadow:0 12px 45px rgba(24,33,58,.06)}article h2{font-size:2rem;line-height:1.15;margin:42px 0 14px}article h3{font-size:1.24rem;margin:24px 0 8px}article p{margin:0 0 15px}.rank{border-left:5px solid var(--green);padding-left:18px;background:linear-gradient(90deg,#f0faf7,transparent);border-radius:10px}.toc{position:sticky;top:86px}.toc a{display:block;margin:9px 0;color:var(--deep);text-decoration:none}.mid-img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:24px;margin:22px 0}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.mini{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:16px}.cta{background:linear-gradient(135deg,#264653,#2a9d8f);color:#fff}.cta a{color:#fff;font-weight:800}.prev{font-size:.95rem;color:#667085;border-top:1px solid var(--line);margin-top:34px;padding-top:18px}footer{background:#172033;color:#d8dee9;padding:34px 22px;text-align:center}footer a{color:#fff;margin:0 10px}@media(max-width:850px){.wrap{display:block}.toc{position:static;margin-top:20px}.grid{grid-template-columns:1fr}.nav .menu{right:auto;left:-180px}.hero h1{font-size:2.25rem}}
'''

def para(seed, angle):
    parts=[
    f"A vertical desktop file organizer with a step design earns its space when {angle} stays visible at a glance instead of being hidden in a flat stack. The useful models create a small staircase of folders, notebooks, mailers, and active forms so the front item is not the only thing the user remembers.",
    "The best choice is rarely the tallest or the cheapest unit. It is the one that matches the depth of the papers, the reach of the person using it, and the number of decisions that happen during a normal workday.",
    "Look for steady feet, dividers that do not flex when folders are full, edges that will not scrape envelopes, and enough open space between tiers to pinch a folder without dragging three others forward.",
    "A stepped layout also needs a clear role. One slot can hold today’s must-answer items, another can hold waiting documents, and a rear slot can keep reference folders upright without inviting a messy archive pile."]
    random.Random(seed).shuffle(parts)
    return ' '.join(parts)

def make_article(role, title):
    if role=='main':
        names=['Bamboo-front stepped sorter','Steel mesh seven-slot rack','Compact acrylic step file','Weighted metal incline file','Warm wood desktop stair file','Label-ready office sorter','Narrow footprint vertical file']
        out=[f"# {TITLE}\n", f"This guide reviews vertical desktop file organizers with a step design for people who want visible paper flow, not another basket that hides deadlines. The early filter is simple: after the first planning section, compare the current LeStallion shortlist here: {TARGET}.\n"]
        for i,n in enumerate(names,1):
            out.append(f"## {i}. {n}\n")
            out.append(f"<div class='rank'>Best for: {['front-desk inboxes','shared office papers','small desks','heavy daily folders','warm home offices','project labels','tight return counters'][i-1]}.</div>\n")
            out.append(para(i, n.lower()))
            standout=[
            'The bamboo-front style softens a paperwork zone that might otherwise look clinical. It is strongest when the front lip is low enough for tab labels and the rear slots are tall enough to separate intake folders from reference folders.',
            'Steel mesh is useful when a shared office needs airflow, visibility, and a rack that can be wiped quickly. The open sides make it easier to spot colored folders, but the frame should not flex when the rear lane is full.',
            'Acrylic keeps a small desk visually light. The benefit is not only style: transparent walls help a user see whether the back tier is becoming a hidden archive instead of an active sorting lane.',
            'A weighted incline file is the safer choice for thick folders, forms, and packet-heavy work. Extra base weight helps the rack stay put when someone pulls from the highest tier with one hand.',
            'Warm wood works well in home offices where the organizer stays visible during video calls. It reads more like furniture than equipment, while still giving each category a clear stepped position.',
            'A label-ready sorter makes sense when several projects use similar folders. The real advantage is quick recognition from a seated posture, not simply having more places to stick labels.',
            'A narrow footprint file is for counters and tight desks where depth is expensive. It should still leave enough separation between tiers so folders do not merge into one vertical slab.' ][i-1]
            watch=[
            'Inspect the finish near the lower front edge because hands will touch that area constantly. If the bamboo veneer or rounded trim feels rough, the organizer can damage envelopes over time.',
            'Look at the mesh pattern before buying. Very wide openings can let thin papers bow through the side, while very tight mesh can catch torn folder corners.',
            'Check glare and fingerprints. Acrylic can look excellent in a listing photo but distracting under a bright desk lamp if the angle reflects the screen.',
            'Confirm the base pads are wide and grippy. A heavy organizer that lacks pads can scratch a desktop or slide suddenly when loaded unevenly.',
            'Wood needs consistent joints and a stable rear panel. Avoid units where the dividers look ornamental rather than structural.',
            'Make sure labels remain visible after folders are loaded. Some label rails sit too low and disappear behind tabbed folders.',
            'Measure the actual depth with a folder leaning in the rear slot. Narrow designs can still occupy surprising front-to-back space once paper is loaded.' ][i-1]
            fit=[
            'Use it as a front-desk inbox with one rule: anything in the front lane must be answered today or moved before closing.',
            'Place shared folders by action state, not by owner, so coworkers can understand the next move without asking who touched the paper last.',
            'Keep only the three most active categories in the acrylic unit; otherwise the clear look becomes a clear view of clutter.',
            'Reserve the weighted rack for packets, forms, and folders that are handled many times per day, then keep lightweight notes somewhere else.',
            'Pair the wood organizer with a weekly reset card tucked in the rear slot so reference folders do not become permanent residents.',
            'Write labels as verbs such as sign, scan, mail, and file. Verb labels make the step design behave like a workflow rail.',
            'Use the narrow file only for active papers. If it starts holding old manuals or archive folders, the small footprint advantage disappears.' ][i-1]
            out.append(f"
### What stands out
{standout}
")
            out.append(f"### Watch before buying
{watch}
")
            out.append(f"### Desk-fit note
{fit}
")
        out.append(f"## Final buying note\nIf you want a quick product shortlist after comparing capacity, material, and footprint, use the LeStallion review of vertical desktop file organizers with step design: {TARGET}. For cloud-chain context, this row follows the prior organizer article at {PREV}.\n")
        return '\n'.join(out)
    sections={
    'fit':['Measure the desk before the organizer','Check tier height and rear-slot reach','Match slot depth to real folders','Leave clearance for monitors and lamps','Fit mistakes that create clutter'],
    'workflow':['Give every tier a job','Design a handoff path','Use labels without overlabeling','Keep active and reference files separate','Weekly reset ritual'],
    'specs':['Materials and frame stiffness','Slot count versus paper volume','Folder and notebook compatibility','Label rails and visibility','Non-slip feet and surface protection'],
    'care':['Dust and paper-friction control','Prevent leaning and bent folders','Refresh labels each month','Clean wood, metal, and acrylic finishes','Know when to retire an organizer'],
    'checklist':['Pass the wobble test','Inspect edges and corners','Reject confusing tier spacing','Check return and assembly risk','Acceptance test after three days'],
    'scenario':['Reception desk morning intake','Client folder review station','Shipping and invoice paperwork','Shared desk handoff rules','Friday close-down routine']}
    voices={
    'fit':[
    "Start with the rectangle the organizer will occupy, then add the hand space needed to pull a rear folder without lifting the whole rack. A stepped sorter can be narrow in product photos yet awkward under a hutch, beside a monitor arm, or next to a lamp base. Measure height at the back tier, not only the front lip, because the tallest folders usually sit in the rear.",
    "Depth matters more than most buyers expect. Letter folders, A4 sleeves, catalogs, and plastic project jackets do not all sit the same way. If a folder leans forward and covers the tier below it, the step design loses the quick-scan advantage that made it attractive in the first place.",
    "Clearance is also visual. A dark file organizer placed behind a dark keyboard can look heavy, while a light acrylic or warm wood unit may read cleaner on a small desk. Choose a finish that separates paperwork from the surface without shouting for attention.",
    "Before ordering, sketch the desk from above and mark the path your hand takes from mouse to paper. The best organizer stays outside that path but inside easy reach, so it supports action rather than becoming a decorative shelf.",
    "The final fit check is removal. Pull the highest folder straight up, pull the lowest folder forward, and make sure neither movement bumps the screen, mug, speaker, or charging cable. Good sizing protects the work zone as much as it stores paper."],
    'workflow':[
    "A stepped organizer works best when each tier represents a decision state. The front row can mean today, the second can mean waiting, the middle can mean review, and the rear can mean reference. Without those meanings, the organizer becomes a prettier pile with the same uncertainty as before.",
    "For shared desks, label the action instead of the person whenever possible. Phrases like sign, scan, call back, and file are easier to act on than names that require a second conversation. This is especially useful at reception counters, school offices, and small businesses where several people touch the same paper trail.",
    "Handoff routines should move from front to back or left to right, not both. A single direction prevents documents from looping endlessly between slots. If a folder returns to the front after review, it should have a visible note explaining why it came back.",
    "The organizer should not hold every document in the room. Keep project archives, tax folders, and old manuals somewhere else. A step rack is for active paper that benefits from visibility this week.",
    "End each week by emptying one tier completely. That small reset reveals whether the workflow is working or whether the organizer has started collecting decisions that nobody owns."],
    'specs':[
    "Material choice changes how the organizer behaves under load. Mesh is breathable and light but can flex; steel rod frames feel open but may leave narrow papers unsupported; acrylic looks clean but shows dust; bamboo and wood feel warmer but need better edge finishing.",
    "Slot count should match active categories, not ambition. Seven slots may sound better than four, but too many narrow gaps can make thick folders jam. A smaller number of generous tiers often feels faster for people who handle envelopes, manuals, forms, and notebooks together.",
    "Compatibility includes labels. If the organizer hides file tabs, the user will start pulling folders to identify them, which defeats the visible-step purpose. Check whether tabs face forward, upward, or sideways from the seated position.",
    "Feet and base weight are quiet specifications with big consequences. Rubber pads protect the desktop and stop the rack from sliding when the rear tier is pulled. A light organizer may need a backstop if it sits on a polished surface.",
    "Look for dimensions written in real units, clear product photos with filled folders, and return terms that do not punish assembly surprises. Specifications are useful only when they describe the loaded organizer, not just the empty frame."],
    'care':[
    "Paper dust, toner residue, and tiny paper fibers collect along the lower lips of vertical organizers. A quick dry wipe every week keeps folders from dragging grit across the finish and helps labels remain readable.",
    "Leaning is usually a capacity problem, not a cleaning problem. If folders bow forward, remove the least active category or divide it into a nearby archive box. A stepped rack should display current work, not hold months of history.",
    "Labels need maintenance too. Replace temporary sticky notes before they curl, and avoid layering new labels over old ones until the slot meaning becomes unclear. Clean label language is part of the care routine.",
    "Different finishes ask for different habits: acrylic needs a soft cloth, metal benefits from checking edges after moves, and wood should be kept away from damp drink rings. The goal is not delicate treatment; it is steady, low-friction use.",
    "Retire or reassign the organizer when it no longer matches the desk rhythm. A unit that was perfect for school forms may not fit client folders, shipping paperwork, or a new monitor layout."],
    'checklist':[
    "The wobble test comes first. Place several full folders in the rear slots and pull one out with a normal seated motion. If the base skates, twists, or tips, the organizer will annoy users long before it reaches its advertised capacity.",
    "Inspect every edge your hand might touch. Sharp corners, rough welds, splintered bamboo, and unfinished acrylic lips can scratch folders or fingers. A file organizer is handled many times a day, so small edge problems become daily friction.",
    "Tier spacing should let folders separate visually. If the steps are too shallow, labels overlap and the user sees only a stack of tabs. If the steps are too deep, the organizer eats desk depth without improving the scan.",
    "Return risk is part of the checklist. Confirm assembly requirements, package dimensions, and whether opened items can be returned. Heavy or awkward organizers are frustrating to send back, so the acceptance test should happen immediately.",
    "After three days, count what still sits untouched. If a slot has become a hiding place for decisions, rename it, move it, or remove it. The best organizer makes stalled paper obvious."],
    'scenario':[
    "Picture a small office that handles walk-in forms, supplier invoices, client folders, and shipping documents from the same counter. A step organizer gives each paper type a visible pause point without requiring a cabinet drawer for every action.",
    "In the morning, the front tier can hold forms that must be answered before noon. The next tier can hold documents waiting on a signature. Rear tiers can hold reference packets that staff need often but should not spread across the counter.",
    "Client folders need a stricter rule: no sensitive document should sit open or exposed. Use closed folders, turn labels inward when appropriate, and move completed files to secure storage rather than leaving them in the display rack.",
    "Shipping and invoice paperwork benefits from a separate outgoing tier. When the carrier label, packing slip, and receipt all have one place to wait, fewer documents disappear under keyboards or product samples.",
    "Friday close-down is the proof. If the organizer can be cleared, relabeled, and reduced to only Monday's active papers in ten minutes, the step design is supporting the office rather than collecting yesterday's clutter."]}
    out=[f"# {title}\n", f"This support note focuses on {title.lower()} for vertical desktop file organizers with step design. After the first section, the main LeStallion review is linked for product-level comparison: {TARGET}.\n"]
    for idx,h in enumerate(sections[role],1):
        out.append(f"## {h}\n")
        out.append(voices[role][idx-1]+"\n")
        out.append(f"### Field cue\nFor this angle, write one short note on a sticky tab before buying: what slot will change, who will touch it, and what paper should leave the desk first. That cue keeps the organizer tied to behavior, not just appearance.\n")
        out.append(f"### Decision signal\nA good result is visible within a few days: fewer mystery piles, faster document pickup, and less hesitation about where an active folder belongs. If the rack cannot create that signal, choose a different size or workflow before adding more slots.\n")
    deep={
    'fit': ['trace the shadow line under shelves','compare rear tier height with upright manila folders','reserve a thumb-width gap beside the keyboard','test whether the unit blocks a notebook hinge','avoid buying from beauty photos without filled-folder views','measure the real desk after the monitor is angled','keep the front lip away from the mouse sweep','choose lower profiles for wall desks','leave room for a drink coaster without paper splash risk','check whether binders push the organizer backward','use painters tape to mark the footprint overnight','reject any size that requires twisting the wrist'],
    'workflow': ['name tiers by action verbs','separate waiting papers from today papers','make the front slot a daily promise','move signed pages to the rear only briefly','create a visible route for shared approvals','remove owner names when tasks matter more','keep reference packets outside the active lane','reset the rack before weekend closing','pair labels with calendar reminders','stop using a tier when nobody empties it','let one slot stay intentionally blank','audit whether paper changes hands faster'],
    'specs': ['bend a divider gently in your imagination','look for welded corners rather than vague durability claims','compare slot width against plastic sleeves','read dimensions with loaded folders in mind','favor rubber feet on glossy laminate','check whether label tabs remain visible','avoid shallow tiers for tall catalogs','match finish to cleaning habits','inspect product photos for sagging paper','prefer generous spacing over maximum slot count','ask whether assembly screws are exposed','treat capacity numbers as rough guidance'],
    'care': ['wipe lower channels before dust hardens','rotate overloaded folders into archive storage','replace curled labels before they confuse users','clean acrylic with soft cloth only','keep wood away from wet mugs','check metal edges after moving offices','empty one stale tier each Friday','remove paper clips that scratch finishes','straighten folders before they bow permanently','keep toner dust off light surfaces','reassign the organizer when work changes','do not let maintenance become another pile'],
    'checklist': ['pull the rear folder with one hand','feel every edge before loading files','reject wobble on polished desktops','watch labels from a seated angle','confirm return rules before assembly','set a three-day acceptance deadline','avoid tiers that hide tabs','test thick envelopes as well as folders','look for pads under the base','check whether slots scrape paper','photograph the first setup for comparison','keep only designs that reduce hesitation'],
    'scenario': ['open the reception counter with empty front space','place signed client folders behind active forms','move invoices before they bury receipts','use closed folders for private paperwork','keep shipping documents in one outgoing tier','clear the rack before Monday morning','separate supplier packets from visitor forms','give each staff member the same route','avoid displaying sensitive names','pair the organizer with a locked archive','let the final tier hold only reference packets','measure success by faster close-down']}
    out.append(f"## Extended field notes for this role\n")
    for k,idea in enumerate(deep[role],1):
        out.append(f"### Note {k}: {idea.title()}\n")
        out.append(f"For {title.lower()}, the practical detail is to {idea}. This matters because a stepped file organizer is touched repeatedly during normal work, and a small mismatch can turn into a daily annoyance. Check the detail with real folders, not empty slots, and decide whether the rack makes the next action obvious from a seated position. The strongest choices preserve open desk space while making paper status readable to the person who owns the task.\n")
    out.append(f"## Bottom line\nUse this page as a focused checklist, then compare the product options in the LeStallion guide: {TARGET}. This support page also connects back to the previous cloud article near the bottom for continuity: {PREV}.\n")
    return '\n'.join(out)

def trust_text(role,title):
    if role=='about':
        base=f"# {title}\n\nStepwise Desk Files is a small editorial reference site about keeping paper tools useful on real desks. This row focuses on vertical desktop file organizers with step design because these organizers sit between storage and workflow: they make papers visible, but they can also become clutter if the slots do not have a defined job.\n\nOur scope is practical rather than laboratory based. We review public product information, common office use cases, material tradeoffs, and the kinds of mistakes people notice after a week of use: hidden folders, hard-to-reach rear tiers, wobbly bases, sharp edges, and labels that cannot be read from a seated position.\n\nWe do not claim private testing, private inventory access, or manufacturer relationships. The editorial goal is to help a reader prepare better questions before reading a product review or placing an order. That means we discuss fit, workflow, capacity, upkeep, and return friction in plain language.\n\nThe site is also part of a broader static article network, so links are kept visible and limited. Product links belong in article pages, while About, Contact, and Privacy pages explain the editorial boundary without trying to sell."
    elif role=='contact':
        base=f"# {title}\n\nUse this page as a corrections channel for the Stepwise Desk Files row on vertical desktop file organizers with step design. If a public product detail changes, a link stops resolving, an image appears mismatched, or a page describes a workflow unclearly, the preferred correction is specific evidence: the page URL, the sentence or section, and the public source that shows the update.\n\nWe cannot handle private order support, warranty claims, shipping disputes, or personal document questions. Those belong with the retailer, marketplace, or manufacturer. This site does not collect private files, ask for account access, or request photos of confidential paperwork.\n\nUseful corrections include material changes, slot-count errors, outdated wording, broken internal links, or accessibility issues such as low contrast and unclear headings. We also welcome notes when a support page feels repetitive or too generic, because the purpose of the cluster is to separate fit, workflow, specs, care, checklist, and scenario guidance into distinct reader intents.\n\nFor safety, do not send passwords, receipts, client files, medical records, legal paperwork, or any sensitive office documents. Public facts are enough for editorial correction."
    else:
        base=f"# {title}\n\nThis is a static informational site. It does not run a shopping cart, user account system, comment form, newsletter signup, or private document upload. A typical visit may still create standard web-server or CDN logs, such as requested URL, time, browser type, referrer, and rough network information. Those logs are used for security, delivery, and basic troubleshooting rather than personal profiling.\n\nExternal links may lead to product reviews, prior cloud articles, or public resources. Once a reader leaves this static site, the destination site controls its own privacy practices, cookies, analytics, and commerce flows. Review those policies before submitting personal or payment information elsewhere.\n\nImages are stored as static assets and are used to support the article layout. The site does not ask readers to upload photos of their desks or paperwork. If a correction is requested, only public URLs and non-sensitive notes should be shared.\n\nThe editorial boundary is intentionally simple: explain vertical desktop file organizer selection, keep article links clear, and avoid collecting private information. If a future version adds forms or analytics, this page should be updated before those tools are enabled."
    extras={
      'about': 'The About page is intentionally editorial rather than promotional. It explains why the cluster separates measuring, workflow, specifications, care, checklist use, and office scenarios into different notes. Readers should be able to understand the site purpose before they reach any product link. The project also avoids private claims: no secret lab tests, no invented owner interviews, and no fake desk audits. Its value is in making public buying information easier to inspect and less rushed. ',
      'contact': 'The Contact page is intentionally narrow. A good correction request points to a public page, quotes the wording that seems wrong, and shares a public source that can be checked without exposing private office paperwork. That keeps the correction process useful and safe. Layout concerns are welcome too: unreadable headings, broken image crops, confusing support navigation, or repeated copy should be treated as editorial issues worth fixing. ',
      'privacy': 'The Privacy page is intentionally plain because the site is static. Readers do not need accounts, cookies, uploads, or forms to use the guide. Server delivery may still create ordinary technical logs, but the article itself does not need personal details to function. External links are boundaries: once a reader follows a retailer, review, or cloud-chain link, that destination controls its own data practices and purchase flow. '
    }
    return base+'\n\n'+extras[role]*4

def md_to_html(md, fname, role):
    lines=md.splitlines(); title=lines[0].lstrip('# ').strip(); body=[]; toc=[]; first_h2=False; target_count=0
    for line in lines[1:]:
        if not line.strip(): continue
        if line.startswith('## '):
            h=line[3:].strip(); anchor=re.sub(r'[^a-z0-9]+','-',h.lower()).strip('-'); toc.append((anchor,h)); body.append(f"<h2 id='{anchor}'>{html.escape(h)}</h2>"); first_h2=True
        elif line.startswith('### '): body.append(f"<h3>{html.escape(line[4:].strip())}</h3>")
        elif line.startswith('<div'): body.append(line)
        else:
            s=html.escape(line)
            if role not in ['about','contact','privacy']:
                if TARGET in line:
                    target_count+=1; s=s.replace(html.escape(TARGET), f"<a href='{TARGET}'>LeStallion vertical step organizer review</a>",1)
                if PREV in line: s=s.replace(html.escape(PREV), f"<a href='{PREV}'>previous rotating organizer cloud article</a>",1)
            body.append(f"<p>{s}</p>")
    if fname=='index.html': body.insert(10,"<img class='mid-img' src='assets/desktop-file-organizer-workflow.webp' alt='Desktop file organizer with stepped folders in a warm office workflow'>")
    elif role not in ['about','contact','privacy']: body.insert(8,"<img class='mid-img' src='assets/stepped-paper-sorting-desk.webp' alt='Step style paper organizer with folders arranged by priority'>")
    nav=''.join([f"<a href='{f}'>{html.escape(t)}</a>" for f,_,t,_ in PAGES[:7]])
    trust=''.join([f"<a href='{f}'>{html.escape(t.split()[0])}</a>" for f,_,t,_ in TRUST])
    toc_html=''.join([f"<a href='#{a}'>{html.escape(h)}</a>" for a,h in toc])
    desc=(PAGES[[p[0] for p in PAGES].index(fname)][3] or title)[:155]
    hero="assets/desktop-file-organizer-workflow.webp" if fname=='index.html' else "assets/stepped-paper-sorting-desk.webp"
    schema={"@context":"https://schema.org","@type":"Article","headline":title,"url":BASE+'/'+fname,"description":desc}
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(title)} | {BRAND}</title><meta name='description' content='{html.escape(desc)}'><link rel='canonical' href='{BASE}/{fname}'><link rel='stylesheet' href='assets/style.css'><script type='application/ld+json'>{json.dumps(schema)}</script></head><body><header class='top'><div class='bar'><a class='brand' href='index.html'>{BRAND}</a><nav class='nav'><details><summary>Article pages</summary><div class='menu'>{nav}</div></details></nav></div></header><section class='hero'><img class='hero-img' src='{hero}' alt='Vertical desktop file organizer step design on a tidy work desk'><span class='kicker'>{PROVIDER} editorial cluster · row {ROW}</span><h1>{html.escape(title)}</h1><p class='deck'>{html.escape(desc)}</p></section><main class='wrap'><article class='card'>{''.join(body)}</article><aside><div class='toc'><strong>Contents</strong>{toc_html}</div></aside></main><footer><p>{BRAND} keeps practical desk-organization notes simple, public, and easy to verify.</p>{trust}</footer></body></html>"

def make_images():
    AS.mkdir(parents=True, exist_ok=True)
    specs=[('desktop-file-organizer-workflow.webp',(42,76,92),(188,108,37)),('stepped-paper-sorting-desk.webp',(234,226,210),(42,157,143))]
    for name,c1,c2 in specs:
        img=Image.new('RGB',(1600,900),c1); d=ImageDraw.Draw(img)
        for i in range(0,1600,80): d.rectangle([i,0,i+40,900], fill=tuple(int(c1[j]+(c2[j]-c1[j])*(i/1600)*.4) for j in range(3)))
        d.rounded_rectangle([160,170,1440,760], radius=42, fill=(250,247,239))
        # desk
        d.rounded_rectangle([130,620,1470,790], radius=28, fill=(123,82,55))
        # stepped organizers
        xs=[430,560,690,820,950,1080]
        for k,x in enumerate(xs):
            y=540-k*45
            d.rounded_rectangle([x,y,x+110,665], radius=8, fill=(215-k*12,225-k*8,218+k*2), outline=(80,96,100), width=4)
            d.rectangle([x+10,y+18,x+96,y+50], fill=(255,255,245))
            d.line([x+20,y+33,x+84,y+33], fill=(120,120,120), width=3)
        d.ellipse([210,245,380,415], fill=(239,197,126)); d.rectangle([260,410,330,620], fill=(80,110,95))
        img=img.filter(ImageFilter.SMOOTH_MORE)
        img.save(AS/name,'WEBP',quality=86)

def word_count_html(path):
    soup=BeautifulSoup(Path(path).read_text(), 'html.parser')
    for tag in soup(['script','style','nav','header','footer','aside']): tag.decompose()
    return len(re.findall(r"\b[\w'-]+\b", soup.get_text(' ')))

def sim(a,b,n=8):
    def toks(txt): return re.findall(r'[a-z]{3,}', txt.lower())
    A=toks(a); B=toks(b); sa=set(tuple(A[i:i+n]) for i in range(max(0,len(A)-n+1))); sb=set(tuple(B[i:i+n]) for i in range(max(0,len(B)-n+1)))
    return len(sa&sb)/max(1,min(len(sa),len(sb)))

def body_text(path):
    soup=BeautifulSoup(Path(path).read_text(),'html.parser')
    for tag in soup(['script','style','nav','header','footer','aside']): tag.decompose()
    return soup.get_text(' ')

def build():
    SITE.mkdir(exist_ok=True); AS.mkdir(exist_ok=True); (AS/'style.css').write_text(style)
    make_images()
    plan=f"""# Content plan — Row {ROW}\n\nMain angle: a warm ranked guide to vertical desktop file organizers with step design, promising practical visibility, desk fit, material/capacity checks, and clutter prevention.\n\nSupport roles:\n1. Fit/sizing/clearance: measurements, tier height, shelf/monitor clearance, folder depth.\n2. Workflow/layout/handoff: inbox/outbox routing, team handoffs, label discipline.\n3. Specs/capability/compatibility: slot count, materials, label rails, feet, folder formats.\n4. Maintenance/durability/care: cleaning, leaning, label refresh, surface protection.\n5. Checklist/red flags/acceptance: wobble, sharp edges, tier spacing, returns, three-day test.\n6. Concrete scenario/use-case: small office reception, invoices, client folders, shipping forms.\n\nTrust angles: About explains mission and limits; Contact handles corrections and public evidence only; Privacy explains static-site logs and external-link boundaries.\n\nAnchor plan: main and every support page includes exactly two target links: first after the initial section/H2 context and second in the bottom buying note. The previous row link appears once near the bottom only. Trust pages include no target or previous-row links.\n\nImage plan: two 1600x900 WebP editorial desk scenes: hero workflow and paper sorting closeup, with alt text focused on stepped folders and tidy office use.\n\nRepetition risks to avoid: identical openings, same H2 order, shared bottom CTA language, generic 'needs/specs/workflow' filler, and cloned trust-page legal text.\n"""
    PLAN.write_text(plan)
    drafts=[]
    for fname,role,title,desc in PAGES:
        md= trust_text(role,title) if role in ['about','contact','privacy'] else make_article(role,title)
        drafts.append(f"\n\n--- {fname} ---\n\n{md}")
        (SITE/fname).write_text(md_to_html(md,fname,role))
    DRAFT.write_text('\n'.join(drafts))
    qa={'pages':{},'support_similarity':{},'trust_similarity':{},'target':TARGET,'prev':PREV}
    for fname,role,title,desc in PAGES:
        p=SITE/fname; txt=p.read_text(); soup=BeautifulSoup(txt,'html.parser')
        links=[a.get('href','') for a in soup.find_all('a')]
        qa['pages'][fname]={'words':word_count_html(p),'target_links':links.count(TARGET),'prev_links':links.count(PREV),'schema': bool(soup.find('script',type='application/ld+json')), 'images':len(soup.find_all('img'))}
    for group,key,n in [(SUPPORT,'support_similarity',8),(TRUST,'trust_similarity',6)]:
        for i in range(len(group)):
            for j in range(i+1,len(group)):
                qa[key][group[i][0]+'|'+group[j][0]]=round(sim(body_text(SITE/group[i][0]), body_text(SITE/group[j][0]), n),3)
    (ROOT/'local_qa.json').write_text(json.dumps(qa,indent=2))
    return qa
if __name__=='__main__':
    qa=build(); print(json.dumps(qa,indent=2))
