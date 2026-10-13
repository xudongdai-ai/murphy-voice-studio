"""Local branding and vector decorations for the singing workspace."""

import base64
from pathlib import Path

APP_NAME = "ai唱歌克隆"


def load_brand_css():
    assets = Path(__file__).resolve().parent
    artwork = base64.b64encode((assets / "ui" / "upload-art.svg").read_bytes()).decode("ascii")
    return (assets / "brand.css").read_text(encoding="utf-8").replace(
        "__UPLOAD_ART__", f"data:image/svg+xml;base64,{artwork}"
    )


HEADER_HTML = """
<section class="brand-shell" aria-label="ai唱歌克隆">
  <svg class="hero-atmosphere" viewBox="0 0 1350 284" preserveAspectRatio="none" aria-hidden="true">
    <defs>
      <radialGradient id="warm-sun" cx="25%" cy="20%" r="85%"><stop stop-color="#f9e6cd" stop-opacity=".8"/><stop offset="1" stop-color="#fffaf3" stop-opacity="0"/></radialGradient>
      <linearGradient id="warm-ribbon" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#e8c8a2" stop-opacity="0"/><stop offset=".55" stop-color="#e3bc8d" stop-opacity=".19"/><stop offset="1" stop-color="#f6e7d6" stop-opacity=".3"/></linearGradient>
    </defs>
    <circle cx="905" cy="170" r="112" fill="url(#warm-sun)"/>
    <path d="M360 145C565 8 611 258 830 191S1098 183 1350 182V258C1114 306 1041 153 835 218S557 63 360 186Z" fill="url(#warm-ribbon)"/>
    <path d="M390 121C571 22 635 271 843 203S1116 307 1350 180" stroke="#fff" stroke-width="1.6" fill="none" opacity=".9"/>
    <path d="M395 175C570 55 650 248 839 219S1126 309 1350 208" stroke="#fff" stroke-width="1" fill="none" opacity=".7"/>
    <path d="M470 69C661 188 651 80 822 16" stroke="#fff" stroke-width="1" fill="none" opacity=".7"/>
  </svg>
  <div class="brand-top">
    <div class="brand-identity">MURPHY <span class="brand-slash">/</span><span class="brand-studio">AI MUSIC STUDIO</span></div>
    <span class="brand-local"><span></span>本地声音工作台</span>
  </div>
  <div class="brand-content">
    <div class="brand-copy">
      <div class="brand-eyebrow">让熟悉的声音，唱出新的可能</div>
      <h1>AI唱歌克隆<span class="brand-title-dot">.</span></h1>
      <p>用 AI 转换歌声与音色，从声音模型到音频导出，一站完成你的声音创作。</p>
      <div class="brand-author"><span>作者 <strong>MurphyProd1</strong></span><span class="brand-divider"></span><span>有问题联系微信：<strong>MurphyProd1</strong></span></div>
    </div>
    <div class="brand-wave" aria-hidden="true">
      <div class="brand-wave-label">VOICE → NEW POSSIBILITIES</div>
      <svg viewBox="0 0 500 138" fill="none">
        <defs><linearGradient id="voice-gradient" x1="0" x2="1"><stop stop-color="#bda28e"/><stop offset=".35" stop-color="#95725d"/><stop offset=".58" stop-color="#e9bf90"/><stop offset=".75" stop-color="#eedaa5"/><stop offset="1" stop-color="#d9ad87"/></linearGradient></defs>
        <path d="M8 66v6m12-15v24m12-18v12m12-20v28m12-36v44m12-58v72m12-65v58m12-75v90m12-62v34m12-55v76m12-87v100m12-120v137m12-94v52m12-47v42m12-61v70m12-82v94m12-75v56m12-47v38m12-28v18m12-22v26m12-19v12m12-25v36m12-39v44m12-57v72m12-82v94m12-76v62m12-52v38m12-32v22m12-25v26m12-43v62m12-69v78m12-59v42m12-33v22m12-25v28m12-41v56m12-48v40m12-30v18m12-21v24m12-14v10m12-12v8" stroke="url(#voice-gradient)" stroke-width="5.5" stroke-linecap="round"/>
      </svg>
      <div class="brand-wave-bottom"><span>CLONE YOUR VOICE</span><span class="wave-separator">|</span><span>CREATE YOUR SOUND</span></div>
    </div>
  </div>
</section>
"""

WORKFLOW_HTML = """
<div class="workflow-guide" aria-label="使用流程">
  <div><span class="step-number">01</span><span><strong>选择声音</strong><small>载入目标模型与索引</small></span></div>
  <span class="step-arrow" aria-hidden="true">→</span>
  <div><span class="step-number">02</span><span><strong>上传音频</strong><small>添加需要转换的人声</small></span></div>
  <span class="step-arrow" aria-hidden="true">→</span>
  <div><span class="step-number">03</span><span><strong>克隆与导出</strong><small>调整参数，生成新歌声</small></span></div>
</div>
"""

FOOTER_HTML = """
<div class="brand-footer">
  <strong>ai唱歌克隆</strong><span>作者：MurphyProd1<span class="footer-divider">｜</span>有问题联系微信：MurphyProd1</span>
</div>
"""
