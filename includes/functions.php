<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/data.php';

function localizedText(array $item, string $field, string $lang): string
{
    $localizedField = $field . '_bn';
    if ($lang === 'bn' && isset($item[$localizedField])) {
        return $item[$localizedField];
    }
    return $item[$field] ?? '';
}

function adminDataFilePath(): string
{
    return __DIR__ . '/../data/news_items.json';
}

function loadManagedNewsItems(): array
{
    $path = adminDataFilePath();
    if (!file_exists($path)) {
        return [];
    }

    $json = file_get_contents($path);
    if ($json === false || trim($json) === '') {
        return [];
    }

    $decoded = json_decode($json, true);
    return is_array($decoded) ? $decoded : [];
}

function getNewsItems(): array
{
    global $newsItems;
    $managed = loadManagedNewsItems();
    $all = array_merge($managed, $newsItems);

    usort($all, static function (array $a, array $b): int {
        return strcmp((string) ($b['date'] ?? ''), (string) ($a['date'] ?? ''));
    });

    return $all;
}

function nextNewsId(array $items): int
{
    $max = 0;
    foreach ($items as $item) {
        $id = (int) ($item['id'] ?? 0);
        if ($id > $max) {
            $max = $id;
        }
    }
    return $max + 1;
}

function addManagedNewsItem(array $input): void
{
    $managed = loadManagedNewsItems();
    $all = getNewsItems();
    $managed[] = [
        'id' => nextNewsId($all),
        'title' => trim((string) ($input['title'] ?? '')),
        'title_bn' => trim((string) ($input['title_bn'] ?? '')),
        'summary' => trim((string) ($input['summary'] ?? '')),
        'summary_bn' => trim((string) ($input['summary_bn'] ?? '')),
        'content' => trim((string) ($input['content'] ?? '')),
        'content_bn' => trim((string) ($input['content_bn'] ?? '')),
        'category' => trim((string) ($input['category'] ?? 'General')),
        'image' => trim((string) ($input['image'] ?? 'https://images.unsplash.com/photo-1495020689067-958852a7765e?auto=format&fit=crop&w=1200&q=80')),
        'date' => trim((string) ($input['date'] ?? date('Y-m-d'))),
        'is_breaking' => !empty($input['is_breaking']),
    ];

    saveManagedNewsItems($managed);
}

function saveManagedNewsItems(array $managed): void
{
    $path = adminDataFilePath();
    $dir = dirname($path);
    if (!is_dir($dir)) {
        mkdir($dir, 0775, true);
    }
    file_put_contents($path, json_encode($managed, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
}

function removeManagedNewsItem(int $id): void
{
    $managed = loadManagedNewsItems();
    $managed = array_values(array_filter($managed, static fn(array $item): bool => (int) ($item['id'] ?? 0) !== $id));
    saveManagedNewsItems($managed);
}

function findNewsById(int $id): ?array
{
    foreach (getNewsItems() as $news) {
        if ((int) ($news['id'] ?? 0) === $id) {
            return $news;
        }
    }
    return null;
}

function isAdminLoggedIn(): bool
{
    return !empty($_SESSION['is_admin_logged_in']);
}

function requireAdminAuth(): void
{
    if (!isAdminLoggedIn()) {
        header('Location: admin.php?action=login');
        exit;
    }
}
