import { lazy, Suspense } from 'react';
import { LoaderCircle } from 'lucide-react';
import { Route, Routes } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { AppShell } from './components/layout/AppShell';
import { routeModuleLoaders } from './navigation/routeModules';

const OverviewPage = lazy(routeModuleLoaders.overview);
const PlanPage = lazy(routeModuleLoaders.plan);
const PlanMasterPage = lazy(routeModuleLoaders.planMaster);
const CalendarPage = lazy(routeModuleLoaders.calendar);
const IterationsPage = lazy(routeModuleLoaders.iterations);
const TeamPage = lazy(routeModuleLoaders.team);
const TasksPage = lazy(routeModuleLoaders.tasks);
const TriagePage = lazy(routeModuleLoaders.triage);
const ProjectsPage = lazy(routeModuleLoaders.projects);
const ProjectDetailPage = lazy(routeModuleLoaders.projectDetail);
const ProjectReleaseDetailPage = lazy(routeModuleLoaders.projectReleaseDetail);
const RoadmapPage = lazy(routeModuleLoaders.roadmap);
const GanttPage = lazy(routeModuleLoaders.gantt);
const AnalyticsPage = lazy(routeModuleLoaders.analytics);
const SettingsPage = lazy(routeModuleLoaders.settings);
const AgentPipelinePage = lazy(routeModuleLoaders.agentPipeline);
const NotFoundPage = lazy(routeModuleLoaders.notFound);

export const RouteLoadingState = () => {
  const { t } = useTranslation();
  return (
    <div
      className="flex min-h-64 items-center justify-center gap-3 text-content-secondary"
      role="status"
      aria-live="polite"
      aria-busy="true"
    >
      <LoaderCircle aria-hidden="true" className="h-5 w-5 animate-spin text-action" />
      <span>{t('routeLoading.message')}</span>
    </div>
  );
};

function App() {
  return (
    <AppShell>
      <Suspense fallback={<RouteLoadingState />}>
        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/plan" element={<PlanPage />} />
          <Route path="/plan/master" element={<PlanMasterPage />} />
          <Route path="/calendar" element={<CalendarPage />} />
          <Route path="/iterations" element={<IterationsPage />} />
          <Route path="/team" element={<TeamPage />} />
          <Route path="/tasks" element={<TasksPage />} />
          <Route path="/triage" element={<TriagePage />} />
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/projects/:projectId" element={<ProjectDetailPage />} />
          <Route path="/projects/:projectId/releases/:releaseId" element={<ProjectReleaseDetailPage />} />
          <Route path="/roadmap" element={<RoadmapPage />} />
          <Route path="/gantt" element={<GanttPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/agent-pipeline" element={<AgentPipelinePage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </AppShell>
  );
}

export default App;
