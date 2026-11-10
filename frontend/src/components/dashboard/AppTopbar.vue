<script setup lang="ts">
import Avatar from 'openvue/avatar';
import Badge from 'openvue/badge';
import Button from 'openvue/button';
import Menu from 'openvue/menu';
import Popover from 'openvue/popover';
import type { MenuItem } from 'openvue/menuitem';
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useTheme } from '@/composables/useTheme';
import { formatRelative } from '@/utils/format';
import AppBreadcrumb from './AppBreadcrumb.vue';
import AppSearchDialog from './AppSearchDialog.vue';
import { useLayout } from '../useLayout.ts';
// TODO: Optimize icons
import '@openvue/openicons/openicons.css';
import { useAuthStore } from '@/stores/auth.ts';

const router = useRouter();
const authStore = useAuthStore();
const { toggleSidebar, openConfigurator, searchOpen } = useLayout();
const { isDark, themeIcon, toggleDark } = useTheme();

const notifications = ref<InstanceType<typeof Popover> | null>(null);
const userMenu = ref<InstanceType<typeof Menu> | null>(null);

const alerts = [
    { id: 'n1', title: 'Order #48219 was refunded', at: '2026-08-30T07:42:00Z', icon: 'oi oi-undo' },
    { id: 'n2', title: 'Aero Keyboard is out of stock', at: '2026-08-30T05:10:00Z', icon: 'oi oi-exclamation-triangle' },
    { id: 'n3', title: 'Priya Raman accepted an invite', at: '2026-08-29T16:03:00Z', icon: 'oi oi-user-plus' },
    { id: 'n4', title: 'Weekly report is ready', at: '2026-08-29T08:00:00Z', icon: 'oi oi-file' }
];

const logout = () => {
    authStore.logout();
    router.push({ name: 'home' })
}

const userItems: MenuItem[] = [
    // { label: 'Profile', icon: 'pi pi-user', command: () => router.push('/profile') },
    // { label: 'Settings', icon: 'pi pi-cog', command: () => router.push('/settings') },
    // { separator: true },
    { label: 'Sign out', icon: 'oi oi-sign-out', command: logout }
];

const alertCount = computed(() => (alerts.length > 99 ? '99+' : String(alerts.length)));

const toggleNotifications = (event: Event) => {
    notifications.value?.toggle(event);
};

const toggleUserMenu = (event: Event) => {
    userMenu.value?.toggle(event);
};

const onKeydown = (event: KeyboardEvent) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        searchOpen.value = true;
    }
};

onMounted(() => window.addEventListener('keydown', onKeydown));
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown));
</script>

<template>
    <header class="topbar">
        <div class="topbar-left">
            <Button icon="oi oi-bars" severity="secondary" text rounded aria-label="Toggle navigation"
                @click="toggleSidebar" />
            <AppBreadcrumb />
        </div>

        <div class="topbar-right">
            <button type="button" class="topbar-user" aria-haspopup="true" @click="toggleUserMenu">
                <Avatar :label="authStore.full_name?.[0]" shape="circle" size="normal" />
                <span class="topbar-user-name">{{ authStore.full_name }}</span>
                <i class="oi oi-angle-down muted" style="font-size: 12px" />
            </button>
        </div>

        <!-- <Popover ref="notifications">
            <div style="width: 320px">
                <p
                    style="font-size: 12px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--p-text-muted-color); padding: 0 4px 8px">
                    Notifications</p>

                <button v-for="alert in alerts" :key="alert.id" type="button" class="search-result"
                    style="align-items: flex-start">
                    <i :class="alert.icon" style="margin-top: 2px" />
                    <span style="display: block">
                        <span style="display: block; font-size: 13px">{{ alert.title }}</span>
                        <span class="cell-sub">{{ formatRelative(alert.at) }}</span>
                    </span>
                </button>
            </div>
        </Popover> -->

        <Menu ref="userMenu" :model="userItems" :popup="true" />
        <AppSearchDialog v-model="searchOpen" />
    </header>
</template>

<style scoped>
.topbar {
    position: sticky;
    top: 0;
    z-index: 800;
    display: flex;
    align-items: center;
    gap: 12px;
    height: var(--deni-topbar-height);
    padding: 0 20px;
    background: var(--deni-panel);
    border-bottom: 1px solid var(--p-content-border-color);
}

.topbar-left {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;
}

.topbar-right {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-left: auto;
}

.topbar-search {
    display: flex;
    align-items: center;
    gap: 8px;
    width: 260px;
    padding: 6px 10px;
    border: 1px solid var(--p-content-border-color);
    border-radius: 4px;
    background: var(--deni-ground);
    color: var(--p-text-muted-color);
    font: inherit;
    font-size: 13px;
    cursor: pointer;
    transition: border-color var(--deni-transition);

    &:hover {
        border-color: var(--p-text-muted-color);
    }

    i {
        font-size: 14px;
    }
}

.topbar-search-key {
    margin-left: auto;
    padding: 1px 5px;
    border: 1px solid var(--p-content-border-color);
    border-radius: 3px;
    background: var(--deni-panel);
    font-size: 11px;
    font-weight: 600;
}

.topbar-notify {
    position: relative;
    display: inline-flex;
}

.topbar-notify-badge {
    position: absolute;
    top: 1px;
    right: 0;
    pointer-events: none;
}

.topbar-divider {
    width: 1px;
    height: 20px;
    margin: 0 6px;
    background: var(--p-content-border-color);
}

.topbar-user {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 8px 4px 4px;
    border: 0;
    border-radius: 4px;
    background: transparent;
    font: inherit;
    cursor: pointer;

    &:hover {
        background: var(--deni-hover);
    }
}

.topbar-user-name {
    font-size: 13px;
    font-weight: 600;
}

.search-result {
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
    padding: 9px 10px;
    border: 0;
    border-radius: 4px;
    background: transparent;
    font: inherit;
    text-align: left;
    cursor: pointer;

    &:hover,
    &:focus-visible {
        background: var(--deni-hover);
        outline: none;
    }

    i {
        color: var(--p-text-muted-color);
        font-size: 14px;
    }
}

.search-result-group {
    margin-left: auto;
    font-size: 11px;
    color: var(--p-text-muted-color);
}

@media (max-width: 768px) {
    .topbar {
        padding: 0 12px;
    }

    .topbar-search {
        width: auto;

        span:not(.topbar-search-key) {
            display: none;
        }
    }

    .topbar-search-key,
    .topbar-user-name,
    .topbar-left .p-breadcrumb {
        display: none;
    }

    .topbar-divider {
        margin: 0 2px;
    }
}
</style>