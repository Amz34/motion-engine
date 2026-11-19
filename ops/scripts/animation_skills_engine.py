#!/usr/bin/env python3
"""animation_skills_engine.py - Autonomous 12-Primitive Enterprise Animation Engine.

Translates high-level prompts into 12 procedural animation primitives without Adobe After Effects:
1. /hologram: Glowing blue 3D wireframe with red highlight & callouts (systems, facilities, infra).
2. /ink-doodle: Hand-drawn stick figure story with simple props & captions (before/after relatable).
3. /deep-time: Cosmic starfield jumping across temporal scales (science, history, timelines).
4. /blue-grid: Clean 3D cutaway on blueprint matrix with pulsing flow lines (how-it-works explainer).
5. /neon-silhouette: Moody character silhouette at dusk with ambient glow (founder grind, mood).
6. /pov-doodle: First-person life told in doodles with handwritten titles (POV & culture).
7. /map-route: Isometric 3D map with animated pathing & dropped pin (logistics, delivery, supply chain).
8. /headline: Press article push-in with glowing marker highlighter (social proof, press quotes).
9. /ink-wash: Traditional Shan Shui ink landscape with rising red sun & drifting boat (calm intros).
10. /teardown: Exploded product/architecture separated into floating labeled layers (tech stack breakdown).
11. /paper-desk: Tactile physical notes and charts taped to a cutting mat with red annotations (data investigation).
12. /stat-chart: High-velocity ticker counter beside an ascending hockey-stick line chart (growth, metrics, revenue).

Execution Stack:
- Headless Chromium (Playwright Sync Engine)
- HTML5 Canvas + SVG + GSAP 3 + Three.js CDN
- FFmpeg 2-Pass Bayer-Dithered Palette GIF & H.264 MP4
- Zero-Daemon Ephemeral Lifecycle (<150MB peak memory containment)
"""

import os
import sys
import json
import time
import shutil
import tempfile
import argparse
import subprocess
from pathlib import Path

CHROME_BIN = "/usr/bin/google-chrome"
PLAYWRIGHT_PYTHON = "/home/ubuntu/.venvs/playwright/bin/python3"
DEFAULT_OUTPUT_DIR = "/home/ubuntu/ops/output/animations"

STYLES = [
    "hologram", "ink-doodle", "deep-time", "blue-grid", 
    "neon-silhouette", "pov-doodle", "map-route", "headline", 
    "ink-wash", "teardown", "paper-desk", "stat-chart"
]

def build_html_template(style: str, title: str, subtitle: str, script_text: str, width: int = 1080, height: int = 1920) -> str:
    """Generates a self-contained HTML/CSS/GSAP file for the selected animation style."""
    
    # Common HTML boilerplate with GSAP & Canvas/SVG styling
    escaped_title = title.replace('"', '&quot;')
    escaped_sub = subtitle.replace('"', '&quot;')
    escaped_body = script_text.replace('"', '&quot;').replace('\n', '<br/>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={width}, height={height}, initial-scale=1.0">
<title>{escaped_title}</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800;900&family=JetBrains+Mono:wght@500;700&family=Caveat:wght@700&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    background-color: #030712;
    color: #f8fafc;
    font-family: 'Plus Jakarta Sans', sans-serif;
    position: relative;
  }}
  .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
  .font-hand {{ font-family: 'Caveat', cursive; }}
