// subpages.jsx — four sub-pages for siyulio.com final design
// Each sub-page reuses the .final design tokens but has its OWN layout
// language matching its content nature.

const MFG_ARTICLES = [
  { num:"01", title:"在傳統製造業導入 AI，最先卡住的不是模型", date:"2026/04/25", read:"8 min", series:"AI 落地系列" },
  { num:"02", title:"當主管、使用者、推動者想的都不一樣時，AI 專案怎麼推", date:"2026/04/05", read:"6 min", series:"AI 落地系列" },
  { num:"03", title:"PoC 之後最容易消失的環節：誰來接著用", date:"2026/03/22", read:"5 min", series:"AI 落地系列" },
  { num:"04", title:"從 SOP 反推 AI 切入點的三個問題", date:"2026/03/10", read:"7 min", series:"工具方法" },
  { num:"05", title:"當資料還沒準備好，能先做什麼", date:"2026/02/28", read:"4 min", series:"工具方法" },
  { num:"06", title:"小公司導入 AI，三個我已經放棄的執念", date:"2026/02/14", read:"6 min", series:"反思" },
];

const AI_ARTICLES = [
  { cat:"工具評析", title:"我目前最常用的 AI 工具組合", date:"2026/04/22", excerpt:"對我來說，AI 工具不是越多越好，而是要能真的接進工作與筆記流程裡。" },
  { cat:"Prompt", title:"如何建立自己的常用指令庫", date:"2026/04/14", excerpt:"我在工作中最常遇到的問題，不是沒有 AI 工具可用，而是每次都要重新想一次怎麼下指令。" },
  { cat:"知識管理", title:"我怎麼用 Obsidian 管理工作中的 AI 知識", date:"2026/04/10", excerpt:"如果不刻意整理，很多有價值的內容都會散在聊天視窗、文件草稿、臨時截圖裡。" },
  { cat:"Prompt", title:"我會留下哪些 Prompt，刪掉哪些 Prompt", date:"2026/04/02", excerpt:"如果什麼都存，最後只會得到一個越來越難找、也越來越不想打開的 Prompt 倉庫。" },
  { cat:"工作流", title:"用 Claude 整理會議記錄的三層流程", date:"2026/03/28", read:"5 min" },
  { cat:"工具評析", title:"換了三套向量資料庫之後我學到什麼", date:"2026/03/15", read:"7 min" },
];

const COFFEE_ENTRIES = [
  { date:"2026/04/24", bean:"衣索比亞 Yirgacheffe G1", note:"花香明顯，後段帶蜜糖甜，今天偏酸了一點，下次水溫降 2 度試試。" },
  { date:"2026/04/22", bean:"哥倫比亞 Pink Bourbon", note:"果汁感很強，像草莓糖。注水節奏要慢，不然會悶。" },
  { date:"2026/04/19", bean:"肯亞 AA Top", note:"番茄酸跟黑醋栗，口感厚實。粉量加到 16g 比較舒服。" },
  { date:"2026/04/15", bean:"巴拿馬 Geisha", note:"留到週末喝。橙花、白桃，餘韻很長。這支不要急。" },
];

const TIMELINE = [
  { year:"2025–", role:"AI 落地與專案推動", org:"傳統製造業", desc:"從零開始建立 AI 工作流，跨業務、IT、現場三方溝通。同時持續寫作與整理方法。" },
  { year:"2022–2025", role:"產品經理 / 全端工程師", org:"B2B SaaS", desc:"從寫程式跨到 PM，學會把工程細節翻譯成商業語言。" },
  { year:"2019–2022", role:"後端工程師", org:"新創團隊", desc:"從 0 到 1 的產品搭建經驗，熟 Node / Python / 雲端架構。" },
  { year:"2015–2019", role:"資訊工程相關科系", org:"國立大學", desc:"在校期間做了三個獨立專案，那時候開始發現自己喜歡寫東西。" },
];

