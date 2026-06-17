import {
  createRouter,
  createRootRoute,
  createRoute,
} from '@tanstack/react-router'
import { RootLayout } from '@/shared/components/RootLayout'
import { HomePage } from '@/features/publications/pages/HomePage'

const rootRoute = createRootRoute({
  component: RootLayout,
})

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: HomePage,
})

const routeTree = rootRoute.addChildren([indexRoute])

export const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
