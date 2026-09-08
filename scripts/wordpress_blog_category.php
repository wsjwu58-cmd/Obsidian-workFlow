<?php
/** Category archive for the wiki blog: module -> subfolder -> notes. */
get_header();
$term = get_queried_object();
$children = get_terms([
    'taxonomy' => 'category',
    'parent' => (int)$term->term_id,
    'hide_empty' => true,
    'orderby' => 'name',
    'order' => 'ASC',
]);
$child_ids = [];
if (!is_wp_error($children)) {
    $child_ids = array_map(static fn($child) => (int)$child->term_id, $children);
}

$managed = [
    'post_type' => 'post',
    'post_status' => 'publish',
    'posts_per_page' => -1,
    'orderby' => 'date',
    'order' => 'DESC',
    'no_found_rows' => true,
    'meta_query' => [[
        'key' => '_wiki_sync_key',
        'compare' => 'EXISTS',
    ]],
];
$root_query = $managed;
$root_query['tax_query'] = [[
    'taxonomy' => 'category',
    'field' => 'term_id',
    'terms' => (int)$term->term_id,
    'include_children' => false,
]];
if ($child_ids) {
    $root_query['tax_query'][] = [
        'taxonomy' => 'category',
        'field' => 'term_id',
        'terms' => $child_ids,
        'operator' => 'NOT IN',
    ];
}
$root_posts = get_posts($root_query);
?>
<div id="container" class="bravada-landing-page one-column wbs-category-page">
    <main id="main" class="main">
        <header class="wbs-category-hero">
            <a class="wbs-category-back" href="<?php echo esc_url(home_url('/')); ?>">← 返回全部模块</a>
            <h1><?php echo esc_html($term->name); ?></h1>
            <p>按子文件夹整理笔记，选择一个主题继续阅读。</p>
        </header>

        <?php if ($child_ids) : ?>
            <section class="wbs-submodule-grid" aria-label="子文件夹">
                <?php foreach ($children as $child) :
                    $child_posts = get_posts(array_merge($managed, ['cat' => (int)$child->term_id, 'fields' => 'ids']));
                ?>
                    <a class="wbs-submodule-card" href="#submodule-<?php echo esc_attr($child->term_id); ?>">
                        <h2><?php echo esc_html($child->name); ?></h2>
                        <span><?php echo esc_html(count($child_posts)); ?> 篇笔记</span>
                    </a>
                <?php endforeach; ?>
            </section>
        <?php endif; ?>

        <?php if ($root_posts) : ?>
            <section class="wbs-note-group" id="submodule-root">
                <h2>模块根目录</h2>
                <div class="wbs-note-grid">
                    <?php foreach ($root_posts as $post) : ?>
                        <a class="wbs-note-card" href="<?php echo esc_url(get_permalink($post)); ?>">
                            <h3><?php echo esc_html(get_the_title($post)); ?></h3>
                            <span class="wbs-note-meta"><?php echo comments_open($post) ? '可发表评论' : '暂不开放评论'; ?></span>
                        </a>
                    <?php endforeach; ?>
                </div>
            </section>
        <?php endif; ?>

        <?php foreach ($children as $child) :
            $posts = get_posts(array_merge($managed, ['cat' => (int)$child->term_id]));
            if (!$posts) continue;
        ?>
            <section class="wbs-note-group" id="submodule-<?php echo esc_attr($child->term_id); ?>">
                <h2><?php echo esc_html($child->name); ?></h2>
                <div class="wbs-note-grid">
                    <?php foreach ($posts as $post) : ?>
                        <a class="wbs-note-card" href="<?php echo esc_url(get_permalink($post)); ?>">
                            <h3><?php echo esc_html(get_the_title($post)); ?></h3>
                            <span class="wbs-note-meta"><?php echo comments_open($post) ? '可发表评论' : '暂不开放评论'; ?></span>
                        </a>
                    <?php endforeach; ?>
                </div>
            </section>
        <?php endforeach; ?>

        <?php if (!$root_posts && !$child_ids) : ?>
            <p class="wbs-note-empty">这个模块暂时没有可展示的笔记。</p>
        <?php endif; ?>
    </main>
</div>
<?php get_footer();