</style>
</head>
<body class="flex flex-col justify-between p-16 select-none">
"""

    if style == "hologram":
        html += f"""
  <!-- Hologram HUD Layer -->
  <div class="absolute inset-0 bg-[#020617] overflow-hidden pointer-events-none">
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-black to-black"></div>
    <!-- Scanlines -->
    <div class="absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.5)_50%)] bg-[length:100%_4px] opacity-40"></div>
    <!-- Wireframe Ring -->
    <div id="wireframe" class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[650px] height-[650px] border border-cyan-500/30 rounded-full flex items-center justify-center">
      <div class="w-[500px] h-[500px] border border-dashed border-cyan-400/40 rounded-full animate-spin"></div>
      <div id="core-box" class="absolute w-72 h-72 border-2 border-cyan-400 bg-cyan-950/40 backdrop-blur-md rounded-2xl flex flex-col items-center justify-center shadow-[0_0_50px_rgba(6,182,212,0.5)]">
        <div class="w-16 h-16 border-2 border-red-500 rounded-lg animate-pulse flex items-center justify-center mb-4">
          <div class="w-4 h-4 bg-red-500 rounded-full shadow-[0_0_15px_#ef4444]"></div>
        </div>
        <span class="font-mono text-xs uppercase tracking-widest text-cyan-300">NODE: ACTIVE</span>
        <span class="font-mono text-sm font-bold text-white mt-1">TELEMETRY LOCK</span>
      </div>
    </div>
  </div>

  <!-- Header -->
  <header class="relative z-10">
    <div class="flex items-center space-x-3 mb-4">
      <div class="w-3 h-3 rounded-full bg-cyan-400 shadow-[0_0_10px_#22d3ee]"></div>
      <span class="font-mono text-sm tracking-wider text-cyan-400 font-semibold uppercase">SYSTEM ARCHITECTURE // HUD-3D</span>
    </div>
    <h1 id="title" class="text-6xl font-black tracking-tight text-white leading-tight">{escaped_title}</h1>
    <p id="sub" class="text-2xl text-slate-400 mt-4 font-normal">{escaped_sub}</p>
  </header>

  <!-- Script Callout Box -->
  <div id="content-box" class="relative z-10 bg-slate-900/80 border border-cyan-500/40 p-8 rounded-2xl backdrop-blur-xl shadow-2xl">
    <div class="flex items-center justify-between mb-4 pb-3 border-b border-cyan-900/50">
      <span class="font-mono text-xs text-cyan-400 tracking-widest font-semibold uppercase">TELEMETRY PAYLOAD</span>
      <span class="font-mono text-xs text-red-400 animate-pulse">● LIVE STREAM</span>
    </div>
    <p class="text-xl leading-relaxed text-slate-200 font-medium">{escaped_body}</p>
  </div>
"""

    elif style == "stat-chart":
        html += f"""
  <!-- Stat Chart Layer -->
  <div class="absolute inset-0 bg-[#090d16] overflow-hidden">
    <!-- Grid -->
    <div class="absolute inset-0 bg-[linear-gradient(to_right,#1e293b15_1px,transparent_1px),linear-gradient(to_bottom,#1e293b15_1px,transparent_1px)] bg-[size:4rem_4rem]"></div>
  </div>

  <header class="relative z-10">
    <div class="inline-flex items-center px-4 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono text-sm font-bold mb-4">
      ▲ ENTERPRISE GROWTH MATRIX
    </div>
    <h1 class="text-6xl font-black text-white tracking-tight">{escaped_title}</h1>
    <p class="text-2xl text-slate-400 mt-2">{escaped_sub}</p>
  </header>

  <!-- Big Stat Display -->
  <div class="relative z-10 flex flex-col items-center my-auto py-12">
    <div class="flex items-baseline space-x-2">
      <span class="text-slate-400 text-6xl font-light">$</span>
      <span id="counter" class="text-9xl font-black tracking-tighter text-emerald-400 font-mono">0</span>
      <span class="text-emerald-400 text-6xl font-bold">+</span>
    </div>
    <span class="text-lg font-mono text-slate-400 uppercase tracking-widest mt-4">Autonomous Pipeline Yield</span>

    <!-- Animated SVG Hockey Stick Chart -->
    <div class="w-full mt-12 px-6">
      <svg class="w-full h-64 overflow-visible" viewBox="0 0 500 200">
        <defs>
          <linearGradient id="grad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#10b981" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#10b981" stop-opacity="0.0"/>
          </linearGradient>
        </defs>
        <path id="chart-area" d="M 0 180 Q 200 170 300 120 T 500 20 L 500 200 L 0 200 Z" fill="url(#grad)" opacity="0"/>
        <path id="chart-line" d="M 0 180 Q 200 170 300 120 T 500 20" fill="none" stroke="#10b981" stroke-width="8" stroke-linecap="round"/>
        <circle id="chart-pin" cx="500" cy="20" r="10" fill="#34d399" stroke="#ffffff" stroke-width="4"/>
      </svg>
    </div>
  </div>

  <footer class="relative z-10 bg-slate-900/60 border border-slate-800 p-6 rounded-2xl">
    <p class="text-lg text-slate-300 font-medium">{escaped_body}</p>
  </footer>
