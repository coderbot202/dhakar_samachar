<?php
session_start();

$supportedLanguages = ['en', 'bn'];
if (isset($_GET['lang']) && in_array($_GET['lang'], $supportedLanguages, true)) {
    $_SESSION['lang'] = $_GET['lang'];
}
$lang = $_SESSION['lang'] ?? 'en';

$supportedThemes = ['sunset', 'ocean', 'forest'];
if (isset($_GET['theme']) && in_array($_GET['theme'], $supportedThemes, true)) {
    $_SESSION['theme'] = $_GET['theme'];
}
$theme = $_SESSION['theme'] ?? 'sunset';

$translations = [
    'en' => [
        'site_name' => 'Dhakar Samachar',
        'tagline' => 'Fast, trusted, and visual-first Bangla news experience.',
        'home' => 'Home',
        'shorts' => 'Shorts',
        'epaper' => 'E-paper',
        'search' => 'Search',
        'privacy' => 'Privacy Policy',
        'terms' => 'Terms & Conditions',
        'latest_news' => 'Latest News',
        'breaking_news' => 'Breaking News',
        'read_more' => 'Read more',
        'hero_title' => 'Modern news portal for Hostinger-ready PHP hosting',
        'hero_subtitle' => 'Built in pure PHP + Bootstrap with multi-language and multi-color themes.',
        'view_epaper' => 'View e-paper',
        'search_placeholder' => 'Search by title or category...',
        'search_btn' => 'Find News',
        'no_results' => 'No matching news found.',
        'multilang' => 'Language',
        'multicolor' => 'Theme',
    ],
    'bn' => [
        'site_name' => 'ঢাকার সংবাদ',
        'tagline' => 'দ্রুত, নির্ভরযোগ্য ও ভিজ্যুয়াল-ফার্স্ট বাংলা নিউজ অভিজ্ঞতা।',
        'home' => 'হোম',
        'shorts' => 'শর্টস',
        'epaper' => 'ই-পেপার',
        'search' => 'সার্চ',
        'privacy' => 'প্রাইভেসি পলিসি',
        'terms' => 'টার্মস অ্যান্ড কন্ডিশনস',
        'latest_news' => 'সর্বশেষ সংবাদ',
        'breaking_news' => 'ব্রেকিং নিউজ',
        'read_more' => 'বিস্তারিত',
        'hero_title' => 'Hostinger-সমর্থিত PHP হোস্টিংয়ের জন্য আধুনিক নিউজ পোর্টাল',
        'hero_subtitle' => 'খাঁটি PHP + Bootstrap দিয়ে তৈরি মাল্টি-ল্যাঙ্গুয়েজ ও মাল্টি-কালার থিম।',
        'view_epaper' => 'ই-পেপার দেখুন',
        'search_placeholder' => 'শিরোনাম বা ক্যাটাগরি দিয়ে খুঁজুন...',
        'search_btn' => 'সংবাদ খুঁজুন',
        'no_results' => 'কোনো মিল পাওয়া যায়নি।',
        'multilang' => 'ভাষা',
        'multicolor' => 'থিম',
    ],
];

function t(string $key): string
{
    global $translations, $lang;
    return $translations[$lang][$key] ?? $key;
}
