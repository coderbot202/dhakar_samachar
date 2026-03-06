<?php
require_once __DIR__ . '/includes/header.php';

$action = $_GET['action'] ?? 'dashboard';
$error = '';
$success = '';

if ($action === 'logout') {
    $_SESSION['is_admin_logged_in'] = false;
    header('Location: admin.php?action=login');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $action === 'login') {
    $username = trim((string) ($_POST['username'] ?? ''));
    $password = trim((string) ($_POST['password'] ?? ''));

    if ($username === $adminUsername && $password === $adminPassword) {
        $_SESSION['is_admin_logged_in'] = true;
        header('Location: admin.php');
        exit;
    }

    $error = 'Invalid admin credentials.';
}

if (!isAdminLoggedIn() && $action !== 'login') {
    header('Location: admin.php?action=login');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $action === 'create') {
    requireAdminAuth();

    $title = trim((string) ($_POST['title'] ?? ''));
    $summary = trim((string) ($_POST['summary'] ?? ''));
    $content = trim((string) ($_POST['content'] ?? ''));

    if ($title === '' || $summary === '' || $content === '') {
        $error = 'Title, summary, and content are required.';
    } else {
        addManagedNewsItem([
            'title' => $title,
            'title_bn' => trim((string) ($_POST['title_bn'] ?? '')),
            'summary' => $summary,
            'summary_bn' => trim((string) ($_POST['summary_bn'] ?? '')),
            'content' => $content,
            'content_bn' => trim((string) ($_POST['content_bn'] ?? '')),
            'category' => trim((string) ($_POST['category'] ?? 'General')),
            'image' => trim((string) ($_POST['image'] ?? '')),
            'date' => trim((string) ($_POST['date'] ?? date('Y-m-d'))),
            'is_breaking' => !empty($_POST['is_breaking']),
        ]);
        $success = 'News uploaded successfully.';
    }
}

if ($action === 'delete' && isset($_GET['id'])) {
    requireAdminAuth();
    removeManagedNewsItem((int) $_GET['id']);
    header('Location: admin.php?deleted=1');
    exit;
}

if (isset($_GET['deleted'])) {
    $success = 'Uploaded news deleted successfully.';
}

$allNews = getNewsItems();
$managedIds = array_map(static fn(array $item): int => (int) ($item['id'] ?? 0), loadManagedNewsItems());
?>

<div class="container">
    <?php if ($action === 'login' && !isAdminLoggedIn()): ?>
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-5">
                <div class="content-card p-4 rounded-4">
                    <h1 class="h4 mb-3"><i class="bi bi-shield-lock me-2"></i>Admin Login</h1>
                    <?php if ($error !== ''): ?>
                        <div class="alert alert-danger"><?= htmlspecialchars($error); ?></div>
                    <?php endif; ?>
                    <form method="post" action="admin.php?action=login">
                        <div class="mb-3">
                            <label class="form-label">Username</label>
                            <input class="form-control" name="username" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input class="form-control" name="password" type="password" required>
                        </div>
                        <button class="btn btn-primary w-100">Login</button>
                    </form>
                </div>
            </div>
        </div>
    <?php else: ?>
        <div class="d-flex flex-wrap justify-content-between align-items-center mb-3 gap-2">
            <h1 class="h3 mb-0">Admin Panel - Day-to-Day Upload</h1>
            <a class="btn btn-outline-light" href="admin.php?action=logout"><i class="bi bi-box-arrow-right me-1"></i>Logout</a>
        </div>

        <?php if ($error !== ''): ?>
            <div class="alert alert-danger"><?= htmlspecialchars($error); ?></div>
        <?php endif; ?>
        <?php if ($success !== ''): ?>
            <div class="alert alert-success"><?= htmlspecialchars($success); ?></div>
        <?php endif; ?>

        <div class="content-card p-4 rounded-4 mb-4">
            <h2 class="h5 mb-3">Upload News</h2>
            <form method="post" action="admin.php?action=create" class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">Title (English)</label>
                    <input class="form-control" name="title" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Title (Bangla)</label>
                    <input class="form-control" name="title_bn">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Category</label>
                    <input class="form-control" name="category" value="General">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Date</label>
                    <input class="form-control" type="date" name="date" value="<?= htmlspecialchars(date('Y-m-d')); ?>">
                </div>
                <div class="col-12">
                    <label class="form-label">Image URL</label>
                    <input class="form-control" name="image" placeholder="https://...">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Summary (English)</label>
                    <textarea class="form-control" name="summary" rows="3" required></textarea>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Summary (Bangla)</label>
                    <textarea class="form-control" name="summary_bn" rows="3"></textarea>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Content (English)</label>
                    <textarea class="form-control" name="content" rows="5" required></textarea>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Content (Bangla)</label>
                    <textarea class="form-control" name="content_bn" rows="5"></textarea>
                </div>
                <div class="col-12 form-check ms-1">
                    <input class="form-check-input" type="checkbox" value="1" id="isBreaking" name="is_breaking">
                    <label class="form-check-label" for="isBreaking">Mark as breaking news</label>
                </div>
                <div class="col-12">
                    <button class="btn btn-danger"><i class="bi bi-cloud-upload me-1"></i>Publish News</button>
                </div>
            </form>
        </div>

        <div class="content-card p-4 rounded-4">
            <h2 class="h5 mb-3">All News</h2>
            <div class="table-responsive">
                <table class="table table-striped align-middle">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Title</th>
                            <th>Category</th>
                            <th>Date</th>
                            <th>Source</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($allNews as $item): ?>
                            <?php $isManaged = in_array((int) $item['id'], $managedIds, true); ?>
                            <tr>
                                <td><?= (int) $item['id']; ?></td>
                                <td><?= htmlspecialchars($item['title']); ?></td>
                                <td><?= htmlspecialchars($item['category']); ?></td>
                                <td><?= htmlspecialchars($item['date']); ?></td>
                                <td><?= $isManaged ? '<span class="badge text-bg-success">Uploaded</span>' : '<span class="badge text-bg-secondary">Seed</span>'; ?></td>
                                <td>
                                    <?php if ($isManaged): ?>
                                        <a class="btn btn-sm btn-outline-danger" href="admin.php?action=delete&id=<?= (int) $item['id']; ?>" onclick="return confirm('Delete this uploaded news?');">Delete</a>
                                    <?php else: ?>
                                        <span class="text-muted small">Not editable</span>
                                    <?php endif; ?>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    <?php endif; ?>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
