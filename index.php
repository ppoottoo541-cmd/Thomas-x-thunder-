<?php
session_start();

// ---------- Configuration ----------
define('SITE_NAME', 'THOMAS X OSIENT');
define('CONTACT', '@TGxTHOMASx');
define('ADMIN_USERNAME', 'admin');           // Default admin username
define('ADMIN_PASSWORD', 'admin123');        // Change after first login

// Files
$users_file = 'users.json';
$apis_file = 'apis.json';
$settings_file = 'settings.json';

// Initialize files if not exist
if (!file_exists($users_file)) file_put_contents($users_file, json_encode([]));
if (!file_exists($apis_file)) file_put_contents($apis_file, json_encode([
    'vehicle' => 'https://invalid-vehicle-api.pagals1818.workers.dev/?vehicle=',
    'number' => 'https://invalid-num-info.vercel.app/api/lund?number='
]));
if (!file_exists($settings_file)) file_put_contents($settings_file, json_encode([
    'admin_user' => ADMIN_USERNAME,
    'admin_pass' => password_hash(ADMIN_PASSWORD, PASSWORD_DEFAULT)
]));

// Load data
$users = json_decode(file_get_contents($users_file), true);
$apis = json_decode(file_get_contents($apis_file), true);
$settings = json_decode(file_get_contents($settings_file), true);

// Helper: save users
function saveUsers($data) {
    global $users_file;
    file_put_contents($users_file, json_encode($data, JSON_PRETTY_PRINT));
}

// Helper: save apis
function saveApis($data) {
    global $apis_file;
    file_put_contents($apis_file, json_encode($data, JSON_PRETTY_PRINT));
}

// ---------- Routing ----------
$action = $_GET['action'] ?? 'home';

// Logout
if ($action === 'logout') {
    session_destroy();
    header('Location: index.php');
    exit;
}

// ---------- Admin check ----------
function isAdmin() {
    global $settings;
    return isset($_SESSION['user']) && $_SESSION['user']['role'] === 'admin';
}

// ---------- Handle actions ----------

// Login
if ($action === 'login' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    $user = $users[$username] ?? null;
    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['user'] = $user;
        $_SESSION['user']['username'] = $username;
        header('Location: index.php');
        exit;
    } else {
        $error = 'Invalid username or password';
    }
}

// Register
if ($action === 'register' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    if (isset($users[$username])) {
        $error = 'Username already exists';
    } elseif (strlen($password) < 4) {
        $error = 'Password too short';
    } else {
        $users[$username] = [
            'password' => password_hash($password, PASSWORD_DEFAULT),
            'credits' => 5, // starting credits
            'role' => 'user',
            'joined' => date('Y-m-d H:i:s')
        ];
        saveUsers($users);
        $_SESSION['user'] = $users[$username];
        $_SESSION['user']['username'] = $username;
        header('Location: index.php');
        exit;
    }
}

// API call (ajax)
if ($action === 'api_call' && isset($_SESSION['user'])) {
    header('Content-Type: application/json');
    $type = $_POST['type'] ?? '';
    $value = $_POST['value'] ?? '';
    $username = $_SESSION['user']['username'];
    $user = &$users[$username];

    if (!in_array($type, ['vehicle', 'number']) || empty($value)) {
        echo json_encode(['error' => 'Invalid request']);
        exit;
    }
    if ($user['credits'] < 1) {
        echo json_encode(['error' => 'Insufficient credits']);
        exit;
    }

    // Deduct credit
    $user['credits']--;
    saveUsers($users);
    $_SESSION['user']['credits'] = $user['credits'];

    // Call API
    $apiUrl = $apis[$type] . urlencode($value);
    $proxyUrl = "https://api.allorigins.win/raw?url=" . urlencode($apiUrl);
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $proxyUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode != 200) {
        echo json_encode(['error' => 'API request failed']);
        exit;
    }

    $data = json_decode($response, true) ?? ['raw' => $response];

    // Remove any unwanted fields (like developer names)
    array_walk_recursive($data, function(&$v, $k) {
        if (in_array(strtolower($k), ['developer','credit','powered_by','author','dev','created_by','ayush','invalid','name'])) {
            $v = null; // or unset? better to unset but recursive walk can't unset easily, we'll do a separate cleaning
        }
    });
    // Actually we need proper cleaning, let's do a function
    function cleanArray($arr) {
        if (!is_array($arr)) return $arr;
        $clean = [];
        foreach ($arr as $key => $value) {
            if (in_array(strtolower($key), ['developer','credit','powered_by','author','dev','created_by','ayush','invalid','name'])) {
                continue;
            }
            if (is_array($value)) {
                $clean[$key] = cleanArray($value);
            } else {
                $clean[$key] = $value;
            }
        }
        return $clean;
    }
    $data = cleanArray($data);

    $result = [
        'status' => 'success',
        'data' => $data,
        'credit' => CONTACT,
        'developer' => SITE_NAME,
        'credits_left' => $user['credits'],
        'timestamp' => date('c')
    ];
    echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
    exit;
}

