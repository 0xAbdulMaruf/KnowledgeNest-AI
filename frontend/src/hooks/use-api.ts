import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import * as api from '@/services/api'
import type { AIProviderConfig, ResourceType, CreateResourcePayload, FacultyUnlockPayload, UpdateResourcePayload } from '@/services/api'

export function useSemesters() {
  return useQuery({
    queryKey: ['semesters'],
    queryFn: api.getSemesters,
    staleTime: 10 * 60 * 1000,
  })
}

export function useSemester(id: number) {
  return useQuery({
    queryKey: ['semester', id],
    queryFn: () => api.getSemester(id),
    enabled: !!id,
    staleTime: 10 * 60 * 1000,
  })
}

export function useSemesterSubjects(id: number) {
  return useQuery({
    queryKey: ['semester', id, 'subjects'],
    queryFn: () => api.getSemesterSubjects(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}

export function useSubjects(semesterId?: number) {
  return useQuery({
    queryKey: ['subjects', semesterId],
    queryFn: () => api.getSubjects(semesterId),
    staleTime: 5 * 60 * 1000,
  })
}

export function useSubject(id: number) {
  return useQuery({
    queryKey: ['subject', id],
    queryFn: () => api.getSubject(id),
    enabled: !!id,
    staleTime: 10 * 60 * 1000,
  })
}

export function useSubjectUnits(id: number) {
  return useQuery({
    queryKey: ['subject', id, 'units'],
    queryFn: () => api.getSubjectUnits(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}

export function useUnit(id: number) {
  return useQuery({
    queryKey: ['unit', id],
    queryFn: () => api.getUnit(id),
    enabled: !!id,
    staleTime: 10 * 60 * 1000,
  })
}

export function useUnitTopics(id: number) {
  return useQuery({
    queryKey: ['unit', id, 'topics'],
    queryFn: () => api.getUnitTopics(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}

export function useTopic(id: number) {
  return useQuery({
    queryKey: ['topic', id],
    queryFn: () => api.getTopic(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}

export function useTopicResources(id: number, type?: ResourceType) {
  return useQuery({
    queryKey: ['topic', id, 'resources', type],
    queryFn: () => api.getTopicResources(id, type),
    enabled: !!id,
  })
}

export function useSearch(q: string) {
  return useQuery({
    queryKey: ['search', q],
    queryFn: () => api.searchTopics(q),
    enabled: !!q && q.length >= 2,
    staleTime: 30 * 1000,
  })
}

export function useRecommendations(topicId: number) {
  return useQuery({
    queryKey: ['recommendations', topicId],
    queryFn: () => api.getRecommendations(topicId),
    enabled: !!topicId,
    staleTime: 5 * 60 * 1000,
  })
}

export function useCreateResource() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateResourcePayload) => api.createResource(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['topic'] })
      queryClient.invalidateQueries({ queryKey: ['faculty', 'resources'] })
      queryClient.invalidateQueries({ queryKey: ['faculty', 'activities'] })
    },
  })
}

export function useUpdateResource() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ resourceId, payload }: { resourceId: number; payload: UpdateResourcePayload }) =>
      api.updateResource(resourceId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['topic'] })
      queryClient.invalidateQueries({ queryKey: ['faculty', 'resources'] })
      queryClient.invalidateQueries({ queryKey: ['faculty', 'activities'] })
    },
  })
}

export function useFacultyUnlock() {
  return useMutation({
    mutationFn: (payload: FacultyUnlockPayload) => api.unlockFaculty(payload),
  })
}

export function useFacultyResources(enabled: boolean, topicId?: number) {
  return useQuery({
    queryKey: ['faculty', 'resources', topicId],
    queryFn: () => api.getFacultyResources(topicId),
    enabled,
  })
}

export function useFacultyActivities(enabled: boolean) {
  return useQuery({
    queryKey: ['faculty', 'activities'],
    queryFn: api.getFacultyActivities,
    enabled,
  })
}

export function useDeleteResource() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (resourceId: number) => api.deleteResource(resourceId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['topic'] })
      queryClient.invalidateQueries({ queryKey: ['faculty', 'resources'] })
      queryClient.invalidateQueries({ queryKey: ['faculty', 'activities'] })
    },
  })
}

export function useRestoreResource() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (resourceId: number) => api.restoreResource(resourceId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['topic'] })
      queryClient.invalidateQueries({ queryKey: ['faculty', 'resources'] })
      queryClient.invalidateQueries({ queryKey: ['faculty', 'activities'] })
    },
  })
}

export function useChatWithAI() {
  return useMutation({
    mutationFn: ({
      topicId,
      question,
      providerConfig,
      mode,
      history,
    }: {
      topicId?: number | null
      question: string
      providerConfig: AIProviderConfig
      mode?: string
      history?: { role: 'user' | 'ai'; content: string }[]
    }) => api.chatWithAIProvider(topicId, question, providerConfig, mode, history || []),
  })
}

export function useTestAIConnection() {
  return useMutation({
    mutationFn: (providerConfig: AIProviderConfig) => api.testAIConnection(providerConfig),
  })
}

export function useHealthCheck() {
  return useQuery({
    queryKey: ['health'],
    queryFn: api.healthCheck,
    refetchInterval: 30000,
    retry: 2,
  })
}