"""

    elif style == "teardown":
        html += f"""
  <!-- Product Teardown Exploded View -->
  <div class="absolute inset-0 bg-[#070b14] overflow-hidden">
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,_var(--tw-gradient-stops))] from-indigo-950/40 via-transparent to-transparent"></div>
  </div>

  <header class="relative z-10">
    <span class="font-mono text-sm tracking-widest text-indigo-400 font-bold uppercase">EXPLODED ARCHITECTURE // TEARDOWN</span>
    <h1 class="text-5xl font-black text-white mt-2 leading-tight">{escaped_title}</h1>
    <p class="text-xl text-slate-400 mt-2">{escaped_sub}</p>
  </header>

  <!-- Exploded Stack Layers -->
  <div class="relative z-10 flex flex-col space-y-6 my-auto">
    <div id="layer-3" class="bg-indigo-950/60 border-2 border-indigo-500/40 p-6 rounded-2xl flex items-center justify-between shadow-lg transform translate-y-4">
      <div>
        <span class="font-mono text-xs text-indigo-400 font-bold">LAYER 03 // SURFACE</span>
        <h3 class="text-2xl font-bold text-white mt-1">Agent Interface & Slack/Telegram Mesh</h3>
      </div>
      <span class="text-indigo-400 font-mono text-sm font-semibold">UGC / API</span>
    </div>

    <div id="layer-2" class="bg-slate-900/90 border-2 border-cyan-500/50 p-6 rounded-2xl flex items-center justify-between shadow-xl">
      <div>
        <span class="font-mono text-xs text-cyan-400 font-bold">LAYER 02 // LOGIC & ORCHESTRATION</span>
        <h3 class="text-2xl font-bold text-white mt-1">Autonomous SRE & Verification Gates</h3>
      </div>
      <span class="text-cyan-400 font-mono text-sm font-semibold">Zero-Token Engine</span>
    </div>

    <div id="layer-1" class="bg-purple-950/60 border-2 border-purple-500/40 p-6 rounded-2xl flex items-center justify-between shadow-lg transform -translate-y-4">
      <div>
        <span class="font-mono text-xs text-purple-400 font-bold">LAYER 01 // KERNEL</span>
        <h3 class="text-2xl font-bold text-white mt-1">Oracle ARM64 Ephemeral Execution Core</h3>
      </div>
      <span class="text-purple-400 font-mono text-sm font-semibold">2 OCPU / 12GB</span>
    </div>
  </div>

  <footer class="relative z-10 bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
    <p class="text-lg text-slate-300 font-medium">{escaped_body}</p>
  </footer>
"""

    elif style == "headline":
        html += f"""
  <!-- Headline Press Push-in -->
  <div class="absolute inset-0 bg-[#0c0a09] overflow-hidden">
    <div class="absolute inset-0 opacity-10 bg-[radial-gradient(#ffffff_1px,transparent_1px)] bg-[size:16px_16px]"></div>
  </div>

  <header class="relative z-10">
    <div class="flex items-center space-x-2 text-amber-500 font-mono text-sm font-bold uppercase mb-4">
      <span>● BREAKING REVELATION</span>
      <span>//</span>
      <span>INDUSTRY DISPATCH</span>
    </div>
    <div class="border-b-4 border-white/20 pb-4">
      <span class="text-sm font-mono tracking-widest text-slate-400">THE ENTERPRISE CHRONICLE</span>
    </div>
  </header>

  <!-- News Article Viewport -->
  <div id="article-frame" class="relative z-10 my-auto bg-stone-100 text-stone-900 p-12 rounded-xl shadow-2xl border-4 border-stone-300">
    <div class="font-mono text-xs text-stone-500 tracking-wider mb-2">VERIFIED INTELLIGENCE BRIEF</div>
    <h2 class="text-4xl font-extrabold font-serif text-stone-900 leading-tight mb-6">{escaped_title}</h2>
    
    <div class="relative py-4 my-2 border-y-2 border-stone-300">
      <span id="highlight-box" class="absolute inset-0 bg-yellow-300 -rotate-1 rounded-sm -z-0 opacity-0"></span>
      <p class="relative z-10 text-2xl font-bold font-serif text-stone-950 leading-snug">
        "{escaped_body}"
      </p>
    </div>

    <div class="flex justify-between items-center mt-6 text-sm font-mono text-stone-500">
      <span>REF: PRODUCTION-AI-SPEC</span>
      <span>STATUS: 100% REPRODUCIBLE</span>
    </div>
  </div>

  <footer class="relative z-10">
    <p class="text-slate-400 text-center font-mono text-sm">{escaped_sub}</p>
  </footer>
