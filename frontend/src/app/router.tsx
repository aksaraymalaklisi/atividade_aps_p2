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
import { PublicationDetailPage } from '@/features/publications/pages/PublicationDetailPage'
import { PublicationForm } from '@/features/publications/components/PublicationForm'
import { EditPublicationPage } from '@/features/publications/pages/EditPublicationPage'

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

const petDetailRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/pet/$id',
  component: PublicationDetailPage,
})

const createPublicationRoute = createRoute({
  getParentRoute: () => protectedRoute,
  path: '/publications/new',
  component: PublicationForm,
})

const editPublicationRoute = createRoute({
  getParentRoute: () => protectedRoute,
  path: '/pet/$id/edit',
  component: EditPublicationPage,
})

import { ChatListPage } from '@/features/chat/pages/ChatListPage'
import { ChatRoomPage } from '@/features/chat/pages/ChatRoomPage'

const chatListRoute = createRoute({
  getParentRoute: () => protectedRoute,
  path: '/chats',
  component: ChatListPage,
})

const chatRoomRoute = createRoute({
  getParentRoute: () => protectedRoute,
  path: '/chats/$roomId',
  component: ChatRoomPage,
})

const routeTree = rootRoute.addChildren([
  indexRoute, 
  loginRoute, 
  registerRoute,
  petDetailRoute,
  protectedRoute.addChildren([
    organizationsRoute, 
    createPublicationRoute, 
    editPublicationRoute,
    chatListRoute,
    chatRoomRoute
  ])
])

export const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