// Shared sub-page nav with active state
function SubNav({ active }) {
  const items = [
    { key:"mfg", label:"製造業 AI", href:"siyulio-mfg.html" },
    { key:"ai", label:"AI 新知", href:"siyulio-ai-notes.html" },
    { key:"coffee", label:"手沖咖啡", href:"siyulio-coffee.html" },
    { key:"about", label:"個人經歷", href:"siyulio-about.html" },
  ];
  return (
    <div className="container">
      <nav className="nav">
        <a href="siyulio-final.html" style={{textDecoration:'none', color:'inherit'}}>
          <div className="logo">
            <div className="logo-mark">JL</div>
            <div className="logo-text">
              <div className="logo-name">siyulio</div>
              <div className="logo-sub">AI field notes by Jason Lin</div>
            </div>
          </div>
        </a>
        <div className="nav-links">
          {items.map((it) => (
            <a key={it.key} href={it.href}
               className={`nav-link ${active === it.key ? 'active' : ''}`}
               style={{textDecoration:'none', color: active === it.key ? 'var(--accent)' : 'var(--text-muted)'}}>
              {it.label}
            </a>
          ))}
        </div>
        <span className="nav-cta">Curated Signal Map →</span>
      </nav>
    </div>
  );
}

function SubFooter() {
  return (
    <div className="container">
      <div className="footer">
        <div>© 2026 Jason Lin · siyulio.com</div>
        <div className="footer-links">
          <a className="nav-link" href="siyulio-final.html" style={{textDecoration:'none'}}>Home</a>
          <a className="nav-link" href="siyulio-mfg.html" style={{textDecoration:'none'}}>製造業 AI</a>
          <a className="nav-link" href="siyulio-ai-notes.html" style={{textDecoration:'none'}}>AI 新知</a>
          <a className="nav-link" href="siyulio-coffee.html" style={{textDecoration:'none'}}>手沖咖啡</a>
          <span className="nav-link">RSS</span>
        </div>
      </div>
    </div>
  );
}

function GlowCardSub({ children, className = "", style }) {
  const ref = React.useRef(null);
  const onMove = (e) => {
    const el = ref.current; if (!el) return;
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    el.style.setProperty('--my', (e.clientY - r.top) + 'px');
  };
  return (
    <div ref={ref} className={`card ${className}`} style={style} onMouseMove={onMove}>{children}</div>
  );
}

// ─── 1. 製造業 AI — 結構索引式（系列 + 編號） ────────────────────
function MfgPage() {
  const series = {};
  MFG_ARTICLES.forEach(a => { (series[a.series] = series[a.series] || []).push(a); });

  return (
    <>
      <SubNav active="mfg" />
      <section className="container" style={{paddingTop: 96, paddingBottom: 64}}>
        <div className="col gap-24" style={{maxWidth: 760}}>
          <div style={{display:'flex', alignItems:'center', gap:12, color:'var(--text-faint)', fontSize:14, fontWeight:300}}>
            <span style={{width:24, height:1, background:'var(--accent)', display:'inline-block'}}></span>
            <span>Manufacturing AI · 現場筆記</span>
          </div>
          <h1 className="h1" style={{fontSize: 56, lineHeight: 1.18, fontWeight: 800}}>
            企業裡推動 <span style={{color:'var(--accent)'}}>AI</span> 的<br/>現場筆記
          </h1>
          <p className="body" style={{fontSize: 17}}>
            聚焦製造現場真正會卡住的流程、阻力與推進方式，讓 AI 不只停在簡報上。這裡的內容多半是系列性的，建議從第一篇開始讀。
          </p>
        </div>

        {/* stats strip */}
        <div style={{display:'flex', gap: 64, marginTop: 56, paddingTop: 32, borderTop:'1px solid var(--border)'}}>
          <div>
            <div className="stat-num" style={{fontSize:36}}>12</div>
            <div className="stat-label" style={{marginTop:8}}>已發表文章</div>
          </div>
          <div>
            <div className="stat-num" style={{fontSize:36}}>3</div>
            <div className="stat-label" style={{marginTop:8}}>系列主題</div>
          </div>
          <div>
            <div className="stat-num" style={{fontSize:36}}>04 / 25</div>
            <div className="stat-label" style={{marginTop:8}}>最近更新</div>
          </div>
        </div>
      </section>

      {/* Series — grouped indexes */}
      {Object.entries(series).map(([seriesName, items], si) => (
        <section key={si} className="container" style={{paddingTop: 56, paddingBottom: 24}}>
          <div style={{display:'grid', gridTemplateColumns:'220px 1fr', gap: 56}}>
            <div style={{position:'sticky', top: 32, alignSelf:'start'}}>
              <div className="eyebrow">SERIES · 0{si+1}</div>
              <h2 className="h2 mt-16" style={{fontSize:24}}>{seriesName}</h2>
              <p className="body-sm mt-16" style={{margin:0}}>{items.length} 篇 · 由淺入深</p>
            </div>
            <div>
              {items.map((a, i) => (
                <GlowCardSub key={i} style={{padding:'24px 28px', marginBottom: 12, display:'grid', gridTemplateColumns:'auto 1fr auto', gap:24, alignItems:'center'}}>
                  <div style={{fontFamily:'var(--font-mono)', fontSize:24, color:'var(--accent)', fontWeight:500}}>{a.num}</div>
                  <div>
                    <div style={{fontWeight:600, fontSize:17, color:'var(--text)', lineHeight:1.45}}>{a.title}</div>
                    <div style={{fontFamily:'var(--font-mono)', fontSize:11, color:'var(--text-faint)', marginTop:6, letterSpacing:'0.08em'}}>{a.date} · {a.read}</div>
                  </div>
                  <span style={{color:'var(--text-faint)', fontSize:14}}>→</span>
                </GlowCardSub>
              ))}
            </div>
          </div>
        </section>
      ))}

      <div style={{paddingBottom: 96}}>
        <SubFooter />
      </div>
    </>
  );
}