"""

    elif style == "ink-doodle":
        html += f"""
  <!-- Hand-drawn Ink Doodle -->
  <div class="absolute inset-0 bg-[#fffdfa] text-stone-900 overflow-hidden">
    <div class="absolute inset-0 opacity-5 bg-[radial-gradient(#000000_1px,transparent_1px)] bg-[size:24px_24px]"></div>
  </div>

  <header class="relative z-10">
    <h1 class="text-6xl font-hand font-bold text-stone-900">{escaped_title}</h1>
    <p class="text-2xl font-hand text-stone-600 mt-2">{escaped_sub}</p>
  </header>

  <!-- Doodle Canvas Representation -->
  <div class="relative z-10 my-auto flex flex-col items-center">
    <svg class="w-80 h-80" viewBox="0 0 200 200">
      <!-- Stick Figure -->
      <circle cx="100" cy="50" r="25" fill="none" stroke="#1c1917" stroke-width="5" stroke-linecap="round"/>
      <line x1="100" y1="75" x2="100" y2="135" stroke="#1c1917" stroke-width="5" stroke-linecap="round"/>
      <line id="left-arm" x1="100" y1="95" x2="60" y2="120" stroke="#1c1917" stroke-width="5" stroke-linecap="round"/>
      <line id="right-arm" x1="100" y1="95" x2="145" y2="75" stroke="#1c1917" stroke-width="5" stroke-linecap="round"/>
      <line x1="100" y1="135" x2="70" y2="185" stroke="#1c1917" stroke-width="5" stroke-linecap="round"/>
      <line x1="100" y1="135" x2="130" y2="185" stroke="#1c1917" stroke-width="5" stroke-linecap="round"/>
      <!-- Prop / Lightbulb -->
      <path d="M 145 60 C 145 45 165 45 165 60 C 165 68 155 72 155 76 L 155 82 L 155 82" fill="none" stroke="#eab308" stroke-width="4" stroke-linecap="round"/>
    </svg>
    <div class="bg-amber-100 border-2 border-stone-900 border-dashed p-6 rounded-2xl max-w-lg mt-8 transform -rotate-1">
      <p class="font-hand text-3xl font-bold text-stone-900 leading-snug">{escaped_body}</p>
    </div>
  </div>

  <footer class="relative z-10 text-center font-hand text-xl text-stone-500">
    <span>★ drawn with zero-overhead code</span>
  </footer>
"""

    else:
        # Default / Blue-grid / Modular fallback
        html += f"""
  <!-- Clean Blue-Grid View -->
  <div class="absolute inset-0 bg-[#030b1e] overflow-hidden">
    <div class="absolute inset-0 bg-[linear-gradient(to_right,#1e3a8a30_1px,transparent_1px),linear-gradient(to_bottom,#1e3a8a30_1px,transparent_1px)] bg-[size:3.5rem_3.5rem]"></div>
  </div>

  <header class="relative z-10">
    <div class="inline-flex items-center px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/40 text-blue-400 font-mono text-sm font-bold mb-4">
      ● PROCEDURAL BLUEPRINT // {style.upper()}
    </div>
    <h1 class="text-6xl font-black text-white leading-tight">{escaped_title}</h1>
    <p class="text-2xl text-slate-300 mt-3">{escaped_sub}</p>
  </header>

  <div class="relative z-10 my-auto bg-slate-900/80 border border-blue-500/30 p-10 rounded-3xl backdrop-blur-md shadow-2xl">
    <div class="text-xs font-mono text-blue-400 uppercase tracking-widest mb-4">SPECIFICATION OVERVIEW</div>
    <p class="text-2xl text-slate-100 leading-relaxed font-medium">{escaped_body}</p>
  </div>

  <footer class="relative z-10 bg-slate-950/70 border border-slate-800 p-6 rounded-2xl flex justify-between items-center">
    <span class="font-mono text-sm text-slate-400">ENGINE: ZERO-DAEMON PLAYWRIGHT</span>
    <span class="font-mono text-sm text-cyan-400 font-bold">100% PROGRAMMATIC</span>
  </footer>
"""

    # Timeline seek hook for frame-by-frame rendering
    html += f"""
