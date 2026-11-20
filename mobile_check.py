import json
from playwright.sync_api import sync_playwright

URL = 'https://imapstudio-jiae.github.io/jia/?cb=mobilecheck'
out = {}

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(
        viewport={'width': 390, 'height': 844},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True,
        user_agent=('Mozilla/5.0 (Linux; Android 14; SM-S918N) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'),
    )
    pg = ctx.new_page()
    pg.goto(URL, wait_until='load')
    pg.wait_for_selector('#dots i')
    pg.wait_for_timeout(700)

    out['viewport'] = [pg.evaluate('innerWidth'), pg.evaluate('innerHeight')]
    out['dots'] = pg.eval_on_selector_all('#dots i', 'els => els.length')
    out['live'] = pg.inner_text('#lockLive')
    out['themeColor'] = pg.eval_on_selector('meta[name="theme-color"]', 'e => e.content')
    out['lockedBefore'] = pg.eval_on_selector('#lock', 'e => !e.classList.contains("gone")')
    pg.screenshot(path='downloads/yeobaek-pin-2024.png')

    for d in ['2', '0', '2', '4']:
        pg.click('[data-k="%s"]' % d)
    pg.wait_for_function("document.querySelector('#lock').classList.contains('gone')", timeout=10000)
    pg.wait_for_timeout(3000)

    out['lockGone'] = pg.eval_on_selector('#lock', 'e => e.classList.contains("gone")')
    out['appHidden'] = pg.eval_on_selector('#app', 'e => e.hidden')
    out['bodyBg'] = pg.evaluate("getComputedStyle(document.body).backgroundImage")
    out['fabButton'] = pg.evaluate("""(() => {const b=document.querySelector('.fab button');const s=getComputedStyle(b);return {text:b.innerText.trim(), bg:s.backgroundColor, color:s.color, display:getComputedStyle(document.querySelector('.fab')).display}})()""")
    out['topPill'] = pg.evaluate("""(() => {const b=document.querySelector('.top-actions .pill.solid');return {text:b.innerText.trim(), display:getComputedStyle(b).display}})()""")
    out['cardBorder'] = pg.evaluate("""(() => {const c=document.querySelector('.rec');return c?getComputedStyle(c).borderColor:null})()""")
    out['footCount'] = pg.inner_text('#footCount')
    pg.screenshot(path='downloads/yeobaek-navy-brighter-mobile.png')
    b.close()

print(json.dumps(out, ensure_ascii=False, indent=1))
