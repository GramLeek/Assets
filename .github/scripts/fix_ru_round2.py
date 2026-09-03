from pathlib import Path
import re
import subprocess

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,expected=1):
    global s
    n=s.count(old)
    if n!=expected:
        raise SystemExit(f'Expected {expected}, found {n}: {old[:120]!r}')
    s=s.replace(old,new,expected)

# Finish obvious mixed-language strings in the RU dictionary only.
rep('stamp:"ПУБЛИЧНЫЙ ПРОТОТИП // BURN НЕ АКТИВЕН"','stamp:"ПУБЛИЧНЫЙ ПРОТОТИП // СЖИГАНИЕ НЕ АКТИВНО"')
rep('hero:\'<b>Играбельный прототип. Без фальшивой utility.</b><br>Убийства дают очки. LEEK пока не сжигается игрой.\'','hero:\'<b>Играбельный прототип. Без выдуманной пользы.</b><br>Убийства дают очки. LEEK пока не сжигается игрой.\'')
rep('tag3:"BURN-МЕХАНИКА // НЕ АКТИВНА"','tag3:"МЕХАНИКА СЖИГАНИЯ // НЕ АКТИВНА"')
rep('proofCopy:\'Публичные кошельки. Live-баланс void-кошелька. Текущий gameplay не создаёт burn-транзакции. <strong>Проверь сам.</strong>\'','proofCopy:\'Публичные кошельки. Баланс void-кошелька в реальном времени. Текущая игра не создаёт транзакций сжигания. <strong>Проверь сам.</strong>\'')
rep('rankSubmit:"ДОБАВИТЬ RUN"','rankSubmit:"ДОБАВИТЬ ЗАБЕГ"')
rep('supplyLive:"void-кошелёк синхронизирован. связь с gameplay: не активна."','supplyLive:"void-кошелёк синхронизирован. связь с игрой: не активна."')
rep('verdictLowText:"Видимые топ-10 не контролируют основную часть выпущенного supply."','verdictLowText:"Видимые топ-10 не контролируют основную часть выпущенной эмиссии."')
rep('verdictHighText:"Небольшая группа контролирует крупную долю. Это факт, но ещё не автоматический rug verdict."','verdictHighText:"Небольшая группа контролирует крупную долю. Это факт, но ещё не автоматический признак рага."')
rep('ticker:burned=>["GAME BURN = НЕ АКТИВЕН",`VOID WALLET: ${human(burned)} LEEK // НЕ ИЗ GAMEPLAY`,"КОШЕЛЁК НЕ НУЖЕН","ПУБЛИЧНЫЙ ПРОТОТИП","СНАЧАЛА ГЕЙМПЛЕЙ"]','ticker:burned=>["СЖИГАНИЕ ИГРОЙ = НЕ АКТИВНО",`VOID-КОШЕЛЁК: ${human(burned)} LEEK // НЕ ИЗ ИГРЫ`,"КОШЕЛЁК НЕ НУЖЕН","ПУБЛИЧНЫЙ ПРОТОТИП","СНАЧАЛА ИГРА"]')

# Polish up static Russian translations that still carried avoidable English.
rep('["Playable prototype. Public wallets. Chain data. No fake utility.","Играбельный прототип. Публичные кошельки. Данные блокчейна. Никакой фальшивой utility."]','["Playable prototype. Public wallets. Chain data. No fake utility.","Играбельный прототип. Публичные кошельки. Данные блокчейна. Никакой выдуманной пользы."]')
rep('["Landscape screen recovery + clear lower combat zone","Восстановление landscape-экрана + чистая нижняя зона боя"]','["Landscape screen recovery + clear lower combat zone","Восстановление альбомного режима + чистая нижняя зона боя"]')
rep('["Global scores are written to Supabase with the public publishable key. Row-level security controls anonymous access. If the database is unavailable, your result remains local and shareable.","Глобальные результаты записываются в Supabase с публичным publishable key. Row-level security контролирует анонимный доступ. Если база недоступна, результат остаётся локальным и им можно поделиться."]','["Global scores are written to Supabase with the public publishable key. Row-level security controls anonymous access. If the database is unavailable, your result remains local and shareable.","Глобальные результаты записываются в Supabase с публичным ключом. Политики доступа на уровне строк контролируют анонимную запись. Если база недоступна, результат остаётся локальным и им можно поделиться."]')

# Add a few runtime translations missed in pass one.
rep('["FULLSCREEN ENGAGED","ПОЛНЫЙ ЭКРАН ВКЛЮЧЁН"],','["FULLSCREEN ENGAGED","ПОЛНЫЙ ЭКРАН ВКЛЮЧЁН"],["INSTALL IS NOT AVAILABLE IN THIS CLIENT","УСТАНОВКА НЕДОСТУПНА В ЭТОМ КЛИЕНТЕ"],["SEALING","ФИКСИРУЕТСЯ"],["COMBO X10","КОМБО X10"],')

# Dynamic supply status must follow language switches too.
rep('$("burnPercent").textContent=pct.toFixed(2)+"% BURNED";','$("burnPercent").textContent=pct.toFixed(2)+(currentLang==="ru"?"% СЖЕЖЕНО":"% BURNED");')
rep('    if(lastScanData)renderScan(lastScanData);','    if(burnDataReady)$("burnPercent").textContent=(liveBurned/CONFIG.totalSupply*100).toFixed(2)+(currentLang==="ru"?"% СЖЕЖЕНО":"% BURNED");\n    if(lastScanData)renderScan(lastScanData);')

# Localize dynamic fallbacks and share-card seal line.
rep('const hash=last.eventHash?last.eventHash.slice(0,12).toUpperCase():"LOCAL";','const hash=last.eventHash?last.eventHash.slice(0,12).toUpperCase():uiText("LOCAL");')
rep('const runStamp=new Date(Number(run.startedAt)||Date.now()).toISOString().slice(0,19).replace("T"," "),runHash=run.eventHash?run.eventHash.slice(0,12).toUpperCase():"SEALING";','const runStamp=new Date(Number(run.startedAt)||Date.now()).toISOString().slice(0,19).replace("T"," "),runHash=run.eventHash?run.eventHash.slice(0,12).toUpperCase():uiText("SEALING");')
rep('c.fillText(`RUN ${runHash} · ${runStamp} UTC`,66,582);','c.fillText(currentLang==="ru"?`ЗАБЕГ ${runHash} · ${runStamp} UTC`:`RUN ${runHash} · ${runStamp} UTC`,66,582);')
rep('box.textContent=tr("challenge")(challengeData.name||"ANOTHER VEGETABLE",challengeData.score);','box.textContent=tr("challenge")(challengeData.name||(currentLang==="ru"?"ДРУГОЙ ОВОЩ":"ANOTHER VEGETABLE"),challengeData.score);')

p.write_text(s,encoding='utf-8')

scripts=re.findall(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>',s)
inline=max(scripts,key=len)
tmp=Path('/tmp/gramleek-inline.js')
tmp.write_text(inline,encoding='utf-8')
subprocess.run(['node','--check',str(tmp)],check=True)
print('Russian localization cleanup applied; JavaScript syntax valid.')
