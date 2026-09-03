from pathlib import Path
import re
import subprocess

path = Path('index.html')
s = path.read_text(encoding='utf-8')


def rep(old, new, expected=1):
    global s
    count = s.count(old)
    if count != expected:
        raise SystemExit(f'Expected {expected} occurrence(s), found {count}: {old[:120]!r}')
    s = s.replace(old, new, expected)

# Result modal: keep trophy/share actions and put leaderboard submission directly beside them.
rep(
'''                <div class="run-badges" id="runBadges" aria-label="Unlocked run badges"></div>
                <div class="screen-actions">''',
'''                <div class="run-badges" id="runBadges" aria-label="Unlocked run badges"></div>
                <div class="result-claim" id="resultClaim">
                  <div class="result-claim-head"><b id="resultClaimTitle">CLAIM THIS RUN</b><span id="resultClaimHint">Save it to the global wall. Sharing stays available.</span></div>
                  <div class="result-claim-form">
                    <input class="rank-input" id="resultName" maxlength="18" autocomplete="nickname" placeholder="YOUR SIGNATURE" aria-label="Signature" />
                    <select class="rank-country" id="resultCountry" aria-label="Country"><option value="">COUNTRY</option></select>
                    <button class="rank-submit" id="resultSubmit" type="button" disabled>ADD TO GLOBAL RANKING</button>
                  </div>
                  <div class="result-status" id="resultStatus" aria-live="polite">Result is being sealed…</div>
                </div>
                <div class="screen-actions">''')

# Styles for the compact claim block in the game-over card.
rep(
'  </style>\n</head>',
'''    .result-claim{margin-top:12px;padding:11px;border:1px solid rgba(37,213,255,.28);background:rgba(37,213,255,.035);text-align:left}
    .result-claim-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:8px}.result-claim-head b{color:var(--cold);font-size:.7rem;letter-spacing:.1em}.result-claim-head span{max-width:260px;color:var(--muted);font-size:.62rem;line-height:1.35;text-align:right}
    .result-claim-form{display:grid;grid-template-columns:minmax(120px,1fr) minmax(116px,.78fr) auto;gap:6px}.result-claim-form .rank-input,.result-claim-form .rank-country{min-width:0;height:38px;padding:0 9px}.result-claim-form .rank-submit{min-height:38px;padding:0 10px;font-size:.66rem;white-space:nowrap}
    .result-status{min-height:18px;margin-top:7px;color:var(--muted);font-size:.62rem;line-height:1.35}.result-status.good{color:var(--acid)}.result-status.error{color:var(--danger)}
    @media(max-width:620px){.result-claim{padding:8px;margin-top:8px}.result-claim-head{display:block}.result-claim-head span{display:block;max-width:none;margin-top:3px;text-align:left}.result-claim-form{grid-template-columns:1fr 1fr}.result-claim-form .rank-submit{grid-column:1/-1;width:100%}}
  </style>
</head>''')

# Better labels for the new UX, in both languages.
rep(
'''      share:"SHARE TROPHY",challengeCopy:"COPY CHALLENGE",retry:"RUN IT BACK →",''',
'''      share:"SHARE RESULT",challengeCopy:"COPY CHALLENGE",retry:"RUN IT BACK →",resultClaim:"CLAIM THIS RUN",resultHint:"Save it to the global wall. Sharing stays available.",resultSealing:"Result is being sealed…",resultAdded:"✓ ADDED TO GLOBAL RANKING",postX:"POST ON X",''')
rep(
'''      share:"ПОДЕЛИТЬСЯ РЕЗУЛЬТАТОМ",challengeCopy:"СКОПИРОВАТЬ ВЫЗОВ",retry:"ЕЩЁ РАЗ →",''',
'''      share:"ПОДЕЛИТЬСЯ РЕЗУЛЬТАТОМ",challengeCopy:"СКОПИРОВАТЬ ВЫЗОВ",retry:"ЕЩЁ РАЗ →",resultClaim:"СОХРАНИТЬ ЭТОТ ЗАБЕГ",resultHint:"Добавь результат в глобальный рейтинг. Возможность поделиться останется.",resultSealing:"Фиксируем результат…",resultAdded:"✓ ДОБАВЛЕНО В РЕЙТИНГ",postX:"ОПУБЛИКОВАТЬ В X",''')

# Populate both country selectors from the same source and keep their values aligned.
pattern = re.compile(r'''  function populateCountries\(\)\{.*?\n  \}\n\n  function supabaseHeaders''', re.S)
match = pattern.search(s)
if not match:
    raise SystemExit('populateCountries block not found')
