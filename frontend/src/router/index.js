import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '@/components/Login.vue'
import Deposit from '@/components/Deposit.vue'
import Withdraw from '@/components/Withdraw.vue'
import PayBill from '@/components/PayBill.vue'
import BuyAirtime from '@/components/BuyAirtime.vue'
import Transfer from '@/components/Transfer.vue'
import Balance from '@/components/Balance.vue'
import TransactionHistory from '@/components/TransactionHistory.vue'
import Register from '@/components/Register.vue'
import PayPal from '@/components/PayPal.vue'
// import Login from './pages/Login.vue'
// import Register from "./pages/Register.vue"

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "about" */ '../views/homepage.vue')
  },
  {
    path: '/login',
    name: 'login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Login
  },

 {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import(/* webpackChunkName: "about" */ '../views/dashboard.vue')
 },
 {
  path: '/deposit',
  name: 'deposit',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: Deposit
},
{
  path: '/withdraw',
  name: 'withdraw',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: Withdraw
},
{
  path: '/payBill',
  name: 'payBill',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: PayBill
},
{
  path: '/buyairtime',
  name: 'buyairtime',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: BuyAirtime
},
{
  path: '/transfer',
  name: 'transfer',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: Transfer
},
{
  path: '/balance',
  name: 'balance',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: Balance
},
{
  path: '/transaction-history',
  name: 'transaction-history',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: TransactionHistory
},
{
  path: '/register',
  name: 'register',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: Register
},
{
  path: '/paypal/create-paypal-payment',
  name: 'paypal',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: PayPal
},
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
