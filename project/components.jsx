// components.jsx — three direction explorations for siyulio.com
// Each direction renders the SAME content (Hero, Article List, Article Page)
// but with different visual treatments. Wrapped in DCArtboards.

const ARTICLES = [
  { cat: "MANUFACTURING AI", title: "在傳統製造業導入 AI，最先卡住的不是模型", date: "2026年4月25日",
    excerpt: "很多人談 AI 落地都從模型聊起，但真正讓專案推不動的，是流程、組織、與一線人員的注意力。" },
  { cat: "AI NOTES", title: "我目前最常用的 AI 工具組合", date: "2026年4月22日",
    excerpt: "對我來說，AI 工具不是越多越好，而是要能真的接進工作與筆記流程裡。" },
  { cat: "HAND DRIP COFFEE", title: "泡咖啡這件事，怎麼幫我整理思緒", date: "2026年4月18日",
    excerpt: "我原本以為泡咖啡只是工作之外的休閒，後來才慢慢發現，它對我最大的價值，反而是把節奏慢下來。" },
  { cat: "AI NOTES", title: "如何建立自己的常用指令庫", date: "2026年4月14日",
    excerpt: "我在工作中最常遇到的問題，不是沒有 AI 工具可用，而是每次都要重新想一次怎麼下指令。" },
  { cat: "AI NOTES", title: "我怎麼用 Obsidian 管理工作中的 AI 知識", date: "2026年4月10日",
    excerpt: "我會想把 AI 相關的內容收進 Obsidian，是因為如果不刻意整理，很多有價值的內容都會散在聊天視窗、文件草稿、臨時截圖裡。" },
  { cat: "MANUFACTURING AI", title: "當主管、使用者、推動者想的都不一樣時，AI 專案怎麼推", date: "2026年4月05日",
    excerpt: "我越來越覺得，很多 AI 專案推不起來，不是因為模型不夠強，而是因為同一個專案裡的三種角色，想的根本不是同一件事。" },
];

const NAV_ITEMS = ["製造業 AI", "AI 新知", "手沖咖啡", "個人經歷"];

// ────────────────────────────────────────────────────────────
// Vercel-style cursor-tracking glow card. Wraps children and sets
// CSS variables --mx/--my so the ::before radial gradient follows
// the pointer.
// ────────────────────────────────────────────────────────────
function GlowCard({ children, className = "", style, onClick }) {
  const ref = React.useRef(null);
  const onMove = (e) => {
    const el = ref.current; if (!el) return;
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    el.style.setProperty('--my', (e.clientY - r.top) + 'px');
  };
  return (
    <div ref={ref} className={`card ${className}`} style={style} onMouseMove={onMove} onClick={onClick}>
      {children}
    </div>
  );
}

// ────────────────────────────────────────────────────────────
// Logo — used across directions
// ────────────────────────────────────────────────────────────
function Logo({ small }) {
  return (
    <div className="logo">
      <div className="logo-mark" style={small ? {width:30,height:30,fontSize:10} : {}}>JL</div>
      <div className="logo-text">
        <div className="logo-name">siyulio</div>
        <div className="logo-sub">AI field notes by Jason Lin</div>
      </div>
    </div>
  );
}

// ────────────────────────────────────────────────────────────
// Navbars — three different treatments
// ────────────────────────────────────────────────────────────
function NavbarA({ tweaks }) {
  // Refined original — kept floating pill but tightened
  return (
    <div style={{display:'flex', justifyContent:'center', paddingTop: 28}}>
      <nav className="nav-a">
        <Logo small />
        <div style={{display:'flex', gap:24, paddingLeft:8}}>
          {NAV_ITEMS.map((n,i)=>(
            <span key={i} className="nav-link">{n}</span>
          ))}
        </div>
        <span className="nav-cta">Curated Signal Map</span>
      </nav>
    </div>
  );
}

