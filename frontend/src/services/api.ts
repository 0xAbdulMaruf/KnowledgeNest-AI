/// <reference types="vite/client" />
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 10000,
})

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

export interface AIResponse {
  answer: string
  topic_name: string
  mode: string
}

export interface CreateResourcePayload {
  topic_id: number
  type: ResourceType
  title: string
  url?: string
  content?: string
  tags?: string[]
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

export const getSubjects = async (semesterId?: number): Promise<Subject[]> => {
  const { data } = await api.get('/subjects/', { params: semesterId ? { semester_id: semesterId } : {} })
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

export const chatWithAI = async (topicId: number | null | undefined, question: string, mode?: string): Promise<AIResponse> => {
  const { data } = await api.post('/ai/chat', {
    topic_id: topicId ?? null,
    question,
    mode: mode || 'answer_question',
  })
  return data
}

export const healthCheck = async (): Promise<{ status: string }> => {
  const { data } = await api.get('/health')
  return data
}

export default api
