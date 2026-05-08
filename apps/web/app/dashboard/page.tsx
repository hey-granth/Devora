'use client'

import { useAuthStore } from '../../../stores/auth'
import { useCurrentOrganization } from '../../../lib/queries/auth'

export default function DashboardPage() {
  const user = useAuthStore((state) => state.user)
  const organization = useAuthStore((state) => state.organization)
  const { data: orgData, isLoading: orgLoading } = useCurrentOrganization()

  const currentOrg = organization || orgData

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Welcome to Devora
        </h1>
        <p className="text-gray-600 mb-6">
          Your AI-native Developer Relations Intelligence Platform is ready to help you understand your developer ecosystem.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-blue-50 rounded-lg p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Developers</p>
                <p className="text-2xl font-bold text-gray-900">-</p>
              </div>
            </div>
          </div>

          <div className="bg-green-50 rounded-lg p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">API Events</p>
                <p className="text-2xl font-bold text-gray-900">-</p>
              </div>
            </div>
          </div>

          <div className="bg-yellow-50 rounded-lg p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-yellow-500 rounded-md p-3">
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Friction Signals</p>
                <p className="text-2xl font-bold text-gray-900">-</p>
              </div>
            </div>
          </div>

          <div className="bg-purple-50 rounded-lg p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Documents</p>
                <p className="text-2xl font-bold text-gray-900">-</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Getting Started</h2>
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <div className="h-6 w-6 rounded-full bg-green-500 flex items-center justify-center">
                  <span className="text-white text-sm font-medium">1</span>
                </div>
              </div>
              <div className="flex-1">
                <h3 className="text-sm font-medium text-gray-900">Install SDK</h3>
                <p className="text-sm text-gray-600">Add the Devora SDK to your application to start collecting telemetry.</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <div className="h-6 w-6 rounded-full bg-blue-500 flex items-center justify-center">
                  <span className="text-white text-sm font-medium">2</span>
                </div>
              </div>
              <div className="flex-1">
                <h3 className="text-sm font-medium text-gray-900">Configure API Key</h3>
                <p className="text-sm text-gray-600">Use your organization's API key to authenticate telemetry events.</p>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <div className="h-6 w-6 rounded-full bg-purple-500 flex items-center justify-center">
                  <span className="text-white text-sm font-medium">3</span>
                </div>
              </div>
              <div className="flex-1">
                <h3 className="text-sm font-medium text-gray-900">Upload Documentation</h3>
                <p className="text-sm text-gray-600">Add your API docs and guides to enable AI-powered insights.</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Organization Info</h2>
          {orgLoading ? (
            <div className="animate-pulse space-y-4">
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3"></div>
            </div>
          ) : currentOrg ? (
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-gray-500">Organization</p>
                <p className="text-lg font-semibold text-gray-900">{currentOrg.name}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Slug</p>
                <p className="text-sm text-gray-900">{currentOrg.slug}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Plan</p>
                <p className="text-sm text-gray-900 capitalize">{currentOrg.plan}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Created</p>
                <p className="text-sm text-gray-900">
                  {new Date(currentOrg.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          ) : (
            <p className="text-gray-500">Loading organization information...</p>
          )}
        </div>
      </div>
    </div>
  )
}
