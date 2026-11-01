# game_data.py
import random

# ==========================================
# الموسوعة السيبرانية (MITRE ATT&CK)
# ==========================================
SECURITY_DOMAINS = [
    ("Web & API Security", "1. أمن تطبيقات الويب وواجهات API"),
    ("Network & Infrastructure", "2. أمن الشبكات والبنية التحتية"),
    ("OS, Kernel & Memory", "3. أمن أنظمة التشغيل والنواة والذاكرة"),
    ("Active Directory & Identity", "4. الدليل النشط وإدارة الهوية"),
    ("Cloud, Docker & Kubernetes", "5. أمن السحابة والحاويات"),
    ("Applied Cryptography & PKI", "6. التشفير التطبيقي والمفاتيح العامة"),
    ("AI, LLM & Agent Security", "7. أمن الذكاء الاصطناعي والنماذج اللغوية"),
    ("Reverse Engineering & Malware", "8. الهندسة العكسية وتحليل البرمجيات الخبيثة")
]

CORE_TECHNIQUES = [
    {
        "code": "SQLi-UNION",
        "name_en": "SQL Injection (UNION Data Extraction)",
        "name_ar": "حقن قواعد البيانات واستخراج الجداول (UNION SQLi)",
        "vec_en": "Injecting UNION SELECT payloads into unparameterized SQL queries.",
        "vec_ar": "حقن عبارات UNION SELECT داخل استعلامات SQL غير المعلمة لسحب جداول البيانات الحساسة.",
        "steps_en": [
            "1. Fuzz input parameters with single quote (').",
            "2. Determine column count using ORDER BY.",
            "3. Extract database schema via UNION SELECT."
        ],
        "steps_ar": [
            "1. اختبار المدخلات بعلامة تنصيص مفردة (').",
            "2. معرفة عدد الأعمدة عبر جملة ORDER BY.",
            "3. سحب الجداول وكلمات المرور باستخدام UNION SELECT."
        ],
        "def_en": "Enforce Parameterized Queries (Prepared Statements).",
        "def_ar": "استخدام الاستعلامات المعلمة (Parameterized Queries / Prepared Statements).",
        "tools": "SQLMap, ModSecurity WAF, SQLAlchemy",
        "vuln_code": "cursor.execute(f\"SELECT * FROM accounts WHERE user = '{username}'\")",
        "sec_code": "cursor.execute(\"SELECT * FROM accounts WHERE user = ?\", (username,))",
        "fix_en": "Use Parameterized Queries",
        "fix_ar": "تطبيق الاستعلامات المعلمة (Parameterized Queries)"
    },
    {
        "code": "XSS-STORED",
        "name_en": "Stored Cross-Site Scripting (Persistent XSS)",
        "name_ar": "البرمجة النصية المخزنة عبر المواقع (Stored XSS)",
        "vec_en": "Saving malicious JavaScript inside database fields.",
        "vec_ar": "تخزين كود JavaScript خبيث داخل قاعدة البيانات ليتم تنفيذه تلقائياً في متصفح كل زائر.",
        "steps_en": [
            "1. Submit comment containing <script>...",
            "2. Wait for administrator or users to view the page.",
            "3. Hijack active sessions using captured cookies."
        ],
        "steps_ar": [
            "1. إرسال تعليق يحتوي على كود جافاسكربت خبيث.",
            "2. انتظار دخول المدير أو المستخدمين لعرض الصفحة المصابة.",
            "3. اختطاف الجلسة النشطة عبر الكوكيز المسروقة."
        ],
        "def_en": "Apply context-aware output encoding (textContent), deploy a strict CSP.",
        "def_ar": "ترميز المخرجات (استخدام textContent بدلاً من innerHTML)، تفعيل سياسة أمان المحتوى (CSP).",
        "tools": "DOMPurify, Content-Security-Policy Header",
        "vuln_code": "commentContainer.innerHTML = userSubmittedComment;",
        "sec_code": "commentContainer.textContent = userSubmittedComment;",
        "fix_en": "Context-Aware Output Encoding + CSP",
        "fix_ar": "ترميز المخرجات (textContent) وتفعيل CSP"
    },
    {
        "code": "CMD-INJECT",
        "name_en": "OS Command Injection",
        "name_ar": "حقن أوامر نظام التشغيل",
        "vec_en": "Appending shell control operators to user input passed into os.system().",
        "vec_ar": "إلحاق فواصل أوامر الشل بمدخلات المستخدم التي تمرر إلى دالة os.system.",
        "steps_en": [
            "1. Find network diagnostic form.",
            "2. Supply 127.0.0.1; id; cat /etc/shadow.",
            "3. Spawn an interactive reverse shell."
        ],
        "steps_ar": [
            "1. إيجاد أداة فحص شبكي في الموقع.",
            "2. إدخال 8.8.8.8 && whoami && cat /etc/passwd.",
            "3. الحصول على تحكم كامل بالخادم عبر شل عكسي."
        ],
        "def_en": "Avoid os.system(); use subprocess.run(['cmd', arg], shell=False).",
        "def_ar": "منع استخدام os.system واستبدالها بـ subprocess.run.",
        "tools": "Python subprocess(shell=False)",
        "vuln_code": "os.system('ping -c 1 ' + target_ip)",
        "sec_code": "subprocess.run(['ping', '-c', '1', target_ip], shell=False)",
        "fix_en": "Use subprocess.run without shell",
        "fix_ar": "استخدام subprocess.run بوضع shell=False"
    }
]

def generate_encyclopedia():
    db = []
    idx_counter = 1
    levels = [("Basic", "أساسي"), ("Advanced", "متقدم")]
    for tier_idx, (tier_en, tier_ar) in enumerate(levels):
         for item in CORE_TECHNIQUES:
             distractors_ar = ["تجاهل المشكلة", "حذف الملفات", "إعادة تشغيل السيرفر"]
             db.append({
                 "idx": idx_counter,
                 "name_ar": f"{item['name_ar']} [{tier_ar}]",
                 "q_ar": f"[طوارئ #{idx_counter}] كيف تمنع هجوم {item['name_ar']}؟",
                 "opts_ar": [item['fix_ar']] + distractors_ar,
                 "ans": 0
             })
             idx_counter += 1
    return db

ENCYCLOPEDIA_DATA = generate_encyclopedia()

# ==========================================
# بيانات طرفية الاختراق (CTF Servers)
# ==========================================
CTF_SERVERS = []
for i in range(1, 11):
    CTF_SERVERS.append({
        "ip": f"10.10.10.{i}",
        "hostname": f"Target-V{i}",
        "vuln": random.choice(["SQLi", "RCE", "XSS", "LFI"]),
        "tool": random.choice(["sqlmap", "hydra", "curl", "msfconsole"]),
        "flag": f"FLAG{{CYBER_{i * 1337}}}",
        "bounty": 100 * i
    })
