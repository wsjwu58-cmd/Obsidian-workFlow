<?php
// CLI only: never place this file in the public document root.
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
ini_set('display_errors', 'stderr');
function fail_sync($message) { throw new RuntimeException($message); }
function managed_posts($key, $type = 'post') {
    return get_posts(['post_type'=>$type, 'post_status'=>array_keys(get_post_stati()),
        'numberposts'=>2, 'meta_key'=>$type === 'post' ? '_wiki_sync_key' : '_wiki_asset_hash',
        'meta_value'=>$key, 'suppress_filters'=>true]);
}
function fingerprint($id) {
    $p = get_post($id);
    $cats = wp_get_post_categories($id); sort($cats);
    return hash('sha256', wp_json_encode([$p->post_title, $p->post_content, $p->post_excerpt, $cats]));
}
try {
    $payload = json_decode(stream_get_contents(STDIN, 8 * 1024 * 1024), true, 512, JSON_THROW_ON_ERROR);
    if (($payload['version'] ?? 0) !== 1) fail_sync('Unsupported payload version');
    $wp = realpath($argv[1] ?? '');
    if (!$wp || !is_file($wp.'/wp-load.php')) fail_sync('WordPress installation not found');
    $lock = fopen(sys_get_temp_dir().'/wiki-blog-'.hash('sha256', $wp).'.lock', 'c');
    if (!$lock || !flock($lock, LOCK_EX | LOCK_NB)) fail_sync('Another blog sync is running');
    define('WP_USE_THEMES', false);
    require $wp.'/wp-load.php';
    require_once ABSPATH.'wp-admin/includes/file.php';
    require_once ABSPATH.'wp-admin/includes/media.php';
    require_once ABSPATH.'wp-admin/includes/image.php';
    if (untrailingslashit(get_option('home')) !== untrailingslashit($payload['site_url'])) fail_sync('Site identity mismatch');
    $author = (int)$payload['author_id'];
    wp_set_current_user($author);
    if (!current_user_can('edit_posts') || !current_user_can('upload_files')) fail_sync('Invalid import author');
    $wiki = realpath($payload['repo'].'/wiki');
    if (!$wiki) fail_sync('wiki root not found');
    $report = ['mode'=>'apply','created'=>[], 'updated'=>[], 'unchanged'=>[], 'conflicts'=>[], 'errors'=>[]];
    $ids = []; $blocked = [];
    // Inspect every existing article before touching its content or its media.
    foreach ($payload['posts'] as $item) {
        $key = $item['key'];
        if (!preg_match('/^[a-z0-9][a-z0-9-]{2,79}$/D', $key) || isset($ids[$key])) fail_sync('Duplicate or invalid note key');
        $matches = managed_posts($key);
        if (count($matches) > 1) fail_sync('Duplicate WordPress identity: '.$key);
        if ($matches) {
            $id = $matches[0]->ID;
            $saved = get_post_meta($id, '_wiki_sync_fingerprint', true);
            if ($matches[0]->post_status === 'trash' || !$saved || !hash_equals($saved, fingerprint($id))) {
                $report['conflicts'][] = ['key'=>$key,'id'=>$id,'reason'=>'WordPress content was edited or trashed; retained'];
                $blocked[$key] = true;
            }
            $ids[$key] = $id;
        } else { $ids[$key] = 0; }
    }
    // Upload local image bytes only; no HTTP request, DNS lookup, or remote credential.
    $asset_urls = [];
    foreach ($payload['assets'] as $sha=>$relative) {
        $used = false;
        foreach ($payload['posts'] as $item) {
            if (!isset($blocked[$item['key']]) && str_contains($item['html'], 'wiki-asset:'.$sha)) $used = true;
        }
        if (!$used) continue;
        $file = realpath($payload['repo'].'/'.$relative);
        if (!$file || !str_starts_with($file, $wiki.DIRECTORY_SEPARATOR)) fail_sync('Image outside wiki');
        if (!preg_match('/^[a-f0-9]{64}$/D', $sha) || !hash_equals($sha, hash_file('sha256', $file))) fail_sync('Image hash mismatch');
        if (filesize($file) > min((int)$payload['max_image_bytes'], 10485760)) fail_sync('Image too large');
        $mime = wp_get_image_mime($file);
        if (!in_array($mime, ['image/png','image/jpeg','image/gif','image/webp'], true)) fail_sync('Invalid image bytes');
        $matches = managed_posts($sha, 'attachment');
        if (count($matches) > 1) fail_sync('Duplicate attachment hash');
        if ($matches && is_file(get_attached_file($matches[0]->ID))) {
            $attachment = $matches[0]->ID;
        } else {
            $tmp = wp_tempnam(basename($file));
            if (!$tmp || !copy($file, $tmp)) fail_sync('Cannot stage image');
            $extension = ['image/png'=>'png','image/jpeg'=>'jpg','image/gif'=>'gif','image/webp'=>'webp'][$mime];
            $attachment = media_handle_sideload(['name'=>'wiki-'.$sha.'.'.$extension,'tmp_name'=>$tmp], 0);
            if (is_wp_error($attachment)) { @unlink($tmp); fail_sync($attachment->get_error_message()); }
            update_post_meta($attachment, '_wiki_asset_hash', $sha);
        }
        $asset_urls[$sha] = wp_get_attachment_url($attachment);
    }
    foreach ($payload['posts'] as $item) {
        $key = $item['key'];
        if (isset($blocked[$key])) continue;
        try {
            $content = preg_replace_callback('/wiki-asset:([a-f0-9]{64})/', function($m) use ($asset_urls) {
                if (!isset($asset_urls[$m[1]])) fail_sync('Missing uploaded image');
                return esc_url($asset_urls[$m[1]]);
            }, $item['html']);
            // Draft targets remain plain text; publishing a target makes this a link on the next sync.
            $content = preg_replace_callback('/<a href="wiki-note:([a-z0-9-]+)">(.*?)<\/a>/s', function($m) use ($ids) {
                $id = $ids[$m[1]] ?? 0;
                if ($id && get_post_status($id) === 'publish') return '<a href="'.esc_url(get_permalink($id)).'">'.$m[2].'</a>';
                return $m[2];
            }, $content);
            $content = preg_replace('/<a data-wiki-unpublished="true">(.*?)<\/a>/s', '$1', $content);
            $content = wp_kses_post($content);
            $title = wp_strip_all_tags($item['title']);
            $category = term_exists($item['category'], 'category');
            if (!$category) $category = wp_insert_term($item['category'], 'category');
            if (is_wp_error($category)) fail_sync($category->get_error_message());
            $cat_id = (int)(is_array($category) ? $category['term_id'] : $category);
            $source_hash = hash('sha256', wp_json_encode([$title, $content, $cat_id]));
            $id = $ids[$key];
            if ($id && get_post_meta($id, '_wiki_sync_source_hash', true) === $source_hash) {
                update_post_meta($id, '_wiki_sync_path', $item['path']);
                $report['unchanged'][] = ['key'=>$key,'id'=>$id];
                continue;
            }
            $data = ['post_title'=>$title,'post_content'=>$content,'post_type'=>'post',
                'post_category'=>[$cat_id], 'ping_status'=>'closed', 'comment_status'=>'closed'];
            if ($id) $data['ID'] = $id;
            else {
                $data['post_status'] = 'draft'; $data['post_author'] = $author;
                $data['post_name'] = 'wiki-'.$key;
                $data['meta_input'] = ['_wiki_sync_key'=>$key];
            }
            $saved = wp_insert_post(wp_slash($data), true);
            if (is_wp_error($saved)) fail_sync($saved->get_error_message());
            update_post_meta($saved, '_wiki_sync_path', $item['path']);
            update_post_meta($saved, '_wiki_sync_source_hash', $source_hash);
            update_post_meta($saved, '_wiki_sync_fingerprint', fingerprint($saved));
            $report[$id ? 'updated' : 'created'][] = ['key'=>$key, 'id'=>$saved, 'status'=>get_post_status($saved)];
            $ids[$key] = $saved;
        } catch (Throwable $e) { $report['errors'][] = ['key'=>$key, 'reason'=>$e->getMessage()]; }
    }
    echo wp_json_encode($report, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES).PHP_EOL;
} catch (Throwable $e) { fwrite(STDERR, $e->getMessage().PHP_EOL); exit(1); }