function NavbarB() {
  // Linear — top-flush, hairline border, no pill chrome
  return (
    <div className="container">
      <nav className="nav-b">
        <Logo small />
        <div className="nav-links">
          {NAV_ITEMS.map((n,i)=>(
            <span key={i} className="nav-link">{n}</span>
          ))}
        </div>
        <span className="nav-cta" style={{borderColor:'var(--border-strong)', color:'var(--text)', background:'transparent'}}>
          Signal Map →
        </span>
      </nav>
    </div>
  );
}

function NavbarC() {
  // Vercel — clean, CTA gold pill
  return (
    <div className="container">
      <nav className="nav-c">
        <Logo small />
        <div style={{display:'flex', gap:32}}>
          {NAV_ITEMS.map((n,i)=>(
            <span key={i} className="nav-link">{n}</span>
          ))}
        </div>
        <span className="nav-cta" style={{background:'var(--text)', color:'#0a0a0a', borderColor:'var(--text)'}}>
          Signal Map
        </span>
      </nav>
    </div>
  );
}

// ────────────────────────────────────────────────────────────
// Hero — the original "two-column starscape + headline" layout,
// but with three direction-specific treatments
// ────────────────────────────────────────────────────────────
function HeroA() {
  return (
    <section className="container" style={{paddingTop: 96, paddingBottom: 96}}>
      <div className="hero-grid">
        <div className="starscape" style={{aspectRatio:'4/3'}} />
        <div className="col gap-24">
          <div className="eyebrow">JASON LIN / AI FIELD NOTES</div>
          <h1 className="h1" style={{maxWidth: 460}}>
            把企業裡真的<br/>用得上的 AI，<br/>整理成可以開始<br/>的做法。
          </h1>
          <p className="body" style={{maxWidth: 460}}>
            我在傳統製造業做 AI 落地，橫跨軟體開發與 PM，也是認真對待手沖咖啡的人。這裡不是 AI 新聞站，而是一個把現場經驗、工具方法與生活感受慢慢寫清楚的地方。
          </p>
          <div className="flex gap-8 mt-8" style={{flexWrap:'wrap'}}>
            <span className="chip">製造業 AI 落地</span>
            <span className="chip">AI 工具與方法</span>
            <span className="chip">手沖咖啡</span>
          </div>
          <div className="flex gap-12 mt-16">
            <span className="btn btn-primary">先看製造業 AI</span>
            <span className="btn btn-ghost">再看 AI 新知</span>
          </div>
        </div>
      </div>
    </section>
  );
}

function HeroB() {
  // Linear style — large headline forward, image as accent on the side
  return (
    <section className="container" style={{paddingTop: 120, paddingBottom: 96}}>
      <div className="col gap-32">
        <div className="eyebrow-muted">Jason Lin · AI Field Notes · 2026</div>
        <h1 className="h1" style={{fontSize: 72, maxWidth: 880, lineHeight: 1.12}}>
          把企業裡真的用得上的 AI，<br/>整理成可以開始的做法。
        </h1>
        <p className="body" style={{maxWidth: 620, fontSize: 17}}>
          我在傳統製造業做 AI 落地，橫跨軟體開發與 PM。這裡不是 AI 新聞站，而是一個把現場經驗、工具方法與生活感受慢慢寫清楚的地方。
        </p>
        <div className="flex gap-12 mt-16">
          <span className="btn btn-primary">開始閱讀</span>
          <span className="btn btn-ghost">關於 Jason</span>
        </div>
      </div>

      <div className="mt-80" style={{display:'grid', gridTemplateColumns:'1.6fr 1fr', gap: 32, alignItems:'stretch'}}>
        <div className="starscape" style={{minHeight: 320}} />
        <div className="col gap-24" style={{padding: 32, border:'1px solid var(--border)', borderRadius:12, background:'var(--surface-1)'}}>
          <div className="eyebrow-muted">Now writing</div>
          <div className="h3">下一篇：把 AI 試行專案<br/>變成日常工作流</div>
          <div className="body-sm" style={{flex:1}}>正在整理一份從 PoC 到日常導入的 6 個關鍵節點。</div>
          <div className="eyebrow-muted">2026 / 04 · IN PROGRESS</div>
        </div>
      </div>
    </section>
  );
}