// ─── 2. AI 新知 — 時間流 + 標籤雲 ──────────────────────────────
function AiNotesPage() {
  const tags = ["工具評析", "Prompt", "知識管理", "工作流", "Claude", "Obsidian"];
  const [active, setActive] = React.useState("全部");

  return (
    <>
      <SubNav active="ai" />
      <section className="container" style={{paddingTop: 96, paddingBottom: 48}}>
        <div className="col gap-24" style={{maxWidth: 760}}>
          <div style={{display:'flex', alignItems:'center', gap:12, color:'var(--text-faint)', fontSize:14, fontWeight:300}}>
            <span style={{width:24, height:1, background:'var(--accent)', display:'inline-block'}}></span>
            <span>AI Notes · 我自己每週在用的</span>
          </div>
          <h1 className="h1" style={{fontSize: 56, lineHeight: 1.18, fontWeight: 800}}>
            工具流、<span style={{color:'var(--accent)'}}>Prompt</span>，<br/>跟我留下來的工作方式
          </h1>
          <p className="body" style={{fontSize: 17}}>
            這裡的內容更新得最頻繁，多半是我自己這週在用、覺得值得留下來的工具或方法。不會評每一個熱門工具，只寫真的接進工作流的。
          </p>
        </div>

        {/* Tag filter */}
        <div style={{display:'flex', gap:8, flexWrap:'wrap', marginTop: 48}}>
          {["全部", ...tags].map((t) => (
            <span key={t} onClick={() => setActive(t)}
              style={{
                padding:'7px 14px', borderRadius:999,
                border:`1px solid ${active===t ? 'var(--accent)' : 'var(--border)'}`,
                color: active===t ? 'var(--accent)' : 'var(--text-muted)',
                background: active===t ? 'var(--accent-soft)' : 'transparent',
                fontSize:13, cursor:'default', transition:'all .18s'
              }}>{t}</span>
          ))}
        </div>
      </section>

      {/* Featured — most recent */}
      <section className="container" style={{paddingBottom: 32}}>
        <GlowCardSub style={{padding: 48, display:'grid', gridTemplateColumns:'1fr 1fr', gap:48, alignItems:'center'}}>
          <div className="thumb" style={{aspectRatio:'4/3', margin:0}} />
          <div className="col gap-16">
            <div className="eyebrow">{AI_ARTICLES[0].cat} · LATEST</div>
            <h2 className="h2" style={{fontSize:30}}>{AI_ARTICLES[0].title}</h2>
            <p className="body">{AI_ARTICLES[0].excerpt}</p>
            <div style={{fontFamily:'var(--font-mono)', fontSize:11, color:'var(--text-faint)', marginTop:8, letterSpacing:'0.08em'}}>
              {AI_ARTICLES[0].date} · 繼續閱讀 →
            </div>
          </div>
        </GlowCardSub>
      </section>

      {/* Two-column flow */}
      <section className="container" style={{paddingBottom: 96}}>
        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap: 24}}>
          {AI_ARTICLES.slice(1).map((a, i) => (
            <GlowCardSub key={i} style={{padding: 32}}>
              <div className="eyebrow">{a.cat}</div>
              <h3 className="h3 mt-16" style={{fontSize: 19, lineHeight: 1.45}}>{a.title}</h3>
              {a.excerpt && <p className="body-sm mt-12" style={{margin:0}}>{a.excerpt}</p>}
              <div style={{fontFamily:'var(--font-mono)', fontSize:11, color:'var(--text-faint)', marginTop:24, letterSpacing:'0.08em'}}>
                {a.date}{a.read ? ` · ${a.read}` : ''}
              </div>
            </GlowCardSub>
          ))}
        </div>
      </section>

      <SubFooter />
    </>
  );
}

