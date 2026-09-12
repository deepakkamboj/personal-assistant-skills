<?php
/**
 * tracker.php — Newsletter open & click tracker
 * Uploaded to: example.com/newsletters/track.php
 *
 * Query params:
 *   ?t=open&n={slug}&e={email_hash}         → log open, return 1×1 GIF
 *   ?t=click&n={slug}&e={email_hash}&u={b64_url} → log click, redirect to URL
 *
 * Logs to: tracking.csv (same directory as this file)
 */

// ── Helpers ──────────────────────────────────────────────────────────────────

function sanitize(string $val): string {
    return preg_replace('/[^a-zA-Z0-9_\-=+\/.]/', '', $val);
}

function log_event(string $type, string $slug, string $email_hash): void {
    $log_file = __DIR__ . '/tracking.csv';
    $timestamp = date('Y-m-d H:i:s');
    $ip = $_SERVER['REMOTE_ADDR'] ?? '';
    $ua = substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 120);
    $line = implode(',', [
        $timestamp,
        $type,
        $slug,
        $email_hash,
        $ip,
        '"' . str_replace('"', '""', $ua) . '"',
    ]) . "\n";
    file_put_contents($log_file, $line, FILE_APPEND | LOCK_EX);
}

function send_pixel(): void {
    // 1×1 transparent GIF
    $gif = base64_decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7');
    header('Content-Type: image/gif');
    header('Content-Length: ' . strlen($gif));
    header('Cache-Control: no-store, no-cache, must-revalidate');
    header('Pragma: no-cache');
    echo $gif;
}

// ── Main ─────────────────────────────────────────────────────────────────────

$type  = sanitize($_GET['t'] ?? '');
$slug  = sanitize($_GET['n'] ?? '');
$ehash = sanitize($_GET['e'] ?? '');

if (!$type || !$slug || !$ehash) {
    http_response_code(400);
    exit('Bad request');
}

if ($type === 'open') {
    log_event('open', $slug, $ehash);
    send_pixel();
    exit;
}

if ($type === 'click') {
    $encoded_url = $_GET['u'] ?? '';
    // Base64 URL-safe decode
    $decoded_url = base64_decode(strtr($encoded_url, '-_', '+/') . str_repeat('=', (4 - strlen($encoded_url) % 4) % 4));

    if (!$decoded_url || !filter_var($decoded_url, FILTER_VALIDATE_URL)) {
        http_response_code(400);
        exit('Invalid redirect URL');
    }

    log_event('click', $slug, $ehash);

    header('HTTP/1.1 302 Found');
    header('Location: ' . $decoded_url);
    exit;
}

http_response_code(400);
exit('Unknown event type');
