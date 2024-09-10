import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import index from "@/views/index/index.vue"
import cs from "@/views/CS/CS.vue"
import csone from "@/views/CS/CS_1725505889816.vue"
import doc from "@/views/main/document.vue"
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: index
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // },
    {
      path: '/index',
      name: 'index',
      component: index,
      children: [
        {path:'/main/document',name:'document',component:doc},
        {path:'/main/cs',name:'cs',component:cs},
        {path:'/main/csone',name:'csone',component:csone},
        ]
    },
  ]
})

export default router