// ─── 3. 手沖咖啡 — 雜誌 / 日誌風 ──────────────────────────────
function CoffeePage() {
  return (
    <>
      <SubNav active="coffee" />
      <section className="container" style={{paddingTop: 96, paddingBottom: 64}}>
        <div className="col gap-24" style={{maxWidth: 760}}>
          <div style={{display:'flex', alignItems:'center', gap:12, color:'var(--text-faint)', fontSize:14, fontWeight:300}}>
            <span style={{width:24, height:1, background:'var(--accent)', display:'inline-block'}}></span>
            <span>Hand Drip Coffee · 慢慢沖、慢慢寫</span>
          </div>
          <h1 className="h1" style={{fontSize: 56, lineHeight: 1.18, fontWeight: 800}}>
            泡咖啡，<br/>是我把<span style={{color:'var(--accent)'}}>節奏慢下來</span>的方式
          </h1>
          <p className="body" style={{fontSize: 17}}>
            原本以為它只是工作之外的休閒，後來才發現：泡咖啡逼我每天有 15 分鐘什麼都不想，只看水流。這個區塊偏個人，不會教學，主要是沖煮日誌跟器材想法。
          </p>
        </div>
      </section>

      {/* Brewing journal — calendar-like cards */}
      <section className="container" style={{paddingBottom: 56}}>
        <div className="eyebrow-muted" style={{marginBottom: 24}}>BREWING JOURNAL · 最近的沖煮紀錄</div>
        <div style={{display:'grid', gridTemplateColumns:'repeat(2, 1fr)', gap: 20}}>
          {COFFEE_ENTRIES.map((e, i) => (
            <GlowCardSub key={i} style={{padding: 32}}>
              <div style={{display:'flex', justifyContent:'space-between', alignItems:'baseline', marginBottom: 16}}>
                <div style={{fontFamily:'var(--font-mono)', fontSize:12, color:'var(--accent)', letterSpacing:'0.1em'}}>{e.date}</div>
                <div style={{display:'flex', gap:6}}>
                  {[1,2,3,4,5].map(n => (
                    <span key={n} style={{width:6, height:6, borderRadius:'50%', background: n <= 4 ? 'var(--accent)' : 'var(--border-strong)'}}></span>
                  ))}
                </div>
              </div>
              <div style={{fontWeight:700, fontSize:18, color:'var(--text)', marginBottom:12}}>{e.bean}</div>
              <p className="body-sm" style={{margin:0}}>{e.note}</p>
            </GlowCardSub>
          ))}
        </div>
      </section>

      {/* Gear / philosophy section */}
      <section className="container" style={{paddingTop: 32, paddingBottom: 96}}>
        <div style={{display:'grid', gridTemplateColumns:'1fr 1.2fr', gap: 56, alignItems:'center', paddingTop: 48, borderTop:'1px solid var(--border)'}}>
          <div className="thumb" style={{aspectRatio:'4/5', margin:0}} />
          <div className="col gap-16">
            <div className="eyebrow">CURRENT SETUP · 我目前在用的</div>
            <h2 className="h2" style={{fontSize: 28}}>器材其實沒那麼重要，但記得寫下來。</h2>
            <p className="body">手沖咖啡很容易掉進「換器材」的坑。我自己的經驗是，先把參數寫清楚，多半就能解決一半的問題。</p>
            <div style={{display:'grid', gridTemplateColumns:'90px 1fr', rowGap:14, columnGap:24, marginTop:16, fontSize:14}}>
              <div style={{color:'var(--text-faint)', fontFamily:'var(--font-mono)', fontSize:11, letterSpacing:'0.1em', paddingTop:2}}>DRIPPER</div>
              <div style={{color:'var(--text)'}}>Origami M · 楓葉摺紙</div>
              <div style={{color:'var(--text-faint)', fontFamily:'var(--font-mono)', fontSize:11, letterSpacing:'0.1em', paddingTop:2}}>GRINDER</div>
              <div style={{color:'var(--text)'}}>1Zpresso K-Plus</div>
              <div style={{color:'var(--text-faint)', fontFamily:'var(--font-mono)', fontSize:11, letterSpacing:'0.1em', paddingTop:2}}>KETTLE</div>
              <div style={{color:'var(--text)'}}>Brewista Artisan</div>
              <div style={{color:'var(--text-faint)', fontFamily:'var(--font-mono)', fontSize:11, letterSpacing:'0.1em', paddingTop:2}}>RECIPE</div>
              <div style={{color:'var(--text)'}}>15g 粉 / 240g 水 / 92°C / 三段注水</div>
            </div>
          </div>
        </div>
      </section>

      <SubFooter />
    </>
  );
}