new_countries = r'''  function populateCountrySelect(select,previous){
    if(!select)return;
    select.innerHTML="";
    const first=document.createElement("option");first.value="";first.textContent=tr("rankCountry");select.appendChild(first);
    let names=null;try{names=new Intl.DisplayNames([currentLang==="ru"?"ru":"en"],{type:"region"})}catch(_){ }
    COUNTRY_CODES.map(code=>({code,name:names?.of(code)||code})).sort((a,b)=>a.name.localeCompare(b.name,currentLang)).forEach(country=>{
      const option=document.createElement("option");option.value=country.code;option.textContent=`${flagEmoji(country.code)} ${country.name}`;select.appendChild(option);
    });
    if(previous)select.value=previous;
  }

  function populateCountries(){
    const previous=$("rankCountry")?.value||$("resultCountry")?.value||localStorage.getItem("leeked-country")||"";
    populateCountrySelect($("rankCountry"),previous);
    populateCountrySelect($("resultCountry"),previous);
  }

  function supabaseHeaders'''
s = s[:match.start()] + new_countries + s[match.end():]

# Helpers: the bottom leaderboard form and result modal are two views of one identity/submission state.
rep(
'''  function renderCareer(){''',
'''  function syncIdentity(source="rank"){
    const fromResult=source==="result",nameSource=fromResult?$("resultName"):$("rankName"),countrySource=fromResult?$("resultCountry"):$("rankCountry");
    const name=(nameSource?.value||"").slice(0,18),country=countrySource?.value||"";
    if($("rankName")&&$("rankName")!==nameSource)$("rankName").value=name;
    if($("resultName")&&$("resultName")!==nameSource)$("resultName").value=name;
    if($("rankCountry")&&$("rankCountry")!==countrySource)$("rankCountry").value=country;
    if($("resultCountry")&&$("resultCountry")!==countrySource)$("resultCountry").value=country;
  }

  function syncResultSubmitUi(){
    const resultButton=$("resultSubmit"),rankButton=$("rankSubmit"),resultStatus=$("resultStatus"),rankStatus=$("rankStatus");
    if(!resultButton)return;
    resultButton.disabled=!!rankButton?.disabled;
    resultButton.textContent=runSubmitted?tr("resultAdded"):tr("rankSubmit");
    if(resultStatus&&rankStatus){
      resultStatus.className="result-status"+(rankStatus.classList.contains("error")?" error":rankStatus.classList.contains("good")?" good":"");
      resultStatus.textContent=rankStatus.textContent||tr("resultSealing");
    }
  }

  function renderCareer(){''')

# Language switch updates the modal as well, without altering share/submission state.
rep(
'''    $("restartBtn").textContent=tr("retry");$("shareBtn").textContent=tr("share");$("challengeBtn").textContent=tr("challengeCopy");''',
'''    $("restartBtn").textContent=tr("retry");$("shareBtn").textContent=tr("share");$("challengeBtn").textContent=tr("challengeCopy");$("xShareBtn").textContent=tr("postX");
    $("resultClaimTitle").textContent=tr("resultClaim");$("resultClaimHint").textContent=tr("resultHint");$("resultName").placeholder=tr("rankName");''')
rep(
'''    applyStaticLanguage(currentLang);
  }''',
'''    applyStaticLanguage(currentLang);syncIdentity("rank");syncResultSubmitUi();
  }''')

# Mirror the verifying state into the modal immediately.
rep(
'''    status.className="rank-status";
    status.textContent=tr("verifying");''',
'''    status.className="rank-status";
    status.textContent=tr("verifying");syncResultSubmitUi();''')

# Once the sealed run exists, both submit entry points become available.
rep(
'''    runProofPending=false;$("rankSubmit").disabled=false;$("shareBtn").disabled=false;$("xShareBtn").disabled=false;
    $("rankStatus").className="rank-status good";$("rankStatus").textContent=tr("runReady")(run);
    renderRanking();''',
'''    runProofPending=false;$("rankSubmit").disabled=false;$("resultSubmit").disabled=false;$("shareBtn").disabled=false;$("xShareBtn").disabled=false;
    $("rankStatus").className="rank-status good";$("rankStatus").textContent=tr("runReady")(run);syncResultSubmitUi();
    renderRanking();''')

# Prepare the claim panel every time the game-over screen appears.
rep(
'''    lastImpactRun=lastCompletedRun;localStorage.setItem("leeked-last-run",JSON.stringify(lastCompletedRun));$("shareBtn").disabled=true;$("xShareBtn").disabled=true;
    const screen=$("gameOverScreen");''',
'''    lastImpactRun=lastCompletedRun;localStorage.setItem("leeked-last-run",JSON.stringify(lastCompletedRun));$("shareBtn").disabled=true;$("xShareBtn").disabled=true;$("resultSubmit").disabled=true;
    syncIdentity("rank");$("resultStatus").className="result-status";$("resultStatus").textContent=tr("resultSealing");
    const screen=$("gameOverScreen");''')

