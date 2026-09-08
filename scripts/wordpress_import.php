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
function managed_posts_by_path($path) {
    return get_posts(['post_type'=>'post', 'post_status'=>['publish','draft','pending','private'],
        'numberposts'=>2, 'meta_key'=>'_wiki_sync_path', 'meta_value'=>$path,
        'suppress_filters'=>true]);
}
function fingerprint($id) {
    $p = get_post($id);
    $cats = wp_get_post_categories($id); sort($cats);
    return hash('sha256', wp_json_encode([$p->post_title, $p->post_content, $p->post_excerpt, $cats]));
}
function normalized_text($value) {
    $value = html_entity_decode(wp_strip_all_tags((string)$value), ENT_QUOTES | ENT_HTML5, 'UTF-8');
    $value = mb_strtolower($value, 'UTF-8');
    return preg_replace('/[\p{P}\p{S}\s]+/u', '', $value) ?? '';
}
function normalized_title($value) {
    $value = normalized_text($value);
    return preg_replace('/(?:知识点梳理|主要功能实现|初步学习|学习笔记|学习|练习|初识|题目操作|题目|总结)$/u', '', $value) ?? $value;
}
function text_similarity($left, $right) {
    $left = preg_split('//u', $left, -1, PREG_SPLIT_NO_EMPTY);
    $right = preg_split('//u', $right, -1, PREG_SPLIT_NO_EMPTY);
    if (count($left) < 3 || count($right) < 3) return 0.0;
    $grams = function($chars) {
        $result = [];
        for ($i = 0; $i <= count($chars) - 3; $i++) {
            $result[implode('', array_slice($chars, $i, 3))] = true;
        }
        return $result;
    };
    $a = $grams($left); $b = $grams($right);
    $intersection = count(array_intersect_key($a, $b));
    $union = count($a) + count($b) - $intersection;
    return $union ? $intersection / $union : 0.0;
}
function ensure_category_path($path) {
    if (!is_array($path) || !$path) fail_sync('Invalid category path');
    $ids = []; $parent = 0;
    foreach ($path as $name) {
        $name = trim(wp_strip_all_tags((string)$name));
        if ($name === '') fail_sync('Empty category name');
        $terms = get_terms(['taxonomy'=>'category', 'hide_empty'=>false, 'parent'=>$parent,
            'name'=>$name, 'number'=>1, 'fields'=>'ids']);
        if (is_wp_error($terms)) fail_sync($terms->get_error_message());
        if ($terms) {
            $id = (int)$terms[0];
        } else {
            $created = wp_insert_term($name, 'category', ['parent'=>$parent]);
            if (is_wp_error($created)) fail_sync($created->get_error_message());
            $id = (int)$created['term_id'];
        }
        $ids[] = $id; $parent = $id;
    }
    return $ids;
}
function find_existing_duplicate($item, $existing) {
    $title = normalized_title($item['title']);
    $content = normalized_text($item['html']);
    foreach ($existing as $post) {
        // Posts already owned by this synchronizer are handled by their stable key.
        if (get_post_meta($post->ID, '_wiki_sync_key', true)) continue;
        $old_title = normalized_title($post->post_title);
        $old_content = normalized_text($post->post_content);
        if ($title !== '' && $title === $old_title && mb_strlen($title, 'UTF-8') >= 4) {
            return ['id'=>(int)$post->ID, 'title'=>$post->post_title, 'reason'=>'normalized title'];
        }
        $title_overlap = mb_strlen($title, 'UTF-8') >= 3 && mb_strlen($old_title, 'UTF-8') >= 3
            && (str_contains($title, $old_title) || str_contains($old_title, $title));
        $similarity = ($content !== '' && $old_content !== '') ? text_similarity($content, $old_content) : 0.0;
        if (($title_overlap && $similarity >= 0.65) || $similarity >= 0.78) {
            return ['id'=>(int)$post->ID, 'title'=>$post->post_title,
                'reason'=>$title_overlap ? 'title and content match' : 'content similarity'];
        }
    }
    return null;
}
try {
    $payload = json_decode(stream_get_contents(STDIN, 8 * 1024 * 1024), true, 512, JSON_THROW_ON_ERROR);
    if (($payload['version'] ?? 0) !== 1) fail_sync('Unsupported payload version');
    $wp_root = realpath($argv[1] ?? '');
    if (!$wp_root || !is_file($wp_root.'/wp-load.php')) fail_sync('WordPress installation not found');
    $lock = fopen(sys_get_temp_dir().'/wiki-blog-'.hash('sha256', $wp_root).'.lock', 'c');
    if (!$lock || !flock($lock, LOCK_EX | LOCK_NB)) fail_sync('Another blog sync is running');
    define('WP_USE_THEMES', false);
    require $wp_root.'/wp-load.php';
    require_once ABSPATH.'wp-admin/includes/file.php';
    require_once ABSPATH.'wp-admin/includes/media.php';
    require_once ABSPATH.'wp-admin/includes/image.php';
    if (untrailingslashit(get_option('home')) !== untrailingslashit($payload['site_url'])) fail_sync('Site identity mismatch');
    $author = (int)$payload['author_id'];
    wp_set_current_user($author);
    if (!current_user_can('edit_posts') || !current_user_can('upload_files')) fail_sync('Invalid import author');
    $wiki = realpath($payload['repo'].'/wiki');
    if (!$wiki) fail_sync('wiki root not found');
    $repo = realpath($payload['repo']);
    $external = realpath($payload['repo'].'/.blog-sync-external');
    $status = ($payload['status'] ?? 'draft') === 'publish' ? 'publish' : 'draft';
    $report = ['mode'=>'apply','created'=>[], 'updated'=>[], 'unchanged'=>[], 'published'=>[], 'comments_opened'=>[], 'duplicates'=>[], 'conflicts'=>[], 'errors'=>[]];
    $ids = []; $blocked = [];
    $existing = get_posts(['post_type'=>'post', 'post_status'=>['publish','draft','pending','private'],
        'numberposts'=>-1, 'suppress_filters'=>true]);
    // Inspect every existing article before touching its content or its media.
    foreach ($payload['posts'] as $item) {
        $key = $item['key'];
        if (!preg_match('/^[a-z0-9][a-z0-9-]{2,79}$/D', $key) || isset($ids[$key])) fail_sync('Duplicate or invalid note key');
        $matches = managed_posts($key);
        if (!$matches) {
            $path_matches = managed_posts_by_path($item['path']);
            if (count($path_matches) === 1) {
                // Migrate a legacy explicit-config identity to the automatic path identity.
                update_post_meta($path_matches[0]->ID, '_wiki_sync_key', $key);
                $matches = $path_matches;
            } elseif (count($path_matches) > 1) {
                fail_sync('Duplicate WordPress path identity: '.$item['path']);
            }
        }
        if (count($matches) > 1) fail_sync('Duplicate WordPress identity: '.$key);
        if ($matches) {
            $id = $matches[0]->ID;
            // Comment availability is a site feature, not wiki content. Repair
            // old imports even when their source hash is unchanged.
            if ($matches[0]->post_status !== 'trash' && $matches[0]->comment_status !== 'open') {
                $opened = wp_update_post(['ID'=>$id, 'comment_status'=>'open'], true);
                if (is_wp_error($opened)) fail_sync($opened->get_error_message());
                $report['comments_opened'][] = ['key'=>$key, 'id'=>$id];
            }
            $saved = get_post_meta($id, '_wiki_sync_fingerprint', true);
            if ($matches[0]->post_status === 'trash' || !$saved || !hash_equals($saved, fingerprint($id))) {
                $report['conflicts'][] = ['key'=>$key,'id'=>$id,'reason'=>'WordPress content was edited or trashed; retained'];
                $blocked[$key] = true;
            }
            $ids[$key] = $id;
        } else {
            $ids[$key] = 0;
            $duplicate = find_existing_duplicate($item, $existing);
            if ($duplicate) {
                // This is a high-confidence match for a legacy, unmanaged
                // post. Adopt it so the note is not lost and its category
                // follows the source folder instead of creating a duplicate.
                update_post_meta($duplicate['id'], '_wiki_sync_key', $key);
                update_post_meta($duplicate['id'], '_wiki_sync_path', $item['path']);
                $ids[$key] = $duplicate['id'];
                $report['duplicates'][] = ['key'=>$key, 'id'=>$duplicate['id'],
                    'title'=>$duplicate['title'], 'reason'=>$duplicate['reason'], 'action'=>'adopted'];
            }
        }
    }
    // Upload image bytes that were staged by the renderer. The renderer only
    // stages local wiki files or images from the configured host allowlist.
    $asset_urls = [];
    foreach ($payload['assets'] as $sha=>$relative) {
        $used = false;
        foreach ($payload['posts'] as $item) {
            if (!isset($blocked[$item['key']]) && str_contains($item['html'], 'wiki-asset:'.$sha)) $used = true;
        }
        if (!$used) continue;
        $file = realpath($payload['repo'].'/'.$relative);
        $in_wiki = $file && str_starts_with($file, $wiki.DIRECTORY_SEPARATOR);
        $in_external = $file && $external && str_starts_with($file, $external.DIRECTORY_SEPARATOR);
        if (!$file || (!$in_wiki && !$in_external)) fail_sync('Image outside allowed staging roots');
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
            $category_ids = ensure_category_path($item['category_path'] ?? [$item['category']]);
            $cat_id = end($category_ids);
            $source_hash = hash('sha256', wp_json_encode([$title, $content, $cat_id]));
            $id = $ids[$key];
            if ($id && get_post_meta($id, '_wiki_sync_source_hash', true) === $source_hash) {
                update_post_meta($id, '_wiki_sync_path', $item['path']);
                if ($status === 'publish' && get_post_status($id) === 'draft') {
                    $saved = wp_update_post(['ID'=>$id, 'post_status'=>'publish'], true);
                    if (is_wp_error($saved)) fail_sync($saved->get_error_message());
                    $report['updated'][] = ['key'=>$key, 'id'=>$id, 'status'=>'publish'];
                } else {
                    $report['unchanged'][] = ['key'=>$key,'id'=>$id];
                }
                continue;
            }
            $data = ['post_title'=>$title,'post_content'=>$content,'post_type'=>'post',
                'post_category'=>$category_ids, 'ping_status'=>'closed', 'comment_status'=>'open'];
            if ($id) {
                $data['ID'] = $id;
                if ($status === 'publish' && get_post_status($id) === 'draft') $data['post_status'] = 'publish';
            }
            else {
                $data['post_status'] = $status; $data['post_author'] = $author;
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
    // The configured sync mode is authoritative for managed notes. This also
    // repairs legacy drafts/pending posts on later runs without touching trash
    // or posts that were blocked as conflicts above.
    if ($status === 'publish') {
        foreach (array_unique(array_filter(array_map('intval', array_values($ids)))) as $managed_id) {
            if (get_post_status($managed_id) === 'trash' || get_post_status($managed_id) === 'publish') continue;
            $saved = wp_update_post(['ID'=>$managed_id, 'post_status'=>'publish'], true);
            if (is_wp_error($saved)) fail_sync($saved->get_error_message());
            $report['published'][] = ['id'=>$managed_id];
        }
    }
    echo wp_json_encode($report, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES).PHP_EOL;
} catch (Throwable $e) { fwrite(STDERR, $e->getMessage().PHP_EOL); exit(1); }