// Admin actions
if (isAdmin() && $action === 'admin') {
    $sub = $_GET['sub'] ?? 'dashboard';

    // Add credits
    if ($sub === 'add_credits' && $_POST) {
        $target = $_POST['username'] ?? '';
        $amount = (int)($_POST['amount'] ?? 0);
        if (isset($users[$target])) {
            $users[$target]['credits'] += $amount;
            saveUsers($users);
            $msg = "Added $amount credits to $target";
        } else {
            $error = "User not found";
        }
    }

    // Update API URLs
    if ($sub === 'update_apis' && $_POST) {
        $apis['vehicle'] = $_POST['vehicle'] ?? $apis['vehicle'];
        $apis['number'] = $_POST['number'] ?? $apis['number'];
        saveApis($apis);
        $msg = "API URLs updated";
    }

    // Change admin password
    if ($sub === 'change_password' && $_POST) {
        $new = $_POST['new_pass'] ?? '';
        if (strlen($new) >= 4) {
            $settings['admin_pass'] = password_hash($new, PASSWORD_DEFAULT);
            file_put_contents($settings_file, json_encode($settings));
            $msg = "Admin password changed";
        } else {
            $error = "Password too short";
        }
    }
}

// ---------- HTML output (with Tailwind) ----------
?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= SITE_NAME ?> | <?= CONTACT ?></title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { background: #020617; }
        .glass { background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .credit-badge { background: linear-gradient(135deg, #3b82f6, #8b5cf6); }
        .json-key { color: #f472b6; }
        .json-string { color: #a3e635; }
        .json-number { color: #fbbf24; }
        .json-boolean { color: #60a5fa; }
    </style>
</head>
<body class="text-gray-200 min-h-screen flex items-center justify-center p-4">

<?php
// If not logged in, show login/register
if (!isset($_SESSION['user'])) {
?>
<div class="max-w-md w-full glass p-8 rounded-3xl">
    <div class="text-center mb-8">
        <span class="credit-badge text-white px-4 py-2 rounded-full text-sm inline-block mb-4"><?= CONTACT ?></span>
        <h2 class="text-3xl font-black"><?= SITE_NAME ?></h2>
        <p class="text-blue-400 text-sm">Login to access services</p>
    </div>

    <?php if (isset($error)): ?><div class="bg-red-600 p-3 rounded-xl mb-4"><?= $error ?></div><?php endif; ?>

    <form method="POST" action="?action=login">
        <input type="text" name="username" placeholder="Username" required class="w-full bg-black/50 border border-slate-700 p-4 rounded-2xl mb-4">
        <input type="password" name="password" placeholder="Password" required class="w-full bg-black/50 border border-slate-700 p-4 rounded-2xl mb-6">
        <button type="submit" class="w-full bg-blue-600 py-4 rounded-2xl font-bold hover:bg-blue-700">Login</button>
    </form>

    <p class="mt-4 text-center">Don't have account? <a href="?action=register" class="text-blue-400">Register</a></p>
</div>
<?php
} elseif ($action === 'register') {
    // Register form (similar)
?>
<div class="max-w-md w-full glass p-8 rounded-3xl">
    <div class="text-center mb-8">
        <span class="credit-badge text-white px-4 py-2 rounded-full text-sm inline-block mb-4"><?= CONTACT ?></span>
        <h2 class="text-3xl font-black">Create Account</h2>
    </div>
    <?php if (isset($error)): ?><div class="bg-red-600 p-3 rounded-xl mb-4"><?= $error ?></div><?php endif; ?>
    <form method="POST" action="?action=register">
        <input type="text" name="username" placeholder="Username" required class="w-full bg-black/50 border border-slate-700 p-4 rounded-2xl mb-4">
        <input type="password" name="password" placeholder="Password (min 4 chars)" required class="w-full bg-black/50 border border-slate-700 p-4 rounded-2xl mb-6">
        <button type="submit" class="w-full bg-green-600 py-4 rounded-2xl font-bold hover:bg-green-700">Register</button>
    </form>
    <p class="mt-4 text-center">Already have account? <a href="index.php" class="text-blue-400">Login</a></p>
</div>
<?php
} elseif (isAdmin() && $action === 'admin') {
    // Admin panel
    $sub = $_GET['sub'] ?? 'dashboard';
?>
<div class="max-w-4xl w-full">
    <div class="glass p-6 rounded-3xl mb-6 flex justify-between items-center">
        <h2 class="text-2xl font-black">⚙️ Admin Panel</h2>
        <div class="flex gap-4">
            <span class="text-blue-400"><?= $_SESSION['user']['username'] ?></span>
            <a href="?action=logout" class="bg-red-600 px-4 py-2 rounded-full text-sm">Logout</a>
        </div>
    </div>

    <div class="grid md:grid-cols-4 gap-4 mb-6">
        <a href="?action=admin&sub=dashboard" class="glass p-4 rounded-2xl text-center hover:bg-blue-600/20">📊 Dashboard</a>
        <a href="?action=admin&sub=users" class="glass p-4 rounded-2xl text-center hover:bg-blue-600/20">👥 Users</a>
        <a href="?action=admin&sub=apis" class="glass p-4 rounded-2xl text-center hover:bg-blue-600/20">🔧 APIs</a>
        <a href="?action=admin&sub=settings" class="glass p-4 rounded-2xl text-center hover:bg-blue-600/20">⚙️ Settings</a>
    </div>

    <?php if (isset($msg)): ?><div class="bg-green-600 p-3 rounded-xl mb-4"><?= $msg ?></div><?php endif; ?>
    <?php if (isset($error)): ?><div class="bg-red-600 p-3 rounded-xl mb-4"><?= $error ?></div><?php endif; ?>

    <?php if ($sub === 'dashboard'): ?>
        <div class="glass p-6 rounded-3xl">
            <h3 class="font-bold text-xl mb-4">Overview</h3>
            <p>Total users: <?= count($users) ?></p>
            <p>Total credits: <?= array_sum(array_column($users, 'credits')) ?></p>
        </div>
    <?php elseif ($sub === 'users'): ?>
        <div class="glass p-6 rounded-3xl">
            <h3 class="font-bold text-xl mb-4">Manage Users</h3>
            <form method="POST" action="?action=admin&sub=add_credits" class="mb-6">
                <div class="flex gap-2">
                    <input type="text" name="username" placeholder="Username" required class="bg-black/50 border border-slate-700 p-2 rounded flex-1">
                    <input type="number" name="amount" placeholder="Credits" required class="bg-black/50 border border-slate-700 p-2 rounded w-24">
                    <button type="submit" class="bg-green-600 px-4 rounded">Add</button>
                </div>
            </form>
            <table class="w-full text-left">
                <thead><tr><th>Username</th><th>Credits</th><th>Role</th></tr></thead>
                <tbody>
                <?php foreach ($users as $name => $u): ?>
                <tr><td><?= $name ?></td><td><?= $u['credits'] ?></td><td><?= $u['role'] ?></td></tr>
                <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    <?php elseif ($sub === 'apis'): ?>
        <div class="glass p-6 rounded-3xl">
            <h3 class="font-bold text-xl mb-4">Update API URLs</h3>
            <form method="POST" action="?action=admin&sub=update_apis">
                <div class="mb-4">
                    <label class="block mb-2">Vehicle API URL</label>
                    <input type="url" name="vehicle" value="<?= htmlspecialchars($apis['vehicle']) ?>" required class="w-full bg-black/50 border border-slate-700 p-3 rounded-2xl">
                </div>
                <div class="mb-4">
                    <label class="block mb-2">Number API URL</label>
                    <input type="url" name="number" value="<?= htmlspecialchars($apis['number']) ?>" required class="w-full bg-black/50 border border-slate-700 p-3 rounded-2xl">
                </div>
                <button type="submit" class="bg-blue-600 px-6 py-3 rounded-2xl">Save Changes</button>
            </form>
        </div>
    <?php elseif ($sub === 'settings'): ?>
        <div class="glass p-6 rounded-3xl">
            <h3 class="font-bold text-xl mb-4">Change Admin Password</h3>
            <form method="POST" action="?action=admin&sub=change_password">
                <input type="password" name="new_pass" placeholder="New Password" required class="w-full bg-black/50 border border-slate-700 p-3 rounded-2xl mb-4">
                <button type="submit" class="bg-blue-600 px-6 py-3 rounded-2xl">Change</button>
            </form>
        </div>
    <?php endif; ?>
</div>
<?php
} else {
    // User dashboard
    $user = $_SESSION['user'];
?>
<div class="container mx-auto px-4 py-6 max-w-4xl">
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
        <span class="credit-badge text-white px-4 py-2 rounded-full text-sm">
            <i class="fas fa-coins mr-2"></i> Credits: <?= $user['credits'] ?>
        </span>
        <div class="flex gap-4">
            <a href="?action=buy" class="bg-green-600 px-6 py-2 rounded-full text-sm font-bold hover:bg-green-700">Buy Credits</a>
            <a href="?action=logout" class="bg-slate-700 px-6 py-2 rounded-full text-sm font-bold hover:bg-slate-600">Logout</a>
        </div>
    </div>

    <!-- Title -->
    <div class="text-center mb-16">
        <span class="credit-badge text-white px-6 py-2 rounded-full inline-block mb-4">
            <i class="fas fa-code mr-2"></i> Developed by <?= CONTACT ?>
        </span>
        <h1 class="text-5xl font-black italic text-white tracking-tighter mb-2 uppercase"><?= SITE_NAME ?></h1>
        <p class="text-blue-400 font-mono tracking-widest text-sm uppercase">Ultimate Search Dashboard</p>
    </div>

    <!-- Services -->
    <div class="grid md:grid-cols-2 gap-8 mb-12">
        <div class="glass p-8 rounded-3xl">
            <h3 class="text-xl font-bold mb-6 text-blue-400 italic"><i class="fas fa-car mr-2"></i> Vehicle Checker</h3>
            <input id="vInput" type="text" placeholder="Number Plate (UP32XX...)" class="w-full bg-black/50 border border-slate-700 p-4 rounded-2xl mb-4 focus:border-blue-500 outline-none">
            <button onclick="callAPI('vehicle')" class="w-full bg-blue-600 hover:bg-blue-700 py-4 rounded-2xl font-black uppercase">Fetch Data (1 Credit)</button>
        </div>
        <div class="glass p-8 rounded-3xl">
            <h3 class="text-xl font-bold mb-6 text-green-400 italic"><i class="fas fa-phone mr-2"></i> Number Info</h3>
            <input id="nInput" type="text" placeholder="Phone Number (91...)" class="w-full bg-black/50 border border-slate-700 p-4 rounded-2xl mb-4 focus:border-green-500 outline-none">
            <button onclick="callAPI('number')" class="w-full bg-green-600 hover:bg-green-700 py-4 rounded-2xl font-black uppercase">Get Info (1 Credit)</button>
        </div>
    </div>

    <!-- Result Box -->
    <div id="resultBox" class="hidden glass p-8 rounded-3xl border-l-8 border-blue-500 mb-12">
        <div class="flex justify-between mb-4">
            <span class="text-blue-400 italic"><i class="fas fa-database mr-1"></i> Response</span>
            <button onclick="copyRes()" class="text-xs bg-slate-800 px-4 py-1 rounded-full hover:bg-slate-700">Copy</button>
        </div>
        <pre id="outputArea" class="text-sm font-mono bg-black/30 p-4 rounded-2xl max-h-96 overflow-auto"></pre>
        <div class="mt-4 text-right text-xs text-blue-400 border-t border-slate-700 pt-3">
            Powered by <?= CONTACT ?> | <?= SITE_NAME ?>
        </div>
    </div>

    <!-- Admin link (if admin) -->
    <?php if ($user['role'] === 'admin'): ?>
    <div class="text-center">
        <a href="?action=admin" class="inline-block bg-purple-600 px-8 py-4 rounded-full font-bold hover:bg-purple-700">Go to Admin Panel</a>
    </div>
    <?php endif; ?>
</div>

<script>
async function callAPI(type) {
    let input = type === 'vehicle' ? document.getElementById('vInput').value.trim() : document.getElementById('nInput').value.trim();
    if (!input) return alert('Enter value');

    const out = document.getElementById('outputArea');
    const resBox = document.getElementById('resultBox');
    resBox.classList.remove('hidden');
    out.innerHTML = '<span class="text-yellow-400">⏳ Processing...</span>';

    const formData = new FormData();
    formData.append('type', type);
    formData.append('value', input);

    try {
        let res = await fetch('?action=api_call', { method: 'POST', body: formData });
        let data = await res.json();
        if (data.error) {
            out.innerHTML = `<span class="text-red-400">❌ ${data.error}</span>`;
        } else {
            out.innerHTML = syntaxHighlight(JSON.stringify(data, null, 2));
            // Update credits in header
            if (data.credits_left !== undefined) {
                document.querySelector('.credit-badge').innerHTML = `<i class="fas fa-coins mr-2"></i> Credits: ${data.credits_left}`;
            }
        }
    } catch (e) {
        out.innerHTML = `<span class="text-red-400">❌ Error: ${e.message}</span>`;
    }
}

function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'json-number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'json-key';
                match = match.replace(/":/g, '":');
            } else {
                cls = 'json-string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'json-boolean';
        } else if (/null/.test(match)) {
            cls = 'json-null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

function copyRes() {
    const text = document.getElementById('outputArea').innerText;
    navigator.clipboard.writeText(text);
    alert('Copied!');
}
</script>

<?php
} // end dashboard
?>
</body>
</html>