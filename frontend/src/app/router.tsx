import {
  createRouter,
  createRootRoute,
  createRoute,
} from '@tanstack/react-router'
import { RootLayout } from '@/shared/components/RootLayout'
import { HomePage } from '@/features/publications/pages/HomePage'
import { LoginPage } from '@/features/auth/pages/LoginPage'
import { RegisterPage } from '@/features/auth/pages/RegisterPage'
import { ProtectedRoute } from '@/features/auth/components/ProtectedRoute'
import { OrganizationsPage } from '@/features/organizations/pages/OrganizationsPage'

const rootRoute = createRootRoute({
  component: RootLayout,
})

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: HomePage,
})

const loginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/login',
  component: LoginPage,
})

const registerRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/register',
  component: RegisterPage,
})

const protectedRoute = createRoute({
  getParentRoute: () => rootRoute,
  id: 'protected',
  component: ProtectedRoute,
})

const organizationsRoute = createRoute({
  getParentRoute: () => protectedRoute,
  path: '/organizations',
  component: OrganizationsPage,
})

const routeTree = rootRoute.addChildren([
  indexRoute, 
  loginRoute, 
  registerRoute,
  protectedRoute.addChildren([organizationsRoute])
])

export const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
