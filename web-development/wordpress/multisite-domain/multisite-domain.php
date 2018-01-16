<?php

/*
Plugin Name: Multisite Domain Displayer
Description: Display the domain name of each site instead of the title.
Version 2.0.0
Author: Alexander Barber
License: MIT
 */

function multisite_domain_switch () {

    global $wp_admin_bar;

    $blavatar = '<div class="blavatar"></div>';

    foreach ((array) $wp_admin_bar->user->blogs as $blog) {

        $menu_id  = 'blog-' . $blog->userblog_id;
        if (defined('SUBDOMAIN_INSTALL') && SUBDOMAIN_INSTALL) {
            $blogname = $blog->domain;
        } else {
            $blogname = $blog->path;
        }
        $wp_admin_bar->add_menu([
            'parent'    => 'my-sites-list',
            'id'        => $menu_id,
            'title'     => $blavatar . $blogname,
            'href'      => get_admin_url($blog->userblog_id)
        ]);

    }
}

add_action('wp_before_admin_bar_render', 'multisite_domain_switch');