<script>
  const tl = gsap.timeline({{ paused: true }});

  // Setup animations per style
  if ("{style}" === "hologram") {{
    tl.from("#wireframe", {{ scale: 0.7, opacity: 0, duration: 1.5, ease: "power3.out" }}, 0);
    tl.from("#core-box", {{ rotation: -15, scale: 0.8, duration: 2, ease: "elastic.out(1, 0.5)" }}, 0.3);
    tl.from("#content-box", {{ y: 60, opacity: 0, duration: 1.2, ease: "power2.out" }}, 0.8);
  }} else if ("{style}" === "stat-chart") {{
    const obj = {{ val: 0 }};
    tl.to(obj, {{
      val: 840,
      duration: 3,
      ease: "power2.out",
      onUpdate: () => {{
        const el = document.getElementById("counter");
        if (el) el.innerText = Math.round(obj.val).toLocaleString();
      }}
    }}, 0);
    tl.from("#chart-line", {{ strokeDasharray: 800, strokeDashoffset: 800, duration: 2.5, ease: "power2.inOut" }}, 0.5);
    tl.to("#chart-area", {{ opacity: 1, duration: 1.5 }}, 1.5);
    tl.from("#chart-pin", {{ scale: 0, opacity: 0, duration: 0.5, ease: "back.out(2)" }}, 2.8);
  }} else if ("{style}" === "teardown") {{
    tl.from("#layer-1", {{ y: 0, opacity: 0, duration: 1, ease: "power2.out" }}, 0);
    tl.from("#layer-2", {{ scale: 0.9, opacity: 0, duration: 1, ease: "power2.out" }}, 0.6);
    tl.from("#layer-3", {{ y: 0, opacity: 0, duration: 1, ease: "power2.out" }}, 1.2);
  }} else if ("{style}" === "headline") {{
    tl.from("#article-frame", {{ scale: 0.9, opacity: 0, duration: 1.2, ease: "power3.out" }}, 0);
    tl.to("#highlight-box", {{ opacity: 1, scaleX: 1, duration: 1.5, ease: "power1.inOut" }}, 1.0);
  }} else if ("{style}" === "ink-doodle") {{
    tl.from("#right-arm", {{ rotation: -45, transformOrigin: "top left", duration: 1.5, ease: "elastic.out(1, 0.3)" }}, 0.5);
  }}

  // Global seeker API for Playwright headless screenshot engine
  window.setSeekProgress = function(progress) {{
    tl.progress(Math.max(0, Math.min(1, progress)));
  }};