// ─── 4. 個人經歷 — 時間軸 + 自介 ──────────────────────────────
function AboutPage() {
  return (
    <>
      <SubNav active="about" />
      <section className="container" style={{paddingTop: 96, paddingBottom: 48}}>
        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap: 80, alignItems:'flex-start'}}>
          <div className="col gap-24">
            <div style={{display:'flex', alignItems:'center', gap:12, color:'var(--text-faint)', fontSize:14, fontWeight:300}}>
              <span style={{width:24, height:1, background:'var(--accent)', display:'inline-block'}}></span>
              <span>About · Jason Lin</span>
            </div>
            <h1 className="h1" style={{fontSize: 52, lineHeight: 1.2, fontWeight: 800}}>
              寫程式、做產品、<br/>跨進<span style={{color:'var(--accent)'}}>製造業 AI</span>。
            </h1>
            <p className="body" style={{fontSize: 17}}>
              我是 Jason，從工程師出身，後來轉到產品經理，現在主要做的是把 AI 真正接進企業的日常工作。寫這個網站，是因為我發現很多有用的觀察，如果不寫下來就會慢慢消失。
            </p>
            <div className="flex gap-12 mt-16">
              <a href="mailto:hello@siyulio.com" className="btn btn-primary" style={{textDecoration:'none'}}>聯絡我</a>
              <span className="btn btn-ghost">下載完整履歷</span>
            </div>
          </div>

          {/* Quick facts side card */}
          <GlowCardSub style={{padding: 40}}>
            <div className="eyebrow">QUICK FACTS</div>
            <div style={{display:'grid', gridTemplateColumns:'100px 1fr', rowGap: 18, columnGap: 24, marginTop: 24, fontSize: 14}}>
              <div style={{color:'var(--text-faint)', fontFamily:'var(--font-mono)', fontSize:11, letterSpacing:'0.1em', paddingTop:3}}>BASE</div>
              <div style={{color:'var(--text)'}}>台灣，但常跑製造現場</div>
              <div style={{color:'var(--text-faint)', fontFamily:'var(--font-mono)', fontSize:11, letterSpacing:'0.1em', paddingTop:3}}>FOCUS</div>
              <div style={{color:'var(--text)'}}>AI 落地、PM、跨團隊推動</div>
              <div style={{color:'var(--text-faint)', fontFamily:'var(--font-mono)', fontSize:11, letterSpacing:'0.1em', paddingTop:3}}>STACK</div>
              <div style={{color:'var(--text)'}}>Node · Python · Claude · Obsidian</div>
              <div style={{color:'var(--text-faint)', fontFamily:'var(--font-mono)', fontSize:11, letterSpacing:'0.1em', paddingTop:3}}>WRITING</div>
              <div style={{color:'var(--text)'}}>每週一到兩篇，週日整理</div>
              <div style={{color:'var(--text-faint)', fontFamily:'var(--font-mono)', fontSize:11, letterSpacing:'0.1em', paddingTop:3}}>OFFLINE</div>
              <div style={{color:'var(--text)'}}>手沖咖啡、慢跑、看書</div>
            </div>
          </GlowCardSub>
        </div>
      </section>

      {/* Timeline */}
      <section className="container" style={{paddingTop: 64, paddingBottom: 64}}>
        <div className="eyebrow-muted" style={{marginBottom: 32}}>EXPERIENCE · 經歷時間軸</div>
        <div style={{position:'relative'}}>
          {/* vertical line */}
          <div style={{position:'absolute', left: 100, top: 12, bottom: 12, width: 1, background:'var(--border)'}}></div>
          {TIMELINE.map((t, i) => (
            <div key={i} style={{display:'grid', gridTemplateColumns:'100px 1fr', gap: 48, padding:'28px 0', alignItems:'flex-start', position:'relative'}}>
              <div style={{fontFamily:'var(--font-mono)', fontSize:13, color:'var(--accent)', letterSpacing:'0.06em', paddingTop:4}}>{t.year}</div>
              {/* dot on the line */}
              <div style={{position:'absolute', left: 96, top: 32, width:9, height:9, borderRadius:'50%', background:'var(--accent)', border:'2px solid var(--bg)', boxShadow:'0 0 0 1px var(--accent)'}}></div>
              <div style={{paddingLeft: 32}}>
                <div style={{fontWeight:700, fontSize:19, color:'var(--text)'}}>{t.role}</div>
                <div style={{fontSize:14, color:'var(--text-muted)', marginTop:4}}>{t.org}</div>
                <p className="body-sm mt-12" style={{margin:0, maxWidth: 580}}>{t.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Writing principles */}
      <section className="container" style={{paddingTop: 32, paddingBottom: 96}}>
        <div style={{paddingTop: 48, borderTop:'1px solid var(--border)'}}>
          <div className="eyebrow-muted" style={{marginBottom: 24}}>WRITING PRINCIPLES · 我寫東西的三個原則</div>
          <div style={{display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap: 24}}>
            {[
              { num:"01", title:"寫真的做過的", desc:"我盡量不寫沒做過的事。如果是觀察別人的，會註明。" },
              { num:"02", title:"先寫下來再修", desc:"不追新聞、不搶熱度，但堅持每週都寫，再慢慢修。" },
              { num:"03", title:"一篇一個重點", desc:"如果一篇有兩個想法，那我就拆成兩篇。讀者時間很貴。" },
            ].map((p, i) => (
              <GlowCardSub key={i} style={{padding: 32}}>
                <div style={{fontFamily:'var(--font-mono)', fontSize:24, color:'var(--accent)', fontWeight:500}}>{p.num}</div>
                <h3 className="h3 mt-16" style={{fontSize:19}}>{p.title}</h3>
                <p className="body-sm mt-8" style={{margin:0}}>{p.desc}</p>
              </GlowCardSub>
            ))}
          </div>
        </div>
      </section>

      <SubFooter />
    </>
  );
}

Object.assign(window, { MfgPage, AiNotesPage, CoffeePage, AboutPage });
