<?php
require_once __DIR__ . '/includes/header.php';
$query = trim($_GET['q'] ?? '');
$results = $newsItems;
if ($query !== '') {
    $results = array_values(array_filter($newsItems, function (array $item) use ($query, $lang): bool {
        $title = strtolower(localizedText($item, 'title', $lang));
        $category = strtolower($item['category']);
        $needle = strtolower($query);
        return str_contains($title, $needle) || str_contains($category, $needle);
    }));
}
?>
<div class="container">
    <div class="content-card p-4 rounded-4 mb-4">
        <h1 class="h3 mb-3"><i class="bi bi-search-heart me-2"></i><?= t('search'); ?></h1>
        <form class="row g-2" method="get">
            <div class="col-md-10">
                <input class="form-control" name="q" value="<?= htmlspecialchars($query); ?>" placeholder="<?= t('search_placeholder'); ?>">
            </div>
            <div class="col-md-2 d-grid">
                <button class="btn btn-primary"><?= t('search_btn'); ?></button>
            </div>
        </form>
    </div>

    <div class="row g-4">
        <?php if (empty($results)): ?>
            <div class="col-12"><div class="alert alert-secondary"><?= t('no_results'); ?></div></div>
        <?php endif; ?>

        <?php foreach ($results as $item): ?>
            <div class="col-md-6 col-lg-4">
                <article class="card news-card h-100">
                    <img class="card-img-top news-img" src="<?= htmlspecialchars($item['image']); ?>" alt="">
                    <div class="card-body d-flex flex-column">
                        <h2 class="h5"><?= htmlspecialchars(localizedText($item, 'title', $lang)); ?></h2>
                        <p><?= htmlspecialchars(localizedText($item, 'summary', $lang)); ?></p>
                        <a href="news.php?id=<?= $item['id']; ?>" class="btn btn-outline-light mt-auto"><?= t('read_more'); ?></a>
                    </div>
                </article>
            </div>
        <?php endforeach; ?>
    </div>
</div>
<?php require_once __DIR__ . '/includes/footer.php'; ?>
