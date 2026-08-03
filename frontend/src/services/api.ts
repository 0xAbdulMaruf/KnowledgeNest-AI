/// <reference types="vite/client" />
import axios from 'axios'

const configuredApiUrl = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')
const apiBaseUrl = configuredApiUrl
  ? configuredApiUrl.endsWith('/api')
    ? configuredApiUrl
    : `${configuredApiUrl}/api`
  : '/api'

const api = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10000,
})

const facultySessionKey = 'faculty_session_token'

export const setFacultySessionToken = (token: string | null) => {
  if (token) {
    sessionStorage.setItem(facultySessionKey, token)
    api.defaults.headers.common.Authorization = `Bearer ${token}`
    return
  }
  sessionStorage.removeItem(facultySessionKey)
  delete api.defaults.headers.common.Authorization
}

const initialFacultyToken = sessionStorage.getItem(facultySessionKey)
if (initialFacultyToken) {
  api.defaults.headers.common.Authorization = `Bearer ${initialFacultyToken}`
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout')
    }
    return Promise.reject(error)
  }
)

export interface Semester {
  id: number
  number: number
  name: string
  subjects?: Subject[]
  subject_count?: number
}

export interface Subject {
  id: number
  name: string
  code: string
  semester_id: number
  semester_number?: number
  description?: string
  tags?: string[]
}

export interface Unit {
  id: number
  number: number
  name: string
  subject_id: number
  description?: string
  topics_count?: number
  topic_count?: number
}

export interface Topic {
  id: number
  name: string
  unit_id: number
  subject_id?: number
  unit_name?: string
  subject_name?: string
  description?: string
  importance_score?: number
  tags?: string[]
  resource_count?: number
}

export type ResourceType = 'college_notes' | 'external_notes' | 'pdf' | 'video' | 'pyq' | 'important_questions' | 'practice_questions' | 'coding_problems' | 'assignment' | 'book' | 'documentation' | 'image'

export interface Resource {
  id: number
  topic_id: number
  type: ResourceType
  title: string
  url?: string
  content?: string
  metadata_?: Record<string, any>
  deleted_at?: string | null
  deleted_by?: string | null
}

export interface FacultyActivity {
  id: number
  teacher_name: string
  action: 'create' | 'update' | 'delete' | 'restore'
  resource_id: number
  created_at: string
}

export interface FacultyUnlockPayload {
  teacher_name: string
  password: string
}

export interface FacultyUnlockResponse {
  access_token: string
  teacher_name: string
}

export interface SearchResult {
  query: string
  subjects: (Subject & { relevance: number; type: string })[]
  topics: (Topic & { relevance: number; type: string })[]
  units: (Unit & { relevance: number; type: string; subject_name?: string })[]
  resources: (Resource & { relevance: number })[]
  total_results: number
}

export interface Recommendation {
  id: number
  name: string
  description: string
  tags: string[]
  unit_id: number
  unit_name?: string
  subject_name?: string
  importance_score: number
  relevance_score: number
  match_reason: string
}

export interface RecommendationResponse {
  topic_id: number
  topic_name: string
  recommendations: Recommendation[]
  total: number
}

export type AIProvider = 'local' | 'openai' | 'anthropic' | 'mimo'

export interface AIProviderConfig {
  provider: AIProvider
  baseUrl?: string
  apiKey?: string
  model?: string
  developerToken?: string
}

export interface AIConfigStatus {
  provider: AIProvider
  model: string
  api_key_configured: boolean
  developer_options_enabled: boolean
}

export const AI_DEVELOPER_CONFIG_KEY = 'kn-ai-developer-config'

export const unlockAIDeveloper = async (password: string): Promise<{ access_token: string }> => {
  const { data } = await api.post('/ai/developer/unlock', { password })
  return data
}

export interface CreateResourcePayload {
  topic_id: number
  type: ResourceType
  title: string
  url?: string
  content?: string
  tags?: string[]
}

export interface UpdateResourcePayload {
  topic_id?: number
  type?: ResourceType
  title?: string
  url?: string
  content?: string
  metadata_?: Record<string, any>
}

export interface FacultyResourceQuery {
  topicId?: number
}

export const getSemesters = async (): Promise<Semester[]> => {
  const { data } = await api.get('/semesters/')
  return data
}

export const getSemester = async (id: number): Promise<Semester> => {
  const { data } = await api.get(`/semesters/${id}`)
  return data
}

export const getSemesterSubjects = async (id: number): Promise<Subject[]> => {
  const { data } = await api.get(`/semesters/${id}/subjects`)
  return data
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}

export const getSubjects = async (semesterId?: number, skip = 0, limit = 20): Promise<PaginatedResponse<Subject>> => {
  const params: Record<string, string | number> = { skip, limit }
  if (semesterId) params.semester_id = semesterId
  const { data } = await api.get('/subjects/', { params })
  // Backward compat: deployed backend may still return a flat array
  if (Array.isArray(data)) {
    return { items: data, total: data.length, skip, limit }
  }
  return data
}

export const getSubject = async (id: number): Promise<Subject> => {
  const { data } = await api.get(`/subjects/${id}`)
  return data
}

export const getSubjectUnits = async (id: number): Promise<Unit[]> => {
  const { data } = await api.get(`/subjects/${id}/units`)
  return data
}

