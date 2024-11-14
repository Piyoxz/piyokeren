import { createRouter, createWebHistory } from 'vue-router';
import Index from "@/pages/index.vue";
import Register from "@/pages/register.vue";
import Add from "@/pages/tambah.vue";
import Edit from "@/pages/ubah.vue";

const routes = [
    {
        path: '/',
        name: "IndexPage",
        component: Index,
    },
    {
        path: "/register",
        name: "RegisterPage",
        component: Register,
    },
    {
        path: "/add",
        name: "AddPage",
        component: Add,
    },
    {
        path: "/edit",
        name: "EditPage",
        component: Edit,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Check localStorage before each route
router.beforeEach((to, from, next) => {
    const userName = localStorage.getItem('userName'); // Check if user is registered

    // If the user is not registered and tries to go anywhere except '/register', redirect them to '/register'
    if (!userName && to.path !== '/register') {
        next('/register');
    }
    // If the user is registered and tries to go to '/register', redirect them to '/'
    else if (userName && to.path === '/register') {
        next('/');
    }
    // Otherwise, proceed to the requested route
    else {
        next();
    }
});

export default router;
