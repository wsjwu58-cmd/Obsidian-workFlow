<?php
/**
 * Small site-level features owned by the wiki -> WordPress sync.
 * This file is installed as a must-use plugin, so it survives theme changes.
 */
if (!defined('ABSPATH')) {
    exit;
}

add_filter('template_include', static function ($template) {
    if (is_front_page() && !is_paged() && !is_admin()) {
        $module_template = __DIR__ . '/wiki-blog-front-page.php';
        if (is_readable($module_template)) {
            return $module_template;
        }
    }
    return $template;
}, 99);

add_action('wp_head', static function () {
    if (!is_front_page() || is_paged()) {
        return;
    }
    ?>
    <style id="wiki-blog-modules">
        .wbs-module-page { max-width: 1180px; margin: 0 auto; padding: 3rem 2rem 5rem; }
        .wbs-module-hero { max-width: 720px; margin: 0 auto 2.5rem; text-align: center; }
        .wbs-module-kicker { color: #0b8993; font-size: .8rem; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; }
        .wbs-module-hero h1 { margin: .4rem 0 .8rem; font-size: clamp(2rem, 4vw, 3.5rem); }
        .wbs-module-hero p:last-child { color: #6d7375; font-size: 1.05rem; line-height: 1.8; }
        .wbs-module-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.2rem; }
        .wbs-module-card { display: flex; min-height: 165px; flex-direction: column; justify-content: space-between; padding: 1.6rem; border: 1px solid rgba(42, 55, 55, .12); background: rgba(255,255,255,.9); box-shadow: 0 10px 30px rgba(42,55,55,.06); color: inherit; text-decoration: none; transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease; }
        .wbs-module-card:hover, .wbs-module-card:focus { border-color: #0b8993; box-shadow: 0 16px 36px rgba(42,55,55,.12); color: inherit; transform: translateY(-3px); }
        .wbs-module-card h2 { margin: .7rem 0 .35rem; font-size: 1.45rem; }
        .wbs-module-count { color: #6d7375; font-size: .95rem; }
        .wbs-module-enter { color: #0b8993; font-size: .9rem; font-weight: 700; }
        .wbs-module-empty { margin: 0 auto; max-width: 620px; padding: 2rem; text-align: center; color: #6d7375; }
        @media (max-width: 640px) { .wbs-module-page { padding: 2rem 1rem 3rem; } .wbs-module-card { min-height: 140px; } }
    </style>
    <?php
}, 100);