function HeroC() {
  // Vercel style — bold centered statement, technical eyebrow
  return (
    <section className="container" style={{paddingTop: 120, paddingBottom: 96}}>
      <div className="col gap-32" style={{alignItems:'flex-start'}}>
        <div className="flex gap-8" style={{alignItems:'center'}}>
          <span className="dot" />
          <span className="eyebrow">Field Notes / v3 · 2026</span>
        </div>
        <h1 className="h1" style={{fontSize: 84, maxWidth: 1000, lineHeight: 1.08, fontWeight: 900}}>
          企業裡真的<br/>
          <span style={{color:'var(--accent)'}}>用得上的 AI</span>，<br/>
          可以開始的做法。
        </h1>
        <p className="body" style={{maxWidth: 580, fontSize: 17}}>
          我在傳統製造業做 AI 落地，橫跨軟體開發與 PM。把現場經驗、工具方法與生活感受慢慢寫清楚的地方。
        </p>
        <div className="flex gap-12 mt-16">
          <span className="btn btn-gold">先看製造業 AI →</span>
          <span className="btn btn-ghost">再看 AI 新知</span>
        </div>
      </div>

      <div className="three-col mt-80">
        <GlowCard>
          <div className="eyebrow">MANUFACTURING AI</div>
          <h3 className="h3 mt-16">製造業 AI</h3>
          <p className="body-sm mt-8">落地阻力、流程拆解、協作現場與導入節奏。</p>
          <div className="eyebrow-muted mt-32">12 ARTICLES →</div>
        </GlowCard>
        <GlowCard>
          <div className="eyebrow">AI NOTES</div>
          <h3 className="h3 mt-16">AI 新知</h3>
          <p className="body-sm mt-8">工具評析、Prompt 方法、值得保留的工作流。</p>
          <div className="eyebrow-muted mt-32">18 ARTICLES →</div>
        </GlowCard>
        <GlowCard>
          <div className="eyebrow">HAND DRIP COFFEE</div>
          <h3 className="h3 mt-16">手沖咖啡</h3>
          <p className="body-sm mt-8">沖煮日誌、器材收藏、豆子風味與生活節奏。</p>
          <div className="eyebrow-muted mt-32">7 ARTICLES →</div>
        </GlowCard>
      </div>
    </section>
  );
}

