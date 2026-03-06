<?php
require_once __DIR__ . '/functions.php';
$currentPath = basename($_SERVER['PHP_SELF']);
?>
<!doctype html>
<html lang="<?= $lang; ?>">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title><?= t('site_name'); ?></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
    <link href="assets/css/style.css" rel="stylesheet">
</head>
<body class="theme-<?= htmlspecialchars($theme); ?>">
<nav class="navbar navbar-expand-lg navbar-dark glass-nav sticky-top">
    <div class="container">
        <a class="navbar-brand fw-bold" href="index.php"><i class="bi bi-newspaper me-2"></i><?= t('site_name'); ?></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#menu">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div id="menu" class="collapse navbar-collapse">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item"><a class="nav-link <?= $currentPath === 'index.php' ? 'active' : ''; ?>" href="index.php"><?= t('home'); ?></a></li>
                <li class="nav-item"><a class="nav-link <?= $currentPath === 'shorts.php' ? 'active' : ''; ?>" href="shorts.php"><?= t('shorts'); ?></a></li>
                <li class="nav-item"><a class="nav-link <?= $currentPath === 'epaper.php' ? 'active' : ''; ?>" href="epaper.php"><?= t('epaper'); ?></a></li>
                <li class="nav-item"><a class="nav-link <?= $currentPath === 'search.php' ? 'active' : ''; ?>" href="search.php"><?= t('search'); ?></a></li>
                <li class="nav-item"><a class="nav-link <?= $currentPath === 'admin.php' ? 'active' : ''; ?>" href="admin.php">Admin</a></li>
            </ul>

            <form class="d-flex gap-2" method="get">
                <select class="form-select form-select-sm" name="lang" onchange="this.form.submit()">
                    <option value="en" <?= $lang === 'en' ? 'selected' : ''; ?>>EN</option>
                    <option value="bn" <?= $lang === 'bn' ? 'selected' : ''; ?>>বাংলা</option>
                </select>
                <select class="form-select form-select-sm" name="theme" onchange="this.form.submit()">
                    <option value="sunset" <?= $theme === 'sunset' ? 'selected' : ''; ?>>Sunset</option>
                    <option value="ocean" <?= $theme === 'ocean' ? 'selected' : ''; ?>>Ocean</option>
                    <option value="forest" <?= $theme === 'forest' ? 'selected' : ''; ?>>Forest</option>
                </select>
            </form>
        </div>
    </div>
</nav>
<main class="py-4">
