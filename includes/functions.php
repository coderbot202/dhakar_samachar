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

function findNewsById(int $id): ?array
{
    global $newsItems;
    foreach ($newsItems as $news) {
        if ($news['id'] === $id) {
            return $news;
        }
    }
    return null;
}