# Use the native share sheet for the dedicated X action on mobile. If unavailable, use the
# twitter.com universal intent rather than x.com so installed X clients have a better chance to intercept it.
pattern = re.compile(r'''  function shareRunOnX\(\)\{.*?\n  \}\n\n  \$\("shareBtn"\)''', re.S)
match = pattern.search(s)
if not match:
    raise SystemExit('shareRunOnX block not found')
new_x = r'''  async function shareRunOnX(){
    if(!lastCompletedRun)return;const run=lastCompletedRun,link=challengeUrl(run);
    const lead=run.boss?(currentLang==="ru"?"Я пережил Admin 64H.":"I survived Admin 64H."):(currentLang==="ru"?`Меня зарага́ли после ${run.kills} убийств.`:`I got rugged after ${run.kills} kills.`);
    const text=currentLang==="ru"?`${lead} ${run.score.toLocaleString()} очков в LEEKed IN. Побей этот результат.`:`${lead} ${run.score.toLocaleString()} score in LEEKed IN. Beat this vegetable.`;
    if(navigator.share){
      try{await navigator.share({title:"LEEKed IN",text,url:link});toast(currentLang==="ru"?"МЕНЮ ПУБЛИКАЦИИ ОТКРЫТО":"SHARE SHEET OPENED");return}
      catch(error){if(error?.name==="AbortError")return}
    }
    const intent=`https://twitter.com/intent/tweet?text=${encodeURIComponent(text+" "+link)}`;
    try{if(isTelegramMiniApp&&tg?.openLink)tg.openLink(intent,{try_instant_view:false});else window.location.href=intent}catch(_){window.open(intent,"_blank","noopener,noreferrer")}
  }

  $("shareBtn")'''
s = s[:match.start()] + new_x + s[match.end():]

# Submit from either location, sync identity in both directions, and keep share actions untouched.
rep(
'''  $("rankSubmit").addEventListener("click",submitVerifiedRun);$("rankCountry").addEventListener("change",event=>{localStorage.setItem("leeked-country",event.target.value);renderRanking()});$("rankName").addEventListener("input",renderRanking);''',
'''  $("rankSubmit").addEventListener("click",async()=>{syncIdentity("rank");await submitVerifiedRun();syncResultSubmitUi()});
  $("resultSubmit").addEventListener("click",async()=>{syncIdentity("result");await submitVerifiedRun();syncResultSubmitUi()});
  $("rankCountry").addEventListener("change",event=>{localStorage.setItem("leeked-country",event.target.value);syncIdentity("rank");renderRanking()});
  $("resultCountry").addEventListener("change",event=>{localStorage.setItem("leeked-country",event.target.value);syncIdentity("result");renderRanking()});
  $("rankName").addEventListener("input",()=>{syncIdentity("rank");renderRanking()});
  $("resultName").addEventListener("input",()=>{syncIdentity("result");renderRanking()});''')

# Final submit state mirrors back into the modal after every DB attempt.
rep(
'''      if(runSubmitted)button.disabled=true;
    }
  }
''',
'''      if(runSubmitted)button.disabled=true;syncResultSubmitUi();
    }
  }
''', expected=1)

# Init the second identity view from the existing saved identity.
rep(
'''    setupTelegram();populateCountries();resetGame();setLanguage(currentLang);loadSupply();refreshGlobalData();requestAnimationFrame(frame);''',
'''    setupTelegram();populateCountries();resetGame();setLanguage(currentLang);syncIdentity("rank");syncResultSubmitUi();loadSupply();refreshGlobalData();requestAnimationFrame(frame);''')

path.write_text(s, encoding='utf-8')

# Syntax-check the inline JS after all replacements.
html = s
scripts = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', html, flags=re.S|re.I)
inline = '\n'.join(x for x in scripts if x.strip() and 'telegram.org/js/' not in x)
Path('/tmp/gramleek-inline.js').write_text(inline, encoding='utf-8')
subprocess.run(['node', '--check', '/tmp/gramleek-inline.js'], check=True)

# Sanity checks for the new flow.
for needle in ['id="resultSubmit"','function syncResultSubmitUi()','navigator.share({title:"LEEKed IN",text,url:link})','https://twitter.com/intent/tweet']:
    if needle not in s:
        raise SystemExit(f'Missing expected result-flow marker: {needle}')
print('Result flow patch and JS syntax check passed.')
