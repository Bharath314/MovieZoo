export interface MenuChild {
    label: string;
    to: string;
}

export type BadgeSource = 'unreadMessages' | 'pendingOrders';

export interface MenuLink {
    label: string;
    icon: string;
    to?: string;
    badge?: BadgeSource;
    children?: MenuChild[];
}

export interface MenuSection {
    label: string;
    items: MenuLink[];
}

export const menu: MenuSection[] = [
    {
        label: 'Overview',
        items: [
            { label: 'Dashboard', icon: 'oi oi-home', to: '/dashboard' },
        ]
    },
    {
        label: 'Content manager',
        items: [
            { label: 'Venues', icon: 'oi oi-box', to: '/dashboard/venues' },
        ]
    },
];