import { Routes, Route } from 'react-router-dom'
import ErrorBoundary from '@/components/ErrorBoundary'
import Layout from '@/components/layout/Layout'
import HomePage from '@/pages/HomePage'
import SubjectsPage from '@/pages/SubjectsPage'
import SubjectDetailPage from '@/pages/SubjectDetailPage'
import UnitPage from '@/pages/UnitPage'
import TopicPage from '@/pages/TopicPage'
import SearchPage from '@/pages/SearchPage'
import FacultyPage from '@/pages/FacultyPage'
import SettingsPage from '@/pages/SettingsPage'

export default function App() {
  return (
    <ErrorBoundary>
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="subjects" element={<SubjectsPage />} />
        <Route path="subjects/:id" element={<SubjectDetailPage />} />
        <Route path="units/:id" element={<UnitPage />} />
        <Route path="topics/:id" element={<TopicPage />} />
        <Route path="search" element={<SearchPage />} />
        <Route path="faculty" element={<FacultyPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
    </Routes>
    </ErrorBoundary>
  )
}
