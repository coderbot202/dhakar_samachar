<?php require_once __DIR__ . '/includes/header.php'; ?>
<div class="container">
    <h1 class="h3 mb-4"><i class="bi bi-file-earmark-pdf-fill me-2"></i><?= t('epaper'); ?></h1>
    <div class="content-card rounded-4 p-4">
        <div class="table-responsive">
            <table class="table table-dark table-hover align-middle">
                <thead><tr><th>Date</th><th>Edition</th></tr></thead>
                <tbody>
                    <?php foreach ($epapers as $paper): ?>
                        <tr>
                            <td><?= htmlspecialchars($paper['date']); ?></td>
                            <td><a href="<?= htmlspecialchars($paper['file']); ?>" class="btn btn-sm btn-outline-info"><i class="bi bi-eye me-1"></i><?= t('view_epaper'); ?></a></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php require_once __DIR__ . '/includes/footer.php'; ?>
