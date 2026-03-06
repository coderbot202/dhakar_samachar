<?php
require_once __DIR__ . '/includes/header.php';
$id = isset($_GET['id']) ? (int) $_GET['id'] : 0;
$news = findNewsById($id);
?>
<div class="container">
    <?php if (!$news): ?>
        <div class="alert alert-warning">News not found.</div>
    <?php else: ?>
        <article class="content-card p-4 rounded-4 shadow-lg">
            <img class="img-fluid rounded-4 mb-3" src="<?= htmlspecialchars($news['image']); ?>" alt="<?= htmlspecialchars(localizedText($news, 'title', $lang)); ?>">
            <div class="d-flex justify-content-between mb-2">
                <span class="badge badge-accent"><?= htmlspecialchars($news['category']); ?></span>
                <small><?= htmlspecialchars($news['date']); ?></small>
            </div>
            <h1 class="h2 mb-3"><?= htmlspecialchars(localizedText($news, 'title', $lang)); ?></h1>
            <p class="lead"><?= htmlspecialchars(localizedText($news, 'summary', $lang)); ?></p>
            <p><?= htmlspecialchars(localizedText($news, 'content', $lang)); ?></p>
            <a class="btn btn-success" target="_blank" href="https://wa.me/?text=<?= rawurlencode(localizedText($news, 'title', $lang) . ' - ' . (isset($_SERVER['HTTP_HOST']) ? $_SERVER['HTTP_HOST'] : 'localhost')); ?>">
                <i class="bi bi-whatsapp me-2"></i>WhatsApp
            </a>
        </article>
    <?php endif; ?>
</div>
<?php require_once __DIR__ . '/includes/footer.php'; ?>