export const getUnit = async (id: number): Promise<Unit> => {
  const { data } = await api.get(`/units/${id}`)
  return data
}

export const getUnitTopics = async (id: number): Promise<Topic[]> => {
  const { data } = await api.get(`/units/${id}/topics`)
  return data
}

export const getTopic = async (id: number): Promise<Topic> => {
  const { data } = await api.get(`/topics/${id}`)
  return data
}

export const getTopicResources = async (id: number, type?: ResourceType): Promise<Resource[]> => {
  const { data } = await api.get(`/topics/${id}/resources`, { params: type ? { type } : {} })
  return data
}

export const unlockFaculty = async (payload: FacultyUnlockPayload): Promise<FacultyUnlockResponse> => {
  const { data } = await api.post('/faculty/unlock', payload)
  return data
}

export const getFacultyResources = async (topicId?: number): Promise<Resource[]> => {
  const { data } = await api.get('/faculty/resources', { params: topicId ? { topic_id: topicId } : {} })
  return data
}

export const getFacultyActivities = async (): Promise<FacultyActivity[]> => {
  const { data } = await api.get('/faculty/activities')
  return data
}

export const searchTopics = async (q: string, limit?: number): Promise<SearchResult> => {
  const { data } = await api.get('/search/', { params: { q, limit: limit || 20 } })
  return data
}

export const getRecommendations = async (topicId: number, limit?: number): Promise<RecommendationResponse> => {
  const { data } = await api.get(`/recommendations/${topicId}`, { params: { limit: limit || 5 } })
  return data
}

export const createResource = async (payload: CreateResourcePayload): Promise<Resource> => {
  const { data } = await api.post('/faculty/resources', payload)
  return data
}

export const updateResource = async (resourceId: number, payload: UpdateResourcePayload): Promise<Resource> => {
  const { data } = await api.put(`/faculty/resources/${resourceId}`, payload)
  return data
}

export const deleteResource = async (resourceId: number): Promise<Resource> => {
  const { data } = await api.delete(`/faculty/resources/${resourceId}`)
  return data
}

export const restoreResource = async (resourceId: number): Promise<Resource> => {
  const { data } = await api.post(`/faculty/resources/${resourceId}/restore`)
  return data
}

export const getAIConfig = async (): Promise<AIConfigStatus> => {
  const { data } = await api.get('/ai/config')
  return data
}

export interface AIStreamCallbacks {
  onChunk: (chunk: string) => void
  onDone?: () => void
}

export const streamChatWithAIProvider = async (
  topicId: number | null | undefined,
  question: string,
  providerConfig: AIProviderConfig | undefined,
  mode: string = 'answer_question',
  scope: string = 'topic',
  history: { role: 'user' | 'ai'; content: string }[] = [],
  callbacks: AIStreamCallbacks,
  signal?: AbortSignal,
): Promise<void> => {
  const response = await fetch(`${apiBaseUrl}/ai/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    signal,
    body: JSON.stringify({
      topic_id: topicId ?? null,
      question,
      mode,
      scope,
      history: history.map((message) => ({ role: message.role === 'ai' ? 'assistant' : 'user', content: message.content })),
      ...(providerConfig ? {
        developer_token: providerConfig.developerToken,
        provider: providerConfig.provider,
        base_url: providerConfig.baseUrl,
        api_key: providerConfig.apiKey,
        model: providerConfig.model,
      } : {}),
    }),
  })

  if (!response.ok) {
    let detail = 'AI provider request failed.'
    try {
      const payload = await response.json()
      if (typeof payload.detail === 'string') detail = payload.detail
    } catch {
      // Keep the safe fallback message.
    }
    throw new Error(detail)
  }

  if (!response.body) throw new Error('Streaming is not supported by this browser.')
  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  const processEvent = (event: string) => {
    const line = event.split('\n').find((entry) => entry.startsWith('data: '))
    if (!line) return
    const payload = JSON.parse(line.slice(6)) as { chunk?: string; done?: boolean; error?: string }
    if (payload.error) throw new Error(payload.error)
    if (payload.chunk) callbacks.onChunk(payload.chunk)
    if (payload.done) callbacks.onDone?.()
  }

  try {
    while (true) {
      const { value, done } = await reader.read()
      if (done) {
        buffer += decoder.decode()
        break
      }
      buffer += decoder.decode(value, { stream: true })
      const events = buffer.split('\n\n')
      buffer = events.pop() || ''
      for (const event of events) processEvent(event)
    }
    if (buffer.trim()) processEvent(buffer)
  } finally {
    reader.releaseLock()
  }
}

export const testAIConnection = async (providerConfig: AIProviderConfig): Promise<{ ok: boolean; provider: string; message: string }> => {
  const { data } = await api.post(
    '/ai/test-connection',
    {
      topic_id: null,
      question: 'Ping',
      mode: 'answer_question',
      ...(providerConfig ? {
        developer_token: providerConfig.developerToken,
        provider: providerConfig.provider,
        base_url: providerConfig.baseUrl,
        api_key: providerConfig.apiKey,
        model: providerConfig.model,
      } : {}),
      history: [],
    },
    { timeout: 45000 }
  )
  return data
}

export const healthCheck = async (): Promise<{ status: string }> => {
  const { data } = await api.get('/health')
  return data
}

export default api