// ────────────────────────────────────────────────────────────
// Article list page — three treatments
// ────────────────────────────────────────────────────────────
function ListA() {
  return (
    <section className="container" style={{paddingTop: 80, paddingBottom: 80}}>
      <div className="flex gap-48" style={{justifyContent:'space-between'}}>
        <div>
          <div className="stat-label">目前已發布</div>
          <div className="stat-num">37</div>
        </div>
        <div>
          <div className="stat-label">主軸內容</div>
          <div className="stat-num">3 個領域</div>
        </div>
        <div>
          <div className="stat-label">最近更新</div>
          <div className="stat-num">04 / 25</div>
        </div>
      </div>

      <div className="three-col mt-64">
        <div className="card">
          <div className="eyebrow">MANUFACTURING AI</div>
          <h3 className="h3 mt-16">製造業 AI</h3>
          <p className="body-sm mt-8">落地阻力、流程拆解、協作現場與導入節奏。</p>
          <div className="eyebrow-muted mt-32">Factory signal system</div>
        </div>
        <div className="card">
          <div className="eyebrow">AI NOTES</div>
          <h3 className="h3 mt-16">AI 新知</h3>
          <p className="body-sm mt-8">工具評析、Prompt 方法、值得保留的工作流。</p>
          <div className="eyebrow-muted mt-32">Prompt signal layer</div>
        </div>
        <div className="card">
          <div className="eyebrow">HAND DRIP COFFEE</div>
          <h3 className="h3 mt-16">手沖咖啡</h3>
          <p className="body-sm mt-8">沖煮日誌、器材收藏、豆子風味與生活節奏。</p>
          <div className="eyebrow-muted mt-32">Coffee motion field</div>
        </div>
      </div>

      <div className="mt-80">
        <div className="eyebrow-muted">START HERE</div>
        <h2 className="h2 mt-16" style={{fontSize: 32}}>先從代表文章開始，不需要先把整個網站翻完。</h2>
        <p className="body mt-16" style={{maxWidth: 620}}>我把最值得先看的內容直接擺在首頁，第一次進來也能快速抓到重點。</p>

        <div className="mt-48">
          {ARTICLES.map((a, i) => (
            <div key={i} className="row">
              <div>
                <div className="cat">{a.cat}</div>
                <div className="row-date">{a.date}</div>
              </div>
              <div>
                <h3 className="row-title">{a.title}</h3>
                <p className="body-sm" style={{margin:0}}>{a.excerpt}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function ListB() {
  // Linear style — table-like, ultra calm
  return (
    <section className="container" style={{paddingTop: 80, paddingBottom: 80}}>
      <div className="col gap-16">
        <div className="eyebrow-muted">All entries</div>
        <h2 className="h2" style={{fontSize: 36}}>Field notes archive</h2>
        <p className="body" style={{maxWidth: 600}}>依時間排序的全部文章，每篇都標註領域與更新日期。</p>
      </div>

      <div className="mt-48">
        {ARTICLES.map((a, i) => (
          <div key={i} className="row" style={{gridTemplateColumns:'140px 1fr 100px', alignItems:'baseline'}}>
            <div className="cat">{a.cat}</div>
            <div>
              <div className="row-title" style={{fontWeight:500}}>{a.title}</div>
              <div className="body-sm" style={{margin:'6px 0 0', color:'var(--text-faint)'}}>{a.excerpt}</div>
            </div>
            <div className="row-date" style={{textAlign:'right', margin:0}}>{a.date.replace('年','/').replace('月','/').replace('日','')}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

function ListC() {
  // Vercel — featured + grid mix
  const [feat, ...rest] = ARTICLES;
  return (
    <section className="container" style={{paddingTop: 80, paddingBottom: 80}}>
      <div className="col gap-16">
        <div className="eyebrow">LATEST · 04 / 2026</div>
        <h2 className="h2" style={{fontSize: 36}}>最近寫了什麼</h2>
      </div>

      <GlowCard className="mt-48" style={{padding: 48}}>
        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap: 48, alignItems:'center'}}>
          <div className="thumb" style={{aspectRatio:'4/3'}} />
          <div className="col gap-16">
            <div className="eyebrow">{feat.cat} · FEATURED</div>
            <h3 className="h2">{feat.title}</h3>
            <p className="body">{feat.excerpt}</p>
            <div className="eyebrow-muted mt-8">{feat.date}  ·  繼續閱讀 →</div>
          </div>
        </div>
      </GlowCard>

      <div className="three-col mt-32">
        {rest.slice(0,3).map((a,i) => (
          <GlowCard key={i}>
            <div className="thumb" style={{marginBottom: 20}} />
            <div className="eyebrow">{a.cat}</div>
            <h3 className="h3 mt-16">{a.title}</h3>
            <p className="body-sm mt-8">{a.excerpt}</p>
            <div className="eyebrow-muted mt-24">{a.date}</div>
          </GlowCard>
        ))}
      </div>

      <div className="mt-32">
        {rest.slice(3).map((a,i) => (
          <div key={i} className="row">
            <div>
              <div className="cat">{a.cat}</div>
              <div className="row-date">{a.date}</div>
            </div>
            <div>
              <h3 className="row-title">{a.title}</h3>
              <p className="body-sm" style={{margin:0}}>{a.excerpt}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

// ────────────────────────────────────────────────────────────
// Article reading page — three treatments
// ────────────────────────────────────────────────────────────
const ARTICLE_BODY = (
  <>
    <p>很多人問我「製造業導入 AI 最大的卡點是什麼」，以前我會回答模型、資料、或工具選型，但實際做了幾個專案以後，我發現真正的瓶頸通常不在技術層。</p>
    <p>第一個會卡住的是<strong>注意力</strong>。一線同事的工作其實已經滿了，當你帶著一個新的 AI 工具進現場，他們需要先騰出一段認真學習的時間，這件事比想像中難。</p>
    <h2>注意力不是訓練時數，是「能不能放下手上的事」</h2>
    <p>很多公司會說「我們有安排教育訓練」，但教育訓練排在工作時間裡，同事多半是邊上課邊回 LINE、邊處理單據。真正能讓注意力進來的，是把 AI 工具直接接進他們現有的流程裡——讓他們在做平常的事情時，順手就用了。</p>
    <blockquote>不要讓人「特地去用 AI」，要讓 AI 在他們本來就要做的事裡出現。</blockquote>
    <p>這個原則改變了我設計專案的方式。我現在會先花時間把現場流程拆乾淨，找出哪一段最痛、最重複、最容易被打斷，然後才回頭討論模型、Prompt 或介面。技術問題其實比想像中好解，難的是把這個「進入點」找對。</p>
    <h2>第二個卡點：誰來判斷「夠好了」</h2>
    <p>AI 的輸出多半是機率性的，你不能要求它每次都 100% 對。所以更重要的是：團隊內部能不能定義一個「在什麼樣的錯誤率下我們就上線」的標準，並且讓使用者也接受這個標準。</p>
  </>
);

function ArticleA() {
  return (
    <article className="container-tight" style={{paddingTop: 96, paddingBottom: 96}}>
      <div className="eyebrow">MANUFACTURING AI · 2026 / 04 / 25</div>
      <h1 className="h1 mt-24" style={{fontSize: 44, lineHeight: 1.25}}>
        在傳統製造業導入 AI，<br/>最先卡住的不是模型
      </h1>
      <p className="body mt-24" style={{fontSize: 17}}>
        三年現場觀察整理：為什麼大多數 AI 試行專案推不動，問題其實不在技術選型。
      </p>
      <div className="thumb mt-48" style={{aspectRatio:'21/9'}} />
      <div className="prose mt-48">{ARTICLE_BODY}</div>
    </article>
  );
}

function ArticleB() {
  return (
    <article className="container" style={{paddingTop: 96, paddingBottom: 96}}>
      <div style={{display:'grid', gridTemplateColumns:'180px 1fr', gap: 64}}>
        <aside className="col gap-16" style={{position:'sticky', top: 32, alignSelf:'start'}}>
          <div className="eyebrow-muted">CATEGORY</div>
          <div className="body-sm" style={{color:'var(--text)'}}>Manufacturing AI</div>
          <div className="eyebrow-muted mt-16">PUBLISHED</div>
          <div className="body-sm" style={{color:'var(--text)'}}>2026 / 04 / 25</div>
          <div className="eyebrow-muted mt-16">READ</div>
          <div className="body-sm" style={{color:'var(--text)'}}>8 min</div>
          <div className="eyebrow-muted mt-16">TAGS</div>
          <div className="body-sm" style={{color:'var(--text-muted)'}}>專案管理 · 現場 · PoC</div>
        </aside>
        <div style={{maxWidth: 640}}>
          <h1 className="h1" style={{fontSize: 48, lineHeight: 1.18}}>
            在傳統製造業導入 AI，最先卡住的不是模型
          </h1>
          <p className="body mt-24" style={{fontSize: 17, color:'var(--text)'}}>
            三年現場觀察：為什麼大多數 AI 試行專案推不動，問題其實不在技術選型。
          </p>
          <div className="prose mt-48">{ARTICLE_BODY}</div>
        </div>
      </div>
    </article>
  );
}

function ArticleC() {
  return (
    <article className="container" style={{paddingTop: 96, paddingBottom: 96}}>
      <div className="container-tight" style={{padding: 0}}>
        <div className="flex gap-8" style={{alignItems:'center'}}>
          <span className="dot" />
          <span className="eyebrow">MANUFACTURING AI</span>
          <span className="eyebrow-muted" style={{marginLeft:8}}>· 2026 / 04 / 25 · 8 MIN</span>
        </div>
        <h1 className="h1 mt-24" style={{fontSize: 56, lineHeight: 1.15}}>
          在傳統製造業導入 AI，<br/>最先卡住的<span style={{color:'var(--accent)'}}>不是模型</span>
        </h1>
        <p className="body mt-24" style={{fontSize: 18}}>
          三年現場觀察整理：為什麼大多數 AI 試行專案推不動，問題其實不在技術選型。
        </p>
      </div>
      <div className="container-tight" style={{padding: 0, marginTop: 56}}>
        <GlowCard style={{padding: 0, overflow:'hidden'}}>
          <div className="thumb" style={{aspectRatio:'21/9', borderRadius: 0, border: 0}} />
        </GlowCard>
        <div className="prose mt-48">{ARTICLE_BODY}</div>
      </div>
    </article>
  );
}

// ────────────────────────────────────────────────────────────
// Footer
// ────────────────────────────────────────────────────────────
function Footer() {
  return (
    <div className="container">
      <div className="footer">
        <div>© 2026 Jason Lin · siyulio.com</div>
        <div className="footer-links">
          <span className="nav-link">Home</span>
          <span className="nav-link">製造業 AI</span>
          <span className="nav-link">AI 新知</span>
          <span className="nav-link">手沖咖啡</span>
          <span className="nav-link">RSS</span>
        </div>
      </div>
    </div>
  );
}

// ────────────────────────────────────────────────────────────
// Direction wrappers — render a complete mini-site per direction
// ────────────────────────────────────────────────────────────
function DirectionA({ tweaks }) {
  return (
    <div className="dir-a page" style={dirVarStyle('a', tweaks)}>
      <NavbarA />
      <HeroA />
      <hr className="hr-faint" />
      <ListA />
      <hr className="hr-faint" />
      <ArticleA />
      <Footer />
    </div>
  );
}
function DirectionB({ tweaks }) {
  return (
    <div className="dir-b page" style={dirVarStyle('b', tweaks)}>
      <NavbarB />
      <HeroB />
      <ListB />
      <hr className="hr-faint" />
      <ArticleB />
      <Footer />
    </div>
  );
}
function DirectionC({ tweaks }) {
  return (
    <div className="dir-c page" style={dirVarStyle('c', tweaks)}>
      <NavbarC />
      <HeroC />
      <hr className="hr-faint" />
      <ListC />
      <hr className="hr-faint" />
      <ArticleC />
      <Footer />
    </div>
  );
}

// Map tweaks (background depth, border strength, accent intensity) onto CSS vars
function dirVarStyle(_dir, t) {
  if (!t) return {};
  const out = {};
  if (t.bgDepth != null) {
    // 0 = pure black, 100 = #1a1a1a-ish
    const v = Math.round(t.bgDepth * 0.16);
    out['--bg'] = `rgb(${v},${v},${v})`;
    out['--surface-1'] = `rgb(${v+10},${v+10},${v+10})`;
    out['--surface-2'] = `rgb(${v+18},${v+18},${v+18})`;
  }
  if (t.borderStrength != null) {
    out['--border'] = `rgba(255,255,255,${t.borderStrength / 1000})`;
    out['--border-strong'] = `rgba(255,255,255,${(t.borderStrength * 2) / 1000})`;
  }
  if (t.accentHue != null) {
    // hue in deg. base ~45 = gold; user can shift toward amber/copper/rose
    out['--accent'] = `oklch(0.82 0.13 ${t.accentHue})`;
  }
  return out;
}

Object.assign(window, {
  DirectionA, DirectionB, DirectionC,
});