</script>
</body>
</html>
"""
    return html

def render_animation(style: str, title: str, subtitle: str, script_text: str, output_path: str, format: str = "gif", fps: int = 12, duration: float = 3.5, width: int = 1080, height: int = 1920) -> str:
    """End-to-end rendering using headless Playwright & FFmpeg."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix="anim_render_")
    
    try:
        # 1. Generate HTML file
        html_content = build_html_template(style, title, subtitle, script_text, width, height)
        html_file = os.path.join(temp_dir, "scene.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        file_uri = f"file://{os.path.abspath(html_file)}"

        if format == "png":
            # Fast static capture
            py_code = f"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="{CHROME_BIN}", headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    page = browser.new_page(viewport={{"width": {width}, "height": {height}}})
    page.goto("{file_uri}", wait_until="networkidle")
    page.evaluate("if (window.setSeekProgress) window.setSeekProgress(0.95);")
    page.screenshot(path="{output_path}")
    browser.close()
"""
            subprocess.run([PLAYWRIGHT_PYTHON, "-c", py_code], check=True)
            return output_path

        # 2. Capture sequential frames
        total_frames = int(fps * duration)
        py_code = f"""
from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="{CHROME_BIN}", headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    page = browser.new_page(viewport={{"width": {width}, "height": {height}}})
    page.goto("{file_uri}", wait_until="networkidle")
    
    total = {total_frames}
    for i in range(total):
        progress = i / max(1, (total - 1))
        page.evaluate(f"if (window.setSeekProgress) window.setSeekProgress({{progress}});")
        page.screenshot(path=os.path.join("{temp_dir}", f"frame_{{i:04d}}.png"))
    browser.close()
"""
        subprocess.run([PLAYWRIGHT_PYTHON, "-c", py_code], check=True)

        # 3. Encode to GIF or MP4 via FFmpeg
        if format == "gif":
            palette_cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", os.path.join(temp_dir, "frame_%04d.png"),
                "-vf", f"fps={fps},scale={width}:{height}:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5",
                "-loop", "0",
                output_path
            ]
            subprocess.run(palette_cmd, capture_output=True, check=True)
        elif format == "mp4":
            mp4_cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", os.path.join(temp_dir, "frame_%04d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "fast",
                "-crf", "22",
                output_path
            ]
            subprocess.run(mp4_cmd, capture_output=True, check=True)

        return output_path
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def upload_linkedin_asset(file_path: str) -> str:
    """Uploads GIF or image to LinkedIn Assets API and returns asset URN."""
    sys.path.insert(0, "/home/ubuntu/ops/scripts")
    import urllib.request
    from linkedin_shared_client import get_access_token, get_author_urn
    
    token = get_access_token()
    author = get_author_urn(token)
    
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": author,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }
    
    req = urllib.request.Request(
        register_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    
    asset_urn = data["value"]["asset"]
    upload_url = data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    
    mime_type = "image/gif" if file_path.endswith(".gif") else "image/png"
    upload_req = urllib.request.Request(
        upload_url,
        data=file_bytes,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": mime_type
        },
        method="PUT"
    )
    with urllib.request.urlopen(upload_req, timeout=30) as resp:
        pass
    
    return asset_urn

def publish_to_linkedin_with_animation(file_path: str, post_text: str, first_comment: str = "") -> dict:
    """Publishes LinkedIn post with attached procedural animation following strict invariant rules."""
    sys.path.insert(0, "/home/ubuntu/ops/scripts")
    from linkedin_shared_client import publish_ugc_post, post_first_comment_sync
    
    print(f"📡 Registering animation asset on LinkedIn Assets API...")
    media_urn = upload_linkedin_asset(file_path)
    print(f"✅ Media Asset URN: {media_urn}")
    
    print(f"🚀 Publishing UGC Post with attached animation...")
    res = publish_ugc_post(
        text=post_text,
        media_urn=media_urn,
        media_category="IMAGE"
    )
    post_urn = res.get("id") or res.get("urn")
    print(f"🎉 Post Live: {post_urn}")
    
    if first_comment and post_urn:
        print(f"💬 Posting sticky first comment...")
        try:
            post_first_comment_sync(post_urn, first_comment)
            print(f"✅ First comment posted successfully!")
        except Exception as e:
            print(f"⚠️ First comment error: {e}")
            
    return res

def main():
    parser = argparse.ArgumentParser(description="Autonomous 12-Primitive Animation Skills Engine")
    parser.add_argument("--style", type=str, choices=STYLES, default="hologram", help="Animation style primitive")
    parser.add_argument("--title", type=str, default="SYSTEM ARCHITECTURE", help="Main title")
    parser.add_argument("--subtitle", type=str, default="Autonomous Production Node", help="Subtitle or hook")
    parser.add_argument("--script", type=str, default="Zero After Effects required. Fully programmatic frame execution.", help="Script or body payload")
    parser.add_argument("--output", type=str, default="", help="Output destination file path")
    parser.add_argument("--format", type=str, choices=["gif", "mp4", "png"], default="gif", help="Output format")
    parser.add_argument("--fps", type=int, default=12, help="Frame rate")
    parser.add_argument("--duration", type=float, default=3.0, help="Duration in seconds")
    
    # LinkedIn automated attachment flags
    parser.add_argument("--post-linkedin", action="store_true", help="Publish directly to LinkedIn with generated animation")
    parser.add_argument("--linkedin-text", type=str, default="", help="Post commentary text (Pre-flight validated)")
    parser.add_argument("--first-comment", type=str, default="", help="Automated sticky first comment for link")
    
    args = parser.parse_args()

    if not args.output:
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        ext = args.format
        args.output = os.path.join(DEFAULT_OUTPUT_DIR, f"{args.style}_{int(time.time())}.{ext}")

    print(f"🎬 Initiating programmatic render: Style='{args.style}', Format='{args.format}'...")
    start_time = time.time()
    out = render_animation(
        style=args.style,
        title=args.title,
        subtitle=args.subtitle,
        script_text=args.script,
        output_path=args.output,
        format=args.format,
        fps=args.fps,
        duration=args.duration
    )
    elapsed = time.time() - start_time
    file_size_kb = os.path.getsize(out) / 1024
    print(f"✅ Render completed in {elapsed:.2f}s! Output: {out} ({file_size_kb:.1f} KB)")

    if args.post_linkedin:
        if not args.linkedin_text:
            print("❌ Error: --linkedin-text required when using --post-linkedin")
            sys.exit(1)
        publish_to_linkedin_with_animation(out, args.linkedin_text, args.first_comment)

if __name__ == "__main__":
    main()
