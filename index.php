<?php require_once __DIR__ . '/includes/header.php'; ?>

<div class="container">
    <section class="hero p-4 p-lg-5 mb-4 shadow-lg">
        <div class="row align-items-center">
            <div class="col-lg-8">
                <h1 class="display-6 fw-bold mb-3"><?= t('hero_title'); ?></h1>
                <p class="lead mb-0"><?= t('hero_subtitle'); ?></p>
            </div>
            <div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
                <span class="badge text-bg-danger"><i class="bi bi-broadcast me-1"></i><?= t('breaking_news'); ?></span>
                <div class="mt-3 d-flex flex-wrap gap-2 justify-content-lg-end">
                    <?php foreach ($newsItems as $item): ?>
                        <?php if ($item['is_breaking']): ?>
                            <a class="badge badge-accent text-decoration-none" href="news.php?id=<?= $item['id']; ?>">
                                <?= htmlspecialchars(localizedText($item, 'title', $lang)); ?>
                            </a>
                        <?php endif; ?>
                    <?php endforeach; ?>
                </div>
            </div>
        </div>
    </section>

    <h2 class="h4 mb-3"><i class="bi bi-stars me-2"></i><?= t('latest_news'); ?></h2>
    <div class="row g-4">
        <?php foreach ($newsItems as $item): ?>
        <div class="col-md-6 col-lg-4">
            <article class="card news-card h-100 shadow-sm">
                <img class="card-img-top news-img" src="<?= htmlspecialchars($item['image']); ?>" alt="<?= htmlspecialchars(localizedText($item, 'title', $lang)); ?>">
                <div class="card-body d-flex flex-column">
                    <div class="d-flex justify-content-between mb-2">
                        <span class="badge text-bg-secondary"><?= htmlspecialchars($item['category']); ?></span>
                        <small><?= htmlspecialchars($item['date']); ?></small>
                    </div>
                    <h3 class="h5"><?= htmlspecialchars(localizedText($item, 'title', $lang)); ?></h3>
                    <p><?= htmlspecialchars(localizedText($item, 'summary', $lang)); ?></p>
                    <a href="news.php?id=<?= $item['id']; ?>" class="btn btn-outline-light mt-auto"><i class="bi bi-arrow-right-circle me-1"></i><?= t('read_more'); ?></a>
                </div>
            </article>
        </div>
        <?php endforeach; ?>
    </div>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
