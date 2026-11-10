<script setup lang="ts">
import AppSidebar from '@/components/dashboard/AppSidebar.vue';
import AppTopbar from '@/components/dashboard/AppTopbar.vue';
import { useLayout } from '@/components/useLayout';

const { containerClass, overlayOpen, closeOverlay } = useLayout();

</script>

<template>
    <div class="layout" :class="containerClass">
        <AppSidebar />

        <button v-if="overlayOpen" class="layout-mask" type="button" aria-label="Close navigation"
            @click="closeOverlay" />

        <div class="layout-main">
            <AppTopbar />

            <main class="layout-content">
                <RouterView v-slot="{ Component }">
                    <component :is="Component" />
                </RouterView>
            </main>
        </div>

    </div>
</template>

<style>
:root {
    --deni-sidebar-width: 248px;
    --deni-topbar-height: 56px;
    --deni-content-max: 1440px;
    --deni-transition: 140ms cubic-bezier(0.4, 0, 0.2, 1);
    --deni-font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;

    --deni-panel: var(--p-content-background);
    --deni-hover: var(--p-content-hover-background);
    --deni-ground: var(--p-surface-50);
    --deni-scroll: var(--p-surface-300);
    --deni-scroll-hover: var(--p-surface-400);
    --deni-mask: color-mix(in srgb, var(--p-surface-900) 40%, transparent);
}

@media (prefers-color-scheme: dark) {
    :root {
        --deni-ground: var(--p-surface-950);
        --deni-scroll: var(--p-surface-700);
        --deni-scroll-hover: var(--p-surface-600);
    }
}
</style>

<style>
.layout {
    min-height: 100vh;
    background: var(--deni-ground);
}

.layout-main {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    margin-left: var(--deni-sidebar-width);
    transition: margin-left var(--deni-transition);
}

@media (min-width: 1025px) {
    .layout-slim {
        --deni-sidebar-width: 68px;
    }
}

.layout-overlay .layout-main,
.layout-collapsed .layout-main {
    margin-left: 0;
}

.layout-content {
    flex: 1 1 auto;
    padding: 24px 32px 48px;
    width: 100%;
    margin: 0 auto;
}

.layout-boxed .layout-content {
    max-width: var(--deni-content-max);
}

.layout-mask {
    position: fixed;
    inset: 0;
    z-index: 900;
    background: var(--deni-mask);
    border: 0;
    padding: 0;
    cursor: pointer;
}

.fullpage {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 24px;
    background: var(--deni-ground);
}

@media (max-width: 1024px) {
    .layout-main {
        margin-left: 0;
    }

    .layout-content {
        padding: 20px 20px 40px;
    }
}
</style>