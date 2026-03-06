<?php require_once __DIR__ . '/includes/header.php'; ?>
<div class="container">
    <h1 class="h3 mb-4"><i class="bi bi-camera-reels-fill me-2"></i><?= t('shorts'); ?></h1>
    <div class="row g-4">
        <?php foreach ($shorts as $item): ?>
            <div class="col-md-6">
                <div class="content-card p-3 rounded-4 h-100">
                    <div class="ratio ratio-16x9 mb-3">
                        <iframe src="<?= htmlspecialchars($item['embed']); ?>" title="short-video" allowfullscreen></iframe>
                    </div>
                    <p class="mb-0"><?= htmlspecialchars(localizedText($item, 'caption', $lang)); ?></p>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
</div>
<?php require_once __DIR__ . '/includes/footer.php'; ?>
