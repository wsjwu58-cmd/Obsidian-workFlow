<?php
/** @var string $template */
get_header();

$categories = get_terms([
    'taxonomy' => 'category',
    'hide_empty' => true,
    'orderby' => 'name',
    'order' => 'ASC',
]);
$modules = [];
if (!is_wp_error($categories)) {
    foreach ($categories as $category) {
        if ((int)$category->parent !== 0 || in_array($category->slug, ['uncategorized', 'wei-fen-lei'], true)) {
            continue;
        }
        $note_ids = get_posts([
            'post_type' => 'post',
            'post_status' => 'publish',
            'category' => $category->term_id,
            'posts_per_page' => -1,
            'fields' => 'ids',
            'no_found_rows' => true,
            'meta_query' => [[
                'key' => '_wiki_sync_key',
                'compare' => 'EXISTS',
            ]],
        ]);
        if (!$note_ids) {
            continue;
        }
        $modules[] = [
            'term' => $category,
            'count' => count($note_ids),
        ];
    }
}
?>
<div id="container" class="bravada-landing-page one-column wbs-module-page">
    <main id="main" class="main">
        <header class="wbs-module-hero">
            <div class="wbs-module-kicker">Knowledge Base</div>
            <h1>按模块浏览笔记</h1>
            <p>把知识按主题收好。选择一个模块，进入该模块的笔记列表。</p>
        </header>

        <?php if ($modules) : ?>
            <section class="wbs-module-grid" aria-label="笔记模块">
                <?php foreach ($modules as $module) : $term = $module['term']; ?>
                    <a class="wbs-module-card" href="<?php echo esc_url(get_category_link($term->term_id)); ?>">
                        <span>
                            <h2><?php echo esc_html($term->name); ?></h2>
                            <span class="wbs-module-count"><?php echo esc_html($module['count']); ?> 篇笔记</span>
                        </span>
                        <span class="wbs-module-enter">进入模块 →</span>
                    </a>
                <?php endforeach; ?>
            </section>
        <?php else : ?>
            <p class="wbs-module-empty">暂时还没有可展示的笔记模块。</p>
        <?php endif; ?>
    </main>
</div>
<?php get_footer();
